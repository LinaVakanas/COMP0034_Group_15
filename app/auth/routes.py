from datetime import datetime, timedelta
from urllib.parse import urlparse, urljoin

from flask import render_template, Blueprint, url_for, flash, redirect, request, abort
from flask_login import login_user, login_required, logout_user, current_user
from sqlalchemy.exc import IntegrityError

from app import db, login_manager
from app.auth.forms import PersonalForm, SignUpForm, LocationForm, LoginForm, SchoolSignupForm
from app.models2_backup import User, OccupationalField, Hobbies, School, PersonalInfo, PersonalIssues, \
    Mentee, Mentor, Location
from functions import is_unique, approve

bp_auth = Blueprint('auth', __name__)


def is_safe_url(target):
    host_url = urlparse(request.host_url)
    redirect_url = urlparse(urljoin(request.host_url, target))
    return redirect_url.scheme in ('http', 'https') and host_url.netloc == redirect_url.netloc


def get_safe_redirect():
    url = request.args.get('next')
    if url and is_safe_url(url):
        return url

    url = request.referrer
    if url and is_safe_url(url):
        return url
    return '/'


@login_manager.user_loader
def user_loader(user_id):

    if user_id is not None:
        return User.query.get(user_id)
    return None


login_manager.login_view = 'auth.login'

@bp_auth.route('/login/', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated is False:
        form = LoginForm()
        next = request.args.get('next')
        if request.method == 'POST' and form.validate():
            user = User.query.filter_by(email=form.email.data).first()
            if user is None or not user.check_password(form.password.data):
                flash('Invalid email or password')
                return redirect(url_for('auth.login'))
            if user.is_active is False:
                flash('Sorry, your account has not been approved yet.')
                return redirect(url_for('main.home'))
            login_user(user, remember=form.remember_me.data, duration=timedelta(minutes=1))

            if user.user_type == 'mentee' or user.user_type == 'mentor':
                if user.user_type == 'mentee':
                    UserType = Mentee
                elif user.user_type == 'mentor':
                    UserType = Mentor
                type_obj = UserType.query.join(User, User.user_id == UserType.user_id).filter(UserType.user_id == user.user_id).first()
                flash('Logged in successfully as {} {}'.format(type_obj.first_name, type_obj.last_name))
            elif user.user_type == 'admin':
                flash('Logged in successfully as System Admin')
            if not is_safe_url(next):
                return abort(400)
            return redirect(next or url_for('main.home'))
        return render_template('login.html', form=form, title="Login")
    else:
        flash('You are already logged in, please log out first if you would like to change users.')
        return redirect(url_for('main.home'))


@bp_auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('main.home'))


@bp_auth.route('/school_signup', methods=['POST', 'GET'])
def school_signup():
    form = SchoolSignupForm(request.form)
    if request.method == 'POST' and form.validate_on_submit():
        try:
            new_school = School(is_approved=False, school_name=form.name.data, school_email=form.email.data, ofsted_ranking=form.ofsted_ranking.data)
            db.session.add(new_school)
            db.session.commit()
        except IntegrityError:
            flash("Your school is already registered.")
        return redirect(url_for('main.home'))

    return render_template('forms/school_signup.html', form=form)


@bp_auth.route('/personal_form/<applicant_type>/<school_id>/', methods=['POST', 'GET'])
def personal_form(applicant_type, school_id):
    if current_user.is_authenticated is True:
        flash('You already have an account.')
        return redirect(url_for('main.home'))
    else:
        school = School.query.filter(School.school_id == school_id).first()
        if is_unique(School, School.school_id, school_id, model2=None, field2=None, data2=None) is True:
            flash('Sorry you have entered an invalid registration link, please contact a system admin. CHANGE THIS TO REDIRECT')
            return redirect(url_for('main.home'))
        else:
            if school.is_approved is False and applicant_type=='mentee':
                flash('Sorry your school has not been approved yet.')
                return redirect(url_for('main.home'))
            else:
                form = PersonalForm(request.form)
                form2 = SignUpForm(request.form)
                if applicant_type == 'mentee':
                    del form.mentor_xperience
                    del form.mentor_occupation
                elif applicant_type == 'mentor':
                    del form.carer_name
                    del form.carer_email
                if request.method == 'POST' and form2.validate_on_submit() and form.validate_on_submit():
                    creation_date = str(datetime.date(datetime.now()))
                    try:
                        new_user = User(email=form2.email.data, user_type=applicant_type, school_id=school_id, bio="",
                                        is_active=False, creation_date=creation_date)
                        new_user.set_password(form2.password.data)
                        db.session.add(new_user)
                        db.session.flush()
                    except IntegrityError:
                        flash("Hm... looks like you've already signed up with this email. You can sign in.")
                        return redirect(url_for('auth.login', title='Login'))

                    if applicant_type == 'mentee':
                        new_user.mentee.append(Mentee(school_id=school_id, first_name=form2.first_name.data,
                                                      last_name=form2.last_name.data, paired=False))
                        new_m = Mentee.query.join(User).filter(Mentee.user_id == new_user.user_id).first()

                        new_user.personal_info.append(PersonalInfo(carer_email=form.carer_email.data, carer_name=form.carer_name.data,
                                                status="S", xperience=None, share_performance=form.share_performance.data,
                                                                   share_personal_issues=form.share_personal_issues.data, share_med_cond=form.share_med_cond.data))

                    elif applicant_type == 'mentor':

                        if form.mentor_xperience.data == '>=2' and form.mentor_occupation.data != 'N':
                            new_user.mentor.append(Mentor(user_id=new_user.user_id, school_id=0, first_name=form2.first_name.data,
                                                last_name=form2.last_name.data, paired=False,is_approved=False))
                            new_m = Mentor.query.join(User).filter(Mentor.user_id == new_user.user_id).first()
                            new_user.personal_info.append(PersonalInfo(carer_email="", carer_name="",status=form.mentor_occupation.data,
                                                                       xperience=form.mentor_xperience.data, share_performance=None, share_personal_issues=form.share_personal_issues.data,
                                                                       share_med_cond=form.share_med_cond.data))

                        else:
                            flash('Sorry, you must have a minimum of two years of experience to sign up as a mentor. '
                                  'We want to ensure mentors have enough experience to help the mentees. \nWe hope you understand!')
                            return redirect(url_for('main.home'))

                    new_user.personal_issues.append(PersonalIssues(depression=form.depression.data, self_harm=form.self_harm.data,
                                                                       family=form.family.data, drugs=form.drugs.data, ed=form.ed.data
                                                                       ))

                    new_user.hobbies.append(Hobbies(football=form.football.data, drawing=form.drawing.data))

                    new_user.occupational_field.append(OccupationalField(eng=form.eng.data, phys=form.phys.data, chem=form.chem.data,
                                                       bio=form.bio.data, med=form.med.data, pharm=form.pharm.data,
                                                       maths=form.maths.data, geo=form.geo.data, hist=form.hist.data,
                                                       finance=form.finance.data, law=form.law.data, engl=form.engl.data
                                                       ))

                    db.session.commit()

                    if applicant_type == 'mentee':
                        return redirect(url_for('auth.location_form', applicant_type=applicant_type, applicant_id=new_user.user_id, title='Location Form'))
                    elif applicant_type == 'mentor':
                        return render_template('home_mentor_pending.html', title='Pending Approval', mentor=new_m)

                    # new_medical = MedicalCond()
                return render_template('forms/PersonalForm.html', title='Signup', form2=form2, form=form, applicant_type=applicant_type)



@bp_auth.route('/location_form/<applicant_type>/<applicant_id>/', methods=['POST', 'GET'])
def location_form(applicant_type, applicant_id):
    form = LocationForm(request.form)
    if current_user.is_authenticated is True:
        flash('You already have an account.')
        return redirect(url_for('main.home'))
    else:
        if applicant_type == 'mentor':
            mentor = Mentor.query.filter(Mentor.user_id == applicant_id).first()
            if mentor.is_approved is False:
                flash("Sorry, you haven't been approved yet. Please wait until an admin approves you.")
                return redirect(url_for('main.home', title='Home'))

        if is_unique(PersonalInfo, PersonalInfo.user_id, applicant_id) is True:
            flash("Sorry you have entered an invalid registration link, as you haven't completed the section before this in "
                  "the registration process. If you have and you think it's a mistake, please contact a system admin.")
            return redirect(url_for('main.home', title='Home'))

        elif is_unique(User, User.user_id, applicant_id) is True:
            flash("Sorry, you can't access this page because we don't have you down as a user. Please contact a system admin"
                  " if you think this is a mistake.")
            return redirect(url_for('main.home', title='Home'))

        elif is_unique(Location, Location.user_id, applicant_id) is False:
            flash("Hm... looks like you've already signed up. You can sign in.")
            return redirect(url_for('auth.login', title='Login'))

        else:
            if request.method == 'POST' and form.validate_on_submit():
                new_location = Location(user_id=applicant_id, address=form.address.data, city=form.city.data.capitalize(),
                                        postcode=form.postcode.data,
                                        avoid_area=form.avoid_area.data)
                if applicant_type == 'mentor':
                    approve(applicant_type, mentor.mentor_id, 'active')
                db.session.add(new_location)
                db.session.commit()
                return redirect(url_for('main.pairing', applicant_type=applicant_type, applicant_id=applicant_id,
                                        location=new_location.city))
            else:
                return render_template('forms/LocationForm.html', title='Signup', form=form, applicant_type=applicant_type)