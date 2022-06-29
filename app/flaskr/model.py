from sqlalchemy import Column, Integer, String, DateTime
from . import db

# metadata.reflect()
# Base = declarative_base(bind=db)


class CocStatusParameters():
    __tablename__ = "coc_status_parameters"
    __table_args__ = {"autoload": True}


class CocMetaInfo():
    __tablename__ = "coc_meta_info"
    # Column('character_id', Integer, primary_key=True)
    # __table_args__ = {"autoload": True}
    # primary key not exist (alternative setting)
    # __table__ = Table('coc_meta_info', metadata,
    #                   Column('character_id', Integer, primary_key=True),
    #                   autoload=True, extend_existing=True)


class CocSkills():
    __tablename__ = "coc_skills"
    __table_args__ = {"autoload": True}


# User model
# class User(db.Model):
#     __tablename__ = "user"
#     __table_args__ = {"autoload": True}

class User(db.Model):
    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)

    def __repr__(self):
        return f'<User {self.username!r}>'

    id = db.Column('id', Integer, primary_key=True)
    username = db.Column('username', String(10), unique=True)
    password = db.Column('password', String(20), unique=True)


# def create_init(app):
#     with app.app_context():
#         app.db.drop_all()
#         app.db.create_all()
#         user_create()
#         app.db.session.commit()


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

    id = Column('id', Integer, primary_key=True)
    author_id = Column('author_id', Integer, unique=True)
    created = Column('created', DateTime, unique=False)
    title = Column('title', String(20), unique=False)
    body = Column('body', String(200), unique=False)

    def __init__(self, name=None, email=None):
        self.name = name
        self.email = email

    def __repr__(self):
        return f'<POST {self.name!r}>'


class Characters(db.Model):
    __tablename__ = 'characters'

    def __init__(self, **kwargs):
        super(Characters, self).__init__(**kwargs)

    def __repr__(self):
        return f'<CHARACTERS {self.id!r}>'

    id = db.Column('id', Integer, primary_key=True)
    user_id = db.Column('user_id', String(32), unique=True)
    character_name = db.Column('character_name', String(255), unique=False)
    player_name = db.Column('player_name', String(20), unique=False)
    game_system = db.Column('game_system', String(20), unique=False)
    prof_img_path = db.Column('prof_img_path', String(50), unique=True)
    tags = db.Column('tags', String(255), unique=False)
    create_time = db.Column('create_time', DateTime, unique=False)
    update_time = db.Column('update_time', DateTime, unique=False)
    delete_time = db.Column('delete_time', DateTime, unique=False)
