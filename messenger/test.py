import os
import unittest

from config import basedir
from app import app, db
from app.models import User, Session
from app.api import make_registration, delete_registration, check_registration, logging_in, logout
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
   
if __name__ == '__main__':
    unittest.main(verbosity=2)