from app import db
from app.models2_backup import User, Mentee, Mentor, Location, Meeting, Pair, School, Admin, PersonalInfo



def populate_db():
    school0 = School(is_approved=1, school_id=0, school_name="", school_email="", ofsted_ranking="")
    user0 = User(user_id=0, user_type='admin', school_id=0, email="admin@admin.com", bio=None, is_active=True, profile_pic=None, creation_date=None)
    user0.set_password('admin123')
    admin = Admin(user_id=0)
    school1 = School(is_approved=1, school_id=1, school_name='Hogwarts',school_email="hogwarts@howarts.ac.uk", ofsted_ranking="1")
    school2 = School(is_approved=1, school_id=2, school_name='Westminster City School', school_email="wcsch@hotmail.com",
                     ofsted_ranking="2")
    school3 = School(is_approved=0, school_id=3, school_name='Greycoats', school_email="greycoats@hotmail.com",
                     ofsted_ranking="3")
    user1 = User(user_type='mentor', school_id=0, email='harrypj@ucl.ac.uk', is_active=True)
    user1.set_password('password1')
    mentor = Mentor(user_id=1, school_id=0, first_name='Harry', last_name='Potter', paired=True, is_approved=True)
    user2 = User(user_type='mentee', school_id=1, email='lily@ucl.ac.uk', is_active=True)

    user2.set_password('password2')
    mentee = Mentee(user_id=2, school_id=1, first_name='Lily', last_name='Weasley', paired=True)
    mentee_location = Location(user_id=2, address="Hogsmeade", city="London",
                               postcode="XR4 5AQ", avoid_area="Neasden")
    user3 = User(user_type='mentee', school_id=1, email='wat@hotmail.com', is_active=False)
    mentee_personal_info = PersonalInfo(carer_email='mum@parents.com', carer_name='Mum Mom', share_performance=True,
                                        user_id=2, share_personal_issues=True, share_med_cond=False)

    user3 = User(user_type='mentee', school_id=1, email='wat@hotmail.com', is_active=False)
    user3.set_password('password3')
    mentee2 = Mentee(user_id=3, school_id=1, first_name='Wat', last_name='Watkinson', paired=False)
    mentee2_location = Location(user_id=3, address="Aberdeen road", city="London",
                               postcode="NW3 5YO", avoid_area="Neasden")


    user4 = User(user_type="mentee", school_id=2, email="ok@hotmail.com", is_active=False)
    user4.set_password('password4')

    mentee3 = Mentee(user_id=4, school_id=2, first_name='Bob', last_name='Jones', paired=False)
    user5 = User(user_type='mentor', school_id=0, email='larry_jake@gmail.com', is_active=False)
    user5.set_password('password5')
    mentor2 = Mentor(user_id=5, school_id=0, first_name='Larry', last_name='Jake', paired=False, is_approved=False)
    mentor2_location = Location(user_id=5, address="Heber road", city="London",
                               postcode="NW3 5AQ", avoid_area="Neasden")
    mentor2_personal_info = PersonalInfo(carer_name='', carer_email='', xperience='>=2', status='S', user_id=5, share_med_cond=True)

    pair = Pair(mentor_id=1, mentee_id=1, creation_date="4/2/2020")
    db.session.add(pair)
    book_meeting = Meeting(pair_id=1, date='3/5/2020', time='17:00',
                            duration='1', address="Kilburn Road", postcode="WY4 5UU", type="Library")
    db.session.add_all([user0,admin])
    db.session.add_all([user1, mentor])
    db.session.add_all([user2, mentee, mentee_personal_info])
    db.session.add_all([user3, mentee2, mentee2_location])
    db.session.add_all([user4, mentee3])
    db.session.add_all([user5, mentor2, mentor2_location, mentor2_personal_info])
    db.session.add_all([school1, school2, school0, school3])
    db.session.add(mentee_location)
    db.session.add(book_meeting)
    db.session.add(mentor2_location)

    db.session.commit()
