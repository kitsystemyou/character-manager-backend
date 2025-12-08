from sqlalchemy import ForeignKey, Integer, String, DateTime, insert, text
from . import db
from flask_marshmallow import Marshmallow
from flask_marshmallow.fields import fields
from datetime import datetime


ma = Marshmallow()


class User(db.Model):
    __tablename__ = 'users'

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)

    def __repr__(self):
        return f'<User {self.user_name!r}>'

    id = db.Column('id', String(36), primary_key=True)
    user_name = db.Column('user_name', String(50), nullable=False)
    email = db.Column('email', String(50), nullable=False)
    login_type = db.Column('login_type', String(20), nullable=False)
    used_system = db.Column('used_system', String(255), nullable=True)
    create_time = db.Column('create_time', DateTime, nullable=False, server_default=text('CURRENT_TIMESTAMP'))
    update_time = db.Column('update_time', DateTime, nullable=False, server_default=text('CURRENT_TIMESTAMP'))
    delete_time = db.Column('delete_time', DateTime, nullable=True)


class CocMetaInfo(db.Model):
    __tablename__ = "coc_meta_info"

    def __init__(self, **kwargs):
        super(CocMetaInfo, self).__init__(**kwargs)

    def __repr__(self):
        return f'<COC_META_INFO {self.character_id!r}>'

    character_id = db.Column('character_id', Integer,
                             ForeignKey('characters.id'), primary_key=True)
    job = db.Column('job', String(10), nullable=True)
    sex = db.Column('sex', String(5), nullable=True)
    age = db.Column('age', String(5), nullable=True)
    height = db.Column('height', String(5), nullable=True)
    weight = db.Column('weight', String(5), nullable=True)
    hair_color = db.Column('hair_color', String(20), nullable=True)
    eye_color = db.Column('eye_color', String(20), nullable=True)
    skin_color = db.Column('skin_color', String(20), nullable=True)
    home_place = db.Column('home_place', String(20), nullable=True)
    mental_disorder = db.Column('mental_disorder', String(10), nullable=True)
    edu_background = db.Column('edu_background', String(10), nullable=True)
    memo = db.Column('memo', String(100), nullable=True)


class CocMetaInfoSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = CocMetaInfo
        include_fk = True
        load_instance = True

    created_time = fields.DateTime('%Y-%m-%dT%H:%M:%S+09:00')
    updated_time = fields.DateTime('%Y-%m-%dT%H:%M:%S+09:00')
    delete_time = fields.DateTime('%Y-%m-%dT%H:%M:%S+09:00')


class CocStatusParameters(db.Model):
    __tablename__ = "coc_status_parameters"

    def __init__(self, **kwargs):
        super(CocStatusParameters, self).__init__(**kwargs)

    def __repr__(self):
        return f'<COC_STATUS_INFO {self.character_id!r}>'

    character_id = db.Column('character_id', Integer,
                             ForeignKey('characters.id'), primary_key=True)
    str = db.Column('str', Integer, nullable=True)
    con = db.Column('con', Integer, nullable=True)
    pow = db.Column('pow', Integer, nullable=True)
    dex = db.Column('dex', Integer, nullable=True)
    app = db.Column('app', Integer, nullable=True)
    size = db.Column('size', Integer, nullable=True)
    inte = db.Column('inte', Integer, nullable=True)
    edu = db.Column('edu', Integer, nullable=True)
    hp = db.Column('hp', Integer, nullable=True)
    mp = db.Column('mp', Integer, nullable=True)
    init_san = db.Column('init_san', Integer, nullable=True)
    current_san = db.Column('current_san', Integer, nullable=True)
    idea = db.Column('idea', Integer, nullable=True)
    knowledge = db.Column('knowledge', Integer, nullable=True)
    damage_bonus = db.Column('damage_bonus', String(20), nullable=True)
    luck = db.Column('luck', Integer, nullable=True)
    max_job_point = db.Column('max_job_point', Integer, nullable=True)
    max_concern_point = db.Column('max_concern_point', Integer, nullable=True)


class CocStatusParametersSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = CocStatusParameters
        include_fk = True
        load_instance = True


class CocSkills(db.Model):
    __tablename__ = "coc_skills"

    def __init__(self, **kwargs):
        super(CocSkills, self).__init__(**kwargs)

    def __repr__(self):
        return f'<COC_SKILLS {self.skill_id!r}>'

    skill_id = db.Column('skill_id', Integer, primary_key=True, autoincrement=True)
    character_id = db.Column('character_id', Integer,
                             ForeignKey('characters.id'), nullable=False)
    skill_name = db.Column('skill_name', String(50), nullable=False)
    job_point = db.Column('job_point', Integer, nullable=True)
    concern_point = db.Column('concern_point', Integer, nullable=True)
    grow = db.Column('grow', Integer, nullable=True)
    other = db.Column('other', Integer, nullable=True)
    skill_type = db.Column('skill_type', Integer, nullable=True)


class CocSkillsSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = CocSkills
        include_fk = True
        load_instance = True


# Upsert サンプル(現状使っていない)
# 使う側 db.session.execute(clause=model.upsert_skill(), params=req_skills)
def upsert_skill():
    stmt = insert(CocSkills)
    return stmt.on_conflict_do_update(
        index_elements=['skill_id'],
        set_={
            'skill_name': stmt.excluded.skill_name,
            'job_point': stmt.excluded.job_point,
            'concern_point': stmt.excluded.concern_point,
            'grow': stmt.excluded.grow,
            'other': stmt.excluded.other,
            'skill_type': stmt.excluded.skill_type,
        })


class Characters(db.Model):
    __tablename__ = 'characters'

    def __init__(self, **kwargs):
        super(Characters, self).__init__(**kwargs)

    def __repr__(self):
        return f'<CHARACTERS {self.id!r}>'

    id = db.Column('id', Integer, primary_key=True, autoincrement=True)
    user_id = db.Column('user_id', String(36), nullable=False)
    character_name = db.Column('character_name', String(255), nullable=False)
    player_name = db.Column('player_name', String(20), nullable=False)
    game_system = db.Column('game_system', String(20), nullable=False)
    prof_img_path = db.Column('prof_img_path', String(50), nullable=True)
    tags = db.Column('tags', String(255), nullable=True)
    create_time = db.Column('create_time', DateTime, nullable=False, server_default=text('CURRENT_TIMESTAMP'))
    update_time = db.Column('update_time', DateTime, nullable=False, server_default=text('CURRENT_TIMESTAMP'))
    delete_time = db.Column('delete_time', DateTime, nullable=True)
    coc_meta_info = db.relationship("CocMetaInfo", backref='characters')
    coc_status_parameters = db.relationship(
        "CocStatusParameters", backref='characters')
    coc_skills = [db.relationship("CocSkills", backref='characters')]


class CharacterSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Characters
        load_instance = True

    created_time = fields.DateTime('%Y-%m-%dT%H:%M:%S+09:00')
    updated_time = fields.DateTime('%Y-%m-%dT%H:%M:%S+09:00')
    delete_time = fields.DateTime('%Y-%m-%dT%H:%M:%S+09:00')
    coc_meta_info = fields.Nested(CocMetaInfoSchema)


DynamicSchema = ma.Schema.from_dict({
    Characters.__tablename__:
        ma.Nested(CharacterSchema, dump_only=True),
    CocMetaInfo.__tablename__:
        ma.Nested(CocMetaInfoSchema, dump_only=True)
})
