from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, Form, SelectField
from wtforms.validators import DataRequired, EqualTo, Email


class MentorSignupForm(FlaskForm):
    first_name = StringField("First name:")
    last_name = StringField("Last name:")
    email = StringField('Email address', validators=[DataRequired(), Email()])
    ## file for DBS ##




class CityBlogSearchForm(Form):
    choices = [('City', 'City'),
               ('Blog', 'Blog')]
    select = SelectField('', choices=choices)
    search = StringField('Search blog or city...', validators=[DataRequired()])


