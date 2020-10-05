from app import db
from app.models import User, Session
import uuid
from flask import request, make_response, jsonify, session, flash

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
    login = User.query.filter_by(username=username).first()
    cur_session = Session.query.filter_by(login=username).first()
    cur_id = Session.query.filter_by(uuid=id_session).first()
    
    if not cur_session and login and login.check_password(password):
        this_session = Session(login=login.username, uuid=id_session)
        session['session_id'] = id_session
        db.session.add(this_session)
        db.session.commit()
        return make_response(id_session, 200)

    elif cur_session and not cur_id:
        session['session_id'] = id_session
        cur_session.uuid =  id_session
        db.session.commit()
        return make_response(id_session, 200)


    elif not login or not login.check_password(password):
        return make_response('Wrong login or password', 200)

    elif cur_session:
        return make_response('You already logged in!', 200)


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
    return make_response('Exit was success!', 200)

