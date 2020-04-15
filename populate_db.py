from app import db
from app.models2_backup import User, Mentee, Mentor, Location, Meeting, Pair, School, Admin, PersonalInfo


def populate_db():
    # DEFAULT REQUIRED DATA
    school0 = School(is_approved=1, school_id=0, school_name="", school_email="", ofsted_ranking="")
    user0 = User(user_id=0, user_type='admin', school_id=0, email="admin@admin.com", bio=None, is_active=True, profile_pic=None, creation_date=None)
    user0.set_password('admin123')
    admin = Admin(user_id=0)

    # --------- SCHOOLS ---------------
    # approved schools
    school1 = School(is_approved=1, school_id=1, school_name='Hogwarts',school_email="hogwarts@howarts.ac.uk", ofsted_ranking="1")
    school2 = School(is_approved=1, school_id=2, school_name='Westminster City School', school_email="wcsch@hotmail.com",
                     ofsted_ranking="2")
    # unapproved school
    school3 = School(is_approved=0, school_id=3, school_name='Crest Academy', school_email="crestgirls@school.com",
                     ofsted_ranking="3")

    # ------------ MENTORS --------------
    # Approved, active, all forms completed, paired
    user1 = User(user_type='mentor', school_id=0, email='harrypj@ucl.ac.uk', is_active=True)
    user1.set_password('password1')
    mentor = Mentor(user_id=1, school_id=0, first_name='Harry', last_name='Potter', paired=True, is_approved=True)
    mentor_location = Location(user_id=1, address="Heber road", city="London",
                                postcode="NW3 5AQ", avoid_area="Neasden")
    mentor_personal_info = PersonalInfo(carer_name='', carer_email='', xperience='>=2', status='S', user_id=1)

    # Approved, active, all forms completed, unpaired
    user2 = User(user_type='mentor', school_id=0, email='ronw@ucl.ac.uk', is_active=True)
    user2.set_password('password2')
    mentor2 = Mentor(user_id=2, school_id=0, first_name='Ron', last_name='Weasley', paired=False, is_approved=True)
    mentor2_location = Location(user_id=2, address="Oxford Street", city="London",
                               postcode="XZ7 9OP", avoid_area="The Burrough")
    mentor2_personal_info = PersonalInfo(carer_name='', carer_email='', xperience='>=2', status='W', user_id=2)

    # Inactive, unapproved, personal info only completed, unpaired
    user3 = User(user_type='mentor', school_id=0, email='larry_jake@gmail.com', is_active=False)
    user3.set_password('password3')
    mentor3 = Mentor(user_id=3, school_id=0, first_name='Larry', last_name='Jake', paired=False, is_approved=False)
    mentor3_personal_info = PersonalInfo(carer_name='', carer_email='', xperience='>=2', status='S', user_id=4)

    # Inactive, approved, personal info only completed, unpaired
    user4 = User(user_type='mentor', school_id=0, email='lauren@gmail.com', is_active=False)
    user4.set_password('password4')
    mentor4 = Mentor(user_id=4, school_id=0, first_name='Lauren', last_name='Parker', paired=False, is_approved=True)
    mentor4_personal_info = PersonalInfo(carer_name='', carer_email='', xperience='>=2', status='W', user_id=4)

    # ------- MENTEES ----------
    # Active, all forms completed, paired
    user5 = User(user_type='mentee', school_id=1, email='lily@ucl.ac.uk', is_active=True)
    user5.set_password('password5')
    mentee = Mentee(user_id=5, school_id=1, first_name='Lily', last_name='Weasley', paired=True)
    mentee_personal_info = PersonalInfo(carer_email='molly@weasley.com', carer_name='Molly Weasley',
                                        share_performance=True, user_id=2, share_personal_issues=True)
    mentee_location = Location(user_id=5, address="Hogsmeade", city="London",
                               postcode="XR4 5AQ", avoid_area="Oxford Street")

    # Inactive, only personal info form filled, unpaired
    user6 = User(user_type='mentee', school_id=1, email='wat@hotmail.com', is_active=False)
    user6.set_password('password6')
    mentee2 = Mentee(user_id=6, school_id=1, first_name='Wat', last_name='Watkinson', paired=False,)
    mentee2_personal_info = PersonalInfo(carer_email='mum@parents.com', carer_name='Mum Mom',
                                        share_performance=True, user_id=6, share_personal_issues=True)

    # Active, all forms completed, unpaired
    user7 = User(user_type="mentee", school_id=2, email="ok@hotmail.com", is_active=True)
    user7.set_password('password7')
    mentee3 = Mentee(user_id=7, school_id=2, first_name='Bob', last_name='Jones', paired=False)
    mentee3_personal_info = PersonalInfo(carer_email='babjones@jones.com', carer_name='Bab Jones',
                                         share_performance=True, user_id=7, share_personal_issues=True)
    mentee3_location = Location(user_id=7, address="Blob road", city="London",
                               postcode="NW3 5YO", avoid_area="Neasden")

    # ----- Pair and Meeting --------
    pair = Pair(mentor_id=1, mentee_id=1, creation_date="4/2/2020")
    meeting = Meeting(pair_id=1, date='3/5/2020', time='17:00',
                            duration='1', address="Kilburn Road", postcode="WY4 5UU", type="Library")

    # UPDATING DATABASE
    db.session.add_all([user0,admin])
    db.session.add_all([school0, school1, school2, school3])

    db.session.add_all([user1, mentor, mentor_personal_info, mentor_location])
    db.session.add_all([user2, mentor2, mentor2_personal_info, mentor2_location])
    db.session.add_all([user3, mentee3, mentor3_personal_info])
    db.session.add_all([user4, mentor4, mentor4_personal_info])

    db.session.add_all([user5, mentee, mentee_personal_info, mentee_location])
    db.session.add_all([user6, mentee2, mentee2_personal_info])
    db.session.add_all([user7, mentee3, mentee3_personal_info, mentee3_location])

    db.session.add_all([pair, meeting])

    db.session.commit()
