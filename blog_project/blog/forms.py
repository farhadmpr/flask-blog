from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    PasswordField,
    BooleanField,
    SubmitField,
    TextAreaField
)
from wtforms.validators import (
    DataRequired,
    Length,
    Email,
    EqualTo,
    ValidationError
)

from .models import User


class RegistrationForm(FlaskForm):
    username = StringField('user name', validators=[
                           DataRequired(), Length(min=4, max=25)])
    email = StringField('user email', validators=[DataRequired(), Email()])
    password = PasswordField('password', validators=[DataRequired()])
    confirm_password = PasswordField('confirm password', validators=[
                                     DataRequired(), EqualTo('password', message='confirm password error')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('this user already exist')


class LoginForm(FlaskForm):
    email = StringField('user email', validators=[DataRequired(), Email()])
    password = PasswordField('password', validators=[DataRequired()])
    remember = BooleanField('remember me')


class UpdateProfileForm(FlaskForm):
    username = StringField('user name', validators=[DataRequired(), Length(min=4, max=25)])    
    password = PasswordField('password', validators=[DataRequired()])


class PostForm(FlaskForm):
    title = StringField('title', validators=[DataRequired()])
    content = TextAreaField('content', validators=[DataRequired()])

class SearchForm(FlaskForm):
    query = StringField('Post Title', validators=[DataRequired()])
    submit = SubmitField('Search')    
    