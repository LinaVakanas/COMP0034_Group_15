from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, Form, SelectField, BooleanField, SelectMultipleField
from wtforms.validators import DataRequired, EqualTo, Email


class MentorSignupForm(FlaskForm):
    first_name = StringField("First name:")
    last_name = StringField("Last name:")
    email = StringField('Email address', validators=[DataRequired(), Email()])
    ## file for DBS ##
    ## file for student or employment ##


class PersonalForm(Form):
    carer_name = StringField("Carer's full name:", validators=DataRequired())
    carer_email = StringField("Carer's email address:", validators=[DataRequired(), Email()])
    choices1 = [('Football', 'Football'),
                ('Drawing', 'Drawing')]  # whatever we decide to use
    hobbies = SelectField('', choices=choices1)
    # personality #
    choices3 = [('Depression', 'Depression'),
                ('Self-harm', 'Self-harm'),
                ('Family problems', 'Family problems'),
                ('Drugs', 'Drugs'),
                ('Eating disorder', 'Eating disorder')]  # this was what i could remember off the top of my head
    personal_issues = SelectField('Which of the following do you relate to?', choices=choices3)
    share_personal_issues = BooleanField('Permission to share your problems with mentor', default="unchecked")
    choices4 = [('University student', 'S'),
                ('Working', 'W'),
                ('Neither', 'N')]
    mentor_occupation = SelectField('What is your current status:', choices=choices4)
    choices5 = [('Less than 2 years', '<2'),
                ('2 years or longer', '>=2)')]
    mentor_xperience = SelectField('How long have you had this occupation for?', choices=choices5)

    choices6 = [('Engineering', 'Engineering'),
                ('Maths', 'Maths'),
                ('Medicine', 'Medicine'),
                ('Sports', 'Sports')]
    mentor_field = SelectField('What field does your occupation lie in?', choices=choices6)

    mentee_field = SelectMultipleField('What field are you interested in for further studies/career?', choices=choices6)

    choices2 = [('???', '???')]  # search what medical stuff usually have
    medical_cond = SelectField('Please select  all the medical conditions'
                               'which apply to you:', choices=choices2)
    share_med_cond = BooleanField('Permission to share medical conditions with mentor.', default="unchecked")
    share_performance = BooleanField('Permission to share school performance with mentor', default="unchecked ")





class LocationForm(Form):
    address = StringField()


class CityBlogSearchForm(Form):
    choices = [('City', 'City'),
               ('Blog', 'Blog')]
    select = SelectField('', choices=choices)
    search = StringField('Search blog or city...', validators=[DataRequired()])


