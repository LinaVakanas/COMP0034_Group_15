# Authors: Mahdi Shah & Lina Vakanas

from datetime import datetime

from flask_wtf import FlaskForm
from wtforms import SelectField, StringField, RadioField, BooleanField
from wtforms.validators import DataRequired


class SearchByForm(FlaskForm):
    """Admin control panel search form to search by city or school and filter by user type.

    Inherits FlaskForm methods.
    """

    choices = [('School', 'School'),
               ('City', 'City')]
    select = SelectField('In:', choices=choices)
    choices2 = [('Mentees and Mentors', 'All'),
                ('Mentee', 'Mentee'),
                ('Mentor', 'Mentor')]
    select2 = SelectField('User Type:', choices=choices2)
    search = StringField('Search:', validators=[DataRequired()])


class SearchForm(FlaskForm):
    """Admin control panel search form to search by user email and filter by database tables.
    Inherits FlaskForm methods.
    """

    choices = [('AllInfo', 'All Info'),
               ('User&Type', 'User & Type'),
               ('PersonalInfo', 'Personal Info'),
               ('Location', 'Location Info'),
               ('Meeting', 'Meetings'),
               ('Pair', 'Pair Info')]
    select = SelectField('Filter by:', choices=choices)
    search = StringField('Search for a specific user:', validators=[DataRequired()])


class ApproveForm(FlaskForm):
    """Form for a checkbox which sets the variable to true when ticked.
    Inherits FlaskForm methods."""

    approve = BooleanField("", default="unchecked")


class BookMeeting(FlaskForm):
    """Form for mentors to book meetings. Allows selecting the day, month and year of the meeting, time of the meeting
     by hour and minute, duration in hours of meeting, the type of area, address and postcode of the location.

     Inherits FlaskForm methods.
     """

    day = SelectField(validators=[DataRequired()])
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
    type = SelectField('Type of area for meeting', choices=area_types,
                       validators=[DataRequired()])  # to validate if mentee said not to go there
    address = StringField('Address:', validators=[DataRequired()])
    postcode = StringField('Postcode:', validators=[DataRequired()])

    def __init__(self, *args, **kwargs):
        super(BookMeeting, self).__init__(*args, **kwargs)
        days = []
        for i in range(1, 32, 1):
            days.append(('{}'.format(i), '{}'.format(i)))
        self.day.choices = days


class ApproveMeeting(FlaskForm):
    """Form to approve meeting, for a checkbox which sets the variable to true when ticked.
    Inherits FlaskForm methods.
    """

    choices = [("1", 'I can make it'), ("0", "I can't make it")]
    approval = SelectField(choices=choices, validators=[DataRequired()])