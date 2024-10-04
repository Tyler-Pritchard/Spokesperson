import os
basedir = os.path.abspath(os.path.dirname(__file__))

# config.py
class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "default_secret_key")
    SESSION_TYPE = 'filesystem'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///spokesperson.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = True
