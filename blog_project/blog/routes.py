from flask import render_template, redirect, url_for, flash, request
from . import app, db, bcrypt
from .forms import RegistrationForm, LoginForm, UpdateProfileForm
from .models import User
from flask_login import login_user, current_user, logout_user, login_required


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
            password=bcrypt.generate_password_hash(
                form.password.data).decode('utf-8')
        )
        db.session.add(user)
        db.session.commit()
        flash('You registered successfully!', 'success')
        return redirect(url_for('home'))

    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        flash('you already logged in', 'info')
        return redirect(url_for('home'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            flash('you logged in successfully', 'info')
            return redirect(next_page if next_page else url_for('home'))
        else:
            flash('email or password is wrong', 'danger')

    return render_template('login.html', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('you logged out successfully', 'info')
    return redirect(url_for('home'))


@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    form = UpdateProfileForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.password = bcrypt.generate_password_hash(
            form.password.data).decode('utf-8')
        db.session.commit()
        flash('Update successfully', 'success')
    elif request.method == 'GET':
        form.username.data = current_user.username    

    return render_template('profile.html', form=form)
