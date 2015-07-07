from flask import render_template, redirect, url_for, request, abort
import random

from application import app
from application.database import Song, Phase, Battle, db

@app.route('/')
def index():
    return render_template('index.html')

###
# Songs
###

@app.route('/songs')
def read_songs():
    songs = Song.query.all()
    return render_template('songs.html', songs = songs, show_controls = True)

@app.route('/song/<int:song_id>')
def read_song(song_id):
    return 'TODO'

@app.route('/song', methods = ['GET'])
def create_song_form():
    return render_template('new_song.html')

@app.route('/song', methods = ['POST'])
def create_song():
    song = Song(artist = request.form['artist'], \
                song = request.form['song'], \
                link = request.form['link'])
    db.session.add(song)
    db.session.commit()

    return redirect(url_for('read_songs'))

###
# Phases
###

@app.route('/phases')
def read_phases():
    phases = Phase.query.all()
    return render_template('phases.html', phases = phases)

@app.route('/phase/create')
def create_first_phase():
    phase = Phase()
    phase.songs = Song.query.all()

    db.session.add(phase)
    db.session.commit()

    return redirect(url_for('read_phases'))

@app.route('/phase/<int:phase_id>')
def read_phase(phase_id):
    phase = Phase.query.get(phase_id)
    return render_template('phase.html', phase = phase)

@app.route('/phase/<int:phase_id>/songs')
def read_phase_songs(phase_id):
    phase_songs = Phase.query.get(phase_id).songs
    return render_template('songs.html', songs = phase_songs, \
                           show_controls = False)

@app.route('/phase/<int:phase_id>/battles')
def read_phase_battles(phase_id):
    phase = Phase.query.get(phase_id)
    return render_template('battles.html', phase = phase)

@app.route('/phase/<int:phase_id>/battles/create')
def create_phase_battles(phase_id):
    return 'TODO'

###
# Battles
###

@app.route('/battle/<int:battle_id>')
def read_battle(battle_id):
    battle = Battle.query.get(battle_id)
    return render_template('battle.html', battle = battle)

@app.route('/battle/<int:battle_id>/start')
def start_battle(battle_id):
    battle = Battle.query.get(battle_id)
    battle.started = True

    db.session.add(battle)
    db.session.commit()

    return redirect(url_for('read_battle', battle_id = battle_id))

@app.route('/battle/<int:battle_id>/finish', methods = ['GET'])
def finish_battle_form(battle_id):
    battle = Battle.query.get(battle_id)
    return render_template('finish_battle.html', battle = battle)

@app.route('/battle/<int:battle_id>/finish', methods = ['POST'])
def finish_battle(battle_id):
    winner_song_ids = request.form.getlist('songs')
    if len(winner_song_ids) != 2:
        abort(500)

    battle = Battle.query.get(battle_id)
    battle.finished = True
    db.session.add(battle)

    winner_songs = Song.query.filter(Song.id.in_(winner_song_ids)).all()
    next_phase = battle.phase.get_next_phase()
    next_phase.songs.extend(winner_songs)
    db.session.add(next_phase)

    db.session.commit()

    return redirect(url_for('read_battle', battle_id = battle_id))

