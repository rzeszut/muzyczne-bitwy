from flask import render_template, redirect, url_for, request, flash

from application import app
from application.database import Song, db

@app.route('/songs')
def read_songs():
    songs = Song.query.all()
    return render_template('song/songs.html', songs = songs, show_controls = True, \
                           backlink = url_for('index'))

@app.route('/song/<int:song_id>')
def read_song(song_id):
    song = Song.query.get(song_id)
    return render_template('song/edit_song.html', song = song)

@app.route('/song/<int:song_id>', methods = ['POST'])
def update_song(song_id):
    song = Song.query.get(song_id)
    song.artist = request.form['artist']
    song.song = request.form['song']
    song.link = empty_to_none(request.form['link'])

    db.session.add(song)
    db.session.commit()

    flash('Piosenka została zapisana.', 'success')
    return redirect(url_for('read_songs'))

def empty_to_none(s):
    return None if s == '' else s

@app.route('/song', methods = ['GET'])
def create_song_form():
    return render_template('song/new_song.html')

@app.route('/song', methods = ['POST'])
def create_song():
    song = Song(artist = request.form['artist'], \
                song = request.form['song'], \
                link = request.form['link'])
    db.session.add(song)
    db.session.commit()

    flash('Piosenka została utworzona.', 'success')
    return redirect(url_for('read_songs'))

