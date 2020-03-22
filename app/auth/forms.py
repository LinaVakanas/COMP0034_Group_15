from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, Form, SelectField, BooleanField, SelectMultipleField
from wtforms.validators import DataRequired, EqualTo, Email, AnyOf


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