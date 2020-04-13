from flask import render_template, Blueprint, url_for, flash, redirect, request

from flask_login import login_required

from app import db
from app.auth.forms import ApproveForm, BookMeeting, \
    ApproveMeeting, SearchForm, SearchByForm
from app.models2_backup import User, School, Pair, PersonalInfo, Mentee, Mentor, Location, Meeting
from app.util.decorators import requires_admin
from functions import is_unique, approve, get_stats, search_by_type, get_data_from_user, get_school_stats

bp_main = Blueprint('main', __name__)

# @login_manager.unauthorized_handler ------------- if we want to customise but idk how to fix next
# def unauthorized():
#     flash('You must be logged in 123')
#     return redirect(url_for('main.login'))



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
        print(search_type)
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

    return render_template('admin/admin_home.html', search=search,stats_dict=stats_dict)


@bp_main.route('/admin/view_schools', methods=['POST', 'GET'])
@login_required
@requires_admin('admin')
def controlpanel_view_schools():
    schools = School.query.filter(School.is_approved == True, School.school_id != 0).all()
    schools_dict = get_school_stats(schools)
    stats_dict = get_stats()
    return render_template('admin/admin_view_schools.html', schools=schools, schools_dict=schools_dict, stats_dict=stats_dict)


@bp_main.route('/admin/pending_schools/', methods=['POST', 'GET'])
@login_required
@requires_admin('admin')
def controlpanel_school():
    form = ApproveForm(request.form)
    stats_dict = get_stats()
    schools = School.query.filter(School.is_approved==False, School.school_id!=0).all()
    if request.method == 'POST' and form.validate_on_submit():
        approved_list = request.form.getlist('approve')
        for id in approved_list:
            school = School.query.filter(School.school_id==id).first()
            school.is_approved = True
            db.session.commit()
        return redirect(url_for('main.controlpanel_home'))
    return render_template('admin/admin_pending_schools.html', schools=schools, form=form, stats_dict=stats_dict)


@bp_main.route('/admin/pending_mentors/', methods=['POST', 'GET'])
@login_required
@requires_admin('admin')
def controlpanel_mentor():
    form = ApproveForm(request.form)
    user_type = 'Mentor'
    stats_dict = get_stats()
    queries = db.session.query(User, Mentor).filter(Mentor.is_approved==False).join(Mentor, User.user_id==Mentor.user_id).all()
    if request.method == 'POST' and form.validate_on_submit():
        approved_list = request.form.getlist('approve')
        for id in approved_list:
            approve('mentor', id, 'approve')
        return redirect(url_for('main.controlpanel_home')) ##### Maybe flash a msg as well
    return render_template('admin/admin_pending_users.html', queries=queries, form=form, user_type=user_type, stats_dict=stats_dict)


@bp_main.route('/admin/view_mentors', methods=['POST', 'GET'])
@login_required
@requires_admin('admin')
def controlpanel_view_mentors():
    search = SearchForm(request.form)
    user_type = 'Mentor'
    stats_dict = get_stats()
    queries = db.session.query(User, Mentor).filter(Mentor.is_approved==True).join(Mentor, User.user_id==Mentor.user_id).all()
    if request.method == 'POST':
        return search_results(search, 'mentor')
    return render_template('admin/admin_view_users.html', queries=queries, search=search, user_type=user_type, stats_dict=stats_dict)


@bp_main.route('/admin/pending_mentees', methods=['POST','GET'])
@login_required
@requires_admin('admin')
def controlpanel_mentee():
    form = ApproveForm(request.form)
    user_type='Mentee'
    stats_dict = get_stats()
    queries = db.session.query(User, Mentee).filter(User.is_active==False).join(Mentee, User.user_id==Mentee.user_id).all()
    if request.method == 'POST' and form.validate_on_submit(): ######## Validate on submit
        approved_list = request.form.getlist('approve')
        for id in approved_list:
            approve('mentee', id, None)
        return redirect(url_for('main.controlpanel_home')) ##### Maybe flash a msg as well
    return render_template('admin/admin_pending_users.html', queries=queries, form=form, user_type=user_type, stats_dict=stats_dict)


@bp_main.route('/admin/view_mentees', methods=['POST', 'GET'])
@login_required
@requires_admin('admin')
def controlpanel_view_mentees():
    search = SearchForm(request.form)
    user_type = 'Mentee'
    stats_dict = get_stats()
    queries = db.session.query(User,Mentee).filter(User.is_active == True).join(Mentee, User.user_id == Mentee.user_id).all()
    if request.method == 'POST':
        return search_results(search, 'mentee')
    return render_template('admin/admin_view_users.html', search=search, queries=queries, user_type=user_type, stats_dict=stats_dict)


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
    if select_string == '':
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
    return render_template('admin/search_results/{}.html'.format(select_string), title='Search Results', results=results, user_type=user_type)


@bp_main.route('/pairing/<applicant_type>/<applicant_id>/<location>/')
def pairing(applicant_type, applicant_id, location):
    user = User.query.filter(User.user_id == applicant_id).first()
    if user.is_active is False:
        flash("You need to be approved by an admin before you can be paired.")
        return redirect(url_for('auth.home', title='Home'))
    else:
        if applicant_type == 'mentee':
            pair_with = db.session.query(Mentor, User).filter(Mentor.paired==False).join(User, User.user_id==Mentor.user_id).\
                filter(User.is_active == True).join(Location, Mentor.user_id == Location.user_id).filter(Location.city==location).first()
            mentor = pair_with[0]
            if not mentor:
                flash("Unfortunately there are no mentors signed up in {} just yet! Sorry for the inconvenience, "
                      "you'll be put on a waiting list and we'll let you know as soon as a mentor is found".format(location))
                return redirect(url_for('main.home', title='Home'))
            mentee = Mentee.query.filter_by(user_id=applicant_id).first()

        elif applicant_type == 'mentor':
            pair_with = db.session.query(Mentee, User).filter(Mentee.paired == False).join(User,User.user_id == Mentee.user_id). \
                filter(User.is_active == True).join(Location, Mentee.user_id == Location.user_id).filter(
                Location.city == location).first()
            if not pair_with:
                flash("Unfortunately there are no mentees signed up in {} yet. Sorry for the inconvenience, "
                      "you'll be put on a waiting list and we will let you know as soon as a mentee is found".format(location))
                return render_template('home.html', title='Home')  ####for now
            mentee = pair_with[0]
            mentor = Mentor.query.filter_by(user_id=applicant_id).first()

        mentor.paired = True
        mentee.paired = True
        new_pair = Pair(mentor_id=mentor.mentor_id, mentee_id=mentee.mentee_id)
        db.session.add(new_pair)
        db.session.commit()

        if applicant_type == 'mentor':
            return render_template('profiles/mentee_profile.html', mentee=mentee, title='Mentee Profile')
        elif applicant_type == 'mentee':
            return render_template('profiles/mentor_profile.html', mentor=mentor, title='Mentor Profile')

        return render_template('home.html', title='Home')


@bp_main.route('/<applicant_type>/<user_id>/view_paired_profile/')
@login_required
def view_paired_profile(applicant_type, user_id):

    if applicant_type == 'mentor':
        mentee = Mentee.query.join(Pair, Pair.mentee_id == Mentee.mentee_id).join(Mentor, Pair.mentor_id == Mentor.mentor_id).\
            filter(Mentor.user_id == user_id).first()
        return render_template('profiles/mentee_profile.html', mentee=mentee, title='Mentee Profile')

    elif applicant_type == 'mentee':
        mentor = Mentor.query.join(Pair, Pair.mentor_id == Mentor.mentor_id).join(Mentee, Pair.mentee_id == Mentee.mentee_id). \
            filter(Mentee.user_id == user_id).first()
        return render_template('profiles/mentor_profile.html', mentor=mentor, title='Mentor Profile')


@bp_main.route('/book-meeting/<mentee_id>/<mentee_user_id>/', methods=['POST', 'GET'])
@login_required
def book_meeting(mentee_id, mentee_user_id):
    query = db.session.query(Mentee, Location, Pair).filter(Mentee.mentee_id == mentee_id).\
        join(Location, Location.user_id == Mentee.user_id).filter(Location.user_id == mentee_user_id).join(Pair, Pair.mentee_id==Mentee.mentee_id).first()
    mentee = query[0]
    mentee_form = query[1]
    pair = query[2]
    form = BookMeeting(request.form)
    form.avoid_area = mentee_form.avoid_area

    if request.method == 'POST' and form.validate_on_submit:
        date = '{day}/{month}/{year}'.format(day=form.day.data, month=form.month.data, year=str(form.year.data))

        # check if that day is already booked
        if is_unique(Meeting, Meeting.date, date, model2=Pair, field2=Pair.id, data2=pair.id) is False:
            flash("Hm... looks like you've already booked a meeting on {date}.".format(date=date))
            # when make a view booking page, link to that one
            return render_template('forms/BookingForm.html', title="Book Meeting", form=form, mentee=mentee)

        else:
            time = '{hour}:{minute}'.format(hour=form.hour.data, minute=form.minute.data)
            new_meeting = Meeting(pair_id=pair.id, date=date, time=time, duration=form.duration.data,
                                  address=form.address.data, postcode=form.postcode.data, type=form.type.data)
            db.session.add(new_meeting)
            db.session.commit()
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
