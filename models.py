from flask_login import UserMixin
from sqlalchemy.orm import relationship
from app import db


##CONFIGURE TABLES
class User(UserMixin, db.Model):
    '''The User table contains id, email, password, name and is_org fields'''
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(250), unique=True, nullable=False)
    password = db.Column(db.String(250), nullable=False)
    name = db.Column(db.String(250), nullable=False)
    is_org = db.Column(db.Boolean, nullable=False)

    # One-to-one relationship with orgs; One-to-many relationship with parties;
    # One-to-many relationship with reviews
    org = relationship("Org", back_populates="user")
    attendance = relationship("Attendance", back_populates="attendee")
    reviews = relationship("Review", back_populates="reviewer")


class Org(db.Model):
    '''The Org table contains id, name, description, img_url, and user_id ForeignKey'''
    __tablename__ = "orgs"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    description = db.Column(db.Text, nullable=False)
    img_url = db.Column(db.String(250), nullable=False)

    # One-to-one relationship with users; One-to-many relationship with parties
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    user = relationship("User", back_populates="org")
    hosted = relationship("Party", back_populates="host")


class Party(db.Model):
    '''The Party table contains id, title, date, time, duration, location, description, img_url fields, and host_id ForeignKey'''
    __tablename__ = "parties"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), nullable=False)
    date = db.Column(db.Date, nullable=False)
    time = db.Column(db.Time, nullable=False)
    duration = db.Column(db.Float, nullable=False)
    location = db.Column(db.String(250), nullable=False)
    description = db.Column(db.Text, nullable=False)
    img_url = db.Column(db.String(250), nullable=False)

    # Many-to-one relationship with organizations; One-to-many relationship with reviews
    host_id = db.Column(db.Integer, db.ForeignKey("orgs.user_id"))
    host = relationship("Org", back_populates="hosted") 
    
    reviews = relationship("Review", back_populates="party")
    attendance = relationship("Attendance", back_populates="party")


class Attendance(db.Model):
    __tablename__ = "attendance"
    id = db.Column(db.Integer, primary_key=True)
    
    # Facilitates many-to-many relationship between users and parties
    attendee_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    attendee = relationship("User", back_populates="attendance")

    party_id = db.Column(db.Integer, db.ForeignKey("parties.id"))
    party = relationship("Party", back_populates="attendance")


class Review(db.Model):
    '''The Review table contains id, music, vibes, drinks, comment fields, and reviewer_id and party_id ForeignKeys'''
    __tablename__ = "reviews"
    id = db.Column(db.Integer, primary_key=True)
    
    music = db.Column(db.Integer)
    vibes = db.Column(db.Integer)
    drinks = db.Column(db.Integer)
    comment = db.Column(db.Text, nullable=False)

    # Many-to-one relationship with users; Many-to-one relationship with parties
    reviewer_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    reviewer = relationship("User", back_populates="reviews")

    party_id = db.Column(db.Integer, db.ForeignKey("parties.id"))
    party = relationship("Party", back_populates="reviews")