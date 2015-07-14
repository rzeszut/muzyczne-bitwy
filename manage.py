#! venv/bin/python3

if __name__ == "__main__":
    from flask.ext.script import Manager

    from application import create_app
    from application.database import db

    manager = Manager(create_app)
    manager.add_option('-c', '--config', dest = 'config', required = False, \
                       default = 'config/dev.py')

    @manager.command
    def create_db():
        db.create_all()

    @manager.command
    def drop_db():
        db.drop_all()

    manager.run()

