import os
import unittest

from flask import url_for
from flask_testing import TestCase

from app import create_app, db
from app.models2 import Mentor, Mentee, User

class BaseTest(TestCase):
    """Base test case"""

    def create_app(self):
        app = create_app('config.TestConfig')
        return app

    def SetUp(self):
        # Called at start of every test
        db.create_all()

        #create dummy data for tests
        self.user1 = User(user_id=1, user_type='mentor', email='harrypj@ucl.ac.uk', password='password1')
        self.mentor = Mentor(user_id=1, school_id=0, first_name='Harry', last_name='Potter')
        self.user2 = User(user_id=2, user_type='mentee', email='lily@ucl.ac.uk', password='password2')
        self.mentee = Mentee(user_id=2, school_id=2, first_name='Lily', last_name='Weasley')
        db.session.add([self.user1, self.mentor])
        db.session.add([self.user2, self.mentee])
        db.session.commit()

    def tearDown(self):
        # Called at end of every test
        db.session.remove()
        db.drop_all()

    def signup(self, first_name, last_name, email, user_type, school_id, password ):
        return self.client.post(
            'personal_form/{applicant}/{school_id}/'.format(applicant=user_type, school_id=school_id),
            data=dict(first_name=first_name, last_name=last_name, email=email, password=password),
            follow_redirects = True
        )

    # test mentee and mentor details:
    mentee_data = dict(first_name = 'Hermione', last_name= 'Granger', school_id= 1, email= 'hermione@hogwart.ac.uk')
    mentor_data = dict(first_name = 'Ron', last_name= 'Weasley', school_id= 0, email= 'weaasleyy@hogwart.ac.uk')


class TestMain(BaseTest):

    def test_personal_issues_form_saved(self):
        target_url = 

