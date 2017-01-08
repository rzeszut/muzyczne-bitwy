import os

SECRET_KEY = os.urandom(24)
SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']

BASIC_AUTH_FORCE = True
BASIC_AUTH_REALM = 'muzyczne-bitwy'
BASIC_AUTH_USERNAME = 'rzeszut'
BASIC_AUTH_PASSWORD = 'warcraft3'

