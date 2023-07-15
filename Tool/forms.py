from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, FileField, IntegerField, RadioField, DateField
from wtforms.validators import DataRequired, Email, EqualTo, Length
from flask_wtf.file import FileField, FileAllowed
from wtforms import ValidationError
from Tool import app,db
from flask_login import current_user
from Tool.models import User


class RegistrationForm(FlaskForm):
    email = StringField('Email1', validators=[DataRequired(), Email()])
    name = StringField('name1', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired(), EqualTo(
        'pass_confirm', message='Passwords must match'), Length(min=8, max=16)])
    pass_confirm = PasswordField(
        'Confirm Password', validators=[DataRequired()])
    submit = SubmitField('Register')


    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError(
                'The email you chose has already been registered')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Log in')


class VisitorForm_1(FlaskForm):
    date = DateField('Date', validators=[DataRequired()])
    size = IntegerField('Size', validators=[DataRequired()])
    submit = SubmitField('Confirm')

