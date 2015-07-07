from flask import render_template, redirect, url_for, request

from application import app
from application.database import Song, db

@app.route('/')
def home():
    return 'Hello World'

@app.route('/songs')
def show_all_songs():
    songs = Song.query.all()
    return render_template('songs.html', songs = songs)

@app.route('/song/<int:id>')
def show_song(id):
    return 'TODO'

@app.route('/song/new')
def new_song():
    return render_template('new_song.html')

@app.route('/song', methods = ['POST'])
def create_song():
    song = Song(artist = request.form['artist'], \
                song = request.form['song'], \
                link = request.form['link'])
    db.session.add(song)
    db.session.commit()

    return redirect(url_for('show_all_songs'))

