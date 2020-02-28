from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from config import DevConfig

db = SQLAlchemy()


def create_app(config_class=DevConfig):
    """Creates an application instance to run using settings from config.py
    :return: A Flask object"""

    app = Flask(__name__)

    app.config.from_object(config_class)

    from populate_db import populate_db
    db.init_app(app)

    # The following is needed if you want to map classes to an existing database
    from app.models3 import User, City, Forecast
    with app.app_context():
        # db.Model.metadata.reflect(db.engine)
        db.create_all()
        populate_db()

    # Register Blueprints
    from app.main.routes import bp_main
    app.register_blueprint(bp_main)

    return app