from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length, Email, EqualTo


class RegistrationForm(FlaskForm):
    username = StringField('user name', validators=[
                           DataRequired(), Length(min=4, max=25)])
    email = StringField('user email', validators=[DataRequired(), Email()])
    password = PasswordField('password', validators=[DataRequired()])
    confirm_password = PasswordField('confirm password', validators=[
                                     DataRequired(), EqualTo('password', message='confirm password error')])
    submit = SubmitField('Register')


class LoginForm(FlaskForm):
    email = StringField('user email', validators=[DataRequired(), Email()])
    password = PasswordField('password', validators=[DataRequired()])
    remember = BooleanField('remember me')