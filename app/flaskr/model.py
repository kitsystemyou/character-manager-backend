from flaskr.db import metadata, db_session
from sqlalchemy import Table, Column, Integer, String, Time
from sqlalchemy.orm import mapper


class User(object):
    query = db_session.query_property()
    def __init__(self, id=None, username=None, password=None):
        self.id = id
        self.username = username
        self.password = password

    def __repr__(self):
        return f'<User {self.username!r}>'
users = Table('user', metadata,
    Column('id', Integer, primary_key=True),
    Column('username', String(10), unique=True),
    Column('password', String(20), unique=True)
)
mapper(User, users)


def create_init(app):
    with app.app_context():
        app.db.drop_all()
        app.db.create_all()
        user_create()
        app.db.session.commit()


def user_create():
    # テストデータ
    users = [
        {"username": "山田太郎"},
        {"username": "上田二郎"},
        {"username": "田中三郎"}
    ]
    for i in users:
        u = User(name=i["username"])
        db.session.add(u)


class Post(object):
    __tablename__ = 'post'
    def __init__(self, name=None, email=None):
        self.name = name
        self.email = email

    def __repr__(self):
        return f'<POST {self.name!r}>'
    
posts = Table('post', metadata,
    Column('id', Integer, primary_key=True),
    Column('author_id', Integer, unique=True),
    Column('created', Time, unique=False),
    Column('title', String(20), unique=False),
    Column('body', String(200), unique=False)
)
mapper(Post, posts)