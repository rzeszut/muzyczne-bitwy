from flask import render_template, redirect, url_for, request, abort

from application import app
from application.database import Song, Battle, db

@app.route('/battle/<int:battle_id>')
def read_battle(battle_id):
    battle = Battle.query.get(battle_id)
    return render_template('battle/battle.html', battle = battle)

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
    return render_template('battle/finish_battle.html', battle = battle)

@app.route('/battle/<int:battle_id>/finish', methods = ['POST'])
def finish_battle(battle_id):
    winner_song_ids = request.form.getlist('songs')
    if len(winner_song_ids) != 2:
        abort(500)

    battle = Battle.query.get(battle_id)
    battle.finished = True
    db.session.add(battle)

    winner_songs = Song.query.filter(Song.id.in_(winner_song_ids)).all()
    next_phase = battle.phase.next_phase
    next_phase.songs.extend(winner_songs)
    db.session.add(next_phase)

    db.session.commit()

    return redirect(url_for('read_battle', battle_id = battle_id))

