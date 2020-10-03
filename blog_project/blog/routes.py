from flask import render_template, redirect, url_for, flash, request, abort
from . import app, db, bcrypt
from .forms import RegistrationForm, LoginForm, UpdateProfileForm, PostForm , SearchForm
from .models import User, Post
from flask_login import login_user, current_user, logout_user, login_required


@app.route('/')
def home():
    posts = Post.query.all()
    return render_template('home.html', posts=posts)


@app.route('/post/<int:post_id>')
def detail(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('detail.html', post=post)


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

@app.route('/post/new', methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(
            title=form.title.data,
            content=form.title.data,
            author=current_user
        )
        db.session.add(post)
        db.session.commit()
        flash('post created')
        return redirect(url_for('profile'))
    return render_template('new_post.html', form=form)


@app.route('/post/<int:post_id>/delete')
@login_required
def delete(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('post deleted', 'success')
    return redirect(url_for('home'))


@app.route('/post/<int:post_id>/update', methods=['GET', 'POST'])
@login_required
def update(post_id):
    post = Post.query.get_or_404(post_id)
    
    if post.author != current_user:
        abort(403)

    form = PostForm()
    
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash('post updated', 'success')
        return redirect(url_for('detail', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
        return render_template('update.html', form=form)

@app.route('/post/search' , methods=['GET', 'POST'])
def search():
    form = SearchForm()  
    if form.validate_on_submit():
        posts = Post.query.filter(Post.title.like(f"%{form.query.data}%")).all()
        if posts:
            return render_template('search.html', posts=posts , form=form)
        else:
            flash('No such post has been found!','danger')
            return render_template('search.html',form=form)    
    return render_template('search.html', form=form)          