from functools import wraps
from textwrap import wrap

from flask import url_for, request, redirect, session, flash
from flask_login import current_user


def requires_admin(user_type):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if current_user.user_type != 'admin':
                flash("You do not have access to that page. Sorry!")
                return redirect(url_for('main.home'))
            return f(*args, **kwargs)
        return decorated_function
    return decorator


def requires_correct_id(f):
    @wraps(f)
    def wrap(user_id, *args, **kwargs):
        if int(current_user.user_id) != int(user_id):
            flash("You do not have access to that page. Sorry!")
            return redirect(url_for('main.home'))
        return f(user_id=user_id, *args, **kwargs)
    return wrap
