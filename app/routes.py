from app import app
from flask import render_template, redirect, url_for, flash, request, jsonify, session
from app.models import User
from app.forms import RegisterForm, LoginForm, TakeForm
from app import db
from flask_login import login_user, logout_user, login_required, current_user
import base64
import cv2
import face_recognition
import os

@app.route('/')
@app.route('/home')
@login_required
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
        # login_user(user_to_create) # login_action
        # You are now logged in as {user_to_create.username}
        flash(f"Account created successfully! ", category='success')
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
            # login_user(attempted_user)
            session["username"] = form.username.data
            
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
    if request.method == "GET":
        return render_template('reg_index.html')
    if request.method == 'POST':
        with open(f"./photos/save/{session.get('username')}.jpeg", "wb") as f:
            image_data = request.form['file'].split(";base64,")[1]
            f.write(base64.b64decode(image_data)) 
    return redirect("home")

@app.route('/check_image', methods=['GET','POST'])
def check_photo():
    # form=TakeForm()
    # if form.validate_on_submit():
    if request.method == "GET":
        return render_template('log_index.html')
    if request.method == 'POST':
        with open(f"./photos/try/{session.get('username')}.jpeg", "wb") as f:
            image_data = request.form['file'].split(";base64,")[1]
            f.write(base64.b64decode(image_data)) 

    img = cv2.imread(f"./photos/save/{session.get('username')}.jpeg")
    rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img_encoding = face_recognition.face_encodings(rgb_img)[0]

    img2 = cv2.imread(f"./photos/try/{session.get('username')}.jpeg")
    rgb_img2 = cv2.cvtColor(img2, cv2.COLOR_BGR2RGB)
    img_encoding2 = face_recognition.face_encodings(rgb_img2)[0]

    recognized = face_recognition.compare_faces([img_encoding], img_encoding2)
    print("Result: ", recognized)
    
    if recognized and recognized[0]:
        attempted_user = User.query.filter_by(username=session.get('username')).first()

        login_user(attempted_user)
        flash(f'Success! You are logged in as: {attempted_user.username}', category='success')
        return redirect("home")
    flash('Your photo is not match! Please try again', category='danger')
    return "your photo is fake"

@app.errorhandler(404)
def error_404(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def error_500(error):
    return render_template('errors/500.html'), 500

    

