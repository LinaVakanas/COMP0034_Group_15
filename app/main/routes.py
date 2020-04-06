from urllib.parse import urlparse, urljoin

from flask import render_template, Blueprint, url_for, flash, redirect, request, Markup, abort
from datetime import datetime, timedelta
import secrets

from flask_login import login_user, login_required, logout_user, current_user

from app import db, mail, login_manager
from app.main.forms import PersonalForm, SignUpForm, LocationForm, ApproveForm, AddSchoolForm, BookMeeting, \
    ApproveMeeting, LoginForm
from app.models2_backup import User, MedicalCond, Message, Chatroom, OccupationalField, Hobbies, School, StudentReview, \
    Pair, PersonalInfo, Report, PersonalIssues, Mentee, Mentor, Location, Meeting
from app.util.decorators import requires_admin
from functions import is_unique

bp_main = Blueprint('main', __name__)


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
    form = LoginForm()
    next = request.args.get('next')
    if request.method == 'POST' and form.validate():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid email or password')
            return redirect(url_for('main.login'))
        login_user(user, remember=form.remember_me.data, duration=timedelta(minutes=1))
        if user.user_type == 'mentee':
            mentee = Mentee.query.join(User, User.user_id == Mentee.user_id).filter(User.user_type=='mentee').first()
            first_name = mentee.first_name
            last_name = mentee.last_name
        elif user.user_type == 'mentor':
            mentor = User.query.join(Mentor, User.user_id == Mentor.user_id).filter(User.user_type=='mentor').first()
            first_name = mentor.first_name
            last_name = mentor.last_name
        elif user.user_type == 'admin':
            first_name = 'System'
            last_name = 'Admin'
        flash('Logged in successfully as {} {}'.format(first_name, last_name))
        if not is_safe_url(next):
            return abort(400)
        return redirect(next or url_for('main.home'))
    return render_template('login.html', form=form, title="Login")


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


@bp_main.route('/admin')
@login_required
@requires_admin('admin')
def controlpanel_home():
    users = User.query.all()
    users_total = User.query.count()
    mentees = Mentee.query.all()
    mentees_total = Mentee.query.count()
    mentors = Mentor.query.all() ## will need filtering for specific numbers such as unapproved etc
    mentors_total = Mentor.query.count()
    schools_total = School.query.count() ###### ACTUAL
    unapproved_mentees_total = Mentee.query.join(User, User.user_id==Mentee.user_id).filter(User.active==False).count()
    unapproved_mentors_total = Mentor.query.join(User, User.user_id==Mentor.user_id).filter(User.active==False).count()
    unapproved_total = unapproved_mentees_total + unapproved_mentors_total
    return render_template('admin_home.html', users=users, users_total=users_total, mentees=mentees, mentees_total=mentees_total, mentors=mentors,
                           mentors_total=mentors_total, schools_total=schools_total, unapproved_mentees_total=unapproved_mentees_total,
                           unapproved_mentors_total=unapproved_mentors_total, unapproved_total=unapproved_total)


@bp_main.route('/admin/pending_mentees', methods=['POST','GET'])
@login_required
@requires_admin('admin')
def controlpanel_mentee(): ############ ISNT SHOWING THE EMAILS
    form = ApproveForm(request.form)
    mentees = Mentee.query.join(User, User.user_id==Mentee.user_id).filter(User.active==False).all()
    if request.method == 'POST': ######## Validate on submit
        approved_list = request.form.getlist('approve')
        for id in approved_list:
            mentee = Mentee.query.filter(Mentee.mentee_id==id).all()
            user_id = mentee[0].user_id
            user = User.query.filter(User.user_id==user_id).all()
            user[0].active = True
            db.session.commit()
        return redirect(url_for('main.controlpanel_home')) ##### Maybe flash a msg as well
    return render_template('admin_pending_mentees.html', mentees=mentees, form=form)


@bp_main.route('/admin/view_mentees')
@login_required
@requires_admin('admin')
def controlpanel_view_mentees():
    mentees = Mentee.query.join(User, User.user_id==Mentee.user_id).filter(User.active==True).all()
    return render_template('admin_view_mentees.html', mentees=mentees)


@bp_main.route('/admin/view_mentors')
@login_required
@requires_admin('admin')
def controlpanel_view_mentors():
    mentors = Mentor.query.join(User, User.user_id==Mentor.user_id).filter(User.active==True).all()
    return render_template('admin_view_mentors.html', mentors=mentors)


@bp_main.route('/admin/pending_mentors/')
@login_required
@requires_admin('admin')
def controlpanel_mentor(): #### Copy from above
    form = ApproveForm(request.form)
    mentors = Mentor.query.join(User, User.user_id==Mentor.user_id).filter(User.active==False).all()
    if request.method == 'POST': ######### Validate on submit
        approved_list = request.form.getlist('approve')
        for id in approved_list:
            mentor = Mentor.query.filter(Mentor.mentor_id==id).all()
            user_id = mentor[0].user_id
            user = User.query.filter(User.user_id==user_id).all()
            user[0].active = True
            db.session.commit()
        return redirect(url_for('main.controlpanel_home')) ##### Maybe flash a msg as well
    return render_template('admin_pending_mentors.html', mentors=mentors)


@bp_main.route('/admin/add_schools', methods=['POST', 'GET'])
@login_required
@requires_admin('admin')
def controlpanel_add_schools():
    form = AddSchoolForm(request.form)
    if request.method == 'POST' and form.validate_on_submit():
        new_school = School(school_status=True, school_name=form.name.data, school_email=form.email.data, ofsted_ranking=form.ofsted_ranking.data)
        db.session.add(new_school)
        db.session.commit()
        return redirect(url_for('main.controlpanel_home'))  ##### Maybe flash a msg as well
    return render_template('admin_add_school.html', form=form)


@bp_main.route('/admin/view_schools')
@login_required
@requires_admin('admin')
def controlpanel_view_schools():
    schools = School.query.all()
    schools_dict = dict()
    for school in schools:
        school_id = school.school_id
        num_mentees = Mentee.query.filter(Mentee.school_id==school_id).count()
        schools_dict[school_id] = num_mentees
    return render_template('admin_view_schools.html', schools=schools, schools_dict=schools_dict)


@bp_main.route('/personal_form/<applicant_type>/<school_id>/', methods=['POST', 'GET'])
def personal_form(applicant_type, school_id):
    if current_user.is_authenticated is False:
        if is_unique(School, School.school_id, school_id, model2=None, id=None) is False:
            form = PersonalForm(request.form)
            form2 = SignUpForm(request.form)
            if request.method == 'POST'and form2.validate_on_submit():
                creation_date = str(datetime.date(datetime.now()))
                # password = secrets.token_hex(8)
                if applicant_type == 'mentee':
                    new_user = User(email=form2.email.data, user_type=applicant_type, school_id=school_id, bio="", creation_date=creation_date, active=False)
                    new_user.set_password(form2.password.data)
                    db.session.add(new_user)
                    db.session.flush()
                    new_user.mentee.append(Mentee(school_id=school_id, first_name=form2.first_name.data,
                                                  last_name=form2.last_name.data, paired=False))
                    new_mentee = Mentee.query.join(User).filter(Mentee.user_id == new_user.user_id).first()

                    new_info = PersonalInfo(user_id=new_user.user_id, carer_email=form.carer_email.data, carer_name=form.carer_name.data,
                                            status="S", xperience=None, share_performance=form.share_performance.data)
                    db.session.flush()
                    db.session.add_all([new_info, new_mentee])

                elif applicant_type == 'mentor':

                    if form.mentor_xperience.data == '>=2' and form.mentor_occupation.data != 'N':
                        new_user = User(email=form2.email.data, school_id=0, user_type=applicant_type, creation_date=creation_date,
                                        bio="", active=False)
                        new_user.set_password(form2.password.data)
                        db.session.add(new_user)
                        db.session.flush()
                        new_user.mentor.append(Mentor(user_id=new_user.user_id, school_id=0, first_name=form2.first_name.data,
                                            last_name=form2.last_name.data, paired=False))
                        new_mentor = Mentor.query.join(User).filter(Mentor.user_id == new_user.user_id).first()
                        new_info = PersonalInfo(user_id=new_user.user_id, carer_email="", carer_name="",
                                                status=form.mentor_occupation.data, xperience=form.mentor_xperience.data, share_performance=None)
                        db.session.add_all([new_info, new_mentor])

                    else:
                        flash('Sorry, you must have a minimum of two years of experience to sign up as a mentor. '
                              'We want to ensure mentors have enough experience to help the mentees. \nWe hope you understand!')
                        return redirect(url_for('main.home'))

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

                if applicant_type == 'mentee':
                    return redirect(url_for('main.location_form', applicant_type=applicant_type, applicant_id=new_user.user_id))
                elif applicant_type == 'mentor':
                    return render_template('home_mentor_pending.html', title='Pending Approval', mentor=new_mentor)

                # new_medical = MedicalCond()
            return render_template('PersonalForm.html', title='Signup', form2=form2, form=form, applicant_type=applicant_type)
        else:
            flash('Sorry you have entered an invalid registration link, please contact a system admin. CHANGE THIS TO REDIRECT')
            return redirect(url_for('main.home'))
    else:
        flash('You cannot sign up as another user while logged in, please log out first.')
        return redirect(url_for('main.home'))


@bp_main.route('/location_form/<applicant_type>/<applicant_id>/', methods=['POST', 'GET'])
def location_form(applicant_type, applicant_id):
    form = LocationForm(request.form)
    if request.method == 'POST' and form.validate_on_submit():
        new_location = Location(user_id=applicant_id, address=form.address.data, city=form.city.data.capitalize(), postcode=form.postcode.data,
                                avoid_area=form.avoid_area.data)
        db.session.add(new_location)
        db.session.commit()
        return redirect(url_for('main.pairing', applicant_type=applicant_type, applicant_id=applicant_id, location=new_location.city))

    return render_template('LocationForm.html', title='Signup', form=form, applicant_type=applicant_type)


@bp_main.route('/pairing/<applicant_type>/<applicant_id>/<location>/', methods=['POST', 'GET'])
def pairing(applicant_type, applicant_id, location):
    # render_template('pairing_load_page.html', title='Pairing . . . ')
    if applicant_type == 'mentee':
        pair_with_mentor = Mentor.query.join(Location, Mentor.user_id == Location.user_id).filter_by(city=location).first()
        pair_with_user = User.query.join(Mentor, User.user_id == Mentor.user_id).filter_by(user_id=pair_with_mentor.user_id).first()
        if not pair_with_mentor:
            flash("Unfortunately there are no mentors signed up in {} just yet! Sorry for the inconvenience, "
                  "you'll be put on a waiting list and we'll let you know as soon as a mentor is found.\n"
                  "For now, you can edit your profile, and get used to the website.".format(location))
            return redirect(url_for('main.home', title='Edit Profile')) ####should be main.edit
        mentee = Mentee.query.filter_by(user_id=applicant_id).first()
        new_pair = Pair(mentor_id=pair_with_mentor.mentor_id, mentee_id=mentee.mentee_id)
        mentee.paired = True
        pair_with_mentor.paired = True
        db.session.add(new_pair)
        db.session.commit()
        return render_template('profiles/mentor_profile.html', title='Mentor Profile', mentor=pair_with_mentor, user=pair_with_user)

    elif applicant_type == 'mentor':
        pair_with_mentee = Mentee.query.join(Location, Mentee.user_id == Location.user_id).filter_by(city=location).first()
        pair_with_user = User.query.join(Mentee, User.user_id == Mentee.user_id).filter_by(user_id=pair_with_mentee.user_id).first()
        if not pair_with_mentee:
            flash("Unfortunately there are no mentees signed up in {} yet. Sorry for the inconvenience, "
                  "you'll be put on a waiting list and we will let you know as soon as a mentee is found.\n"
                  "For now, you can edit your profile, and get used to the website.".format(location))
            return render_template('home.html', title='Home')  ####for now
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
            return render_template('BookingForm.html', title="Book Meeting", form=form, mentee=mentee)

        # check if that day is already booked
        elif is_unique(Meeting, Meeting.date, date, model2=Pair, id=pair_id) is False:
            flash("Hm... looks like you've already booked a meeting on {date}."
                  .format(date=date)) ### try to do w js so doesn't need to render
            # when make a view booking page, link to that one
            return render_template('BookingForm.html', title="Book Meeting", form=form, mentee=mentee)

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
            return render_template('meeting_confirmation.html', title="Meeting Confirmation", approval="1", user="mentor")

    return render_template("BookingForm.html", title="Book Meeting", form=form, mentee=mentee)


@bp_main.route('/confirm-meeting/<meeting_id>/', methods=['POST', 'GET'])
def confirm_meeting(meeting_id):
    form = ApproveMeeting(request.form)
    meeting = Meeting.query.filter_by(meeting_id=meeting_id).first()
    if request.method == 'POST':
        approval = form.approval.data
        meeting.mentee_approval = approval
        print(approval)
        db.session.commit()
        return render_template('meeting_confirmation.html', title="Meeting Confirmation",
                               approval=approval, user="mentee")

    return render_template('meeting_approval.html', title="Review Meeting", form=form, meeting=meeting)
