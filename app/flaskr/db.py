import click
from flask import current_app, g
from flask.cli import with_appcontext
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import scoped_session, sessionmaker


username = 'root'
password = 'pass'
host = '127.0.0.1'
port = '3306'
db_name = 'charamane'

SQLALCHEMY_DATABASE_URI =\
    'mysql://' + username + ':' + password + \
    '@' + host + ':' + port + '/' + db_name

engine = create_engine(SQLALCHEMY_DATABASE_URI)
metadata = MetaData()
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))


def init_db():
    metadata.create_all(bind=engine)


def get_db():
    if 'db' not in g:
        return db_session
    else:
        return


def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()


def shutdown_session(exception=None):
    db_session.remove()


@click.command('init-db')
@with_appcontext
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')


def init_app(app):
    app.teardown_appcontext(close_db)
    app.teardown_appcontext(shutdown_session)
    app.cli.add_command(init_db_command)
