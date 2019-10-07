# -*- encoding: utf-8 -*-
"""
Now UI Dashboard - coded in Flask
Author: AppSeed.us - App Generator 
"""

# all the imports necessary
from flask import json, url_for, redirect, Markup, Response, render_template, flash, g, session, jsonify, request, send_from_directory
from werkzeug.exceptions import HTTPException, NotFound, abort

import os

from app  import app

from flask       import url_for, redirect, render_template, flash, g, session, jsonify, request, send_from_directory
from flask_login import login_user, logout_user, current_user, login_required
from app         import app, lm, db, bc
from . models    import User
from . common    import COMMON, STATUS
from . assets    import *
from . forms     import LoginForm, RegisterForm

import os, shutil, re, cgi, json, random, time
from datetime import datetime


random.seed()  # Initialize the random number generator

# provide login manager with load_user callback
@lm.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# authenticate user
@app.route('/logout.html')
def logout():
    logout_user()
    return redirect(url_for('index'))

# register user
@app.route('/register.html', methods=['GET', 'POST'])
def register():
    
    # define login form here
    form = RegisterForm(request.form)

    msg = None

    # custommize your pate title / description here
    page_title       = 'Register - Flask Now UI Dashboard | AppSeed App Generator'
    page_description = 'Open-Source Flask Now UI Dashboard, registration page.'

    # check if both http method is POST and form is valid on submit
    if form.validate_on_submit():

        # assign form data to variables
        username = request.form.get('username', '', type=str)
        password = request.form.get('password', '', type=str) 
        name     = request.form.get('name'    , '', type=str) 
        email    = request.form.get('email'   , '', type=str) 

        # filter User out of database through username
        user = User.query.filter_by(user=username).first()

        # filter User out of database through username
        user_by_email = User.query.filter_by(email=email).first()

        if user or user_by_email:
            msg = 'Error: User exists!'
            
        else:                    
            pw_hash = bc.generate_password_hash(password)

            user = User(username, pw_hash, name, email)

            user.save()

            msg = 'User created, please <a href="' + url_for('login') + '">login</a>'     

    # try to match the pages defined in -> themes/light-bootstrap/pages/
    return render_template( 'layouts/default.html',
        title=page_title,
        content=render_template( 'pages/register.html', 
           form=form,
           msg=msg) )

# authenticate user
@app.route('/login.html', methods=['GET', 'POST'])
def login():
    
    # define login form here
    form = LoginForm(request.form)

    # Flask message injected into the page, in case of any errors
    msg = None

    # custommize your page title / description here
    page_title = 'Login - Flask Now UI Dashboard | AppSeed App Generator'
    page_description = 'Open-Source Flask Now UI Dashboard, login page.'

    # check if both http method is POST and form is valid on submit
    if form.validate_on_submit():

        # assign form data to variables
        username = request.form.get('username', '', type=str)
        password = request.form.get('password', '', type=str) 

        # filter User out of database through username
        user = User.query.filter_by(user=username).first()

        if user:
            
            if bc.check_password_hash(user.password, password):
                login_user(user)
                return redirect(url_for('index'))
            else:
                msg = "Wrong password. Please try again."
        else:
            msg = "Unkkown user"

    # try to match the pages defined in -> themes/light-bootstrap/pages/
    return render_template( 'layouts/default.html',
        title=page_title,
        content=render_template( 'pages/login.html', 
           form=form,
           msg=msg) )


    @app.route('/emailescalation.html')
    def emailescalation():
        return render_template( 'pages/emailescalation.html', title='Email & Escalation', description='ipNX Dashboard')


    @app.route('/retailsupport.html')
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


    @app.route('/ishop.html')
    def ishop():
        return render_template( 'pages/ishop.html', title='i-Shop', description='ipNX Dashboard' )

    @app.route('/ticketingresolution.html')
    def ticketingresolution():
        return render_template( 'pages/ticketingresolution.html', title='Ticketing and Resolution', description='ipNX Dashboard' )

    @app.route('/social.html')
    def social():

        return render_template( 'pages/social.html', title='Social Media', description='ipNX Dashboard')

    @app.route('/cxretention.html')
    def cxretention():
        return render_template('pages/cxretention.html', title='Customer Experience and Retention', description='ipNX Dashboard')

# App main route + generic routing
@app.route('/', defaults={'path': 'index.html'})
@app.route('/<path>')
def index(path):

    inactiveCustomers = 34546
    activeCustomers = 7654984
    numberOfCalls = 123456
    numberOfRetailCustomers = 455674666

    try:
        return render_template('pages/'+path, numberOfCalls=numberOfCalls, numberOfRetailCustomers=numberOfRetailCustomers, inactiveCustomers=inactiveCustomers, activeCustomers=activeCustomers)
    except:
        abort(404)


def http_err(err_code):
           
    err_msg = 'Oups !! Some internal error ocurred. Thanks to contact support.'
            
    if 400 == err_code:
        err_msg = "It seems like you are not allowed to access this link."

    elif 404 == err_code:    
        err_msg  = "The URL you were looking for does not seem to exist."
        err_msg += "<br /> Define the new page in /pages"
                
    elif 500 == err_code:    
        err_msg = "Internal error. Contact the manager about this."

    else:
        err_msg = "Forbidden access."

    return err_msg
                
@app.errorhandler(401)
def e401(e):
    return http_err( 401) # "It seems like you are not allowed to access this link."

@app.errorhandler(404)
def e404(e):
    return http_err( 404) # "The URL you were looking for does not seem to exist.<br><br>
                          # If you have typed the link manually, make sure you've spelled the link right."
@app.errorhandler(500)
def e500(e):
    return http_err( 500) # "Internal error. Contact the manager about this."

@app.errorhandler(403)
def e403(e):
    return http_err( 403 ) # "Forbidden access."

@app.errorhandler(410)
def e410(e):
    return http_err( 410) # "The content you were looking for has been deleted."

    