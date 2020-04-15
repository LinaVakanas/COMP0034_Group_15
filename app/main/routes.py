from datetime import datetime

from flask import render_template, Blueprint, url_for, flash, redirect, request
from flask_login import login_required
from sqlalchemy.exc import IntegrityError

from app import db
from app.main.forms import ApproveForm, BookMeeting, \
    ApproveMeeting, SearchForm, SearchByForm
from app.models2_backup import User, School, Pair, PersonalInfo, Mentee, Mentor, Location, Meeting
from app.util.decorators import requires_admin, requires_correct_id
from app.util.functions import approve, get_stats, search_by_type, get_data_from_user, get_school_stats, validate_date

bp_main = Blueprint('main', __name__)


@bp_main.route('/')
def home():
    return render_template('home.html', title="Home")


@bp_main.route('/admin/', methods=['POST', 'GET'])
@login_required
@requires_admin('admin')
def controlpanel_home():
    search = SearchByForm(request.form)
    stats_dict = get_stats()

    if request.method == 'POST' and search.validate_on_submit():
        search_type = search.select.data
        user_type = search.select2.data
        search_string = search.search.data

        if user_type == 'Mentees and Mentors':
            results = []
            mentees_results = search_by_type('Mentee', search_type, search_string)
            results.extend(mentees_results)
            mentor_results = search_by_type('Mentor', search_type, search_string)
            results.extend(mentor_results)
        else:
            results = search_by_type(user_type, search_type, search_string)

        return render_template('admin/search_results/{}.html'.format(search_type), search_term=search_string,
                               results=results, user_type=user_type, title='Search Results')

    return render_template('admin/admin_home.html', search=search, stats_dict=stats_dict,
                           title='Administrator Control Panel')


@bp_main.route('/admin/view_schools', methods=['POST', 'GET'])
@login_required
@requires_admin('admin')
def controlpanel_view_schools():
    schools = School.query.filter(School.is_approved == True, School.school_id != 0).all()
    schools_dict = get_school_stats(schools)
    stats_dict = get_stats()
    return render_template('admin/admin_view_schools.html', schools=schools, schools_dict=schools_dict,
                           stats_dict=stats_dict, title="Schools")


@bp_main.route('/admin/pending_schools/', methods=['POST', 'GET'])
@login_required
@requires_admin('admin')
def controlpanel_school():
    form = ApproveForm(request.form)
    stats_dict = get_stats()
    schools = School.query.filter(School.is_approved == False, School.school_id != 0).all()

    if request.method == 'POST' and form.validate_on_submit():
        approved_list = request.form.getlist('approve')
        for id in approved_list:
            school = School.query.filter(School.school_id == id).first()
            school.is_approved = True
            db.session.commit()
        return redirect(url_for('main.controlpanel_home'))

    return render_template('admin/admin_pending_schools.html', schools=schools, form=form, stats_dict=stats_dict,
                           title="Pending Schools")


@bp_main.route('/admin/pending_mentors/', methods=['POST', 'GET'])
@login_required
@requires_admin('admin')
def controlpanel_mentor():
    form = ApproveForm(request.form)
    user_type = 'Mentor'
    stats_dict = get_stats()
    queries = db.session.query(User, Mentor).filter(Mentor.is_approved is False).\
        join(Mentor, User.user_id == Mentor.user_id).all()

    if request.method == 'POST' and form.validate_on_submit():
        approved_list = request.form.getlist('approve')
        for id in approved_list:
            approve('mentor', id, 'approve')
        return redirect(url_for('main.controlpanel_home'))

    return render_template('admin/admin_pending_users.html', queries=queries, form=form, user_type=user_type,
                           stats_dict=stats_dict, title="Pending Mentors")


@bp_main.route('/admin/view_mentors', methods=['POST', 'GET'])
@login_required
@requires_admin('admin')
def controlpanel_view_mentors():
    search = SearchForm(request.form)
    user_type = 'Mentor'
    stats_dict = get_stats()
    queries = db.session.query(User, Mentor).filter(Mentor.is_approved is True).\
        join(Mentor, User.user_id == Mentor.user_id).all()

    if request.method == 'POST':
        return search_results(search, 'mentor')
    return render_template('admin/admin_view_users.html', queries=queries, search=search, user_type=user_type,
                           stats_dict=stats_dict, type='mentors', title="Mentors")


@bp_main.route('/admin/pending_mentees', methods=['POST', 'GET'])
@login_required
@requires_admin('admin')
def controlpanel_mentee():
    form = ApproveForm(request.form)
    user_type = 'Mentee'
    stats_dict = get_stats()
    queries = db.session.query(User, Mentee).filter(User.is_active is False).\
        join(Mentee, User.user_id == Mentee.user_id).all()

    if request.method == 'POST' and form.validate_on_submit():
        approved_list = request.form.getlist('approve')
        for id in approved_list:
            approve('mentee', id, None)
        return redirect(url_for('main.controlpanel_home'))
    return render_template('admin/admin_pending_users.html', queries=queries, form=form, user_type=user_type,
                           stats_dict=stats_dict, title="Pending Mentees")


@bp_main.route('/admin/view_mentees', methods=['POST', 'GET'])
@login_required
@requires_admin('admin')
def controlpanel_view_mentees():
    search = SearchForm(request.form)
    user_type = 'Mentee'
    stats_dict = get_stats()
    queries = db.session.query(User, Mentee).filter(User.is_active is True).\
        join(Mentee,  User.user_id == Mentee.user_id).all()

    if request.method == 'POST':
        return search_results(search, 'mentee')
    return render_template('admin/admin_view_users.html', search=search, queries=queries, user_type=user_type,
                           stats_dict=stats_dict, type='mentees', title="Mentees")


@bp_main.route('/admin/<user_type>/search-results/')
@login_required
@requires_admin('admin')
def search_results(search, user_type):
    # set strings to data from form
    search_string = search.search.data.lower()
    select_string = search.select.data

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
    if select_string == 'AllInfo':
        personal_info = get_data_from_user(UserType, PersonalInfo, User.email, search_string)
        location = get_data_from_user(UserType, Location, User.email, search_string)
        meetings = get_data_from_user(UserType, Meeting, User.email, search_string)
        user = get_data_from_user(UserType, 'User&Type', User.email, search_string)
        pair = get_data_from_user(UserType, Pair, User.email, search_string)
        if not user:
            flash("'{searched}' is not in the database".format(searched=search_string.capitalize()))
            return redirect('/admin/view_{}s'.format(user_type))
        return render_template('admin/search_results/all.html'.format(select_string), title='Search Results',
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
    return render_template('admin/search_results/{}.html'.format(select_string), title='Search Results',
                           results=results, user_type=user_type)


@bp_main.route('/pairing/<applicant_type>/<user_id>/')
@login_required
@requires_correct_id
def pairing(applicant_type, user_id):
    user = User.query.filter(User.user_id == user_id).first()
    location_form = Location.query.filter(Location.user_id == user.user_id).first()
    location = location_form.city
    if user.is_active is False:
        flash("You need to be approved by an admin before you can be paired.")
        return redirect(url_for('main.home', title='Home'))
    else:
        if applicant_type == 'mentee':
            mentor = Mentor.query.join(User, Mentor.user_id == User.user_id).\
                filter(Mentor.paired == False, User.is_active == True).\
                join(Location, Mentor.user_id == Location.user_id).filter(Location.city == location).first()
            if not mentor:
                flash("Unfortunately there are no mentors signed up in {} just yet! Sorry for the inconvenience, "
                      "you'll be put on a waiting list and we'll let you know as soon as a mentor is found".
                    format(location))
                return redirect(url_for('main.home', title='Home'))
            mentee = Mentee.query.filter_by(user_id=user_id).first()

        elif applicant_type == 'mentor':
            mentee = Mentee.query.join(User, Mentee.user_id == User.user_id). \
                filter(Mentee.paired == False, User.is_active == True). \
                join(Location, Mentee.user_id == Location.user_id).filter(Location.city == location).first()
            if not mentee:
                flash("Unfortunately there are no mentees signed up in {} yet. Sorry for the inconvenience, "
                      "you'll be put on a waiting list and we will let you know as soon as a mentee is found".
                      format(location))
                return render_template('home.html', title='Home')
            mentor = Mentor.query.filter_by(user_id=user_id).first()

        creation_date = str(datetime.date(datetime.now()))
        mentor.paired = True
        mentee.paired = True
        new_pair = Pair(mentor_id=mentor.mentor_id, mentee_id=mentee.mentee_id, creation_date=creation_date)
        db.session.add(new_pair)
        db.session.commit()

        if applicant_type == 'mentor':
            return render_template('profiles/mentee_profile.html', mentee=mentee, title='Mentee Profile')
        elif applicant_type == 'mentee':
            return render_template('profiles/mentor_profile.html', mentor=mentor, title='Mentor Profile')

        return render_template('home.html', title='Home')


@bp_main.route('/<applicant_type>/<user_id>/view_paired_profile/')
@login_required
@requires_correct_id
def view_paired_profile(applicant_type, user_id):
    if applicant_type == 'mentor':
        mentee = Mentee.query.join(Pair, Pair.mentee_id == Mentee.mentee_id).\
            join(Mentor,Pair.mentor_id == Mentor.mentor_id).filter(Mentor.user_id == user_id).first()

        if not mentee:
            return render_template('pair_me.html', title='Not yet paired :(', pair_with='mentee')
        else:
            return render_template('profiles/mentee_profile.html', mentee=mentee, title='Mentee Profile')

    elif applicant_type == 'mentee':
        mentor = Mentor.query.join(Pair, Pair.mentor_id == Mentor.mentor_id).\
            join(Mentee, Pair.mentee_id == Mentee.mentee_id).filter(Mentee.user_id == user_id).first()

        if not mentor:
            return render_template('pair_me.html', title='Not yet paired :(', pair_with='mentor')

        return render_template('profiles/mentor_profile.html', mentor=mentor, title='Mentor Profile')


@bp_main.route('/<applicant_type>/<user_id>/profile/')
@login_required
@requires_correct_id
def view_own_profile(applicant_type, user_id):
    if applicant_type == 'mentee':
        user = Mentee.query.filter(Mentee.user_id == user_id).first()
    elif applicant_type == 'mentor':
        user = Mentor.query.filter(Mentor.user_id == user_id).first()
    return render_template('profiles/own_profile.html', user=user, title='My Profile')


@bp_main.route('/book-meeting/<applicant_type>/<user_id>/', methods=['POST', 'GET'])
@login_required
@requires_correct_id
def book_meeting(applicant_type, user_id):
    if applicant_type == 'mentor':
        mentee = Mentee.query.join(Pair, Pair.mentee_id == Mentee.mentee_id).\
            join(Mentor, Pair.mentor_id == Mentor.mentor_id).filter(Mentor.user_id == user_id).first()

        if not mentee:
            flash("Sorry, you haven't been paired with a mentee yet. We'll let you know as soon as we pair you.")
            return redirect(url_for('main.home'))

        query = db.session.query(Mentee, Location, Pair).filter(Mentee.mentee_id == mentee.mentee_id). \
            join(Location, Location.user_id == Mentee.user_id).filter(Location.user_id == mentee.user_id).\
            join(Pair, Pair.mentee_id == Mentee.mentee_id).first()

    mentee = query[0]
    mentee_form = query[1]
    pair = query[2]
    form = BookMeeting(request.form)
    avoid_area = mentee_form.avoid_area

    if request.method == 'POST' and form.validate_on_submit:
        date_validation = validate_date(day=form.day.data, month=form.month.data, year=form.year.data)

        if date_validation is not True:
            flash(date_validation)
            return redirect(url_for('main.book_meeting', applicant_type='mentor', user_id=user_id))

        if form.address.data == avoid_area:
            flash("Sorry bud, your mentee doesn't feel comfortable going there. "
                  "In the interest of their well-being, please pick another area!")
            return redirect(url_for('main.book_meeting', applicant_type='mentor', user_id=user_id))

        elif form.postcode.data == avoid_area:
            flash("Sorry bud, your mentee doesn't feel comfortable going there. "
                  "In the interest of their well-being, please pick another area!")
            return redirect(url_for('main.book_meeting', applicant_type='mentor', user_id=user_id))

        date = '{day}/{month}/{year}'.format(day=form.day.data, month=form.month.data, year=str(form.year.data))
        time = '{hour}:{minute}'.format(hour=form.hour.data, minute=form.minute.data)
        try:
            new_meeting = Meeting(pair_id=pair.id, date=date, time=time, duration=form.duration.data,
                                  address=form.address.data, postcode=form.postcode.data, type=form.type.data)
            db.session.add(new_meeting)
            db.session.commit()

        except IntegrityError:
            flash("Hm... looks like you've already booked a meeting on {date}.".format(date=date))
            return redirect(url_for('main.book_meeting', applicant_type='mentor', user_id=user_id))
        return render_template('meeting/meeting_confirmation.html', title="Meeting Confirmation", approval="1",
                               user="mentor") ########################## Approval

    return render_template("forms/BookingForm.html", title="Book Meeting", form=form, mentee=mentee)


@bp_main.route('/confirm-meeting/<meeting_id>/', methods=['POST', 'GET'])
@login_required
def confirm_meeting(meeting_id):
    form = ApproveMeeting(request.form)
    meeting = Meeting.query.filter_by(meeting_id=meeting_id).first()
    if request.method == 'POST' and form.validate_on_submit():
        approval = form.approval.data
        meeting.mentee_approval = approval
        db.session.commit()
        return render_template('meeting/meeting_confirmation.html', title="Meeting Confirmation",
                               approval=approval, user="mentee")

    return render_template('meeting/meeting_approval.html', title="Review Meeting", form=form, meeting=meeting)
