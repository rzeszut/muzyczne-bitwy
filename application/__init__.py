from flask import Flask

def create_app(config):
    app = Flask('muzyczne-bitwy')
    app.config.from_pyfile(config)

    from application.database import db
    db.init_app(app)

    from application.util import jinja2_utilities
    app.context_processor(jinja2_utilities)

    from application.views import index, songs, phases, battles
    app.register_blueprint(index)
    app.register_blueprint(songs)
    app.register_blueprint(phases)
    app.register_blueprint(battles)

    return app

