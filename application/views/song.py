from flask import render_template, redirect, url_for, request

from application import app
from application.database import Song, db

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

