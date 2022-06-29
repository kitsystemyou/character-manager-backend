from cgitb import html
import os
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_sqlalchemy.model import DefaultMeta, Model

username = 'root'
password = 'pass'
host = '127.0.0.1'
port = '3306'
db_name = 'charamane'
db = SQLAlchemy()


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        SQLALCHEMY_DATABASE_URI='mysql://' + username + ':' + password +
        '@' + host + ':' + port + '/' + db_name
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    db.init_app(app)

    # Create app blueprints
    from . import auth
    app.register_blueprint(auth.bp)

    from . import character
    app.register_blueprint(character.bp)
    app.add_url_rule('/', endpoint='index')

    # a simple page that says hello
    @app.route('/hello')
    def hello():
        hello = {'aroha': 'konnitiha'}
        return jsonify(hello)

    return app
