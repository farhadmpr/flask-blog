from flask import render_template, redirect, url_for, flash
from . import app, db, bcrypt
from .forms import RegistrationForm, LoginForm
from .models import User
from flask_login import login_user


@app.route('/')
def home():
    return render_template('home.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(
            username=form.username.data,            
            email=form.email.data,            
            password=bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        )
        db.session.add(user)
        db.session.commit()
        flash('You registered successfully!', 'success')
        return redirect(url_for('home'))
    
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            flash('you logged in successfully', 'info')
            return redirect(url_for('home'))
        else:
            flash('email or password is wrong', 'danger')
    else:
        flash('please enter correct email', 'danger')

    return render_template('login.html', form=form)