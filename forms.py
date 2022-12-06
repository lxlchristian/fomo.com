from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, TimeField, DateField, SelectField, FloatField
from wtforms.validators import DataRequired, URL, Email
from flask_ckeditor import CKEditorField
from datetime import datetime


class HostPartyForm(FlaskForm):
    '''Setting up the form for hosting events using WTForms'''
    title = StringField("Event Name", validators=[DataRequired()])
    date = DateField("Date", validators=[DataRequired()])
    time = TimeField("Start time", validators=[DataRequired()])
    duration = FloatField("Duration (in hours)", validators=[DataRequired()])
    location = StringField("Location", validators=[DataRequired()])
    img_url = StringField("Publicity Image (URL)", validators=[DataRequired(), URL()])
    description = CKEditorField("Event Description", validators=[DataRequired()])
    submit = SubmitField("Submit Post")

    # Create custom validator to check that the date of the party being hosted only is after today
    # If happening today, check that the time is later than the current time
    def validate(self):
        rv = FlaskForm.validate(self)
        if not rv:
            return False

        if self.date.data < datetime.today().date() or (self.date.data == datetime.today().date() and self.time.data < datetime.today().time()):
            self.date.errors.append('Event cannot be in the past!')
            return False

        return True


class UserRegisterForm(FlaskForm):
    '''Setting up the registration form for users using WTForms'''
    name = StringField("Name", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Register")


class OrgRegisterForm(FlaskForm):
    '''Setting up the registration form for organizations using WTForms'''
    name = StringField("Organization Name", validators=[DataRequired()])
    img_url = StringField("Display Photo (URL)", validators=[DataRequired(), URL()])
    description = CKEditorField("Description of Organization", validators=[DataRequired()])
    email = StringField("Organization Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Register")


class LoginForm(FlaskForm):
    '''Setting up the Login form using WTForms'''
    email = StringField("Email", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Log In")


class ReviewForm(FlaskForm):
    '''Setting up the party review form using WTForms'''
    music = SelectField('Music', choices=[(1,'1'), (2,'2'), (3,'3'), (4,'4'), (5, '5')], validators=[DataRequired()])
    drinks = SelectField('Drinks', choices=[(1,'1'), (2,'2'), (3,'3'), (4,'4'), (5, '5')], validators=[DataRequired()])
    vibes = SelectField('Vibes', choices=[(1,'1'), (2,'2'), (3,'3'), (4,'4'), (5, '5')], validators=[DataRequired()])
    comment = CKEditorField("Comment")
    submit = SubmitField("Review")