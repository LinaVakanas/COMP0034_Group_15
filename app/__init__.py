from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail


from config import DevConfig

db = SQLAlchemy()
mail = Mail()
login_manager = LoginManager()


def create_app(config_class=DevConfig):
    """Creates an application instance to run using settings from config.py
    :return: A Flask object"""

    app = Flask(__name__)

    app.config.from_object(config_class)

    db.init_app(app)
    mail.init_app(app)
    login_manager.init_app(app)

    from populate_db import populate_db

    # The following is needed if you want to map classes to an existing database
    from app.models2_backup import User, Mentee, Mentor, Admin, Teacher, School, Report, Message, Chatroom, Pair, PersonalIssues, \
        PersonalInfo, Hobbies, MedicalCond, Location, OccupationalField, StudentReview
    with app.app_context():
        db.drop_all()
        db.create_all()
        populate_db()


    # Register Blueprints
    from app.main.routes import bp_main
    app.register_blueprint(bp_main)

    from app.auth.routes import bp_auth
    app.register_blueprint(bp_auth)

    return app

