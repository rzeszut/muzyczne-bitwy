from flask.ext.sqlalchemy import SQLAlchemy
from application import app

db = SQLAlchemy(app)

class Song(db.Model):
    __table_args__ = {'sqlite_autoincrement': True}

    id = db.Column(db.Integer, primary_key = True, nullable = False)
    artist = db.Column(db.String(128), nullable = False)
    song = db.Column(db.String(128), nullable = False)
    link = db.Column(db.String(256))

