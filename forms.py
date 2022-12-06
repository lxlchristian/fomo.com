from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, TimeField, DateField, SelectField, FloatField
from wtforms.validators import DataRequired, URL, Email, ValidationError
from flask_ckeditor import CKEditorField
from datetime import datetime


class HostPartyForm(FlaskForm):
    title = StringField("Event Name", validators=[DataRequired()])
    date = DateField("Date", validators=[DataRequired()])
    time = TimeField("Start time", validators=[DataRequired()])
    duration = FloatField("Duration (in hours)", validators=[DataRequired()])
    location = StringField("Location", validators=[DataRequired()])
    img_url = StringField("Publicity Image (URL)", validators=[DataRequired(), URL()])
    description = CKEditorField("Event Description", validators=[DataRequired()])
    submit = SubmitField("Submit Post")

    # def validate(self):
    #     rv = FlaskForm.validate(self)
    #     if not rv:
    #         return False

    #     if self.date.data < datetime.today().date() or (self.date.data == datetime.today().date() and self.time.data < datetime.today().time()):
    #         self.date.errors.append('Event cannot be in the past!')
    #         return False

    #     return True


class UserRegisterForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Register")


class OrgRegisterForm(FlaskForm):
    name = StringField("Organization Name", validators=[DataRequired()])
    img_url = StringField("Display Photo (URL)", validators=[DataRequired(), URL()])
    description = CKEditorField("Description of Organization", validators=[DataRequired()])
    email = StringField("Organization Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Register")


class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Log In")


class ReviewForm(FlaskForm):
    music = SelectField('Music', choices=[(1,'1'), (2,'2'), (3,'3'), (4,'4'), (5, '5')], validators=[DataRequired()])
    drinks = SelectField('Drinks', choices=[(1,'1'), (2,'2'), (3,'3'), (4,'4'), (5, '5')], validators=[DataRequired()])
    vibes = SelectField('Vibes', choices=[(1,'1'), (2,'2'), (3,'3'), (4,'4'), (5, '5')], validators=[DataRequired()])
    comment = CKEditorField("Comment")
    submit = SubmitField("Review")