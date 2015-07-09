from flask import render_template, redirect, url_for, request, flash
import random

from application import app
from application.database import Song, Phase, Battle, db

@app.route('/phases')
def read_phases():
    phases = Phase.query.all()
    return render_template('phase/phases.html', phases = phases)

@app.route('/phase/create')
def create_first_phase():
    phase = Phase()
    phase.songs = Song.query.all()

    db.session.add(phase)
    db.session.commit()

    flash('Pierwsza faza została utworzona.', 'success')
    return redirect(url_for('read_phases'))

@app.route('/phase/<int:phase_id>')
def read_phase(phase_id):
    phase = Phase.query.get(phase_id)
    return render_template('phase/phase.html', phase = phase)

@app.route('/phase/<int:phase_id>/songs')
def read_phase_songs(phase_id):
    phase_songs = Phase.query.get(phase_id).songs
    return render_template('song/songs.html', songs = phase_songs, \
                           show_controls = False, \
                           backlink = url_for('read_phase', phase_id = phase_id))

@app.route('/phase/<int:phase_id>/battles')
def read_phase_battles(phase_id):
    phase = Phase.query.get(phase_id)
    return render_template('phase/battles.html', phase = phase)

@app.route('/phase/<int:phase_id>/battles/create')
def create_phase_battles(phase_id):
    phase = Phase.query.get(phase_id)

    songs = random.shuffle(list(phase.songs))
    for battle_songs in partition(songs, 4):
        if len(battle_songs) == 4:
            create_battle(phase, *battle_songs)
        else:
            add_songs_to_next_phase(phase.next_phase, battle_songs)

    db.session.add(phase)
    db.session.commit()

    flash('Bitwy dla fazy {} zostały utworzone.'.format(phase_id), 'success')
    return redirect(url_for('read_phase_battles', phase_id = phase_id))

def partition(l, n):
    for i in xrange(0, len(l), n):
        yield l[i : i + n]

def create_battle(phase, song1, song2, song3, song4):
    battle = Battle(song1 = song1, song2 = song2, song3 = song3, \
                    song4 = song4, phase = phase)
    phase.battles.append(battle)

    db.session.add(battle)

def add_songs_to_next_phase(phase, songs):
    phase.songs.extend(songs)
    db.session.add(phase)

