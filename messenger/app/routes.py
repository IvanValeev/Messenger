# -*- coding: utf-8 -*-
from flask import render_template, flash, redirect, url_for, session
from app import app
from flask import request, make_response, jsonify
from api_actions import make_registration, delete_registration, check_registration, logging_in, logout
from app.models import User, Session
from flask_login import current_user, login_user
import json
import uuid
from functools import wraps
from app.forms import LoginForm, RegistrationForm
import time
  

def login_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if session.get('session_id', None):
        # if Session.query.filter_by(uuid=session.get('session_id', None)).first():
            return f(*args, **kwargs)
        else:
            return 'First you need to login!'
    return wrapper

@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/register', methods = ['GET', 'POST'])
def register():
    form = RegistrationForm()
    if request.method == 'GET':
        return render_template('register.html', title='Register', form=form)

    elif request.method == 'POST':
        if check_registration(username=request.form['username']):
            return 'You alredy have registration!'
        try:
            if request.form['password'] == request.form['password2']:
                make_registration(request.form['username'], request.form['password'])
                return redirect(url_for('login'))
            else:
                return 'Password does not match!'
        except:
            message = {'Error happend!' : 500}
            return jsonify(message)


@app.route('/deactivate', methods=['GET','POST'])
@login_required
def deactivate():
    if not check_registration(username=session.get('username', None)):
        return make_response('Registration not found!', 200)

    delete_registration(username=session.get('username', None))
    return make_response('Registration successful delete!', 200)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST':
        session['username'] = request.form['username']
        user = User.query.filter_by(username=session.get('username', None)).first()
        if user and user.check_password(request.form['password']):
            logging_in(username=request.form['username'], password=request.form['password'])
            session.permanent = True
            return redirect(url_for('index'))
        else:
            return 'Wrong login or password!'

    elif request.method == 'GET':
        return render_template('login.html', title='Sign In', form=form)


@app.route('/logout', methods=['POST', 'GET'])
@login_required
def logout_user():
    user = session.get('session_id', None)
    return logout(user)

    
    


