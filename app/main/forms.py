from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, Form, SelectField, BooleanField, SelectMultipleField
from wtforms.validators import DataRequired, EqualTo, Email, AnyOf
import json


# class MentorSignUpForm(FlaskForm):
#     first_name = StringField("First name:")
#     last_name = StringField("Last name:")
#     email = StringField('Email address', validators=[DataRequired(), Email()])
    ## file for DBS ##
    ## file for student or employment ##


class SignUpForm(FlaskForm):
    first_name = StringField("First name:")
    last_name = StringField("Last name:")
    email = StringField('Email address', validators=[DataRequired(), Email()])


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

    share_personal_issues = BooleanField('Permission to share your problems with mentor', default="unchecked")
    choices4 = [('S', 'University student'),
                ('W', 'Working'),
                ('N', 'Neither')]
    mentor_occupation = SelectField('What is your current status:', choices=choices4)
    choices5 = [('<2', 'Less than 2 years'),
                ('>=2', '2 years or longer')]
    mentor_xperience = SelectField('How long have you had this occupation for?', choices=choices5)

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

    med1 = BooleanField('???', default="unchecked" )  # search what medical stuff usually have
    share_med_cond = BooleanField('Permission to share medical conditions with mentor.', default="unchecked")
    share_performance = BooleanField('Permission to share school performance with mentor', default="unchecked ")


class LocationForm(FlaskForm):
    with open('C:/Users/Mahdi/Documents/UCL Mechanical Engineering/3rd Year/COMP0034 - Web Development/COMP0034_Group_15 -/gb.json') as f:
        cities_dict = json.load(f)
        cities_list = []
        for dict in cities_dict:
            cities_list.append(dict['city'])
    address = StringField('Address:', validators=[DataRequired()])
    city = StringField('City:', validators=[DataRequired(), AnyOf(cities_list)])
    postcode = StringField('Postcode:', validators=[DataRequired()])
    avoid_area = StringField('Please specify the address of any areas which you want to avoid:')
    # choices5 = [('bus', 'Bus'),
    #             ('undrgrnd', 'Underground'),
    #             ('foot', 'By Foot')]
    # mentee_transport = SelectMultipleField('Please select which modes of transport you can take:', choices=choices5, validators=[DataRequired()])
    # choices6 = choices5.append(('car', 'Car'))
    # mentor_transport = SelectMultipleField('Please select which modes of transport you can take:', choices=choices6, validators=[DataRequired()])


class ApproveForm(FlaskForm):
    approve = BooleanField("",default="unchecked")