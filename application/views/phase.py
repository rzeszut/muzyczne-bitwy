from flask import render_template, redirect, url_for, request

from application import app
from application.database import Song, Phase, db

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
    # TODO: get all songs for this phase, create randomized battles,
    # TODO: any leftover songs go to the next phase
    return 'TODO'

