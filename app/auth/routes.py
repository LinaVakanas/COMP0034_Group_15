from flask import render_template, Blueprint, url_for, flash, redirect, request, Markup
from datetime import datetime
from flask_mail import Message
import secrets

from app import db
from app.auth.forms import PersonalInfoForm, SignUpForm, LocationForm, BookMeeting
from app.models2_backup import User, MedicalCond, Chatroom, OccupationalField, Hobbies, School, StudentReview, \
    Pair, PersonalInfo, Report, PersonalIssues, Mentee, Mentor, Location, Meeting
from functions import is_unique

bp_auth = Blueprint('auth', __name__)


@bp_auth.route('/')
def home():
    return render_template('home.html', title="Home")


@bp_auth.route('/testing/')
def testing():
    mahdi = Mentor(first_name= "Mahdi", last_name= "Shah")
    return render_template('home_mentor_pending.html', mentor=mahdi)


@bp_auth.route('/mentee_signup/<applicant>/<school_id>/', methods=['POST', 'GET'])
def mentee_signup(applicant,school_id):
    form = SignUpForm(request.form)
    if request.method == 'POST'and form.validate():
        creation_date = str(datetime.date(datetime.now()))
        password = secrets.token_hex(8)
        new_user = User(email=form.email.data, user_type=applicant, school_id=school_id, password=password,
                        bio="", creation_date=creation_date, active=False)
        db.session.add(new_user)
        db.session.flush()

        new_mentee = Mentee(school_id=school_id, first_name=form.first_name.data,
                            last_name=form.last_name.data, user_id=new_user.user_id, email=new_user.email)
        db.session.add(new_mentee)
        db.session.commit()
        return redirect(url_for('auth.personal_info', applicant=applicant, school_id=new_user.school_id))
    return render_template('auth/signup.html', form=form, title='Signup')


@bp_auth.route('/mentor_signup/<applicant>/<school_id>/', methods=['POST', 'GET'])
def mentor_signup(applicant,school_id):
    form = SignUpForm(request.form)
    if request.method == 'POST' and form.validate():
        creation_date = str(datetime.date(datetime.now()))
        password = secrets.token_hex(8)
        new_user = User(email=form.email.data, user_type=applicant, school_id=school_id, password=password, bio="",
                        creation_date=creation_date, active=False)
        db.session.add(new_user)
        db.session.flush()
        new_mentor = Mentor(school_id=school_id, first_name=form.first_name.data,
                            last_name=form.last_name.data, user_id=new_user.user_id, email=new_user.email)
        db.session.add(new_mentor)
        db.session.commit()
        return redirect(url_for('auth.personal_info', applicant=applicant, school_id=new_user.school_id))
    return render_template('auth/signup.html', form=form, title='Signup')


@bp_auth.route('/personal_info/<applicant>/<school_id>/', methods=['POST', 'GET'])
def personal_info(applicant, school_id):
    form = PersonalInfoForm(request.form)
    # print(form)
    # print('blah')
    if request.method == 'POST' and form.validate():
        print('blah')
        if applicant == 'mentee':
            print('blah')
            new_user = User(email='hermione@hogwarts.ac.uk', user_type='mentee', school_id=school_id, password='password3')
            db.session.add(new_user)
            db.session.flush()
            new_info = PersonalInfo(user_id=new_user.user_id, carer_email=form.carer_email.data, carer_name=form.carer_name.data,
                                    status="S", xperience=None, share_performance=form.share_performance.data)
            db.session.add(new_info)
            db.session.commit()
            return redirect(url_for('auth.location_form'))
        elif applicant == 'mentor':
            if form.mentor_xperience.data == '>=2' and form.mentor_occupation.data != 'N':
                new_info = PersonalInfo(carer_email=None, carer_name=None,
                                        status=form.mentor_occupation.data, xperience=form.mentor_xperience.data,
                                        share_performance=None)
                db.session.add(new_info)
                db.session.commit()
                return redirect(url_for('auth.location_form', title='Location'))

            else:
                flash('Sorry, you must have a minimum of two years of experience to sign up as a mentor. '
                      'We want to ensure mentors have enough experience to help the mentees. \nWe hope you understand!')
                return redirect(url_for('auth.home'))
    return render_template('auth/personal_info_form.html', form=form, title='Personal Info', applicant=applicant)


@bp_auth.route('/location_form/<applicant>/<applicant_id>', methods=['POST', 'GET'])
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
            return redirect(url_for('main.load_pairing', applicant=applicant, applicant_id=applicant_id, location=new_location))

    return render_template('LocationForm.html', title='Signup', form=form, applicant=applicant)


@bp_auth.route('/pairing/<applicant>/<applicant_id>/<location>/', methods=['POST', 'GET'])
def load_pairing(applicant, applicant_id, location):
    new_user = User(email='hermione@hogwarts.ac.uk', user_type='mentee', school_id=2, password='password3')
    db.session.add(new_user)
    db.session.flush()
    render_template('pairing_load_page.html', title='Pairing . . . ')
    if applicant == 'mentee':
        new_mentee = Mentee(school_id=3, email="hary@potter.com", first_name='hARRY', last_name='Potter',
                            user_id=new_user.user_id)
        db.session.add(new_mentee)
        mentor = Mentor.query.join(Location, Mentor.user_id == Location.user_id).filter_by(city=location.city, user_type='mentor').first()
        if not mentor:
            flash("Unfortunately there are no mentors signed up in {} just yet! Sorry for the inconvenience, "
                  "you'll be put on a waiting list and we'll let you know as soon as a mentor is found.\n"
                  "For now, you can edit your profile, and get used to the website.".format(location.city))
            return redirect(url_for('main.edit_profile', title='Edit Profile'))
        mentee = Mentee.query.filter_by(user_id=applicant_id).all()
        new_pair = Pair(mentor_id=mentor.mentor_id, mentee_id=mentee.mentee_id)

    elif applicant == 'mentor':
        mentee = Mentee.query.join(Location, Mentee.user_id == Location.user_id).filter_by(city='London',
                                                                                           user_type='mentee').first()
        if not mentee:
            flash("Unfortunately there are no mentors signed up in {} yet. Sorry for the inconvenience, "
                  "you'll be put on a waiting list and we will let you know as soon as a mentee is found.\n"
                  "For now, you can edit your profile, and get used to the website.".format(location.city))
        mentor = Mentor.query.filter_by(user_id=applicant_id).all()
        new_pair = Pair(mentor_id=mentor.mentor_id, mentee_id=mentee.mentee_id)
    return render_template(url_for('mentor_profile', pair=new_pair))


@bp_auth.route('/book-meeting/<pair_id>', methods=['POST', 'GET'])
def book_meeting(pair_id):
    if request.method == 'POST':
        form = BookMeeting(request.form)
        date = form.day.data+form.month.data+str(form.year.data)
        mentee_user = User.query.join(Mentee).join(Pair).first()
        print(mentee_user.user_id)

        # check if the area is a place mentee didnt want to go
        mentee_form = Location.query.join(User).filter(User.user_id == mentee_user.user_id).first()
        print(mentee_form)
        if form.address.data == mentee_form.avoid_area:
            flash("Sorry bud, your mentee doesn't feel comfortable going there. In the interest of their wellbeing, please pick another area!")
            return render_template('BookingForm.html', title="Book Meeting")

        # check if that day is already booked
        elif is_unique(Meeting, Meeting.date, date, model2=Pair, id=pair_id) is False:
            flash("Hm... looks like you've already booked a meeting for {date}.".format(date=date)) ### try to do w js so doesn't need to render
            return render_template('BookingForm.html', title="Book Meeting")

        else:
            new_meeting = Meeting(pair_id=pair_id, day=form.day.data, month=form.month.data, year=str(form.year.data),
                                  date=date, minute=form.minute.data, hour=form.hour.data, duration=form.duration.data,
                                  address=form.address.data, postcode=form.postcode.data, type=form.type.data)
            db.session.add(new_meeting)
            db.session.commit()
            mentee_user = User.query.join(Mentee).join(Pair).join(Meeting).first()
            # email = Message(subject="Confirm your Meeting", recipients=mentee_user.email,
            #                 body="Hi {name}, \nYour mentor has booked a meeting with you on {date} at {time}. "
            #                      "Please click the link below to review this.".format(name=mentee_user.name, date=new_meeting.date, time=new_meeting.time))
            # mail.send(email)
            return render_template('home.html') ##### NEED TO MAKE A BOOKING CONFIRMATION PAGE

    return render_template("BookingForm.html", title="Book Meeting")



