import datetime
from datetime import datetime

from flask import request
from app import db
from app.auth.forms import SearchByForm
from app.models2_backup import Mentor, User, Mentee, School, Location, Pair, Meeting, Admin


def is_unique(model, field, data, model2=None, field2=None, data2=None):
    if model2 and field2 and data2:
        check = model.query.join(model2).filter(field == data).filter(field2 == data2).first()
    else:
        check = model.query.filter(field == data).one_or_none()
    if check:
        return False
    else:
        return True


def approve(user_type, id, approve_type):
    if user_type == 'mentor':
        UserType = Mentor
        user_type_id = UserType.mentor_id
    elif user_type == 'mentee':
        UserType = Mentee
        user_type_id = UserType.mentee_id
    query = db.session.query(UserType, User).filter(user_type_id == id). \
        join(User, User.user_id == UserType.user_id).first()
    if user_type == 'mentor':
        if approve_type == 'approve':
            query[0].is_approved = True
        elif approve_type == 'active':
            query[1].is_active = True
    elif user_type == 'mentee':
        query[1].is_active = True

    db.session.commit()


def validate_date(day, month, year):
    today = datetime.now().date()
    date = datetime(int(year), int(month), int(day)).date()
    if date < today:
        message = "Sorry, you can't go back in time bud! Please pick a later day or month."
        return message
    if date == today:
        message = "Sorry, you have to book at least one day in advance. Please pick a later day."
        return message
    else:
        return True


def get_stats():
    search = SearchByForm(request.form)

    # SCHOOLS
    approved_schools_total = School.query.filter(School.is_approved == True, School.school_id != 0).count()
    unapproved_schools_total = School.query.filter(School.is_approved == False, School.school_id != 0).count()
    schools_total = approved_schools_total + unapproved_schools_total

    # MENTEES
    approved_mentees_total = Mentee.query.join(User, User.user_id == Mentee.user_id).filter(
        User.is_active == True).count()
    unapproved_mentees_total = Mentee.query.join(User, User.user_id == Mentee.user_id).filter(
        User.is_active == False).count()
    mentees_total = approved_mentees_total + unapproved_mentees_total

    # MENTORS
    approved_mentors_total = Mentor.query.join(User, User.user_id == Mentor.user_id).filter(
        Mentor.is_approved == True).count()
    unapproved_mentors_total = Mentor.query.join(User, User.user_id == Mentor.user_id).filter(
        Mentor.is_approved == False).count()
    mentors_total = approved_mentors_total + unapproved_mentors_total

    # TOTAL
    unapproved_total = unapproved_mentees_total + unapproved_mentors_total
    approved_total = approved_mentees_total + approved_mentors_total
    totals = mentors_total + mentees_total

    stats_dict = {'users_total': str(totals), 'mentors_total': str(mentors_total), 'mentees_total': str(mentees_total),
                  'schools_total': str(schools_total), 'approved_total':str(approved_total),'unapproved_total':str(unapproved_total),
                  'approved_schools_total': str(approved_schools_total), 'unapproved_schools_total': str(unapproved_schools_total),
                  'approved_mentees_total': str(approved_mentees_total), 'unapproved_mentees_total': str(unapproved_mentees_total),
                  'approved_mentors_total': str(approved_mentors_total), 'unapproved_mentors_total': str(unapproved_mentors_total)}
    return stats_dict

def get_school_stats(schools):
    schools_dict = dict()
    for school in schools:
        school_id = school.school_id
        num_mentees = Mentee.query.filter(Mentee.school_id == school_id).count()
        schools_dict[school_id] = num_mentees
    return schools_dict

def search_by_type(user_type, search_type, search_string):

    if user_type == 'Mentee':
        UserType = Mentee
    elif user_type == 'Mentor':
        UserType = Mentor

    if search_type == 'City':
        results = db.session.query(Location, User, UserType).filter(Location.city.contains(search_string)). \
            join(User, Location.user_id == User.user_id).join(UserType, User.user_id == UserType.user_id).all()
    elif search_type == 'School':
        results = db.session.query(School, User, UserType).filter(School.school_name.contains(search_string)). \
            join(User, School.school_id == User.school_id).join(UserType, User.user_id == UserType.user_id).all()

    return results


def get_data_from_user(UserType, DataType, user_field, data):

    if UserType == Mentee:
        # id's and class of user PAIRED WITH the user searching for
        PairedType = Mentor
        paired_w_type_id = Mentor.mentor_id
        paired_w_id = Pair.mentor_id

        # id's of user searching for
        type_id = Mentee.mentee_id
        paired_id = Pair.mentee_id

    else:
        # id's and class of user PAIRED WITH the user searching for
        PairedType = Mentee
        paired_w_type_id = Mentee.mentee_id
        paired_w_id = Pair.mentee_id

        # id's of user searching for
        type_id = Mentor.mentor_id
        paired_id = Pair.mentor_id

    if DataType == Meeting:
        results = db.session.query(User, UserType, Meeting). \
            filter(user_field.contains(data)). \
            join(UserType, User.user_id == UserType.user_id).join(Pair, paired_id == type_id). \
            join(Meeting, Meeting.pair_id == Pair.id).all()

    elif DataType == Pair:
        results = db.session.query(User, UserType, Pair, PairedType). \
            filter(user_field.contains(data)). \
            join(UserType, User.user_id == UserType.user_id).join(Pair, paired_id == type_id). \
            join(PairedType, paired_w_id == paired_w_type_id).first()

    elif DataType == 'User&Type':
        results = db.session.query(User, UserType). \
            filter(user_field.contains(data)). \
            join(UserType, User.user_id == UserType.user_id).first()

        # if results hasn't been defined yet
    else:
        results = db.session.query(User, UserType, DataType). \
            filter(user_field.contains(data)). \
            join(UserType, User.user_id == UserType.user_id). \
            join(DataType, DataType.user_id == User.user_id).first()
    return results


def create_admin():
    check = is_unique(User, User.user_id, 0)
    if check is True:
        user0 = User(user_id=0, email='admin@admin.com', user_type='admin', school_id=0, bio="",
                     is_active=True, creation_date='')
        admin = Admin(user_id=0)
        user0.set_password('admin123')
        db.session.add_all([user0, admin])
        db.session.commit()

