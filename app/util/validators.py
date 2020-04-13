from wtforms.validators import ValidationError
from datetime import datetime


def correct_date(day, month):
    today = datetime.date(datetime.now())

    def _correct_date(form, field):
        if field.data == today.year and day < today.day and month <= today.month:
            message = "Sorry, you can't go back in time bud! Please pick a later day or month."
            raise ValidationError(message)
        elif field.data == today.year and day == today and month == today.month:
            message = "Sorry, you have to book at least one day in advance. Please pick a later day."
            raise ValidationError(message)

    return _correct_date


class Unique(object):
    def __init__(self, model, field, message=""):
        self.model = model
        self.field = field
        self.message = message

    def __call__(self, form, field):
        is_unique = self.model.query.filter_by(self.field == field.data).first()
        if is_unique:
            raise ValidationError(self.message)
