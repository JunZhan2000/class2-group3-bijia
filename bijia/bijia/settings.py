import os


FLASK_APP = os.getenv('FLASK_APP,' 'bijia')
SECRET_KEY = os.getenv('SECRET_KEY', 'secret string')
SQLALCHEMY_TRACK_MODIFICATIONS = False