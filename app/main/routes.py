from flask import render_template, Blueprint, url_for, flash, redirect, request
from datetime import datetime
import secrets

from app import db
from app.main.forms import PersonalForm, SignUpForm, LocationForm, ApproveForm, AddSchoolForm
from app.models2_backup import User, MedicalCond, Message, Chatroom, OccupationalField, Hobbies, School, StudentReview, \
    Pair, PersonalInfo, Report, PersonalIssues, Mentee, Mentor, Location

bp_main = Blueprint('main', __name__)


@bp_main.route('/')
def home():
    return render_template('home.html', title="Home")


@bp_main.route('/testing')
def testing():
    mahdi = Mentor(first_name= "Mahdi", last_name= "Shah")
    return render_template('home_mentor_pending.html', mentor=mahdi)


@bp_main.route('/admin')
def controlpanel_home():
    users = User.query.all()
    users_total = User.query.count()
    mentees = Mentee.query.all()
    mentees_total = Mentee.query.count()
    mentors = Mentor.query.all() ## will need filtering for specific numbers such as unapproved etc
    mentors_total = Mentor.query.count()
    # schools_total = School.query.count() ###### ACTUAL
    schools_total = Mentee.query.group_by(Mentee.school_id).count() ### Dummy bc using mentee instead of schools cuz we havent added schools
    return render_template('admin_home.html', users=users, users_total=users_total, mentees=mentees, mentees_total=mentees_total, mentors=mentors, mentors_total=mentors_total, schools_total=schools_total)


@bp_main.route('/admin/pending_mentees', methods=['POST','GET'])
def controlpanel_mentee():
    form = ApproveForm(request.form)
    mentees = Mentee.query.join(User, User.user_id==Mentee.user_id).filter(User.active==False).all()
    if request.method == 'POST':
        approved_list = request.form.getlist('approve')
        for id in approved_list:
            mentee = Mentee.query.filter(Mentee.mentee_id==id).all()
            user_id = mentee[0].user_id
            user = User.query.filter(User.user_id==user_id).all()
            user[0].active = True
            db.session.commit()
        return redirect(url_for('main.controlpanel_home')) ##### Maybe flash a msg as well
    return render_template('admin_pending_mentees.html', mentees=mentees, form=form)


@bp_main.route('/admin/pending_mentors/')
def controlpanel_mentor(): #### Copy from above
    mentors = Mentor.query.all()
    ####mentors = db.session.query(Mentee).filter(mentees.... change for actual filtering for approved)
    return render_template('admin_pending_mentors.html', mentors=mentors)


@bp_main.route('/admin/add_schools', methods=['POST', 'GET'])
def controlpanel_add_schools():
    form = AddSchoolForm(request.form)
    if request.method == 'POST' and form.validate_on_submit():
        new_school = School(school_status=True, school_name=form.name.data, school_email=form.email.data, ofsted_ranking=form.ofsted_ranking.data)
        db.session.add(new_school)
        db.session.commit()
        return redirect(url_for('main.controlpanel_home'))  ##### Maybe flash a msg as well
    return render_template('admin_add_school.html', form=form)


@bp_main.route('/admin/view_schools')
def controlpanel_view_schools():############# This can be made better, also we need to make school_id a foreign key
    schools = School.query.all()
    schools_dict = dict()
    for school in schools: ##### After joining the school table, this might change
        school_id = school.school_id
        num_mentees = Mentee.query.filter(Mentee.school_id==school_id).count()
        schools_dict[school_id] = num_mentees
    print(schools_dict)
    return render_template('admin_view_schools.html', schools=schools, schools_dict=schools_dict)


@bp_main.route('/personal_form/<applicant>/<school_id>/', methods=['POST', 'GET'])
def personal_form(applicant, school_id):
    form = PersonalForm(request.form)
    form2 = SignUpForm(request.form)
    if request.method == 'POST'and form2.validate_on_submit():
        creation_date = str(datetime.date(datetime.now()))
        password = secrets.token_hex(8)
        if applicant == 'mentee':
            print(str(password))
            new_user = User(email=form2.email.data, user_type=applicant, school_id=school_id, password=password, bio="", creation_date=creation_date, active=False)
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
                new_user = User(email=form2.email.data, school_id=0, user_type=applicant, creation_date=creation_date,
                                bio="", password=password, active=False)
                db.session.add(new_user)
                db.session.flush()
                print("user id =" + str(new_user.user_id))
                new_mentor = Mentor(user_id=new_user.user_id, school_id=0, first_name=form2.first_name.data,
                                    last_name=form2.last_name.data, email=new_user.email) #### REMOVED PAIRED STATUS=False
                new_info = PersonalInfo(user_id=new_user.user_id, carer_email="N/A", carer_name="N/A",
                                        status=form.mentor_occupation.data, xperience=form.mentor_xperience.data, share_performance=None)
                db.session.add_all([new_info, new_mentor])

            else:
                flash('Sorry, you must have a minimum of two years of experience to sign up as a mentor. '
                      'We want to ensure mentors have enough experience to help the mentees. \nWe hope you understand!')
                return redirect(url_for('main.home'))

        print("depression ="+str(form.depression.data))
        print("share personal issues ="+str(form.share_personal_issues.data))
        new_issues = PersonalIssues(depression=form.depression.data, self_harm=form.self_harm.data, family=form.family.data, drugs=form.drugs.data, ed=form.ed.data, user_id=new_user.user_id, share_personal_issues=form.share_personal_issues.data)
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
            return render_template('home_mentor_pending.html', title='Pending Approval', mentor=new_mentor)


        # new_medical = MedicalCond()
    return render_template('PersonalForm.html', title='Signup', form2=form2, form=form, applicant=applicant)


@bp_main.route('/location_form/<applicant>/<applicant_id>/', methods=['POST', 'GET'])
def location_form(applicant, applicant_id):
    form = LocationForm(request.form)
    if request.method == 'POST' and form.validate_on_submit():
        if applicant == 'mentor' and form.city.data.lower() != 'london':
            flash("Sadly we are only based at London for now. \nWe'll keep you on a waiting list and email you if we expand "
                  "to your city. We hope you understand.")
            return redirect(url_for('main.home', title='Home'))

        elif applicant == 'mentee' and form.city.data.lower() != 'london':
            flash("Hm... are you sure that's the right city? We only send out application forms to students from London.")

        else:
            new_location = Location(user_id=applicant_id, address=form.address.data, city=form.city.data.capitalize(), postcode=form.postcode.data,
                                    avoid_area=form.avoid_area.data)
            db.session.add(new_location)
            db.session.commit()
            return redirect(url_for('main.pairing', applicant=applicant, applicant_id=applicant_id, location=new_location.city))

    return render_template('LocationForm.html', title='Signup', form=form, applicant=applicant)


@bp_main.route('/pairing/<applicant>/<applicant_id>/<location>/', methods=['POST', 'GET'])
def pairing(applicant, applicant_id, location):
    # render_template('pairing_load_page.html', title='Pairing . . . ')
    if applicant == 'mentee':
        pair_with_mentor = Mentor.query.join(Location, Mentor.user_id == Location.user_id).filter_by(city='London').first()
        pair_with_user = User.query.join(Mentor, User.user_id == Mentor.user_id).filter_by(user_id = pair_with_mentor.user_id).first()
        if not pair_with_mentor:
            flash("Unfortunately there are no mentors signed up in {} just yet! Sorry for the inconvenience, "
                  "you'll be put on a waiting list and we'll let you know as soon as a mentor is found.\n"
                  "For now, you can edit your profile, and get used to the website.".format(location))
            return redirect(url_for('main.home', title='Edit Profile')) ####should be edit
        mentee = Mentee.query.filter_by(user_id=applicant_id).first()
        new_pair = Pair(mentor_id=pair_with_mentor.mentor_id, mentee_id=mentee.mentee_id)
        db.session.add(new_pair)
        db.session.commit()
        return render_template('profiles/mentor_profile.html', title='Mentor Profile', mentor=pair_with_mentor, user=pair_with_user)

    elif applicant == 'mentor':
        pair_with = Mentee.query.join(Location, Mentee.user_id == Location.user_id).filter_by(city='London').first()
        user = User.query.join(Mentor, User.user_id == Mentor.user_id).filter_by(user_id=pair_with.user_id).first()
        if not pair_with:
            flash("Unfortunately there are no mentees signed up in {} yet. Sorry for the inconvenience, "
                  "you'll be put on a waiting list and we will let you know as soon as a mentee is found.\n"
                  "For now, you can edit your profile, and get used to the website.".format(location))
            return render_template('home.html', title='Home')  ####for now
        mentor = Mentor.query.filter_by(user_id=applicant_id).first()
        new_pair = Pair(mentor_id=mentor.mentor_id, mentee_id=pair_with.mentee_id)
        db.session.add(new_pair)
        db.session.commit()
        return render_template('profiles/mentee_profile.html', mentee=pair_with, user=user, title='Mentee Profile')
    
    return render_template('home.html', title='Home') ####for now

#
# @bp_main.route('/book_meeting/')
# def book_meeting():













