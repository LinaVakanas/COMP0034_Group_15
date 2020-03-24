import os
import unittest

from flask import url_for
from flask_testing import TestCase

from app import create_app, db
from app.models2_backup import Mentor, Mentee, User, PersonalInfo, PersonalIssues


class BaseTest(TestCase):
    """Base test case"""

    def create_app(self):
        app = create_app('config.TestConfig')
        return app

    def SetUp(self):
        # Called at start of every test
        db.create_all()

        # create dummy data for tests
        self.user1 = User(user_type='mentor', email='harrypj@ucl.ac.uk', password='password1')
        self.mentor = Mentor(user_id=1, school_id=0, first_name='Harry', last_name='Potter')
        self.user2 = User(user_type='mentee', email='lily@ucl.ac.uk', password='password2')
        self.mentee = Mentee(user_id=2, school_id=2, first_name='Lily', last_name='Weasley')
        db.session.add_all([self.user1, self.mentor])
        db.session.add_all([self.user2, self.mentee])
        db.session.commit()

    def tearDown(self):
        # Called at end of every test
        db.session.remove()
        db.drop_all()

    def signup(self, first_name, last_name, email, user_type, school_id, password):
        return self.client.post(
            'personal_form/{applicant}/{school_id}/'.format(applicant=user_type, school_id=school_id),
            data=dict(first_name=first_name, last_name=last_name, email=email, password=password),
            follow_redirects=True
        )

    # test mentee and mentor details:
    mentee_data = dict(user_id=3, first_name='Hermione', last_name='Granger', school_id=1,
                       email='hermione@hogwarts.ac.uk', password='password3')
    mentee_personal_issues_data = dict(user_id=3, depression=False, self_harm=True, family=True, drugs=False, ed=True,
                                       share_personal_issues=True)
    mentee_personal_info = dict(carer_email='emma@gmail.com', carer_name='Emma Granger', share_performance=False,
                                status='S', xperience=None, user_id=3)
    mentee_hobbies = dict(user_id=3, football=True, drawing=False)

    mentor_data = dict(user_id=4, first_name='Ron', last_name='Weasley', school_id=0, email='weaasleyy@hogwart.ac.uk',
                       password='password4')
    mentor_personal_issues_data = dict(user_id=4, depression=True, self_harm=True, family=False, drugs=True, ed=True,
                                       share_personal_issues=False)
    mentor_personal_info = dict(carer_email='', carer_name='', share_performance=False,
                                status='W', xperience='=>2', user_id=4)
    mentor_hobbies = dict(user_id=4, football=False, drawing=False)


class TestMain(BaseTest):
    pass


class TestAuth(BaseTest):

    def test_mentee_personal_info_form_saved(self):
        count = PersonalInfo.query.count()
        response = self.client.post(url_for('auth.personal_info',
                                            applicant='mentee', school_id=self.mentee_data.get('school_id')), data=dict(
            carer_name=self.mentee_personal_info.get('carer_name'),
            carer_email=self.mentee_personal_info.get('carer_email'),
            share_performance=self.mentee_personal_info.get('share_performance')
        ))
        count2 = PersonalInfo.query.count()
        print(count2)
        self.assertEqual(count2 - count, 1)
        # self.assertEqual(response.status_cod, 200)

    def test_personal_issues_form_saved(self):
        count = PersonalIssues.query.count()
        response = self.client.post(url_for('auth.personal_issues_form',
                                            applicant=self.mentee_data.get('user_type'),
                                            user_id=self.mentee_data.get('user_id')), data=dict(
            depression=self.mentee_personal_issues_data.get('depression'),
            family=self.mentee_personal_issues_data.get('family'),
            ed=self.mentee_personal_issues_data.get('ed'),
            self_harm=self.mentee_personal_issues_data.get('self_harm'),
            drugs=self.mentee_personal_issues_data.get('drugs'),
            share_personal_issues=self.mentee_personal_issues_data.get('share_personal_issues')
        ), follow_redirects=True)
        count2 = PersonalIssues.query.count()
        self.assertEqual(count2 - count, 1)
        self.assertEqual(response.status_cod, 200)

    def test_registration_form_displays(self):
        target_url = url_for('auth.mentee_signup', applicant='mentee',
                             school_id=self.mentee_data.get('school_id'))
        response = self.client.get(target_url)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Signup', response.data)

    def test_register_mentee_success(self):
        count = Mentee.query.count()
        print(count)
        response = self.client.post(url_for('auth.mentee_signup',
                                            applicant='mentee',
                                            school_id=self.mentee_data.get('school_id')), data=dict(
            email=self.mentee_data.get('email'),
            first_name=self.mentee_data.get('first_name'),
            last_name=self.mentee_data.get('last_name'),
        ), follow_redirects=True)
        count2 = Mentee.query.count()
        print(count2)
        self.assertEqual(count2 - count, 1)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Personal Info', response.data)

    def test_register_mentee_user_success(self):
        count = User.query.count()
        print(count)
        response = self.client.post(url_for('auth.mentee_signup',
                                            applicant='mentee',
                                            school_id=self.mentee_data.get('school_id')), data=dict(
            email=self.mentee_data.get('email'),
            first_name=self.mentee_data.get('first_name'),
            last_name=self.mentee_data.get('last_name'),
        ), follow_redirects=True)
        count2 = User.query.count()
        print(count2)
        self.assertEqual(count2 - count, 1)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Personal Info', response.data)

    def test_register_mentor_success(self):
        count = Mentor.query.count()
        response = self.client.post(url_for('auth.mentor_signup',
                                            applicant='mentor',
                                            school_id=self.mentor_data.get('school_id')), data=dict(
            email=self.mentor_data.get('email'),
            first_name=self.mentor_data.get('first_name'),
            last_name=self.mentor_data.get('last_name'),
        ), follow_redirects=True)
        count2 = Mentor.query.count()
        print(count2)
        self.assertEqual(count2 - count, 1)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Personal Info', response.data)

    def test_register_mentor_user_success(self):
        count = User.query.count()
        response = self.client.post(url_for('auth.mentor_signup',
                                            applicant='mentor',
                                            school_id=self.mentor_data.get('school_id')), data=dict(
            email=self.mentor_data.get('email'),
            first_name=self.mentor_data.get('first_name'),
            last_name=self.mentor_data.get('last_name'),
        ), follow_redirects=True)
        count2 = User.query.count()
        print(count2)
        self.assertEqual(count2 - count, 1)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Personal Info', response.data)

if __name__ == '__main__':
    unittest.main()
