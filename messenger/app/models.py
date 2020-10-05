from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import login


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


@login.user_loader
def load_user(id):
    return User.query.get(int(id))