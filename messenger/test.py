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

    
    def test_main_page(self):
        response = self.app.get('/', follow_redirects=True)
        self.assertEqual(response.status_code, 200)


    def test_check_registration(self):
        excepted = True
        self.assertEqual(check_registration('test'), excepted)

    def test_loggining_in(self):
        response = self.app.post('/login', data=dict(username='Ivan', password='Valeev'), follow_redirects=True)
        self.assertEqual(response.status_code, 200)


   
    

if __name__ == '__main__':
    unittest.main(verbosity=2)