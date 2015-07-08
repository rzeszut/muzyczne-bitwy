from flask import render_template

from application import app

@app.route('/')
def index():
    return render_template('index.html')

from application.views.song import *
from application.views.phase import *
from application.views.battle import *

