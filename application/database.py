from flask.ext.sqlalchemy import SQLAlchemy
from datetime import date, timedelta

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

    __NOT_STARTED = 0
    __STARTED = 1
    __FINISHED = 2
    __CHECK_CONDITION = 'state IN ({})'.format( \
        ', '.join(map(str, [__NOT_STARTED, __STARTED, __FINISHED])))

    id = db.Column(db.Integer, primary_key = True, nullable = False)
    song1_id = db.Column(db.ForeignKey('song.id'), nullable = False)
    song2_id = db.Column(db.ForeignKey('song.id'), nullable = False)
    song3_id = db.Column(db.ForeignKey('song.id'), nullable = False)
    song4_id = db.Column(db.ForeignKey('song.id'), nullable = False)
    phase_id = db.Column(db.ForeignKey('phase.id'), nullable = False)

    state = db.Column(db.Integer, \
                      db.CheckConstraint(__CHECK_CONDITION), \
                      nullable = False, default = __NOT_STARTED)
    start_date = db.Column(db.Date)

    song1 = db.relationship('Song', foreign_keys = song1_id)
    song2 = db.relationship('Song', foreign_keys = song2_id)
    song3 = db.relationship('Song', foreign_keys = song3_id)
    song4 = db.relationship('Song', foreign_keys = song4_id)
    phase = db.relationship('Phase', foreign_keys = phase_id, \
                            backref = db.backref('battles'))

    @property
    def songs(self):
        return [self.song1, self.song2, self.song3, self.song4]

    @property
    def started(self):
        return self.state == self.__STARTED

    @property
    def finished(self):
        return self.state == self.__FINISHED

    @property
    def finish_date(self):
        return self.start_date + timedelta(days = 7)

    def start(self):
        self.state = self.__STARTED
        self.start_date = date.today()

    def finish(self):
        self.state = self.__FINISHED

phase_songs = db.Table('phase_songs',
    db.Column('song_id', db.ForeignKey('song.id'), nullable = False),
    db.Column('phase_id', db.ForeignKey('phase.id'), nullable = False)
)

class Phase(db.Model):
    __table_args__ = {'sqlite_autoincrement': True}

    id = db.Column(db.Integer, primary_key = True, nullable = False)

    songs = db.relationship('Song', secondary = phase_songs)

    @property
    def next_phase(self):
        next_phase = Phase.query.get(self.id + 1)
        if next_phase is None:
            next_phase = Phase()
            db.session.add(next_phase)
        return next_phase

