import os

CONFIGS = {
    "development": "urlinfo.config.DevelopmentConfig",
    "testing": "urlinfo.config.TestingConfig",
    "default": "urlinfo.config.DevelopmentConfig"
}

def configure_app(app, config_name=None):
    config_name_touse = os.getenv('FLASK_CONFIGURATION', 'default') if config_name == None else config_name
    app.config.from_object(CONFIGS[config_name_touse]) # object-based default configuration
    #app.config.from_pyfile('config.cfg', silent=True) # instance-folders configuration

class DefaultConfig(object):
    DEBUG = False
    TESTING = False
    DB_ENGINE = "sqlite"
    DATABASE = 'urlinfo.sqlite'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class DevelopmentConfig(DefaultConfig):
    DEBUG = True
    TESTING = True

class TestingConfig(DefaultConfig):
    DEBUG = False
    TESTING = True
    DATABASE = 'test_urlinfo.sqlite' #override for testing
