from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, BooleanField, RadioField
from wtforms.validators import DataRequired, Email, ValidationError
import json

from datetime import datetime
from flask import current_app as app


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

    share_personal_issues = BooleanField('', default="unchecked")
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
            for dict in cities_dict:
                cities_list.append((dict['city'], dict['city']))
        self.city.choices = cities_list


class SchoolSignupForm(FlaskForm):
    name = StringField('Name:', validators=[DataRequired()])
    email = StringField('School Email:', validators=[DataRequired(), Email()])
    ofsted_ranking = StringField('Ofsted Ranking:', validators=[DataRequired()])


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField()
