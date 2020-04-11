import os
import unittest

from flask import url_for
from flask_testing import TestCase

from app import create_app, db
from app.models2_backup import Mentor, Mentee, User, PersonalInfo, PersonalIssues, Pair, Location, Meeting, School


class BaseTest(TestCase):
    """Base test case"""

    def create_app(self):
        app = create_app('config.TestConfig')
        return app

    def SetUp(self):
        # Called at start of every test
        db.create_all()

        # create dummy data for tests
        self.school0 = School(is_approved=0, school_id=0, school_name="", school_email="", ofsted_ranking="")
        self.user1 = User(user_type='mentor', school_id=0, email='harrypj@ucl.ac.uk', is_active=True)
        self.user1.set_password('password1')
        self.mentor = Mentor(user_id=1, school_id=0, first_name='Harry', last_name='Potter', paired=True, is_approved=True)
        self.school1 = School(is_approved=1, school_id=1, school_name='Hogwarts', school_email="hogwarts@howarts.ac.uk",
                         ofsted_ranking="1")
        self.user2 = User(user_type='mentee', school_id=1, email='lily@ucl.ac.uk', is_active=True)
        self.user2.set_password('password2')
        self.mentee = Mentee(user_id=2, school_id=1, first_name='Lily', last_name='Weasley', paired=True)
        self.mentee_location = Location(user_id=2, address="Hogmeade", city="London",
                                        postcode="XR4 5AQ", avoid_area="Neasden")
        self.meeting = Meeting(pair_id=1, date='5/5/2020', time='1700',
                               duration='1', address="Kilburn Road", postcode="XY4 5UU", type="Library",
                               mentee_approval=False)

        db.session.add_all([self.school0, self.school1])
        db.session.add_all([self.user1, self.mentor])
        db.session.add_all([self.user2, self.mentee])
        db.session.add(self.mentee_location)
        db.session.flush()

        self.pair = Pair(mentor_id=self.mentor.mentor_id, mentee_id=self.mentee.mentee_id)
        db.session.add(self.pair)
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
    mentee_data = dict(user_id=4, user_type='mentee', first_name='Hermione', last_name='Granger', school_id=1,
                       password='password3', email='test@mail.com')
    mentee_personal_issues_data = dict(user_id=4, depression=False, self_harm=True, family=True, drugs=False, ed=True,
                                       )
    mentee_personal_info = dict(carer_email='emma@gmail.com', carer_name='Emma Granger', share_performance=False,
                                user_id=4, share_personal_issues=True,
                                share_med_cond=True)
    mentee_hobbies = dict(user_id=4, football=True, drawing=False)

    mentor_data = dict(user_id=5, user_type='mentor', first_name='Ron', last_name='Weasley', school_id=0,
                       password='password4', email='test2@mail.com')

    mentor_personal_issues_data = dict(user_id=5, depression=True, self_harm=True, family=False, drugs=True, ed=True,
                                       )
    mentor_personal_info = dict(status='W', xperience='>=2', user_id=5, share_personal_issues=False, share_med_cond=False,
                                )
    mentor_hobbies = dict(user_id=5, football=False, drawing=False)
    book_meeting = dict(pair_id=1, day='3', month='5', year=2020, date='3/5/2020', hour='17', minute='00', time='1700',
                        duration='1', address="Kilburn Road", postcode="WY4 5UU", type="Library")


class TestMain(BaseTest):
    pass


class TestAuth(BaseTest):

    def test_mentee_personal_info_form_saved(self):
        BaseTest.SetUp(self)
        count = PersonalInfo.query.count()
        response = self.client.post(url_for('auth.personal_form',
                                            applicant_type=self.mentee_data.get('user_type'),
                                            school_id=self.mentee_data.get('school_id')), data=dict(
            email=self.mentee_data.get('email'),
            user_type=self.mentee_data.get('user_type'),
            school_id=self.mentee_data.get('school_id'),
            first_name=self.mentee_data.get('first_name'),
            last_name=self.mentee_data.get('last_name'),
            password=self.mentee_data.get('password'),
            carer_email=self.mentee_personal_info.get('carer_email'),
            carer_name=self.mentee_personal_info.get('carer_name'),
            share_performance=self.mentee_personal_info.get('share_performance'),
            share_personal_issues=self.mentee_personal_info.get('share_personal_issues'),
            share_med_cond=self.mentee_personal_info.get('share_med_cond')
        ), follow_redirects=True)
        count2 = PersonalInfo.query.count()
        print(count2)
        self.assertEqual(count2 - count, 1)
        self.assertEqual(response.status_code, 200)

    def test_registration_form_displays(self):
        BaseTest.SetUp(self)
        target_url = url_for('auth.personal_form', applicant_type='mentee',
                             school_id=self.mentee_data.get('school_id'))
        response = self.client.get(target_url)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Signup', response.data)

    def test_register_mentee_success(self):
        BaseTest.SetUp(self)
        mentees = Mentee.query.with_entities(Mentee.first_name, Mentee.last_name).all()
        print(mentees)
        count = Mentee.query.count()
        print(count)
        response = self.client.post(url_for('auth.personal_form',
                                            applicant_type=self.mentee_data.get('user_type'),
                                            school_id=self.mentee_data.get('school_id')), data=dict(
            email=self.mentee_data.get('email'),
            user_type=self.mentee_data.get('user_type'),
            school_id=self.mentee_data.get('school_id'),
            first_name=self.mentee_data.get('first_name'),
            last_name=self.mentee_data.get('last_name'),
            password=self.mentee_data.get('password'),
            carer_email=self.mentee_personal_info.get('carer_email'),
            carer_name=self.mentee_personal_info.get('carer_name'),
            share_performance=self.mentee_personal_info.get('share_performance'),
            share_personal_issues=self.mentee_personal_info.get('share_personal_issues'),
            share_med_cond=self.mentee_personal_info.get('share_med_cond')
        ), follow_redirects=True)
        count2 = Mentee.query.count()
        print(count2)
        self.assertEqual(count2 - count, 1)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Signup', response.data)

    def test_register_mentee_user_success(self):
        BaseTest.SetUp(self)
        count = User.query.count()
        print(count)
        response = self.client.post(url_for('auth.personal_form',
                                            applicant_type=self.mentee_data.get('user_type'),
                                            school_id=self.mentee_data.get('school_id')), data=dict(
            email=self.mentee_data.get('email'),
            user_type=self.mentee_data.get('user_type'),
            school_id=self.mentee_data.get('school_id'),
            first_name=self.mentee_data.get('first_name'),
            last_name=self.mentee_data.get('last_name'),
            password=self.mentee_data.get('password'),
            carer_email=self.mentee_personal_info.get('carer_email'),
            carer_name=self.mentee_personal_info.get('carer_name'),
            share_performance=self.mentee_personal_info.get('share_performance'),
            share_personal_issues=self.mentee_personal_info.get('share_personal_issues'),
            share_med_cond=self.mentee_personal_info.get('share_med_cond')
        ), follow_redirects=True)
        count2 = User.query.count()
        print(count2)
        self.assertEqual(count2 - count, 1)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Signup', response.data)

    def test_register_mentor_success(self): #########################################################
        BaseTest.SetUp(self)
        count = Mentor.query.count()
        print(count)
        response = self.client.post(url_for('auth.personal_form',
                                            applicant_type=self.mentor_data.get('user_type'),
                                            school_id=self.mentor_data.get('school_id')), data=dict(
            email=self.mentor_data.get('email'),
            user_type=self.mentor_data.get('user_type'),
            school_id=self.mentor_data.get('school_id'),
            first_name=self.mentor_data.get('first_name'),
            last_name=self.mentor_data.get('last_name'),
            password=self.mentor_data.get('password'),
            status=self.mentor_personal_info.get('status'),
            xperience=self.mentor_personal_info.get('xperience'),
            share_personal_issues=self.mentor_personal_info.get('share_personal_issues'),
            share_med_cond=self.mentor_personal_info.get('share_med_cond')
        ), follow_redirects=True)
        count2 = Mentor.query.count()
        print(count2)
        self.assertEqual(count2 - count, 1)
        self.assertEqual(response.status_code, 200)
        # self.assertIn(b'Signup', response.data)

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

    def test_book_meeting_success(self):
        BaseTest.SetUp(self)

        count = Meeting.query.count()
        print(count)
        response = self.client.post(url_for('main.book_meeting', mentee_id=self.pair.mentee_id, mentee_user_id=self.mentee.user_id), data=dict(
            day=self.book_meeting.get('day'),
            month=self.book_meeting.get('month'),
            year=self.book_meeting.get('year'),
            hour=self.book_meeting.get('hour'),
            minute=self.book_meeting.get('minute'),
            duration=self.book_meeting.get('duration'),
            type=self.book_meeting.get('type'),
            address=self.book_meeting.get('address'),
            postcode=self.book_meeting.get('postcode'),
        ), follow_redirects=True)
        count2 = Meeting.query.count()
        print(count2)
        self.assertEqual(count2 - count, 1)
        self.assertEqual(response.status_code, 200)

    def test_confirm_meeting_success(self):
        BaseTest.SetUp(self)
        print(self.meeting)
        db.session.add(self.meeting)
        db.session.commit()
        meeting = Meeting.query.first()

        response = self.client.post(url_for('main.confirm_meeting', meeting_id=meeting.meeting_id), data=dict(
            approval=True,
        ), follow_redirects=True)
        meeting = Meeting.query.first()
        self.assertTrue(meeting.mentee_approval)
        self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()
