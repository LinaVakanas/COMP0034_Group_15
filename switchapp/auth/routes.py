# Authors: Mahdi Shah & Lina Vakanas

from datetime import datetime, timedelta
from urllib.parse import urlparse, urljoin

from flask import render_template, Blueprint, url_for, flash, redirect, request, abort
from flask_login import login_user, login_required, logout_user
from sqlalchemy.exc import IntegrityError

from switchapp import db, login_manager
from switchapp.auth.forms import PersonalForm, SignUpForm, LocationForm, LoginForm, SchoolSignupForm
from switchapp.models import User, OccupationalField, Hobbies, School, PersonalInfo, PersonalIssues, Mentee, Mentor, Location
from switchapp.util.decorators import requires_anonymous
from switchapp.util.functions import is_unique, approve

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
@requires_anonymous
def login():
    """Function used to login the user (implemented from Flask-Login).

    Checks login details against stored details in the database. Checks whether users have been approved.
    Also stores 'next' param for redirects.
    Users must be anonymous to access this route (requires_anonymous decorator).

    Returns:
        redirect(): login page again upon incorrect details.
            or
        redirect(): home page if user.is_active is False.
            or
        redirect(): home page or next page, logged in if details correct.
            or
        redirect(): controlpanel_home page if user_type == 'admin'.
    """

    form = LoginForm()
    next = request.args.get('next')

    if request.method == 'POST' and form.validate():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid email or password')
            return redirect(url_for('auth.login', next=next))
        if user.is_active is False:
            flash('Sorry, your account has not been approved yet.')
            return redirect(url_for('main.home'))
        login_user(user, remember=form.remember_me.data, duration=timedelta(minutes=1))

        if user.user_type == 'mentee' or user.user_type == 'mentor':
            if user.user_type == 'mentee':
                UserType = Mentee
            elif user.user_type == 'mentor':
                UserType = Mentor
            type_obj = UserType.query.join(User, User.user_id == UserType.user_id).filter(
                UserType.user_id == user.user_id).first()
            flash('Logged in successfully as {} {}'.format(type_obj.first_name, type_obj.last_name))
        elif user.user_type == 'admin':
            flash('Logged in successfully as System Admin')
            return redirect(url_for('main.controlpanel_home'))

        if not is_safe_url(next):
            return abort(400)
        return redirect(next or url_for('main.home'))

    return render_template('login.html', form=form, title="Login")


@bp_auth.route('/logout/')
@login_required
def logout():
    """Function used to log out the user (implemented from Flask-Login).

    Users must be logged in to access this route (login_required decorator).

    Returns:
        redirect(): home page.
    """

    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('main.home'))


@bp_auth.route('/school_signup/', methods=['POST', 'GET'])
@requires_anonymous
def school_signup():
    """Function used to sign up a school.

    Instantiates a SchoolSignupForm object and retrieves data from form fields.
    Users must be anonymous to access this route (requires_anonymous decorator).

    Returns:
        redirect(): home page.
    """

    form = SchoolSignupForm(request.form)

    if request.method == 'POST' and form.validate_on_submit():
        try:
            new_school = School(is_approved=False, school_name=form.name.data, school_email=form.email.data,
                                ofsted_ranking=form.ofsted_ranking.data)
            db.session.add(new_school)
            db.session.commit()
        except IntegrityError:
            flash("Your school is already registered.")
        return redirect(url_for('main.home'))

    return render_template('forms/school_signup.html', form=form, title='School Signup')


@bp_auth.route('/personal_form/<applicant_type>/<school_id>/', methods=['POST', 'GET'])
@requires_anonymous
def personal_form(applicant_type, school_id):
    """Function used to begin registration process for a user.

    Instantiates a PersonalForm and SignUpForm object and retrieves data from form fields.
    School ID is validated and checked if it exists in database with is_approved == True.
    Mentors must have school_ID == 0. All users must use a unique email to signup, duplicate emails will not
    be accepted.
    Users must be anonymous to access this route (requires_anonymous decorator).
    Mentees will be passed to location form route while mentors must wait for admin approval.

    Keyword arguments:
    applicant_type -- mentee or mentor
    school ID -- Unique ID belonging to user's school (default 0 for Mentors)

    Returns:
        redirect(): home page if school id is not in database.
            or
        redirect(): home page if school.is_approved == False.
            or
        redirect(): home page if user_type == mentor and school_id != 0.
            or
        redirect(): login page if new_user.email exists in database.
            or
        redirect(): home page if user_type == mentor and xperience < 2 years.
            or
        redirect(): location_form page if user_type == mentee.
            or
        redirect(): home_mentor_pending if user_type == mentor.
    """

    school = School.query.filter(School.school_id == school_id).first()

    if is_unique(School, School.school_id, school_id) is True:
        flash(
            'Sorry you have entered an invalid registration link (School ID doesnt exist), please contact a system '
            'admin.')
        return redirect(url_for('main.home'))
    else:
        if school.is_approved is False:
            flash('Sorry your school has not been approved yet.')
            return redirect(url_for('main.home'))
        elif applicant_type == 'mentor' and school.school_id != 0:
            flash('Sorry you have entered an invalid registration link. Please use the signup button.')
            return redirect(url_for('main.home'))
        else:
            form = PersonalForm(request.form)
            form2 = SignUpForm(request.form)

            if applicant_type == 'mentee':
                del form.xperience
                del form.status
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
                    return redirect(url_for('auth.login'))

                if applicant_type == 'mentee':
                    new_user.mentee.append(Mentee(school_id=school_id, first_name=form2.first_name.data,
                                                  last_name=form2.last_name.data, paired=False))
                    new_m = Mentee.query.join(User).filter(Mentee.user_id == new_user.user_id).first()
                    new_user.personal_info.append(
                        PersonalInfo(carer_email=form.carer_email.data, carer_name=form.carer_name.data,
                                     status="S", xperience=None, share_performance=form.share_performance.data,
                                     share_personal_issues=form.share_personal_issues.data))

                elif applicant_type == 'mentor':
                    if form.xperience.data == '>=2' and form.status.data != 'N':
                        new_user.mentor.append(
                            Mentor(user_id=new_user.user_id, school_id=0, first_name=form2.first_name.data,
                                   last_name=form2.last_name.data, paired=False, is_approved=False))
                        new_m = Mentor.query.join(User).filter(Mentor.user_id == new_user.user_id).first()
                        new_user.personal_info.append(
                            PersonalInfo(carer_email="", carer_name="", status=form.status.data,
                                         xperience=form.xperience.data, share_performance=None,
                                         share_personal_issues=form.share_personal_issues.data))
                    else:
                        flash('Sorry, you must have a minimum of two years of experience to sign up as a mentor. '
                              'We want to ensure mentors have enough experience to help the mentees. \n'
                              'We hope you understand!')
                        return redirect(url_for('main.home'))

                new_user.personal_issues.append(
                    PersonalIssues(depression=form.depression.data, self_harm=form.self_harm.data,
                                   family=form.family.data, drugs=form.drugs.data, ed=form.ed.data
                                   ))

                new_user.hobbies.append(Hobbies(football=form.football.data, drawing=form.drawing.data))

                new_user.occupational_field.append(
                    OccupationalField(eng=form.eng.data, phys=form.phys.data, chem=form.chem.data,
                                      bio=form.bio.data, med=form.med.data, pharm=form.pharm.data,
                                      maths=form.maths.data, geo=form.geo.data, hist=form.hist.data,
                                      finance=form.finance.data, law=form.law.data, engl=form.engl.data
                                      ))

                db.session.commit()

                if applicant_type == 'mentee':
                    return redirect(
                        url_for('auth.location_form', applicant_type=applicant_type, applicant_id=new_user.user_id)
                    )

                elif applicant_type == 'mentor':
                    return render_template('home_mentor_pending.html', title='Pending Approval', mentor=new_m)

            return render_template('forms/PersonalForm.html', title='Signup', form2=form2, form=form,
                                   applicant_type=applicant_type)


@bp_auth.route('/location_form/<applicant_type>/<applicant_id>/', methods=['POST', 'GET'])
@requires_anonymous
def location_form(applicant_type, applicant_id):
    """Function used to complete registration process for a user.

    Instantiates a LocationForm object and retrieves data from form fields.
    Applicant ID is validated to verify identity of applicant.
    Users must be anonymous to access this route (requires_anonymous decorator).
    Mentees are redirected to home page to wait for admin approval.
    Mentors are logged in and redirected to pairing page.

    Keyword arguments:
    Applicant_type -- mentee or mentor
    Applicant ID -- Unique User ID belonging to user

    Returns:
        redirect(): home page if applicant_type == mentor and mentor.is_approved == False.
            or
        redirect(): home page if personal_form for user doesnt exist.
            or
        redirect(): home page if user doesnt exist.
            or
        redirect(): login page if location form corresponding to user id already exists.
            or
        redirect(): pairing page  if applicant_type == mentor.
            or
        redirect(): home page if applicant_type == mentee.
    """

    form = LocationForm(request.form)

    if applicant_type == 'mentor':
        mentor = Mentor.query.filter(Mentor.user_id == applicant_id).first()
        if mentor.is_approved is False:
            flash("Sorry, you haven't been approved yet. Please wait until an admin approves you.")
            return redirect(url_for('main.home'))

    if is_unique(PersonalInfo, PersonalInfo.user_id, applicant_id) is True:
        flash(
            "Sorry you have entered an invalid registration link, as you haven't completed the section before this in "
            "the registration process. If you have and you think it's a mistake, please contact a system admin.")
        return redirect(url_for('main.home'))

    elif is_unique(User, User.user_id, applicant_id) is True:
        flash(
            "Sorry, you can't access this page because we don't have you down as a user. Please contact a system admin"
            " if you think this is a mistake.")
        return redirect(url_for('main.home'))

    elif is_unique(Location, Location.user_id, applicant_id) is False:
        flash("Hm... looks like you've already signed up. You can sign in.")
        return redirect(url_for('auth.login'))

    else:
        if request.method == 'POST' and form.validate_on_submit():
            new_location = Location(user_id=applicant_id, address=form.address.data, city=form.city.data,
                                    postcode=form.postcode.data,
                                    avoid_area=form.avoid_area.data)

            if applicant_type == 'mentor':
                approve(applicant_type, mentor.mentor_id, 'active')

            db.session.add(new_location)
            db.session.commit()

            if applicant_type == 'mentor':
                user = user_loader(applicant_id)
                login_user(user)
                return redirect(url_for('main.pairing'))

            elif applicant_type == 'mentee':
                flash("You have successfully completed the signing up process! Please wait for "
                      "our admins to verify this and approve. You will receive an email when this is done.")
                return redirect(url_for('main.home'))
        else:
            return render_template('forms/LocationForm.html', title='Signup', form=form, applicant_type=applicant_type)
