import os
import secrets
from PIL import Image
from flask import render_template, url_for, flash, redirect, request, session
from flaskblog import app, db
from flaskblog.forms import RegistrationForm, LoginForm, AdminLoginForm, AddPlacesForm
from flaskblog.models import User, Admin, AddPlaces
from flask_login import login_user, current_user, logout_user, login_required
import os

image_folder = os.path.join('static', 'Images')
app.config['UPLOAD_FOLDER'] = image_folder


@app.route("/")
@app.route("/home")
def home():
    full_filename = os.path.join(app.config['UPLOAD_FOLDER'], 'logo1.jpg')
    places = AddPlaces.query.all()
    return render_template('home.html', places=places, logo = full_filename)


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

@app.route("/adminlogin", methods=['GET', 'POST'])
def adminlogin():
    full_filename = os.path.join(app.config['UPLOAD_FOLDER'], 'logo1.jpg')
    form = AdminLoginForm()
    if form.validate_on_submit():
        if form.username.data == 'Admin11' and form.password.data == 'muskan':
            session['logged_in'] = True
            flash('You have been logged in!', 'success')
            return redirect(url_for('addPlaces'))    
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('adminlogin.html', title='Login', form=form, logo = full_filename)


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/place_img', picture_fn)

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn

@app.route("/addPlaces/new", methods=['GET', 'POST'])
def new_place():
    if not session.get('logged_in'):
        return render_template('adminlogin.html', title='Login', form=form, logo = full_filename)
    else:
        form = AddPlacesForm()
        if form.validate_on_submit():
            pic_file = save_picture(form.image.data)

            addP = AddPlaces(name=form.placeName.data, city=form.cityName.data, image=pic_file,
                                 desc=form.description.data,features=form.features.data)
            db.session.add(addP)
            db.session.commit()
            flash('Places has been added')
            return redirect(url_for('home'))
        return render_template('addplace.html', title='New Place', form=form)


