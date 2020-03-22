import os
import unittest

from flask import url_for
from flask_testing import TestCase

from app import create_app, db
from app.models2_backup import Mentor, Mentee, User

class BaseTest(TestCase):
    """Base test case"""

    def create_app(self):
        app = create_app('config.TestConfig')
        return app

    def SetUp(self):
        # Called at start of every test
        db.create_all()

        #create dummy data for tests
        self.user1 = User(user_type='mentor', email='harrypj@ucl.ac.uk', password='password1')
        self.mentor = Mentor(user_id=1, school_id=0, first_name='Harry', last_name='Potter')
        self.user2 = User(user_type='mentee', email='lily@ucl.ac.uk', password='password2')
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
    mentee_data = dict(user_id=3, first_name = 'Hermione', last_name= 'Granger', school_id= 1, email= 'hermione@hogwart.ac.uk', password='password3')
    mentor_data = dict(user_id=4, first_name = 'Ron', last_name= 'Weasley', school_id= 0, email= 'weaasleyy@hogwart.ac.uk', password='password4')





class TestAuth(BaseTest):

    def test_registration_form_displays(self):
        target_url = url_for('auth.personal_forms')
        response = self.client.get(target_url)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Signup', response.data)

    def test_register_mentee_success(self):
        count = Mentee.query.count()
        response = self.client.post(url_for('auth.signup'), data=dict(
            user_email=self.mentee_data.get('email'),
            first_name=self.mentee_data.get('first_name'),
            last_name=self.mentee_data.get('last_name'),
            user_id=self.mentee_data.get('user_id'),
            school_id = self.mentee_data.get('school_id')
        ), follow_redirects=True)
        count2 = Mentee.query.count()
        self.assertEqual(count2 - count, 1)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Address', response.data)

    def test_register_mentee_user_success(self):
        count = User.query.count()
        response = self.client.post(url_for('auth.signup'), data=dict(
            email=self.mentee_data.get('email'),
            user_type="mentee",
            user_password=self.mentee_data.get('password'),
            first_name=self.mentee_data.get('first_name'),
            last_name=self.mentee_data.get('last_name'),
            school_id=self.mentee_data.get('school_id')
        ), follow_redirects=True)
        count2 = User.query.count()
        self.assertEqual(count2 - count, 1)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Address', response.data)
        

    # def test_register_mentor_success(self):
    #     count = Mentor.query.count()
    #     response = self.client.post(url_for('auth.signup'), data=dict(
    #         user_email=self.mentor_data.get('email'),
    #         first_name=self.mentor_data.get('first_name'),
    #         last_name=self.mentor_data.get('last_name'),
    #         user_id=self.mentor_data.get('user_id'),
    #         school_id = self.mentor_data.get('school_id')
    #     ), follow_redirects=True)
    #     count2 = Mentor.query.count()
    #     self.assertEqual(count2 - count, 1)
    #     self.assertEqual(response.status_code, 200)
    #     self.assertIn(b'Address', response.data)
    #
    #
    # def test_register_mentor_user_success(self):
    #     count = User.query.count()
    #     response = self.client.post(url_for('auth.signup'), data=dict(
    #         user_email=self.mentor_data.get('email'),
    #         first_name=self.mentor_data.get('first_name'),
    #         last_name=self.mentor_data.get('last_name'),
    #         school_id=self.mentor_data.get('school_id')
    #     ), follow_redirects=True)
    #     count2 = User.query.count()
    #     self.assertEqual(count2 - count, 1)
    #     self.assertEqual(response.status_code, 200)
    #     self.assertIn(b'Address', response.data)