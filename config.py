"""Flask config class"""
from os.path import dirname, abspath, join


class Config(object):
    """Set Flask base configuration"""
    CSRF_ENABLED = True
    SECRET_KEY = '93b35eaab44cb731d5ea79c9032f4d71f3d4510b9e72'

    #General Config
    DEBUG = False
    TESTING = False

    #forms config
    WTF_CSRF_SECRET_KEY = 'this-is-not-random-but-should-be'

    # Database config
    CWD = dirname(abspath(__file__))
    SQLALCHEMY_DATABASE_URI = 'sqlite:///'+join(CWD, 'webapp_sqlite.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class TestConfig(Config):
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    WTF_CSRF_ENABLED = False
    PRESERVE_CONTEXT_ON_EXCEPTION = False


class ProductConfig(Config):
    DEBUG = False
    TESTING = False


class DevConfig(Config):
    DEBUG = True


app_config = {
    'development': DevConfig,
    'production': ProductConfig,
    'testing': TestConfig
}
