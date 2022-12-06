from flask import Flask, render_template, redirect, url_for, flash, abort
from flask_bootstrap import Bootstrap
from flask_ckeditor import CKEditor
from flask_login import login_user, LoginManager, login_required, current_user, logout_user
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import asc, desc, func
from functools import wraps
from forms import HostPartyForm, UserRegisterForm, OrgRegisterForm, LoginForm, ReviewForm
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import os

SECRET_KEY = os.urandom(32)

app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY

ckeditor = CKEditor(app)
bootstrap = Bootstrap(app)

# Create database
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///<wyd2nite>.db"
db = SQLAlchemy(app)

# Import models
from models import User, Org, Party, Review

# Create all tables from models.py
with app.app_context():
    db.create_all()
    db.session.commit()


# Setup Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)

# Load user
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


# Wrapper function to make it such that only organizations can log in
def orgs_only(func):
    @wraps(func)
    def inner(*args, **kwargs):
        if current_user.is_authenticated and Org.query.filter_by(user_id=current_user.id).first():
            return func(*args, **kwargs)
        else:
            return abort(403)
    return inner


@app.route('/')
def get_all_posts():
    # Query the database for the three parties happening the soonest, and the organizations they are hosted by
    NUM_PARTIES = 3
    parties = Party.query.filter(Party.date >= datetime.today().date()).order_by(asc(Party.date)).all()[:NUM_PARTIES]
    orgs = [Org.query.filter(Org.user_id == party.host_id).first() for party in parties]

    return render_template("index.html", parties=parties, orgs=orgs, num_parties=len(parties))

@app.route('/register', methods=["GET", "POST"])
@app.route('/register/<string:user_type>', methods=["GET", "POST"])
def register(user_type="user"):
    # If the user is already logged in, send them to the index page
    if current_user.is_authenticated:
        return redirect(url_for("get_all_posts"))

    # Toggle which form is initialized based on the parameters
    if user_type == "user":
        form = UserRegisterForm()
    elif user_type == "org":
        form = OrgRegisterForm()
    else:
        return redirect(url_for("register", user_type="user"))

    if form.validate_on_submit():
        salted_password = generate_password_hash(password=form.password.data, method="pbkdf2:sha256", salt_length=8)
        # Query database if email already exists
        if User.query.filter_by(email=form.email.data).first():
            flash("A user/organization with that email already exists. Log in instead.")
            return redirect(url_for("register", user_type=user_type))

        else:
            is_org = user_type == "org"
            new_user = User(email=form.email.data, password=salted_password, name=form.name.data, is_org=is_org)
            db.session.add(new_user)
            db.session.commit()

            if is_org:
                new_org = Org(name=form.name.data, img_url=form.img_url.data, description=form.description.data, user_id=new_user.id)
                db.session.add(new_org)
                db.session.commit()                

            flash("Successful registration.")
            login_user(new_user)
            return redirect(url_for("get_all_posts"))
    return render_template("register.html", form=form, user_type=user_type)


@app.route('/login', methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("get_all_posts"))

    form = LoginForm()
    user = User.query.filter_by(email=form.email.data).first()

    if form.validate_on_submit():
        if not user:
            flash("User with that email does not exist.")
            return redirect(url_for("login"))

        elif not check_password_hash(user.password, form.password.data):
            flash("Password incorrect. Try again.")
            return redirect(url_for("login"))

        else:
            flash(f"Welcome, {user.name}.")
            login_user(user)
            return redirect(url_for("get_all_posts"))

    return render_template("login.html", form=form)


@app.route('/logout')
def logout():
    flash("You have logged out successfully.")
    logout_user()
    return redirect(url_for('get_all_posts'))


@app.route('/host', methods=["GET", "POST"])
@orgs_only
def host():
    form = HostPartyForm()
    if form.validate_on_submit():
        new_party = Party(title=form.title.data,
                          date=form.date.data, 
                          time=form.time.data, 
                          duration=form.duration.data,
                          location=form.location.data,
                          description=form.description.data,
                          img_url=form.img_url.data,
                          host_id=current_user.id)
        db.session.add(new_party)
        db.session.commit()

        flash("You're hosting a party!")
        return redirect(url_for("get_all_posts"))
    return render_template("host.html", form=form)


@app.route('/organizations')
def organizations():
    # Get a list of all Org objects and their respective emails (queried from the users table)
    orgs = Org.query.order_by(asc(Org.name)).all()
    emails = [User.query.filter(User.id == org.user_id).first().email for org in orgs]
    return render_template("orgs.html", orgs=orgs, emails=emails, length=len(orgs))


@app.route('/organizations/<string:org_name>')
@app.route('/organizations/<string:org_name>/<int:org_index>')
def organization(org_name, org_index=0):
    # Query for all the organizations with the name entered in the parameter
    orgs = Org.query.filter(Org.name == org_name).all()

    # If it is an empty list, flash a message and redirect to all organizations
    if not orgs:
        flash("The organization you're looking for doesn't exist.")
        return redirect(url_for("organizations"))

    # Else, display the nth element on the list of organizations that came back from that query
    try:
        org = orgs[org_index]
    
    except IndexError:
        return redirect(url_for("organizations"))
    
    else:
        # Get emails, as well as parties in a list of tuples of the form (<Party X>, <Org Y>)
        email = User.query.filter(User.id == org.user_id).first().email
        parties = db.session.query(Party).filter(Party.host_id == org.user_id).order_by(desc(Party.date)).all()
        return render_template("org.html", org=org, email=email, parties=parties)


@app.route('/parties')
def parties():
    # Get a list of tuples of the form (<Party X>, <Org Y>)
    parties_soon = db.session.query(Party, Org).filter(Party.date >= datetime.today().date(), Party.host_id == Org.user_id).order_by(asc(Party.date)).all()
    parties_over = db.session.query(Party, Org).filter(Party.date < datetime.today().date(), Party.host_id == Org.user_id).order_by(desc(Party.date)).all()

    return render_template("parties.html", parties_soon=parties_soon, parties_over=parties_over)


@app.route('/parties/<string:party_title>', methods=["GET", "POST"])
@app.route('/parties/<string:party_title>/<int:party_index>', methods=["GET", "POST"])
def party(party_title, party_index=0):
    # Create a WTForm for rating parties and add its data to the database
    form = ReviewForm()
    if form.validate_on_submit():
        new_party = Review(music=form.music.data,
                          drinks=form.drinks.data, 
                          vibes=form.vibes.data, 
                          comment=form.comment.data,
                          reviewer_id=current_user.id,
                          party_id=Party.query.filter(Party.title == party_title).all()[party_index].id)
        db.session.add(new_party)
        db.session.commit()

        flash("Party reviewed!")
        return redirect(url_for("parties"))

    # Query for all the parties with the name entered in the parameter
    parties = Party.query.filter(Party.title == party_title).all()

    # If it is an empty list, flash a message and redirect to all parties
    if not parties:
        flash("The party you're looking for doesn't exist.")
        return redirect(url_for("parties"))

    # Else, display the nth element on the list of parties that came back from that query
    try:
        party = parties[party_index]
    
    except IndexError:
        return redirect(url_for("parties"))
    
    else:
        # Get the name of the host organization
        org = Org.query.filter(party.host_id == Org.user_id).first().name

        # Send over the reviews and average ratings to be displayed at the bottom of the page
        # Get a list of tuplets of the form (<Review X>, <User Y>)
        reviews = db.session.query(Review, User).filter(Review.party_id == party.id, User.id==Review.reviewer_id).all()
        avg_ratings = { "music": db.session.query(func.avg(Review.music)).first()[0],
                        "vibes": db.session.query(func.avg(Review.vibes)).first()[0], 
                        "drinks": db.session.query(func.avg(Review.drinks)).first()[0] }
        return render_template("party.html", form=form, all_reviews=reviews, avg_ratings=avg_ratings, party=party, org=org, date_now=datetime.today().date())


if __name__ == "__main__":
    app.run(debug=True)
