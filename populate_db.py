from app import db
from app.models2_backup import User, Mentee, Mentor, Location, Meeting, Pair

def populate_db():
    user1 = User(user_type='mentor', school_id=0, email='harrypj@ucl.ac.uk', password='password1')
    mentor = Mentor(user_id=1, school_id=0, first_name='Harry', last_name='Potter')

    user2 = User(user_type='mentee', school_id=1, email='lily@ucl.ac.uk', password='password2')
    mentee = Mentee(user_id=2, school_id=1, first_name='Lily', last_name='Weasley')
    mentee_location = Location(user_id=2, address="Hogmeade", city="London",
                                    postcode="XR4 5AQ", avoid_area="Neasden")
    pair = Pair(mentor_id=1, mentee_id=1, creation_date="4/2/2020")
    db.session.add(pair)
    book_meeting = Meeting(pair_id=1, day='3', month='5', year=2020, date='352020', hour='17', minute='00', time='1700',
                            duration='1', address="Kilburn Road", postcode="WY4 5UU", type="libr")
    db.session.add_all([user1, mentor])
    db.session.add_all([user2, mentee])
    db.session.add(mentee_location)
    db.session.add(book_meeting)

    db.session.commit()
