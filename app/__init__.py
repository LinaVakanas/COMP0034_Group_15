# code for error pages taken from Flask documentation: https://flask.palletsprojects.com/en/1.1.x/patterns/errorpages/

from flask import Flask, render_template
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

from config import DevConfig

db = SQLAlchemy()
login_manager = LoginManager()

def page_not_found(e):
    return render_template('errors/404.html'), 404


def internal_server_error(e):
    return render_template('errors/500.html'), 500


def create_app(config_class=DevConfig):
    """Creates an application instance to run using settings from config.py
    :return: A Flask object"""

    app = Flask(__name__)

    app.register_error_handler(404, page_not_found)
    app.register_error_handler(500, internal_server_error)

    app.config.from_object(config_class)

    db.init_app(app)
    login_manager.init_app(app)
    #
    from app.util.functions import create_admin
    from populate_db import populate_db

    # If a populated database is required, please comment out create_admin(),
    # and un-comment db.drop_all() and populate_db()
    from app.models import User, Mentee, Mentor, Admin, School, Pair, PersonalIssues, PersonalInfo, Hobbies, Location, \
        OccupationalField
    with app.app_context():
        # db.drop_all()
        db.create_all()
        # create_admin()
        # populate_db()

    # Register Blueprints
    from app.main.routes import bp_main
    app.register_blueprint(bp_main)

    from app.auth.routes import bp_auth
    app.register_blueprint(bp_auth)

    return app

