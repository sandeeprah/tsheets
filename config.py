import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    DEBUG = True
    TEMPLATES_AUTO_RELOAD = True
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'super-secret'
    SECURITY_PASSWORD_SALT = 'my_precious_two'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'application.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
