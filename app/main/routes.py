from urllib.parse import urlparse, urljoin

from flask import render_template, Blueprint, url_for, flash, redirect, request, Markup, abort
from datetime import datetime, timedelta
import secrets

from sqlalchemy import or_

from app import db, mail
from app.main.forms import PersonalForm, SignUpForm, LocationForm, ApproveForm, AddSchoolForm, BookMeeting, ApproveMeeting, SearchForm, SearchByForm
from flask_login import login_user, login_required, logout_user, current_user

from app import db, mail, login_manager
from app.main.forms import PersonalForm, SignUpForm, LocationForm, ApproveForm, AddSchoolForm, BookMeeting, \
    ApproveMeeting, LoginForm
from app.models2_backup import User, MedicalCond, Message, Chatroom, OccupationalField, Hobbies, School, StudentReview, \
    Pair, PersonalInfo, Report, PersonalIssues, Mentee, Mentor, Location, Meeting
from app.util.decorators import requires_admin
from functions import is_unique, approve
from sqlalchemy.exc import IntegrityError

bp_main = Blueprint('main', __name__)


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
            join(Meeting, Meeting.pair_id == Pair.id).first()

    elif DataType == Pair:
        results = db.session.query(User, UserType, Pair, PairedType).\
            filter(user_field.contains(data)).\
            join(UserType, User.user_id == UserType.user_id).join(Pair, paired_id == type_id).\
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


login_manager.login_view = 'main.login'

@bp_main.route('/login/', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated is False:
        form = LoginForm()
        next = request.args.get('next')
        if request.method == 'POST' and form.validate():
            user = User.query.filter_by(email=form.email.data).first()
            if user is None or not user.check_password(form.password.data):
                flash('Invalid email or password')
                return redirect(url_for('main.login'))
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


@bp_main.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('main.home'))


# @login_manager.unauthorized_handler ------------- if we want to customise but idk how to fix next
# def unauthorized():
#     flash('You must be logged in 123')
#     return redirect(url_for('main.login'))


@bp_main.route('/')
def home():
    return render_template('home.html', title="Home")


@bp_main.route('/testing')
def testing():
    mahdi = Mentor(first_name= "Mahdi", last_name="Shah")
    return render_template('home_mentor_pending.html', mentor=mahdi)


@bp_main.route('/admin/', methods=['POST', 'GET'])
@login_required
@requires_admin('admin')
def controlpanel_home():
    search = SearchByForm(request.form)
    users = User.query.all()
    users_total = User.query.count()
    mentees = Mentee.query.all()
    mentees_total = Mentee.query.count()
    mentors = Mentor.query.all() ## will need filtering for specific numbers such as unapproved etc
    mentors_total = Mentor.query.count()
    schools_total = School.query.count() ###### ACTUAL
    unapproved_mentees_total = Mentee.query.join(User, User.user_id==Mentee.user_id).filter(User.is_active==False).count()
    unapproved_mentors_total = Mentor.query.join(User, User.user_id==Mentor.user_id).filter(User.is_active==False).count()
    unapproved_total = unapproved_mentees_total + unapproved_mentors_total

    if request.method == 'POST' and search.validate_on_submit():
        search_type = search.select.data
        user_type = search.select2.data
        search_string = search.search.data

        if user_type == 'Mentee':
            if search_type == 'City':
                results = db.session.query(Location, User, Mentee).filter(Location.city.contains(search_string)).\
                join(User, Location.user_id == User.user_id).join(Mentee, User.user_id == Mentee.user_id).all()
            elif search_type == 'School':
                results = db.session.query(School, User, Mentee).filter(School.school_name.contains(search_string)).\
                    join(User, School.school_id == User.school_id).join(Mentee, User.user_id == Mentee.user_id).all()

        elif user_type == 'Mentor':
            if search_type == 'City':
                results = db.session.query(Location, User, Mentor).filter(Location.city.contains(search_string)). \
                    join(User, Location.user_id == User.user_id).join(Mentor, User.user_id == Mentor.user_id).all()
            elif search_type == 'School':
                results = db.session.query(School, User, Mentor).filter(School.school_name.contains(search_string)). \
                    join(User, School.school_id == User.school_id).join(Mentor, User.user_id == Mentor.user_id).all()

        elif user_type == 'All':
            user_type = 'Mentees and Mentors'
            if search_type == 'City':
                results = []
                mentors = db.session.query(Location, User, Mentor).filter(Location.city.contains(search_string)). \
                    join(User, Location.user_id == User.user_id).join(Mentor, User.user_id == Mentor.user_id).all()
                results.extend(mentors)
                mentees = db.session.query(Location, User, Mentee).filter(Location.city.contains(search_string)). \
                    join(User, Location.user_id == User.user_id).join(Mentee, User.user_id == Mentee.user_id).all()
                results.extend(mentees)

            elif search_type == 'School':
                results = []
                mentors = db.session.query(School, User, Mentor).filter(School.school_name.contains(search_string)). \
                    join(User, School.school_id == User.school_id).join(Mentor, User.user_id == Mentor.user_id).all()
                results.extend(mentors)
                mentees = db.session.query(School, User, Mentee).filter(School.school_name.contains(search_string)). \
                    join(User, School.school_id == User.school_id).join(Mentee, User.user_id == Mentee.user_id).all()
                results.extend(mentees)

        return render_template('admin/search_results_{}.html'.format(search_type), search_term=search_string,
                               results=results, user_type=user_type)

    return render_template('admin/admin_home.html', search=search,  users=users, users_total=users_total, mentees=mentees, mentees_total=mentees_total, mentors=mentors,
                           mentors_total=mentors_total, schools_total=schools_total, unapproved_mentees_total=unapproved_mentees_total,
                           unapproved_mentors_total=unapproved_mentors_total, unapproved_total=unapproved_total)


@bp_main.route('/admin/pending_mentees', methods=['POST','GET'])
@login_required
@requires_admin('admin')
def controlpanel_mentee():
    form = ApproveForm(request.form)
    queries = db.session.query(User, Mentee).filter(User.is_active==False).join(Mentee, User.user_id==Mentee.user_id).all()
    if request.method == 'POST': ######## Validate on submit
        approved_list = request.form.getlist('approve')
        for id in approved_list:
            approve('mentee', id, None)
        return redirect(url_for('main.controlpanel_home')) ##### Maybe flash a msg as well
    return render_template('admin/admin_pending_mentees.html', queries=queries, form=form)


@bp_main.route('/admin/view_mentees', methods=['POST', 'GET'])
@login_required
@requires_admin('admin')
def controlpanel_view_mentees():
    search = SearchForm(request.form)
    queries = db.session.query(User,Mentee).filter(User.is_active == True).join(Mentee, User.user_id == Mentee.user_id).all()
    if request.method == 'POST':
        return search_results(search, 'mentee')
    return render_template('admin/admin_view_mentees.html', search=search, queries=queries)


@bp_main.route('/admin/<user_type>/search-results/')
@login_required
@requires_admin('admin')
def search_results(search, user_type):
    # set strings to data from form
    search_string = search.search.data.lower()
    select_string = search.select.data
    results = ''

    if search_string == '':
        flash("Please enter a value")
        return redirect('/admin/view_mentees')

    # set user type to search through
    if user_type == 'mentee':
        UserType = Mentee
    elif user_type == 'mentor':
        UserType = Mentor
    else:
        flash("ERROR with user type, try again.")
        return redirect('/admin/view_{}s'.format(user_type))

    # get selected information
    if select_string == '':
        personal_info = get_data_from_user(UserType, PersonalInfo, User.email, search_string)
        location = get_data_from_user(UserType, Location, User.email, search_string)
        meetings = get_data_from_user(UserType, Meeting, User.email, search_string)
        user = get_data_from_user(UserType, 'User&Type', User.email, search_string)
        pair = get_data_from_user(UserType, Pair, User.email, search_string)
        if not user:
            flash("'{searched}' is not in the database".format(searched=search_string.capitalize()))
            return redirect('/admin/view_{}s'.format(user_type))
        return render_template('admin/search_results_all.html'.format(select_string), title='Search Results',
                               personal_info=personal_info, location=location, meetings=meetings, user=user,
                               user_type=user_type, pair=pair)
    else:
        if select_string == 'Location':
            SearchType = Location
        elif select_string == 'PersonalInfo':
            SearchType = PersonalInfo
        elif select_string == 'Meeting':
            SearchType = Meeting

        elif select_string == 'User&Type':
            SearchType = 'User&Type'
        elif select_string == 'Pair':
            SearchType = Pair

        results = get_data_from_user(UserType, SearchType, User.email, search_string)

    # if no results found
    if not results:
        flash("'{searched}' is not in the database".format(searched=search_string.capitalize()))
        return redirect('/admin/view_mentees')
    return render_template('admin/search_results_{}.html'.format(select_string), title='Search Results', results=results, user_type=user_type)


@bp_main.route('/admin/view_mentors', methods=['POST', 'GET'])
@login_required
@requires_admin('admin')
def controlpanel_view_mentors():
    search = SearchForm(request.form)
    queries = db.session.query(User, Mentor).filter(Mentor.is_approved==True).join(Mentor, User.user_id==Mentor.user_id).all()
    if request.method == 'POST':
        return search_results(search, 'mentor')
    return render_template('admin/admin_view_mentors.html', queries=queries, search=search)


@bp_main.route('/admin/pending_mentors/', methods=['POST', 'GET'])
@login_required
@requires_admin('admin')
def controlpanel_mentor(): #### Copy from above
    form = ApproveForm(request.form)
    queries = db.session.query(User, Mentor).filter(Mentor.is_approved==False).join(Mentor, User.user_id==Mentor.user_id).all()
    if request.method == 'POST': ######### Validate on submit
        approved_list = request.form.getlist('approve')
        for id in approved_list:
            approve('mentor', id, 'approve')
        return redirect(url_for('main.controlpanel_home')) ##### Maybe flash a msg as well
    return render_template('admin/admin_pending_mentors.html', queries=queries, form=form)


@bp_main.route('/admin/view_schools')
@login_required
@requires_admin('admin')
def controlpanel_view_schools():
    schools = School.query.filter(School.is_approved == True).all()
    schools_dict = dict()
    for school in schools:
        school_id = school.school_id
        num_mentees = Mentee.query.filter(Mentee.school_id==school_id).count()
        schools_dict[school_id] = num_mentees
    return render_template('admin/admin_view_schools.html', schools=schools, schools_dict=schools_dict)


@bp_main.route('/admin/pending_schools/', methods=['POST', 'GET'])
@login_required
@requires_admin('admin')
def controlpanel_school(): #### Copy from above
    form = ApproveForm(request.form)
    schools = School.query.filter(School.is_approved==False, School.school_id!=0).all()
    if request.method == 'POST': ######### Validate on submit
        approved_list = request.form.getlist('approve')
        for id in approved_list:
            school = School.query.filter(School.school_id==id).first()
            school.is_approved = True
            db.session.commit()
        return redirect(url_for('main.controlpanel_home'))
    return render_template('admin/admin_pending_schools.html', schools=schools, form=form)


@bp_main.route('/add_school', methods=['POST', 'GET']) ########### Maybe Change name
def school_signup():
    form = AddSchoolForm(request.form)
    if request.method == 'POST' and form.validate_on_submit():
        new_school = School(is_approved=False, school_name=form.name.data, school_email=form.email.data, ofsted_ranking=form.ofsted_ranking.data)
        db.session.add(new_school)
        db.session.commit()
        return redirect(url_for('main.home'))  ##### Maybe flash a msg as well
    return render_template('admin/admin_add_school.html', form=form)


@bp_main.route('/personal_form/<applicant_type>/<school_id>/', methods=['POST', 'GET'])
def personal_form(applicant_type, school_id):
    # Check that school already exists in the database
    if current_user.is_authenticated is True:
        flash('You already have an account.')
        return redirect(url_for('main.home'))
    else:
        school = School.query.filter(School.school_id == school_id).first()
        if school.is_approved is False:
            flash('Sorry your school has not been approved yet.')
            return redirect(url_for('main.home'))
        else:
            if is_unique(School, School.school_id, school_id, model2=None, field2=None, data2=None) is False:
                form = PersonalForm(request.form)
                form2 = SignUpForm(request.form)
                if request.method == 'POST'and form2.validate_on_submit():
                    creation_date = str(datetime.date(datetime.now()))
                    try:
                        new_user = User(email=form2.email.data, user_type=applicant_type, school_id=school_id, bio="", is_active=False, creation_date=creation_date)
                        new_user.set_password(form2.password.data)
                        db.session.add(new_user)
                        db.session.flush()
                    except IntegrityError:
                        flash("Hm... looks like you've already signed up with this email. You can sign in.")
                        return redirect(url_for('main.home', title='Home')) ### SIGN IN PAGE WHEN MAKE

                    if applicant_type == 'mentee':

                        new_user.mentee.append(Mentee(school_id=school_id, first_name=form2.first_name.data,
                                                      last_name=form2.last_name.data, paired=False, is_active=False))
                        new_m = Mentee.query.join(User).filter(Mentee.user_id == new_user.user_id).first()

                        new_user.personal_info.append(PersonalInfo(carer_email=form.carer_email.data, carer_name=form.carer_name.data,
                                                status="S", xperience=None, share_performance=form.share_performance.data,
                                                                   share_personal_issues=form.share_personal_issues.data, share_med_cond=form.share_med_cond.data))

                    elif applicant_type == 'mentor':

                        if form.mentor_xperience.data == '>=2' and form.mentor_occupation.data != 'N':
                            new_user.mentor.append(Mentor(user_id=new_user.user_id, school_id=0, first_name=form2.first_name.data,
                                                last_name=form2.last_name.data, paired=False, is_active=False,is_approved=False))
                            new_m = Mentor.query.join(User).filter(Mentor.user_id == new_user.user_id).first()
                            new_user.personal_info.append(PersonalInfo(carer_email="", carer_name="",status=form.mentor_occupation.data,
                                                                       xperience=form.mentor_xperience.data, share_performance=None))

                        else:
                            flash('Sorry, you must have a minimum of two years of experience to sign up as a mentor. '
                                  'We want to ensure mentors have enough experience to help the mentees. \nWe hope you understand!')
                            return redirect(url_for('main.home'))

                    new_user.personal_issues.append(PersonalIssues(depression=form.depression.data, self_harm=form.self_harm.data,
                                                                       family=form.family.data, drugs=form.drugs.data, ed=form.ed.data,
                                                                       user_id=new_user.user_id, share_personal_issues=form.share_personal_issues.data))

                    new_user.hobbies.append(Hobbies(football=form.football.data, drawing=form.drawing.data, user_id=new_user.user_id))

                    new_user.occupational_field.append(OccupationalField(eng=form.eng.data, phys=form.phys.data, chem=form.chem.data,
                                                       bio=form.bio.data, med=form.med.data, pharm=form.pharm.data,
                                                       maths=form.maths.data, geo=form.geo.data, hist=form.hist.data,
                                                       finance=form.finance.data, law=form.law.data, engl=form.engl.data,
                                                       user_id=new_user.user_id))

                    db.session.commit()

                    if applicant_type == 'mentee':
                        return redirect(url_for('main.location_form', applicant_type=applicant_type, applicant_id=new_user.user_id))
                    elif applicant_type == 'mentor':
                        return render_template('home_mentor_pending.html', title='Pending Approval', mentor=new_m)

                    # new_medical = MedicalCond()
                return render_template('forms/PersonalForm.html', title='Signup', form2=form2, form=form, applicant_type=applicant_type)
            else:
                flash('Sorry you have entered an invalid registration link, please contact a system admin. CHANGE THIS TO REDIRECT')
                return redirect(url_for('main.home'))


@bp_main.route('/location_form/<applicant_type>/<applicant_id>/', methods=['POST', 'GET'])
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
            return redirect(url_for('main.home', title='Home'))  ### SIGN IN PAGE WHEN MAKE
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

@bp_main.route('/pairing/<applicant_type>/<applicant_id>/<location>/')
def pairing(applicant_type, applicant_id, location):
    user = User.query.filter(User.user_id == applicant_id).first()
    if user.is_active is False:
        flash("You need to be approved by an admin before you can be paired.")
        return redirect(url_for('main.home', title='Home'))
    else:
        if applicant_type == 'mentee':
            pair_with_mentor = Mentor.query.join(Location, Mentor.user_id == Location.user_id).\
                filter(Location.city==location, Mentor.paired==False).join(User, User.user_id==Mentor.user_id).\
                filter(User.is_active == True).first()
            if not pair_with_mentor:
                flash("Unfortunately there are no mentors signed up in {} just yet! Sorry for the inconvenience, "
                      "you'll be put on a waiting list and we'll let you know as soon as a mentor is found.\n"
                      "For now, you can edit your profile, and get used to the website.".format(location))
                return redirect(url_for('main.home', title='Edit Profile')) ####should be main.edit
            pair_with_user = User.query.join(Mentor).filter_by(user_id=pair_with_mentor.user_id).first()
            mentee = Mentee.query.filter_by(user_id=applicant_id).first()
            new_pair = Pair(mentor_id=pair_with_mentor.mentor_id, mentee_id=mentee.mentee_id)
            mentee.paired = True
            pair_with_mentor.paired = True
            db.session.add(new_pair)
            db.session.commit()
            return render_template('profiles/mentor_profile.html', title='Mentor Profile', mentor=pair_with_mentor, user=pair_with_user)

        elif applicant_type == 'mentor':
            pair_with_mentee = Mentee.query.join(Location, Mentee.user_id == Location.user_id).\
                filter(Location.city==location, Mentee.paired==False).join(User, User.user_id==Mentee.user_id).\
                filter(User.is_active == True).first()
            if not pair_with_mentee:
                flash("Unfortunately there are no mentees signed up in {} yet. Sorry for the inconvenience, "
                      "you'll be put on a waiting list and we will let you know as soon as a mentee is found.\n"
                      "For now, you can edit your profile, and get used to the website.".format(location))
                return render_template('home.html', title='Home')  ####for now
            pair_with_user = User.query.join(Mentee).filter_by(user_id=pair_with_mentee.user_id).first()
            mentor = Mentor.query.filter_by(user_id=applicant_id).first()
            new_pair = Pair(mentor_id=mentor.mentor_id, mentee_id=pair_with_mentee.mentee_id)
            mentor.paired = True
            pair_with_mentee.paired = True
            db.session.add(new_pair)
            db.session.commit()
            return render_template('profiles/mentee_profile.html', mentee=pair_with_mentee, user=pair_with_user, title='Mentee Profile')

        return render_template('home.html', title='Home') ####for now


@bp_main.route('/book-meeting/<pair_id>/<mentee_id>/<mentee_user_id>/', methods=['POST', 'GET'])
def book_meeting(pair_id, mentee_id, mentee_user_id):
    form = BookMeeting(request.form)
    mentee = Mentee.query.filter(Mentee.mentee_id == mentee_id).first()
    if request.method == 'POST' and form.validate_on_submit:
        date = '{day}/{month}/{year}'.format(day=form.day.data, month=form.month.data, year=str(form.year.data))
        mentee_user = User.query.filter(User.user_id == mentee_user_id).first()

        # check if the area is a place mentee didnt want to go
        mentee_form = Location.query.join(User).filter(User.user_id == mentee_user.user_id).first()
        if form.address.data == mentee_form.avoid_area:
            flash("Sorry bud, your mentee doesn't feel comfortable going there. In the interest of their well-being, please pick another area!")
            return render_template('forms/BookingForm.html', title="Book Meeting", form=form, mentee=mentee)

        # check if that day is already booked
        elif is_unique(Meeting, Meeting.date, date, model2=Pair, field2=Pair.id, data2=pair_id) is False:
            flash("Hm... looks like you've already booked a meeting on {date}."
                  .format(date=date)) ### try to do w js so doesn't need to render
            # when make a view booking page, link to that one
            return render_template('forms/BookingForm.html', title="Book Meeting", form=form, mentee=mentee)

        else:
            time = '{hour}:{minute}'.format(hour=form.hour.data, minute=form.minute.data)
            new_meeting = Meeting(pair_id=pair_id, day=form.day.data, month=form.month.data, year=str(form.year.data),
                                  date=date, minute=form.minute.data, hour=form.hour.data, time=time,
                                  duration=form.duration.data, address=form.address.data, postcode=form.postcode.data,
                                  type=form.type.data) #### IM THINKING WE SHOULD ONLY KEEP DATE AND TIME, NOT DAY, MONTH ETC...
            db.session.add(new_meeting)
            db.session.commit()
            # email = Message(subject="Confirm your Meeting", recipients=mentee_user.email,
            #                 body="Hi {name}, \nYour mentor has booked a meeting with you on {date} at {time}. "
            #                      "Please click the link below to review this.".format(name=mentee_user.name, date=new_meeting.date, time=new_meeting.time))
            # mail.send(email)
            return render_template('meeting/meeting_confirmation.html', title="Meeting Confirmation", approval="1", user="mentor")

    return render_template("forms/BookingForm.html", title="Book Meeting", form=form, mentee=mentee)


@bp_main.route('/confirm-meeting/<meeting_id>/', methods=['POST', 'GET'])
def confirm_meeting(meeting_id):
    form = ApproveMeeting(request.form)
    meeting = Meeting.query.filter_by(meeting_id=meeting_id).first()
    if request.method == 'POST':
        approval = form.approval.data
        meeting.mentee_approval = approval
        db.session.commit()
        return render_template('meeting/meeting_confirmation.html', title="Meeting Confirmation",
                               approval=approval, user="mentee")

    return render_template('meeting/meeting_approval.html', title="Review Meeting", form=form, meeting=meeting)
