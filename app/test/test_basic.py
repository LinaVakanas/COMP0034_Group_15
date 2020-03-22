import os
import unittest

from flask import url_for
from flask_testing import TestCase

from app import create_app, db
from app.models2 import Mentor, Mentee, User, PersonalInfo, PersonalIssues

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
    mentee_data = dict(first_name='Hermione', last_name= 'Granger', school_id= 1, email= 'hermione@hogwart.ac.uk')
    mentee_personal_issues_data = dict(user_id=3, depression=False, self_harm=True, family=True, drugs=False, ed=True,
                                       share_personal_issues=True)
    mentee_personal_info = dict(carer_email='emma@parent.uk', carer_name='Emma Granger', share_performance=False,
                                status='S', xperience=None, user_id=3)
    mentee_hobbies = dict(user_id=3, football=True, drawing=False)

    mentor_data = dict(first_name='Ron', last_name='Weasley', school_id=0, email='weaasleyy@hogwart.ac.uk')
    mentor_personal_issues_data = dict(user_id=4, depression=True, self_harm=True, family=False, drugs=True, ed=True,
                                       share_personal_issues=False)
    mentor_personal_info = dict(carer_email='', carer_name='', share_performance=False,
                                status='W', xperience='=>2', user_id=4)
    mentor_hobbies = dict(user_id=4, football=False, drawing=False)


class TestMain(BaseTest):
    def test_database(self):
        testing = os.path.exists("webapp_sqlite.db")
        self.assertTrue(testing)

class TestAuth(BaseTest):

    def test_personal_issues_form_saved(self):
        count = PersonalIssues.query.count()
        response = self.client.post(url_for('auth.personal_issues_form'), data=dict(
            depression=self.mentee_personal_issues_data.get('depression'),
            family=self.mentee_personal_issues_data.get('family'),
            ed=self.mentee_personal_issues_data.get('ed'),
            self_harm=self.mentee_personal_issues_data.get('self_harm'),
            drugs=self.mentee_personal_issues_data.get('drugs'),
            share_personal_issues=self.mentee_personal_issues_data.get('share_personal_issues')
        ), follow_redirects=True)
        count2 = PersonalIssues.query.count()
        self.assertEqual(count2-count, 1)
        self.assertEqual(response.status_cod, 200)

if __name__ == '__main__':
    unittest.main()

