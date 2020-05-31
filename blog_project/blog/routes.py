from flask import render_template
from . import app
from .forms import RegistrationForm, LoginForm

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/register')
def register():
    form = RegistrationForm()
    return render_template('register.html', form=form)
