from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, Form, SelectField, BooleanField, SelectMultipleField
from wtforms.validators import DataRequired, EqualTo, Email, AnyOf
from app.util.validators import correct_date, Unique
from app.models2_backup import Meeting
import json
from datetime import datetime


class SignUpForm(FlaskForm):
    first_name = StringField("First name:")
    last_name = StringField("Last name:")
    email = StringField('Email address', validators=[DataRequired(), Email()])


class PersonalInfoForm(FlaskForm):
    carer_name = StringField("Carer's full name:", validators=[DataRequired()])
    carer_email = StringField("Carer's email address:", validators=[DataRequired(), Email()])
    share_performance = BooleanField(label='Share school performance', default="unchecked")

    choices4 = [('S', 'University student'),
                ('W', 'Working'),
                ('N', 'Neither')]
    mentor_occupation = SelectField('What is your current status:', choices=choices4, validators=None)

    choices5 = [('<2', 'Less than 2 years'),
                ('>=2', '2 years or longer')]
    mentor_xperience = SelectField('How long have you had this occupation for?', choices=choices5, validators=None)

    def __repr__(self):
        return '<AUTH PERSONAL INFO FORM>'

# football = BooleanField('Football', default="unchecked")
# drawing = BooleanField('Drawing', default="unchecked")
# blob = BooleanField()
#
# depression = BooleanField(label='Depression', default="unchecked")
# self_harm = BooleanField(label='Self-harm', default="unchecked")
# family = BooleanField(label='Family Problems', default="unchecked")
# drugs = BooleanField(label='Drugs', default="unchecked")
# ed = BooleanField(label='Eating Disorder', default="unchecked")
#
# share_personal_issues = BooleanField('Permission to share your problems with mentor', default="unchecked")


class LocationForm(FlaskForm):
    with open('C:/Users/linav/Documents/UCL/Year 3/COMP0034 - Web Development/Group 15 branch 2/gb.json') as f:
        cities_dict = json.load(f)
        cities_list = []
        for dict in cities_dict:
            cities_list.append(dict['city'])
    address = StringField('Address:', validators=[DataRequired()])
    city = StringField('City:', validators=[DataRequired(), AnyOf(cities_list)])
    postcode = StringField('Postcode:', validators=[DataRequired()])
    avoid_area = StringField('Please specify the address of any areas which you want to avoid:')


class BookMeeting(FlaskForm):
    days = []
    for i in range(31):
        days.append(i)
    day = SelectField(choices=days, validators=[DataRequired()])
    months = [('1', 'Jan'), ('2', 'Feb'), ('3', 'Mar'), ('4', 'Apr'), ('5', 'May'), ('6', 'Jun'),
              ('7', 'Jul'), ('8', 'Augu'), ('9', 'Sept'), ('10', 'Oct'), ('11', 'Nov'), ('12', 'Dec')]
    month = SelectField(choices=months, validators=[DataRequired()])
    today = datetime.date(datetime.now())
    years = [(today.year, today.year), (today.year + 1, today.year + 1)]
    year = SelectField(choices=years, validators=[DataRequired(), correct_date(day, month)])
    hours = [('15', '15'), ('16', '16'), ('17', '17')]
    hour = SelectField(choices=hours)
    minutes = [('00', '00'), ('15', '15'), ('30', '30')]
    minute = SelectField(choices=minutes)
    durations = [('1', '1 hour'), ('1.5', '1.5 hour'), ('2', '2 hours'), ('2.5', '2.5 hours')]
    duration = SelectField(choices=durations, validators=[DataRequired()])

    area_types = [('libr', 'Library'), ('museum', 'Museum'), ('school', 'School'), ('coffe', 'Coffee Shop')]
    type = SelectField(choices=area_types, validators=[DataRequired()]) # to validate if mentee said not to go there
    address = StringField('Address:', validators=[DataRequired()])
    postcode = StringField('Postcode:', validators=[DataRequired()])
