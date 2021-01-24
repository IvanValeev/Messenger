from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import login
from datetime import datetime


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(64), index = True, unique = True)
    email = db.Column(db.String(120), index = True, unique = False)
    password_hash = db.Column(db.String(128))

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Session(db.Model):
    __tablename__ = 'Sessions'
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(64), index = True, unique = True)
    uuid = db.Column(db.String(64), index = True, unique = True)
    

    def __repr__(self):
        return '<Session of user {}>'.format(self.login)

class Friends(db.Model):
    __tablename__ = 'Friends'
    id = db.Column(db.Integer, primary_key=True)
    main_friend =  db.Column(db.String(64), index = True, unique = False)
    friend = db.Column(db.String(64), index = True, unique = False)

    def __repr__(self):
        return '<{} is friend of user {}>'.format(self.friend, self.main_friend)

class Messages(db.Model):
    __tablename__ = 'Messages'
    id = db.Column(db.Integer, primary_key=True)
    sender = db.Column(db.String(64), index = True, unique = False)
    receiver = db.Column(db.String(64), index = True, unique = False)
    msg_text  = db.Column(db.String(256), index = True, unique = False)
    time_stamp = db.Column(db.DateTime, index = True, default = datetime.utcnow)

    def __repr__(self):
        return '<Message of user {}>'.format(self.receiver)


@login.user_loader
def load_user(id):
    return User.query.get(int(id))