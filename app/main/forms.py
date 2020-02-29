from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, Form, SelectField
from wtforms.validators import DataRequired, EqualTo, Email


class MentorSignupForm(FlaskForm):
    first_name = StringField("First name:")
    last_name = StringField("Last name:")
    email = StringField('Email address', validators=[DataRequired(), Email()])
    ## file for DBS ##


class PersonalForm(Form):
    carer_name = StringField("Carer's full name:", validators=DataRequired())
    carer_email = StringField("Carer's email address:", validators=[DataRequired(), Email()])
    choices1 = [('Football', 'Football'),
                ('Drawing', 'Drawing')]  # whatever we decide to use
    hobbies = SelectField('', choices=choices1)
    # personality #
    choices2 = [('???', '???')]  # search what medical stuff usually have
    medical_cond = SelectField('', choices=choices2)
    choices3 = [('Depression', 'Depression'),
                ('Self-harm', 'Self-harm'),
                ('Family problems', 'Family problems'),
                ('Drugs', 'Drugs'),
                ('Eating disorder', 'Eating disorder')]  # this was what i could remember off the top of my head
    personal_issues = SelectField('', choices=choices3)
    choices4 = ['University student']
    mentor_occupation =



class CityBlogSearchForm(Form):
    choices = [('City', 'City'),
               ('Blog', 'Blog')]
    select = SelectField('', choices=choices)
    search = StringField('Search blog or city...', validators=[DataRequired()])


