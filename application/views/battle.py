from flask import Blueprint, render_template, redirect, url_for, request, abort, flash
from operator import itemgetter

from application.database import Song, Battle, db, transactional
from application.util import shuffled

battles = Blueprint('battles', __name__)

@battles.route('/battle/<int:battle_id>')
def read_battle(battle_id):
    battle = Battle.query.get(battle_id)
    return render_template('battle/battle.html', battle = battle)

@battles.route('/battle/<int:battle_id>/start')
@transactional
def start_battle(battle_id):
    battle = Battle.query.get(battle_id)
    battle.start()
    db.session.add(battle)

    flash('Bitwa została rozpoczęta.', 'success')
    return redirect(url_for('battles.read_battle', battle_id = battle_id))

@battles.route('/battle/<int:battle_id>/finish', methods = ['GET'])
def finish_battle_form(battle_id):
    battle = Battle.query.get(battle_id)
    return render_template('battle/finish_battle.html', battle = battle)

@battles.route('/battle/<int:battle_id>/finish', methods = ['POST'])
@transactional
def finish_battle(battle_id):
    winners_count = int(request.form['winners'])
    song_ids = map(int, request.form.getlist('songs'))
    song_points = map(int, request.form.getlist('points'))

    songs = sorted(shuffled(zip(song_ids, song_points)), \
                   key = itemgetter(1), reverse = True)
    winner_song_ids = list(map(itemgetter(0), songs[:winners_count]))

    battle = Battle.query.get(battle_id)
    battle.finish()
    db.session.add(battle)

    winner_songs = Song.query.filter(Song.id.in_(winner_song_ids)).all()
    next_phase = battle.phase.next_phase
    next_phase.songs.extend(winner_songs)
    db.session.add(next_phase)

    flash('Bitwa została zakończona.', 'success')
    return redirect(url_for('battles.read_battle', battle_id = battle_id))

