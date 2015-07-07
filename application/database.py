from flask.ext.sqlalchemy import SQLAlchemy
from application import app

db = SQLAlchemy(app)

class Song(db.Model):
    __table_args__ = {'sqlite_autoincrement': True}

    id = db.Column(db.Integer, primary_key = True, nullable = False)
    artist = db.Column(db.String(128), nullable = False)
    song = db.Column(db.String(128), nullable = False)
    link = db.Column(db.String(256))

class Battle(db.Model):
    __table_args__ = {'sqlite_autoincrement': True}

    id = db.Column(db.Integer, primary_key = True, nullable = False)
    song1_id = db.Column(db.ForeignKey(Song.id), nullable = False)
    song2_id = db.Column(db.ForeignKey(Song.id), nullable = False)
    song3_id = db.Column(db.ForeignKey(Song.id), nullable = False)
    song4_id = db.Column(db.ForeignKey(Song.id), nullable = False)
    phase_id = db.Column(db.ForeignKey('phase.id'), nullable = False)

    started = db.Column(db.Boolean, nullable = False, default = False)
    finished = db.Column(db.Boolean, nullable = False, default = False)

    song1 = db.relationship('Song', foreign_keys = song1_id)
    song2 = db.relationship('Song', foreign_keys = song2_id)
    song3 = db.relationship('Song', foreign_keys = song3_id)
    song4 = db.relationship('Song', foreign_keys = song4_id)
    phase = db.relationship('Phase', foreign_keys = phase_id, \
                            backref = db.backref('battles'))

phase_songs = db.Table('phase_songs',
    db.Column('song_id', db.ForeignKey('song.id')),
    db.Column('phase_id', db.ForeignKey('phase.id'))
)

class Phase(db.Model):
    __table_args__ = {'sqlite_autoincrement': True}

    id = db.Column(db.Integer, primary_key = True, nullable = False)

    songs = db.relationship('Song', secondary = phase_songs, \
                            backref = db.backref('songs'))

    def get_next_phase(self):
        next_phase = Phase.query.get(self.id + 1)
        if next_phase is None:
            next_phase = Phase()
            db.session.add(next_phase)
        return next_phase


