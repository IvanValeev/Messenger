from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = 'top secret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///C:/Users/Иван/messenger/mysql.db' 
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    def __repr__(self):
        return '<User {}>'.format(self.username)

# db.create_all() #не забыть эту комманду для создания таблицы, если её не существует

# u1 = User(username = 'Peter', email = '1123@gmail.com')
# db.session.add(u1)
# db.session.commit()

res = User.query.all()

for user in res:
    db.session.delete(user)

db.session.commit()

# for user in res:
#     print(user.username, user.email)

# @app.route('/')
# def smth():
#     return 'HI!'

# if __name__ == '__main__':
#     app.run(debug=True)