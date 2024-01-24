import os
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_cors import CORS


username = os.environ.get('DB_USER', 'root')
password = os.environ.get('DB_PASS', 'pass')
host = os.environ.get('DB_HOST', '127.0.0.1')
port = os.environ.get('DB_PORT', '3306')
db_name = os.environ.get('DB_NAME', 'charamane')
db = SQLAlchemy()
ma = Marshmallow()
origins = ["http://localhost:3000", "http://localhost:3000/"]


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        SQLALCHEMY_TRACK_MODIFICATIONS=True,
        SQLALCHEMY_DATABASE_URI=f"mysql://{username}:{password}@{host}:{port}/{db_name}",
        SSL_MODE="VERIFY_IDENTITY",
        SSL_CA="/etc/ssl/certs/ca-certificates.crt"
    )

    CORS(
        app,
        supports_credentials=True,
        origins=origins,
        methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        allow_headers=["*"],
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
    ma.init_app(app)

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
