import os

DEBUG = True

SECRET_KEY = os.urandom(24)
SQLALCHEMY_DATABASE_URI = 'sqlite:///mb17.db'

BASIC_AUTH_FORCE = True
BASIC_AUTH_REALM = 'muzyczne-bitwy'
BASIC_AUTH_USERNAME = 'admin'
BASIC_AUTH_PASSWORD = 'admin1'

