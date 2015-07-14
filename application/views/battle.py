from flask import render_template, redirect, url_for, request, abort, flash
from operator import itemgetter

from application import app
from application.database import Song, Battle, db
from application.util import shuffled

@app.route('/battle/<int:battle_id>')
def read_battle(battle_id):
    battle = Battle.query.get(battle_id)
    return render_template('battle/battle.html', battle = battle)

@app.route('/battle/<int:battle_id>/start')
def start_battle(battle_id):
    battle = Battle.query.get(battle_id)
    battle.start()

    db.session.add(battle)
    db.session.commit()

    flash('Bitwa została rozpoczęta.', 'success')
    return redirect(url_for('read_battle', battle_id = battle_id))

@app.route('/battle/<int:battle_id>/finish', methods = ['GET'])
def finish_battle_form(battle_id):
    battle = Battle.query.get(battle_id)
    return render_template('battle/finish_battle.html', battle = battle)

@app.route('/battle/<int:battle_id>/finish', methods = ['POST'])
def finish_battle(battle_id):
    winners_count = int(request.form['winners'])
    song_ids = request.form.getlist('songs')
    song_points = request.form.getlist('points')

    songs = sorted(shuffled(zip(song_ids, song_points)), \
                   key = itemgetter(1), reverse = True)
    winner_song_ids = list(map(songs[:winners_count], itemgetter(0)))

    battle = Battle.query.get(battle_id)
    battle.finish()
    db.session.add(battle)

    winner_songs = Song.query.filter(Song.id.in_(winner_song_ids)).all()
    next_phase = battle.phase.next_phase
    next_phase.songs.extend(winner_songs)
    db.session.add(next_phase)

    db.session.commit()

    flash('Bitwa została zakończona.', 'success')
    return redirect(url_for('read_battle', battle_id = battle_id))

