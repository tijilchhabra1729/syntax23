from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, FileField, IntegerField, RadioField, DateField
from wtforms.validators import DataRequired, Email, EqualTo, Length
from flask_wtf.file import FileField, FileAllowed
from wtforms import ValidationError

from flask_login import current_user
from Tool.models import User


class RegistrationForm(FlaskForm):
    interest = TextAreaField('interest', validators=[DataRequired()])
    phone1 = IntegerField('phone1', validators=[DataRequired()])
    phoneb = IntegerField('phoneb', validators=[DataRequired()])
    email1 = StringField('Email1', validators=[DataRequired(), Email()])
    emailb = StringField('Emailb', validators=[DataRequired(), Email()])
    name1 = StringField('name1', validators=[DataRequired()])
    name2 = StringField('name2', validators=[DataRequired()])
    name3 = StringField('name3')
    name4 = StringField('name4')
    name5 = StringField('name5')
    school1 = StringField('school1', validators=[DataRequired()])
    school2 = StringField('school2', validators=[DataRequired()])
    school3 = StringField('school3', validators=[DataRequired()])
    school4 = StringField('school4')
    school5 = StringField('school5')
    school6 = StringField('school6')
    password = PasswordField('Password', validators=[DataRequired(), EqualTo(
        'pass_confirm', message='Passwords must match'), Length(min=8, max=16)])
    pass_confirm = PasswordField(
        'Confirm Password', validators=[DataRequired()])
    submit = SubmitField('Register')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError(
                'The email you chose has already been registered')

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError(
                'The username yuo chose has already been registered')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Log in')
