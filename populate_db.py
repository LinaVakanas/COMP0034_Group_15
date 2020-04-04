from app import db
from app.models2_backup import User, Mentee, Mentor, Location, Meeting, Pair, School



def populate_db():
    school1 = School(school_status=1, school_id=1, school_name='Hogwarts',school_email="hogwarts@howarts.ac.uk", ofsted_ranking="1")
    school2 = School(school_status=1, school_id=2, school_name='Westminster City School', school_email="wcsch@hotmail.com",
                     ofsted_ranking="2")
    user1 = User(user_type='mentor', school_id=0, email='harrypj@ucl.ac.uk', password='password1')
    mentor = Mentor(user_id=1, school_id=0, first_name='Harry', last_name='Potter', paired=True)
    user2 = User(user_type='mentee', school_id=1, email='lily@ucl.ac.uk', password='password2')
    mentee = Mentee(user_id=2, school_id=1, first_name='Lily', last_name='Weasley', paired=True)
    mentee_location = Location(user_id=2, address="Hogmeade", city="London",
                               postcode="XR4 5AQ", avoid_area="Neasden")
    user3 = User(user_type='mentee', school_id=1, email='wat@hotmail.com', password='password3')
    mentee2 = Mentee(user_id=3, school_id=1, first_name='Wat', last_name='Watkinson', paired=False)
    user4 = User(user_type="mentee", school_id=2, email="ok@hotmail.com", password='password4')
    mentee3 = Mentee(user_id=4, school_id=2, first_name='Bob', last_name='Jones', paired=False)
    user5 = User(user_type='mentor', school_id=0, email='larry_jake@gmail.com', password='password5')
    mentor2 = Mentor(user_id=5, school_id=0, first_name='Larry', last_name='Jake', paired=False)
    mentor2_location = Location(user_id=5, address="Heber road", city="London",
                               postcode="NW3 5AQ", avoid_area="Neasden")

    pair = Pair(mentor_id=1, mentee_id=1, creation_date="4/2/2020")
    db.session.add(pair)
    book_meeting = Meeting(pair_id=1, day='3', month='5', year=2020, date='352020', hour='17', minute='00', time='1700',
                            duration='1', address="Kilburn Road", postcode="WY4 5UU", type="libr")
    db.session.add_all([user1, mentor])
    db.session.add_all([user2, mentee])
    db.session.add_all([user3, mentee2])
    db.session.add_all([user4, mentee3])
    db.session.add_all([user5, mentor2])
    db.session.add_all([school1, school2])
    db.session.add(mentee_location)
    db.session.add(book_meeting)

    db.session.commit()
