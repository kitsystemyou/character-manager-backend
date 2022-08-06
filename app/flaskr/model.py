from sqlalchemy import ForeignKey, Integer, String, DateTime, insert
from . import db
from flask_marshmallow import Marshmallow
from flask_marshmallow.fields import fields


ma = Marshmallow()


class User(db.Model):
    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)

    def __repr__(self):
        return f'<User {self.username!r}>'

    id = db.Column('id', Integer, primary_key=True)
    username = db.Column('username', String(10), unique=False)
    password = db.Column('password', String(20), unique=False)

# 本稼働用
# class User(db.Model):
#     def __init__(self, **kwargs):
#         super(User, self).__init__(**kwargs)

#     def __repr__(self):
#         return f'<User {self.username!r}>'

#     id = db.Column('id', Integer, primary_key=True)
#     username = db.Column('user_name', String(10), unique=False)
#     password = db.Column('password', String(20), unique=False)
#     create_time = db.Column('create_time', DateTime, unique=False)
#     update_time = db.Column('update_time', DateTime, unique=False)
#     delete_time = db.Column('delete_time', DateTime, unique=False)


class CocMetaInfo(db.Model):
    __tablename__ = "coc_meta_info"

    def __init__(self, **kwargs):
        super(CocMetaInfo, self).__init__(**kwargs)

    def __repr__(self):
        return f'<COC_META_INFO {self.character_id!r}>'

    character_id = db.Column('character_id', Integer,
                             ForeignKey('characters.id'), primary_key=True)
    job = db.Column('job', String(10), unique=False)
    sex = db.Column('sex', String(5), unique=False)
    age = db.Column('age', String(5), unique=False)
    height = db.Column('height', String(5), unique=False)
    weight = db.Column('weight', String(5), unique=False)
    hair_color = db.Column('hair_color', String(20), unique=False)
    eye_color = db.Column('eye_color', String(20), unique=False)
    skin_color = db.Column('skin_color', String(20), unique=False)
    home_place = db.Column('home_place', String(20), unique=False)
    mental_disorder = db.Column('mental_disorder', String(10), unique=False)
    edu_background = db.Column('edu_background', String(10), unique=False)
    memo = db.Column('memo', String(100), unique=False)


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
    str = db.Column('str', Integer, unique=False)
    con = db.Column('con', Integer, unique=False)
    pow = db.Column('pow', Integer, unique=False)
    dex = db.Column('dex', Integer, unique=False)
    app = db.Column('app', Integer, unique=False)
    size = db.Column('size', Integer, unique=False)
    inte = db.Column('inte', Integer, unique=False)
    edu = db.Column('edu', Integer, unique=False)
    hp = db.Column('hp', Integer, unique=False)
    mp = db.Column('mp', Integer, unique=False)
    init_san = db.Column('init_san', Integer, unique=False)
    current_san = db.Column('current_san', Integer, unique=False)
    idea = db.Column('idea', Integer, unique=False)
    knowledge = db.Column('knowledge', Integer, unique=False)
    damage_bonus = db.Column('damage_bonus', Integer, unique=False)
    luck = db.Column('luck', Integer, unique=False)
    max_job_point = db.Column('max_job_point', Integer, unique=False)
    max_concern_point = db.Column('max_concern_point', Integer, unique=False)


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

    skill_id = db.Column('skill_id', Integer, primary_key=True)
    character_id = db.Column('character_id', Integer,
                             ForeignKey('characters.id'))
    skill_name = db.Column('skill_name', String, unique=False)
    job_point = db.Column('job_point', Integer, unique=False)
    concern_point = db.Column('concern_point', Integer, unique=False)
    grow = db.Column('grow', Integer, unique=False)
    other = db.Column('other', Integer, unique=False)
    skill_type = db.Column('skill_type', Integer, unique=False)


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
