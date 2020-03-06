from flask import render_template, Blueprint, url_for, flash, redirect, request
from sqlalchemy.exc import IntegrityError

from app import db
from app.main.forms import PersonalForm, LocationForm
from app.models import User, MedicalCond, Mentor, Message, Chatroom, OccupationalField, Hobbies, School, StudentReview, \
    Pair, PersonalInfo, Report

bp_main = Blueprint('main', __name__)


@bp_main.route('/personal_form/<applicant>', methods=['POST', 'GET'])
def personal_form(applicant):
    form = PersonalForm(request.form)
    if request.method == 'POST':
        if applicant == 'mentee':
            new_info = PersonalInfo(carer_email=PersonalForm.carer_email.data, carer_name=PersonalForm.carer_name.data,
                                    status="S", xperience=None, share_performance=PersonalForm.share_performance.data)
            db.session.add(new_info)
            db.session.commit()



        elif applicant == 'mentor':
            new_info = PersonalInfo(carer_email=None, carer_name=None,
                                    status=form.mentor_occupation.data, xperience=form.mentor_xperience.data,
                                    share_performance=None)
            db.session.add(new_info)
            db.session.commit()


        response = form.mentee_field.data
        new_occupation = OccupationalField(eng=response[0], maths=response[1])
        db.session.add(new_occupation)
        db.session.commit()



