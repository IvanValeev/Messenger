from app import db
from app.models import User, Session, Friends
import uuid
from flask import request, make_response, jsonify, session, flash, redirect, url_for, render_template

def make_registration(login, pswd):
    user = User(username=login)
    user.set_password(pswd)
    db.session.add(user)
    db.session.commit()

def delete_registration(username):
    user = User.query.filter_by(username=username).scalar()
    cur_session = Session.query.filter_by(login=username).first()
    db.session.delete(user)
    db.session.delete(cur_session)
    db.session.commit()

def check_registration(username):
    if User.query.filter_by(username=username).scalar():
        return True
    else:
        return False

def logging_in(username, password):
    id_session = str(uuid.uuid1())
    cur_session = Session.query.filter_by(login=username).first()
    
    if not cur_session:
        this_session = Session(login=username, uuid=id_session)
        session['session_id'] = id_session
        db.session.add(this_session)
        db.session.commit()
        return make_response(id_session, 200)
        # return render_template('index.html', user=session.get('session_id', None))

    elif cur_session and cur_session.uuid == session.get('session_id', None):
        return make_response('You already logged in!', 200)


    elif cur_session and cur_session.uuid != session.get('session_id', None):
        session['session_id'] = id_session
        cur_session.uuid =  id_session
        db.session.commit()
        # return make_response('Enter success!', 200)
        return render_template('index.html', user=session.get('session_id', None))
    
    # elif not login or not login.check_password(password):
    #     return make_response('Wrong login or password', 200)

    


# def logout(username):
#     cur_session = Session.query.filter_by(uuid=session['session_id']).first()
#     db.session.delete(cur_session)
#     db.session.commit()
#     return make_response('Exit was success!', 200)

def logout(username):
    cur_session = Session.query.filter_by(uuid=session.get('session_id', None)).first()
    session.pop(username, None)
    session.pop(session['session_id'], None)
    db.session.delete(cur_session)
    db.session.commit()
    session.clear()
    return make_response('Exit was success!', 200)
    # return redirect(url_for('index'))


def add_to_friend_list(username, friend_name):
    if username == friend_name:
        print("You can't add yourself to friends.")
    elif check_registration(friend_name):
        user = Friends(main_friend = username, friend = friend_name)
        db.session.add(user)
        db.session.commit()
    else:
        print("This user has no registration.")


def kick_from_friends(username, friend_name):
    lost_friend = Friends.query.filter_by(main_friend=username, friend = friend_name).first()
    if username == friend_name:
        print("You can't kick yourself from friend list.")
    elif lost_friend:
        db.session.delete(lost_friend)
        db.session.commit()
    else:
        print('This person is not your friend.')


def kick_all_friends(username):
    all_friends = Friends.query.filter_by(main_friend=username).all()
    for friend in all_friends:
        db.session.delete(friend)
    db.session.commit()

def find_friend_of_user(username, friend_name):
    if username == friend_name:
        return 'You trying to find yourself.'
    friend = Friends.query.filter_by(main_friend=username, friend = friend_name).first()
    return friend


def find_all_friends_of_user(username):
    list_of_friends = Friends.query.filter_by(main_friend=username).all()
    return list_of_friends