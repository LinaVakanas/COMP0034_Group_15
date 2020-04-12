import os
import unittest

from flask import url_for
from flask_login import current_user, login_manager, login_user, AnonymousUserMixin
from flask_login._compat import unicode
from flask_testing import TestCase

from app import create_app, db
from app.models2_backup import Mentor, Mentee, User, PersonalInfo, PersonalIssues, Pair, Location, Meeting, School, \
    Admin


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
        self.user0 = User(user_id=0, user_type='admin', school_id=0, email="admin@admin.com", bio=None, is_active=True,
                     profile_pic=None, creation_date=None)
        self.user0.set_password('admin123')
        self.admin = Admin(user_id=0)
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

        # UNPAIRED MENTEE MENTOR
        self.user3 = User(user_type='mentor', school_id=0, email='mentor@ucl.ac.uk', is_active=True)
        self.user3.set_password('password3')
        self.mentor2 = Mentor(user_id=3, school_id=0, first_name='Mentor', last_name='Potter', paired=False,
                             is_approved=True)
        self.mentor2_location = Location(user_id=3, address="Hogmeade", city="London",
                                        postcode="XR4 5AQ", avoid_area="Neasden")

        self.user4 = User(user_type='mentee', school_id=1, email='mentee@ucl.ac.uk', is_active=True)
        self.user4.set_password('password4')
        self.mentee2 = Mentee(user_id=4, school_id=1, first_name='Mentee', last_name='Weasley', paired=False)
        self.mentee2_location = Location(user_id=4, address="Blop", city="London",
                                        postcode="XR4 5AQ", avoid_area="Neasden")

        # INACTIVE MENTOR AND MENTEES
        self.user5 = User(user_type='mentor', school_id=0, email='mentor1@ucl.ac.uk', is_active=False)
        self.user5.set_password('password3')
        self.mentor3 = Mentor(user_id=5, school_id=0, first_name='Mahdi', last_name='Shah', paired=False,
                              is_approved=False)

        self.user6 = User(user_type='mentee', school_id=1, email='mentee1@ucl.ac.uk', is_active=False)
        self.user6.set_password('password4')
        self.mentee3 = Mentee(user_id=6, school_id=1, first_name='Mahir', last_name='Shah', paired=False)


        self.user7 = User(user_type='mentor', school_id=0, email='harley@quin.uk', is_active=True)
        self.user7.set_password('password3')
        self.mentor4 = Mentor(user_id=7, school_id=0, first_name='Harley', last_name='Quinn', paired=False,
                              is_approved=True)
        self.mentor4_location = Location(user_id=7, address="Oxford Street", city="London",
                                         postcode="XR4 5AQ", avoid_area="Kilburn")
        self.mentor4_personal_info = PersonalInfo(user_id=7, status='S', xperience='>=2', share_personal_issues=True,
                                              carer_email='', carer_name='', share_med_cond=True)


        db.session.add_all([self.school0, self.school1])
        db.session.add_all([self.user1, self.mentor])
        db.session.add_all([self.user2, self.mentee])
        db.session.add(self.mentee_location)
        db.session.add_all([self.user3, self.mentor2, self.mentor2_location])
        db.session.add_all([self.user4, self.mentee2, self.mentee2_location])
        db.session.add_all([self.user5, self.mentor3, self.user6, self.mentee3])
        db.session.add_all([self.user7, self.mentor4, self.mentor4_personal_info])
        db.session.add_all([self.user0, self.admin])
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

    mentor_personal_issues_data = dict(user_id=5, depression=True, self_harm=True, drugs=True, ed=True,
                                       )
    mentor_personal_info = dict(carer_email='', carer_name='', status='W', xperience='>=2', user_id=5, share_personal_issues=True, share_med_cond=True,
                                )
    mentor_hobbies = dict(user_id=5, football=True)
    book_meeting = dict(pair_id=1, day='3', month='5', year=2020, date='3/5/2020', hour='17', minute='00', time='1700',
                        duration='1', address="Kilburn Road", postcode="WY4 5UU", type="Library")

    mentor4_location_data = dict(user_id=7, address="Oxford Street", city="London",
                                     postcode="XR4 5AQ", avoid_area="Kilburn")


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

    def test_mentor_location_form_saved(self):
        BaseTest.SetUp(self)
        count = Location.query.count()
        print(self.user7.user_id)

        response = self.client.post(url_for('auth.location_form', applicant_type=self.user7.user_type, applicant_id=self.user7.user_id),data=dict(
            address=self.mentor4_location_data.get('address'),
            city=self.mentor4_location_data.get('city'),
            postcode=self.mentor4_location_data.get('postcode'),
            avoid_area=self.mentor4_location_data.get('avoid_area')
        ), follow_redirects=True)
        count2 = Location.query.count()
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

    def test_register_mentee_failed_invalid_school_ID(self):
        BaseTest.SetUp(self)
        mentees = Mentee.query.with_entities(Mentee.first_name, Mentee.last_name).all()
        print(mentees)
        count = Mentee.query.count()
        print(count)
        response = self.client.post(url_for('auth.personal_form',
                                            applicant_type=self.mentee_data.get('user_type'),
                                            school_id=2), data=dict(
            email=self.mentee_data.get('email'),
            user_type=self.mentee_data.get('user_type'),
            school_id=2,
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
        self.assertEqual(count2 - count, 0)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Sorry you have entered an invalid', response.data)

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
        self.assertIn(b'Pending Approval', response.data)

    def test_register_mentor_user_success(self):
        BaseTest.SetUp(self)
        count = User.query.count()
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
        count2 = User.query.count()
        print(count2)
        self.assertEqual(count2 - count, 1)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Pending Approval', response.data)

    def test_admin_approve_mentee_success(self):
        BaseTest.SetUp(self)
        AnonymousUserMixin.user_type = 'admin'
        # unapproved_mentees = Mentee.query.join(User, User.user_id == Mentee.user_id).filter(User.is_active == False).with_entities(Mentee.first_name, Mentee.last_name).all()
        count = Mentee.query.join(User, User.user_id==Mentee.user_id).filter(User.is_active==False).count()
        print(count)
        response = self.client.post(url_for('main.controlpanel_mentee'), data=dict(
            approve=self.mentee3.mentee_id
        ), follow_redirects=True)
        count2 = Mentee.query.join(User, User.user_id==Mentee.user_id).filter(User.is_active==False).count()
        print(count2)
        self.assertEqual(count2 - count, -1)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Administrator Control Panel', response.data)

    def test_admin_approve_mentor_success(self):
        BaseTest.SetUp(self)
        AnonymousUserMixin.user_type = 'admin'
        # unapproved_mentors = mentor.query.join(User, User.user_id == mentor.user_id).filter(User.is_active == False).with_entities(mentor.first_name, mentor.last_name).all()
        count = Mentor.query.join(User, User.user_id==Mentor.user_id).filter(Mentor.is_approved==False).count()
        print(count)
        response = self.client.post(url_for('main.controlpanel_mentor'), data=dict(
            approve=self.mentor3.mentor_id
        ), follow_redirects=True)
        count2 = Mentor.query.join(User, User.user_id==Mentor.user_id).filter(Mentor.is_approved==False).count()
        print(count2)
        self.assertEqual(count2 - count, -1)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Administrator Control Panel', response.data)

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

    def test_pair_mentee_mentor_success(self):
        BaseTest.SetUp(self)
        count = Pair.query.count()
        response = self.client.get(url_for('main.pairing', applicant_type=self.user4.user_type,
                                            applicant_id=self.user4.user_id, location=self.mentee2_location.city),
                                   follow_redirects=True)
        count2 = Pair.query.count()
        self.assertEqual(count2 - count, 1)
        mentee = Mentee.query.filter(Mentee.user_id == self.user4.user_id).first()
        self.assertTrue(mentee.paired)
        self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()
