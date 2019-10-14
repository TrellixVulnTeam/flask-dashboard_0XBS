# all the imports necessary

from flask import json, url_for, redirect, Markup, Response, render_template, flash, g, session, jsonify, request, send_from_directory
from werkzeug.exceptions import HTTPException, NotFound, abort

import os
import secrets
from PIL import Image
from app  import app

from flask       import url_for, redirect, render_template, flash, g, session, jsonify, request, send_from_directory
from flask_login import login_user, logout_user, current_user, login_required
from app         import app, lm, db, bc
from . models    import User
from . common    import COMMON, STATUS
from . assets    import *
from . forms     import LoginForm, RegisterForm, UpdateAccountForm
import os, shutil, re, cgi, json, random, time
from datetime import datetime


random.seed()  # Initialize the random number generator

# provide login manager with load_user callback
@lm.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
@app.route('/index')
@login_required
def index():
    inactiveCustomers = 34546
    activeCustomers = 7654984
    numberOfCalls = 123456
    numberOfRetailCustomers = 455674666
    return render_template('pages/index.html', numberOfCalls=numberOfCalls, numberOfRetailCustomers=numberOfRetailCustomers, inactiveCustomers=inactiveCustomers, activeCustomers=activeCustomers)


# authenticate user
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile', picture_fn)

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn

@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        current_user.firstName = form.firstName.data
        current_user.lastName = form.lastName.data
        current_user.about = form.about.data
        user = User(username=current_user.username, firstName=current_user.firstName, email=current_user.email, lastName=current_user.lastName, about=current_user.about, image_file=image_file)
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username 
        form.email.data = current_user.email
        form.firstName.data = current_user.firstName
        form.lastName.data = current_user.lastName
    image_file = url_for('static', filename='profile/' + current_user.image_file)
    return render_template( 'pages/account.html', title='Account details', description='ipNX Dashboard', image_file=image_file, form=form)
# register user
@app.route('/register', methods=['GET', 'POST'])

def register():
    
    # define login form here
    form = RegisterForm()

    msg = None

   
    if form.validate_on_submit():

        hashed_password = bc.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, password=hashed_password, firstName=form.firstName.data, email=form.email.data, lastName=form.lastName.data, about=form.about.data, image_file=form.picture.data)
        user.save()
        msg = 'User created, please <a href="' + url_for('login') + '">login</a>'     

    
    return render_template( 'pages/register.html', title='Register',form=form, msg=msg)

@app.route('/emailescalation')
@login_required
def emailescalation():
    return render_template( 'pages/emailescalation.html', title='Email & Escalation', description='ipNX Dashboard')


@app.route('/retailsupport')
@login_required
def retailsupport():
    totalCalls = 144452637733663

    return render_template( 'pages/retailsupport.html',  title='Retail Support Center', description='ipNX Dashboard', totalCalls=totalCalls)
@app.route('/chart-data')
def chart_data():
    def generate_random_data():
        while True:
            json_data = json.dumps(
                {'time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 'value': random.random() * 100})
            yield f"data:{json_data}\n\n"
            time.sleep(1)

    return Response(generate_random_data(), mimetype='text/event-stream')


@app.route('/ishop')
@login_required
def ishop():
    return render_template( 'pages/ishop.html', title='i-Shop', description='ipNX Dashboard' )

@app.route('/ticketingresolution')
@login_required
def ticketingresolution():
    return render_template( 'pages/ticketingresolution.html', title='Ticketing and Resolution', description='ipNX Dashboard' )

@app.route('/social')
@login_required
def social():

    return render_template( 'pages/social.html', title='Social Media', description='ipNX Dashboard')

@app.route('/cxretention')
@login_required
def cxretention():
    return render_template('pages/cxretention.html', title='Customer Experience and Retention', description='ipNX Dashboard')


# App main route + generic routing
# authenticate user
@app.route('/', methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bc.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            return redirect(url_for('index'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
            
    # try to match the pages defined in -> themes/light-bootstrap/pages/
    return render_template('pages/login.html', title='Login', form=form)

@app.errorhandler(401)
def e401(e):
    flash('It seems like you are not allowed to access this link. Login using the sidebar login link to gain access.', 'danger')
    return render_template('pages/error.html', title='Error'), 401 

@app.errorhandler(404)
def e404(e):
    flash("The URL you were looking for does not seem to exist.If you have typed the link manually, make sure you've spelled the link right.", 'danger')
    return render_template('pages/error.html', title='Error'), 404# 
@app.errorhandler(500)
def e500(e):
    flash('Internal error. Seek technical support for this...', 'danger')
    return render_template('pages/error.html', title='Error'), 500

@app.errorhandler(403)
def e403(e):
    flash('Forbidden access. You must be logged in to access the content.', 'danger')
    return render_template('pages/error.html', title='Error'), 403

@app.errorhandler(410)
def e410(e):
    flash('The content you were looking for has been deleted.', 'danger')
    return render_template('pages/error.html', title='Error'), 410

    