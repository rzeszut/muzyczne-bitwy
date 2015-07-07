from flask import Flask

app = Flask('muzyczne-bitwy')
app.config.from_pyfile('application.cfg')

import application.views

