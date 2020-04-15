from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, Form, SelectField, BooleanField, SelectMultipleField, RadioField
from wtforms.validators import DataRequired, EqualTo, Email, AnyOf, ValidationError
import json

from app.util.validators import correct_date
from datetime import datetime
from flask import current_app as app


class SearchByForm(FlaskForm):
    choices = [('School', 'School'),
               ('City', 'City')]
    select = SelectField('In:', choices=choices)
    choices2 = [('Mentees and Mentors', 'All'),
                ('Mentee', 'Mentee'),
                ('Mentor', 'Mentor')]
    select2 = SelectField('User Type:', choices=choices2)
    search = StringField('Search:', validators=[DataRequired()])


class SearchForm(FlaskForm):
    choices = [('AllInfo', 'All Info'),
               ('User&Type','User & Type'),
               ('PersonalInfo', 'Personal Info'),
               ('Location', 'Location Info'),
               ('Meeting', 'Meetings'),
               ('Pair', 'Pair Info')]
    select = SelectField('Filter by:', choices=choices)
    search = StringField('Search for a specific user:', validators=[DataRequired()])


class SignUpForm(FlaskForm):
    first_name = StringField("First name:", id="first name")
    last_name = StringField("Last name:", id="last name")
    email = StringField('Email address', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])

    def validate_password(self, password):
        if len(password.data) < 8:
            raise ValidationError("Your password must be more than 8 characters.")


class PersonalForm(FlaskForm):
    carer_name = StringField("Carer's full name:", validators=[DataRequired()])
    carer_email = StringField("Carer's email address:", validators=[DataRequired(), Email()])
    football = BooleanField('Football', default="unchecked")
    drawing = BooleanField('Drawing', default="unchecked")
    blob = BooleanField()

    depression = BooleanField(label='Depression', default="unchecked")
    self_harm = BooleanField(label='Self-harm', default="unchecked")
    family = BooleanField(label='Family Problems', default="unchecked")
    drugs = BooleanField(label='Drugs', default="unchecked")
    ed = BooleanField(label='Eating Disorder', default="unchecked")

    share_personal_issues = BooleanField('',default="unchecked")
    choices4 = [('S', 'University student'),
                ('W', 'Working'),
                ('N', 'Neither')]
    status = SelectField('What is your current occupational status:', choices=choices4, validators=[DataRequired()])
    choices5 = [('<2', 'Less than 2 years'),
                ('>=2', '2 years or longer')]
    xperience = SelectField('How long have you had this occupation for?', choices=choices5, validators=[DataRequired()])

    eng = BooleanField('Engineering', default="unchecked")
    chem = BooleanField('Chemistry', default="unchecked")
    bio = BooleanField('Biology', default="unchecked")
    pharm = BooleanField('Pharmacy', default="unchecked")
    phys = BooleanField('Physics', default="unchecked")
    med = BooleanField('Medicine', default="unchecked")
    hist = BooleanField('History', default="unchecked")
    maths = BooleanField('Maths', default="unchecked")
    engl = BooleanField('English', default="unchecked")
    geo = BooleanField('Geography', default="unchecked")
    law = BooleanField('Law', default="unchecked")
    finance = BooleanField('Finance', default="unchecked")

    share_performance = BooleanField('Permission to share school performance with mentor', default="unchecked ")


class LocationForm(FlaskForm):
    address = StringField('Address:', validators=[DataRequired()])
    city = SelectField('City:', validators=[DataRequired()])
    postcode = StringField('Postcode:', validators=[DataRequired()])
    avoid_area = StringField('Please specify the address of any areas which you want to avoid:')

    def __init__(self, *args, **kwargs):
        super(LocationForm, self).__init__(*args, **kwargs)
        with app.open_resource('static/json/gb.json') as f:
            cities_dict = json.load(f)
            cities_list = []
            # You could do what I have below, which gives you a number for each city e.g. 1 London, or you could just repeat the city e.g. London London)
            n = 1
            for dict in cities_dict:
                cities_list.append((dict['city'], dict['city']))
        self.city.choices = cities_list



class SchoolSignupForm(FlaskForm):
    name = StringField('Name:', validators=[DataRequired()])
    email = StringField('School Email:', validators=[DataRequired(), Email()])
    ofsted_ranking = StringField('Ofsted Ranking:', validators=[DataRequired()])


class ApproveForm(FlaskForm):
    approve = BooleanField("",default="unchecked")


class BookMeeting(FlaskForm):
    days = []
    for i in range(1,32,1):
        days.append(('{}'.format(i), '{}'.format(i)))
    day = SelectField(choices=days, validators=[DataRequired()])
    months = [('1', 'Jan'), ('2', 'Feb'), ('3', 'Mar'), ('4', 'Apr'), ('5', 'May'), ('6', 'Jun'),
              ('7', 'Jul'), ('8', 'Augu'), ('9', 'Sept'), ('10', 'Oct'), ('11', 'Nov'), ('12', 'Dec')]
    month = SelectField(choices=months, validators=[DataRequired()])
    today = datetime.date(datetime.now())
    years = [(today.year, today.year), (today.year + 1, today.year + 1)]
    year = SelectField(choices=years, validators=[DataRequired()])
    hours = [('15', '15'), ('16', '16'), ('17', '17')]
    hour = SelectField(choices=hours)
    minutes = [('00', '00'), ('15', '15'), ('30', '30')]
    minute = SelectField(choices=minutes)
    durations = [('1', '1 hour'), ('1.5', '1.5 hour'), ('2', '2 hours'), ('2.5', '2.5 hours')]
    duration = SelectField('Meeting Duration', choices=durations, validators=[DataRequired()])

    area_types = [('Library', 'Library'), ('Museum', 'Museum'), ('School', 'School'), ('Coffee Shop', 'Coffee Shop')]
    type = SelectField('Type of area for meeting', choices=area_types, validators=[DataRequired()]) # to validate if mentee said not to go there
    address = StringField('Address:', validators=[DataRequired()])
    postcode = StringField('Postcode:', validators=[DataRequired()])


class ApproveMeeting(FlaskForm):
    choices = [(1, 'I can make it'), (0, "I can't make it")]
    approval = RadioField(choices=choices, validators=[DataRequired()])


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField()
