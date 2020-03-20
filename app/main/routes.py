from flask import render_template, Blueprint, url_for, flash, redirect, request
from datetime import datetime
import secrets

from app import db
from app.main.forms import PersonalForm, SignUpForm, LocationForm
from app.models2 import User, MedicalCond, Message, Chatroom, OccupationalField, Hobbies, School, StudentReview, \
    Pair, PersonalInfo, Report, PersonalIssues, Mentee, Mentor, Location

bp_main = Blueprint('main', __name__)


@bp_main.route('/')
def home():
    return render_template('home.html', title="Home")

@bp_main.route('/testing')
def testing():
    mahdi = Mentor(first_name= "Mahdi", last_name= "Shah")
    return render_template('home_mentor_pending.html', mentor=mahdi)

@bp_main.route('/personal_form/<applicant>/<school_id>/', methods=['POST', 'GET'])
def personal_form(applicant, school_id):
    form = PersonalForm(request.form)
    form2 = SignUpForm(request.form)
    if request.method == 'POST'and form2.validate_on_submit():
        creation_date = str(datetime.date(datetime.now()))
        password = secrets.token_hex(8)
        if applicant == 'mentee':

            new_user = User(email=form2.email.data, school_id=school_id, user_type=applicant, creation_date=creation_date,
                            bio="", password=password)
            db.session.add(new_user)
            db.session.flush()
            print("user id 1 ="+str(new_user.user_id))
            new_mentee = Mentee(user_id=new_user.user_id, school_id=school_id, first_name=form2.first_name.data,
                                last_name=form2.last_name.data, email=new_user.email)

            new_info = PersonalInfo(user_id=new_user.user_id, carer_email=form.carer_email.data, carer_name=form.carer_name.data,
                                    status="S", xperience=None, share_performance=form.share_performance.data)
            db.session.flush()
            print("mentee id ="+ str(new_mentee.user_id))
            print("user id 2 ="+str(new_info.user_id))
            db.session.add_all([new_info, new_mentee])
            print("user email ="+str(new_user.email))

        elif applicant == 'mentor':

            if form.mentor_xperience.data == '>=2' and form.mentor_occupation.data != 'N':
                new_user = User(email=form2.email.data, school_id=school_id, user_type=applicant, creation_date=creation_date,
                                bio="", password=password)

                new_mentor = Mentor(school_id=0, first_name=form2.first_name.data,
                                    last_name=form2.last_name.data, email=new_user.email)
                new_info = PersonalInfo(carer_email=None, carer_name=None,
                                        status=form.mentor_occupation.data, xperience=form.mentor_xperience.data, share_performance=None)
                db.session.add_all([new_info, new_user, new_mentor])

            else:
                flash('Sorry, you must have a minimum of two years of experience to sign up as a mentor. '
                      'We want to ensure mentors have enough experience to help the mentees. \nWe hope you understand!')
                return redirect(url_for('main.home'))

        print("depression ="+str(form.depression.data))
        new_issues = PersonalIssues(depression=form.depression.data, self_harm=form.self_harm.data, family=form.family.data, drugs=form.drugs.data, ed=form.ed.data, user_id=new_user.user_id, share_personal_issues=True)
        ## ADD SHARE PERSONAL ISSUES TO HTML
        db.session.add(new_issues)

        new_hobbies = Hobbies(football=form.football.data, drawing=form.drawing.data, user_id=new_user.user_id)
        db.session.add(new_hobbies)

        new_occupation = OccupationalField(eng=form.eng.data, phys=form.phys.data, chem=form.chem.data,
                                           bio=form.bio.data, med=form.med.data, pharm=form.pharm.data,
                                           maths=form.maths.data, geo=form.geo.data, hist=form.hist.data,
                                           finance=form.finance.data, law=form.law.data, engl=form.engl.data, user_id=new_user.user_id)
        db.session.add(new_occupation)
        db.session.commit()

        if applicant == 'mentee':
            return redirect(url_for('main.location_form', applicant=applicant, applicant_id=new_mentee.user_id))
        elif applicant == 'mentor':
            redirect(url_for(home))


        # new_medical = MedicalCond()
    return render_template('PersonalForm.html', title='Signup', form2=form2, form=form, applicant=applicant)


@bp_main.route('/location_form/<applicant>/<applicant_id>/', methods=['POST', 'GET'])
def location_form(applicant, applicant_id):
    form = LocationForm(request.form)
    if request.method == 'POST' and form.validate_on_submit():
        if applicant == 'mentor' and form.city.data.lower() != 'london':
            flash("Sadly we are only based at London for now. \nWe'll keep you on a waiting list and email you if we expand "
                  "to your city. We hope you understand.")
            return render_template('home.html', title='Home')

        elif applicant== 'mentee' and form.city.data.lower() != 'london':
            flash("Hm... are you sure that's the right city? We only send out application forms to students from London.")

        else:
            new_location = Location(user_id=applicant_id, address=form.address.data, city=form.city.data, postcode=form.postcode.data,
                                    avoid_area=form.avoid_area.data)
            db.session.add(new_location)
            db.session.commit()
            return redirect(url_for('main.load_pairing', applicant=applicant, applicant_id=applicant_id))

    return render_template('LocationForm.html', title='Signup', form=form, applicant=applicant)


@bp_main.route('/pairing/', methods=['POST', 'GET'])
def load_pairing(applicant, applicant_id):
    return render_template('pairing_load_page.html', title='Load Pairing')


















