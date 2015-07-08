#! venv/bin/python3

from flask.ext.script import Manager

from application import app
from application.database import db

manager = Manager(app)

@manager.command
def create_db():
    db.create_all()

@manager.command
def drop_db():
    db.drop_all()

if __name__ == "__main__":
    manager.run()

