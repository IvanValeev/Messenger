# -*- coding: utf-8 -*-
from flask import render_template, flash, redirect, url_for, session
from app import app, db
from flask import request, make_response, jsonify
from app.api import make_registration, delete_registration, check_registration, logging_in, logout, send_msg, add_to_friend_list, find_all_friends_of_user, get_all_incoming_msg
from app.models import User, Session
from flask_login import current_user, login_user
import json
import uuid
from functools import wraps
from app.forms import LoginForm, RegistrationForm, SendMessageForm, AddFriendsForm
import time
    

def login_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        cur_user = Session.query.filter_by(login=session.get('username', None)).first()
        if cur_user and session.get('session_id', None) == cur_user.uuid:
            return f(*args, **kwargs)
        else:
            return 'First you need to login!'
    return wrapper

@app.route('/home')
@app.route('/index')
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods = ['GET', 'POST'])
def register():
    if request.method == 'GET':
        form = RegistrationForm()
        return render_template('register.html', title='Register', form=form)

    elif request.method == 'POST':
        if check_registration(username=request.form['username']):
                return 'You alredy have registration!'
        form = RegistrationForm()
        if form.validate_on_submit():
            if request.form['password'] == request.form['password2']:
                    make_registration(request.form['username'], request.form['password'])
                    flash('Congratulations, you are now a registered user!')
                    return redirect(url_for('login'))
            redirect(url_for('register'))
        return render_template('register.html', title='Register', form=form)


    # if request.method == 'GET':
    #     form = RegistrationForm()
    #     return render_template('register.html', title='Register', form=form)

    # elif request.method == 'POST':
    #     form = RegistrationForm()
    #     if check_registration(username=request.form['username']):
    #         # return 'You alredy have registration!'
    #         flash('You alredy have registration!')
    #         return redirect(url_for('login'))
    #     # try:
    #     #     if request.form['password'] == request.form['password2']:
    #     #         make_registration(request.form['username'], request.form['password'])
    #     #         flash('Congratulations, you are now a registered user!')
    #     #         return redirect(url_for('login'))
    #     #     else:
    #     #         flash('Password does not match!')
    #     #         # return 'Password does not match!'
    #     #         return render_template('register.html', title='Register', form=form)
    #     # except:
    #     #     message = {'Error happend!' : 500}
    #     #     return jsonify(message)
        
    #     if request.form['password'] == request.form['password2']:
    #         make_registration(request.form['username'], request.form['password'])
    #         flash('Congratulations, you are now a registered user!')
    #         return redirect(url_for('login'))
    #     else:
    #         flash('Password does not match!')
    #         # return 'Password does not match!'
    #         return render_template('register.html', title='Register', form=form)
    


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
            session.permanent = True
            return logging_in(username=request.form['username'], password=request.form['password'])
            # return redirect(url_for('index'))
        else:
            return 'Wrong login or password!'

    elif request.method == 'GET':
        return render_template('login.html', title='Sign In', form=form)


@app.route('/logout', methods=['POST', 'GET'])
@login_required
def logout_user():
    user = session.get('session_id', None)
    return logout(user)


@app.route('/send_msg', methods=['POST', 'GET'])
@app.route('/send_message', methods=['POST', 'GET'])
@login_required
def sending_msg():
    form = SendMessageForm()
    if request.method == 'GET':
        return render_template('send_msg.html', title = 'Send message', form=form)
    elif request.method == 'POST':
        send_msg(sender=session['username'], receiver=request.form['receiver'], msg_text=request.form['msg'])
        return render_template('send_msg.html', title = 'Send message', form=form)

@app.route('/add_friend', methods=['POST', 'GET'])
@login_required
def add_friend():
    form = AddFriendsForm()
    if request.method == 'GET':
        return render_template('add_friends.html', form=form)
    elif request.method == 'POST':
        add_to_friend_list(session['username'], request.form['friend'])
        return redirect(url_for('user', username=session['username']))

@app.route('/user/<username>')
@login_required
def user(username):
    user=username
    return render_template('user_page.html', user=user)


@app.route('/list_of_friends')
@login_required
def list_of_friends():
    list_friends = find_all_friends_of_user(session['username'])
    return render_template('list_of_friends.html', list_of_friends=list_friends)


@app.route('/incoming_messages')
@login_required
def incoming_messages():
    list_of_messages = get_all_incoming_msg(session['username'])
    return render_template('incoming_msg.html', list_of_msgs = list_of_messages) 