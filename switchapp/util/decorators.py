# requires_admin decorator based off Jose Salvatierra's code written on tecladocode,
# reference: https://blog.tecladocode.com/learn-python-defining-user-access-roles-in-flask/
# date of retrieval: 12/04/2020

# requires_anonymous, requires_correct_id structure based off Julian Nash's code on decorators on pythonise,
# reference: https://pythonise.com/series/learning-flask/custom-flask-decorators
# date of retrieval: 14/03/2020
# Authors: Mahdi Shah & Lina Vakanas

from functools import wraps

from flask import url_for, redirect, flash
from flask_login import current_user


def requires_admin(user_type):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if current_user.user_type != 'admin':
                flash("You do not have access to that page. Sorry! (Only system admins)")
                return redirect(url_for('main.home'))
            return f(*args, **kwargs)
        return decorated_function
    return decorator


def requires_correct_id(f):
    """Decorator function which protects decorated routes from being by accessed by incorrect users.

    Checks the signed in user (current_user)'s user ID and compares it to that which the decorated function has in its
    arguments.

    Keywords:
        f: the decorated function

    Returns:
        url_for(): home, if the signed user's user ID is incorrect, and flashed a message.
            or
        f: the decorated function.
    """

    @wraps(f)
    def wrap(user_id, *args, **kwargs):
        if int(current_user.user_id) != int(user_id):
            flash("You do not have access to that page. Sorry!")
            return redirect(url_for('main.home'))
        return f(user_id=user_id, *args, **kwargs)
    return wrap


def requires_anonymous(f):
    """Decorator function which protects decorated routes from being by accessed when a user is signed in.

    Checks whether a user is signed in (the current_user is anonymous).

    Keywords:
        f: the decorated function.

    Returns:
        url_for(): home, if the signed user's user ID is incorrect, and flashes a message, depending on the function
        name (f.__name__).
            or
        f: the decorated function.
    """

    @wraps(f)
    def wrap(*args, **kwargs):
        if current_user.is_anonymous is True:
            return f(*args, **kwargs)

        else:
            if f.__name__ == 'location_form' or f.__name__ == 'personal_form':
                flash("You cannot sign up while logged in. If this isn't your account and you wish to create one, "
                      "please log out first.")
                return redirect(url_for('main.home'))

            elif f.__name__ == 'login':
                flash('You are already logged in, please log out first if you would like to change users.')
                return redirect(url_for('main.home'))

            else:
                flash("You can't do this while logged in. Please log out first.")
                return redirect(url_for('main.home'))

    return wrap
