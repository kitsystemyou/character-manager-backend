import click
from flask import current_app, g
from flask.cli import with_appcontext
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import scoped_session, sessionmaker


def get_db():
    if 'db' not in g:
        return g.db
    else:
        return g.db


def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()


def shutdown_session(exception=None):
    g.db.remove()


# @click.command('init-db')
# @with_appcontext
# def init_db_command():
#     """Clear the existing data and create new tables."""
#     init_db()
#     click.echo('Initialized the database.')


# def init_app(app):
#     engine = create_engine(SQLALCHEMY_DATABASE_URI)
#     g.db = scoped_session(sessionmaker(autocommit=False,
#                                        autoflush=False,
#                                        bind=engine))
#     Base = declarative_base()
#     Base.metadata.bind = engine
#     app.teardown_appcontext(close_db)
#     app.teardown_appcontext(shutdown_session)
#     # app.cli.add_command(init_db_command)
