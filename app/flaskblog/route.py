from flask import render_template, url_for, flash, redirect, request
from flaskblog import app, db
from flaskblog.forms import RegistrationForm, LoginForm
from flaskblog.models import User
from flask_login import login_user, current_user, logout_user, login_required
import os

image_folder = os.path.join('static', 'Images')
app.config['UPLOAD_FOLDER'] = image_folder
posts = [
    {
        'author': 'Corey Schafer',
        'title': 'Blog Post 1',
        'content': 'First post content',
        'date_posted': 'April 20, 2018'
    },
    {
        'author': 'Jane Doe',
        'title': 'Blog Post 2',
        'content': 'Second post content',
        'date_posted': 'April 21, 2018'
    }
]



@app.route("/")
@app.route("/home")
def home():
    full_filename = os.path.join(app.config['UPLOAD_FOLDER'], 'logo1.jpg')
    return render_template('home.html', posts=posts, logo = full_filename)


@app.route("/about")
def about():
    full_filename = os.path.join(app.config['UPLOAD_FOLDER'], 'logo1.jpg')
    return render_template('about.html', title='About', logo = full_filename)


@app.route("/register", methods=['GET', 'POST'])
def register():
    full_filename = os.path.join(app.config['UPLOAD_FOLDER'], 'logo1.jpg')
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        #hash_pswd = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form, logo = full_filename)


@app.route("/login", methods=['GET', 'POST'])
def login():
    full_filename = os.path.join(app.config['UPLOAD_FOLDER'], 'logo1.jpg')
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and form.password == user.password:
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
            flash('You have been logged in!', 'success')
            
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', title='Login', form=form, logo = full_filename)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route("/account")
@login_required
def account():
    return render_template('account.html', title='Suggestions')


