import os
import unittest

from config import basedir
from app import app, db
from app.models import User, Session, Friends
from app.api import make_registration, delete_registration, check_registration, logging_in, logout, add_to_friend_list, kick_from_friends, kick_all_friends, find_friend_of_user
from app.api import find_all_friends_of_user
from flask import current_app, make_response, session

class TestCase(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        app.config['CSRF_ENABLED'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'test.db')
        self.app = app.test_client()
        db.create_all()
        app_context = app.app_context()
        app_context.push()
        make_registration('test', 'test')
        make_registration('test1', 'test')
        make_registration('test2', 'test')
        add_to_friend_list('test', 'test1')
        add_to_friend_list('test', 'test2')


    def tearDown(self):
        db.session.remove()
        db.drop_all()

    
    def test_show_main_page(self):
        response = self.app.get('/', follow_redirects=True)
        self.assertEqual(response.status_code, 200)


    def test_show_login_page(self):
        response = self.app.get('/login', follow_redirects=True)
        self.assertEqual(response.status_code, 200)


    def test_check_registration(self):
        excepted = True
        self.assertEqual(check_registration('test'), excepted)


    def test_success_loggining_in(self):
        response = self.app.post('/login', data=dict(username='test', password='test'), follow_redirects=True)
        print(response.data)
        self.assertTrue(response.data != 'Wrong login or password!')


    def test_false_loggining_in(self):
        response = self.app.post('/login', data=dict(username='1', password='2'), follow_redirects=True)
        self.assertEqual(response.data , b'Wrong login or password!')


    def test_false_loggining_in_wrong_login(self):
        response = self.app.post('/login', data=dict(username='1', password='test'), follow_redirects=True)
        self.assertEqual(response.data , b'Wrong login or password!')


    def test_false_loggining_in_wrong_password(self):
        response = self.app.post('/login', data=dict(username='test', password='2'), follow_redirects=True)
        self.assertEqual(response.data , b'Wrong login or password!')


    def test_login_require_logout(self):
        response = self.app.get('/logout')
        self.assertEqual(response.data , b'First you need to login!')


    def test_logout(self):
        resp = self.app.post('/login', data=dict(username='test', password='test'), follow_redirects=True)
        response = self.app.get('/logout')
        self.assertEqual(response.data , b'Exit was success!')


    def test_login_require_deactivate_registration(self):
        response = self.app.get('/deactivate')
        self.assertEqual(response.data , b'First you need to login!')


    def test_deactivate_registration(self):
        resp = self.app.post('/login', data=dict(username='test', password='test'), follow_redirects=True)
        response = self.app.get('/deactivate')
        self.assertEqual(response.data , b'Registration successful delete!')


    def test_add_yourself_to_friends(self):
        add_to_friend_list('test', 'test')
        resp = Friends.query.filter_by(main_friend='test', friend = 'test').first()
        expected = None
        self.assertEqual(expected , resp)


    def test_success_add_to_friend_list(self):
        add_to_friend_list('test', 'test2')
        user = Friends.query.filter_by(main_friend='test', friend = 'test2').first()
        expected = 'test2'
        self.assertEqual(expected , user.friend)


    def test_add_to_friends_unregistreted_user(self):
        add_to_friend_list('test', 'Pedro')
        user = Friends.query.filter_by(main_friend='test', friend = 'Pedro').first()
        expected = None
        self.assertEqual(expected , user)


    def test_kick_yourself_from_friends(self):
        expected = Friends.query.filter_by(main_friend='test').all()
        resp = 2
        kick_from_friends('test', 'test')
        self.assertEqual(len(expected) , resp)


    def test_kick_from_friends(self):
        resp = 1
        kick_from_friends('test', 'test1')
        expected = Friends.query.filter_by(main_friend='test').all()
        self.assertEqual(len(expected) , resp)


    def test_kick_unregistreted_user_from_friends(self):
        expected = Friends.query.filter_by(main_friend='test').all()
        resp = 2
        kick_from_friends('test', 'test123')
        self.assertEqual(len(expected) , resp)


    def test_kick_all_friends(self):
        resp = 0
        kick_all_friends('test')
        expected = Friends.query.filter_by(main_friend='test').all()
        self.assertEqual(len(expected) , resp)

    
    def test_find_yourself_in_friend_list(self):
        friend = Friends.query.filter_by(main_friend='test', friend = 'test').first()
        expected = None
        self.assertEqual(expected , friend)
    

    def test_find_friend_in_list(self):
        main_user = Friends.query.filter_by(main_friend='test', friend = 'test1').first()
        expected = 'test1'
        self.assertEqual(expected , main_user.friend)


    def test_find_all_friends(self):
        result = []
        expected = ['test1', 'test2']
        list_of_friends = Friends.query.filter_by(main_friend='test').all()
        for friend in list_of_friends:
            result.append(friend.friend)
        self.assertEqual(expected , result)
    

if __name__ == '__main__':
    unittest.main(verbosity=2)