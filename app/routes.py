from app import app
from flask import render_template, redirect, url_for, flash, request, jsonify, session
from app.models import User
from app.forms import RegisterForm, LoginForm
from app import db
from flask_login import login_user, logout_user, login_required, current_user
import base64


@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')


@app.route('/register', methods=['GET', 'POST'])
def register_page():
    form = RegisterForm()
    if form.validate_on_submit():
        user_to_create = User(username=form.username.data,
                email_address=form.email_address.data,
                password=form.password1.data)
        db.session.add(user_to_create)
        db.session.commit()
        login_user(user_to_create)
        flash(f"Account created successfully! You are now logged in as {user_to_create.username}", category='success')
        session["username"] = form.username.data
        return redirect(url_for('take_photo'))
    if form.errors != {}: #If there are not errors from the validations
        for err_msg in form.errors.values():
            flash(f'There was an error with creating a user: {err_msg}', category='danger')
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login_page():
    form = LoginForm()
    if form.validate_on_submit():
        attempted_user = User.query.filter_by(username=form.username.data).first()
        if attempted_user and attempted_user.check_password_correction(
                attempted_password=form.password.data
        ):
            login_user(attempted_user)
            flash(f'Success! You are logged in as: {attempted_user.username}', category='success')
            return redirect(url_for('check_photo'))
        else:
            flash('Username and password are not match! Please try again', category='danger')

    return render_template('login.html', form=form)

@app.route('/logout')
def logout_page():
    logout_user()
    flash("You have been logged out!", category='info')
    return redirect(url_for("home"))

@app.route('/save_image', methods=['GET','POST'])
def take_photo():
    form = RegisterForm()
    if request.method == "GET":
        return render_template('index.html')
    if request.method == 'POST':
        with open(f"./photos/save/{session.get('username')}.jpeg", "wb") as f:
            image_data = request.form['file'].split(";base64,")[1]
            f.write(base64.b64decode(image_data)) 
    return jsonify(request.form['userID'], request.form['file'])

@app.route('/check_image', methods=['GET','POST'])
def check_photo():
    form = LoginForm()
    if request.method == "GET":
        return render_template('index.html')
    if request.method == 'POST':
        with open(f"./photos/try/{session.get('username')}.jpeg", "wb") as f:
            image_data = request.form['file'].split(";base64,")[1]
            f.write(base64.b64decode(image_data)) 
    return jsonify(request.form['userID'], request.form['file'])
