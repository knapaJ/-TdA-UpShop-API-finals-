import os
import datetime

import flask
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
# SQLite ForeignKey constraints enforcement enable, as per: https://stackoverflow.com/a/15542046
# from sqlalchemy import event
# from sqlalchemy.engine import Engine
# from sqlite3 import Connection as SQLite3Connection
# @event.listens_for(Engine, "connect")
# def _set_sqlite_pragma(dbapi_connection, connection_record):
#     if isinstance(dbapi_connection, SQLite3Connection):
#         cursor = dbapi_connection.cursor()
#         cursor.execute("PRAGMA foreign_keys=ON;")
#         cursor.close()


# Create DB engine
db = SQLAlchemy()


def create_app(test_config=None):
    # Import ORM models
    from app.models import User, Commit

    # Create and configure app
    app = Flask("app", instance_relative_config=True)
    # Create preliminary config, will be used, if no config.py file is found.
    app.config.from_mapping(
        SECRET_KEY='dev',
        SQLALCHEMY_DATABASE_URI="sqlite:///" + os.path.join(app.instance_path, "app.db")
    )

    if test_config is None:
        # Load instance config, since no test config has been provided
        app.config.from_pyfile('config.py', silent=True)
    else:
        # Load provided test config
        app.config.from_mapping(test_config)

    # Make sure instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # Attach DB to app
    db.init_app(app)

    @app.cli.command()
    def createdb():
        print(f"Creating DB at {app.config['SQLALCHEMY_DATABASE_URI']}")
        db.create_all()

    @app.cli.command()
    def seeddata():
        print("Seeding testing data values ...", end='')
        print("DONE")

    @app.cli.command()
    def dropdb():
        print(f"Dropping db ...", end='')
        db.drop_all()
        print(f"DONE")

    # hello world just for testing
    @app.route('/hello-world')
    def hello_world():
        return f"Hello world!<br/> Application root is: {app.config['APPLICATION_ROOT']}<br/> URL for this page is: " \
               f"{flask.url_for('hello_world', _external=True)}<br/>" \
               f"<img src=\"https://picsum.photos/seed/paisdpaishdpai/200\"/>", 200

    from app.blueprints_private.user import private_user_endpoint
    app.register_blueprint(private_user_endpoint, url_prefix="/private/user")

    from app.blueprints.user import user_endpoint
    app.register_blueprint(user_endpoint, url_prefix="/user")

    from app.blueprints_private.commit import private_commit_endpoint
    app.register_blueprint(private_commit_endpoint, url_prefix="/private/commit")

    from app.blueprints.commit import commit_endpoint
    app.register_blueprint(commit_endpoint, url_prefix="/commit")

    return app
