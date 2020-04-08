from flask import flash, request, redirect, url_for

# class Unique(object):
#     def __init__(self, model, field, message="", data):
#         self.model = model
#         self.field = field
#         self.message = message


# Checks if already exists in database
from app import db
from app.models2_backup import Mentor, User, Mentee


def is_unique(model, field, data, model2=None, field2=None, data2=None):
    if model2 and field2 and data2:
        check = model.query.join(model2).filter(field == data).filter(field2 == data2).first()
    else:
        check = model.query.filter(field == data).first()
    if check:
        return False
    else:
        return True

#
# def create_user(applicant, email, user_type, school_id, password, creation_date):
#     if applicant == 'mentee':
#         new_user = User(email, user_type, school_id, password, creation_date, bio="", active=False)
#         return new_user
#     elif applicant == 'mentor':
#         new_user = User(email=form2.email.data, school_id=0, user_type=applicant_type, creation_date=creation_date,
#                         bio="", password=password, active=False)



def approve(user_type, id):
    if user_type == 'mentor':
        mentor = Mentor.query.filter(Mentor.mentor_id==id).first()
        user = User.query.filter(User.user_id==mentor.user_id).first()
    if user_type == 'mentee':
        mentee = Mentee.query.filter(Mentee.mentee_id == id).first()
        user = User.query.filter(User.user_id == mentee.user_id).first()
    user.is_active = True
    db.session.commit()