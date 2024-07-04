import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///cardio_app.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
