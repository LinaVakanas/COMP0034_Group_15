from flask import render_template, Blueprint, url_for, flash, redirect, request
from sqlalchemy.exc import IntegrityError

from app import db
from app.main.forms import PersonalForm, MenteeSignUpForm, MentorSignUpForm
from app.models import User, MedicalCond, Mentor, Message, Chatroom, OccupationalField, Hobbies, School, StudentReview, \
    Pair, PersonalInfo, Report, PersonalIssues, Mentee

bp_main = Blueprint('main', __name__)


@bp_main.route('/')
def home():
    return render_template('home.html', title="Home")


@bp_main.route('/personal_form/<applicant>/<school_id>/', methods=['POST', 'GET'])
def personal_form(applicant, school_id):
    form = PersonalForm(request.form)
    form2 = MenteeSignUpForm(request.form)
    form3 = MentorSignUpForm(request.form)
    if request.method == 'POST':
        if applicant == 'mentee':

            new_mentee = Mentee(first_name=form2.first_name.data, last_name=form2.last_name.data,
                                school_id=school_id)
            new_user = User(email=form2.email.data, user_type=1)

            new_info = PersonalInfo(carer_email=form.carer_email.data, carer_name=form.carer_name.data,
                                    status="S", xperience=None, share_performance=form.share_performance.data)
            db.session.add(new_info, new_mentee, new_user)
            # db.session.commit()

        elif applicant == 'mentor':

            new_mentor = Mentor(first_name=form3.first_name.data, last_name=form3.last_name.data,
                                school_id=school_id)
            new_user = User(email=form3.email.data, user_type=2)
            new_info = PersonalInfo(carer_email=None, carer_name=None,
                                    status=form.mentor_occupation.data, xperience=form.mentor_xperience.data,
                                    share_performance=None)
            db.session.add(new_info, new_user, new_mentor)
            # db.session.commit()

        response1 = form.personal_issues.data
        new_issues = PersonalIssues(depression=response1[0], self_harm=response1[1])
        db.session.add(new_issues)
        # db.session.commit()

        response2 = form.hobbies.data
        new_hobbies = Hobbies(football=response2[0], drawing=response2[1])
        db.session.add(new_hobbies)
        # db.session.commit()

        response3 = form.field.data
        new_occupation = OccupationalField(eng=response3[0], maths=response3[1])
        db.session.add(new_occupation)
        db.session.commit()

        # response4 = form.field.data
        # new_medical = MedicalCond()
    return render_template('PersonalForm.html', title='Signup', form2=form2, form3=form3, form=form, applicant=applicant)








