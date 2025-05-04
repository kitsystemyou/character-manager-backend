import datetime
from flask import (
    Blueprint, flash, g, render_template, request, jsonify
)
from werkzeug.exceptions import abort
from http import HTTPStatus
from . import model, db
from sqlalchemy import desc
from datetime import datetime
from flaskr.auth import login_required
from flaskr.model import (
    CharacterSchema, Characters, CocMetaInfo, CocMetaInfoSchema, CocSkillsSchema,
    CocStatusParameters, CocStatusParametersSchema, CocSkills
)

bp = Blueprint('character', __name__)


@bp.route('/')
def index():
    characters = Characters.query.order_by(desc(model.Characters.id))
    return render_template('character/index.html', characters=characters)


@bp.route('/character')
def list_character():
    characters = Characters.query.order_by(desc(model.Characters.id))
    return jsonify({'result': CharacterSchema(many=True).dump(characters)}), 200


@bp.route('/character/<int:id>')
def get_character(id):
    character = Characters.query.filter_by(id=id).first()
    print(character)
    return jsonify({'status': 'ok', 'character': CharacterSchema(many=False).dump(character)})


@bp.route('/character_info/<int:id>')
def get_character_meta_info(id):
    print(id)
    character_info = db.session.query(Characters, CocMetaInfo).join(
        CocMetaInfo, Characters.id == CocMetaInfo.character_id).filter(Characters.id == id).first()
    """
        if using Dynamic Schema
        data = {Characters.__tablename__: character_info[0],
                CocMetaInfo.__tablename__: character_info[1]}
        dynamic_schema = DynamicSchema(many=False)
        return jsonify({'status': 'ok', "result": dynamic_schema.dump(data)})
    """
    c = CharacterSchema(many=False).dump(character_info[0])
    c['coc_meta_info'] = CocMetaInfoSchema(many=False).dump(character_info[1])
    print(c)
    return jsonify({'status': 'ok', "result": c})


@bp.route('/character_info_status/<int:id>')
def get_characters_info_status(id):
    print(id)
    character = db.session.query(Characters, CocMetaInfo, CocStatusParameters).\
        join(CocMetaInfo, Characters.id == CocMetaInfo.character_id).\
        join(CocStatusParameters, Characters.id == CocStatusParameters.character_id).\
        filter(Characters.id == id).first()
    c = CharacterSchema(many=False).dump(character[0])
    c["coc_meta_info"] = CocMetaInfoSchema(many=False).dump(character[1])
    c["coc_status_parameters"] = CocStatusParametersSchema(
        many=False).dump(character[2])
    return jsonify({"result": c}), 200


@bp.route('/character_all_info/<int:id>')
def get_character_all_info(id):
    print(id)
    character = db.session.query(Characters, CocMetaInfo, CocStatusParameters).\
        join(CocMetaInfo, Characters.id == CocMetaInfo.character_id).\
        join(CocStatusParameters, Characters.id == CocStatusParameters.character_id).\
        filter(Characters.id == id).first()
    c = CharacterSchema(many=False).dump(character[0])

    # この APIだけ BasicInfo をネスト内に入れてルートから消す
    basic_info_keys = ["character_name", "player_name", "game_system", "prof_img_path", "tags"]
    c["basic_character_info"] = {key: c[key] for key in basic_info_keys}
    [c.pop(k) for k in ["character_name", "player_name", "game_system", "prof_img_path"]]

    c["coc_meta_info"] = CocMetaInfoSchema(many=False).dump(character[1])
    c["coc_status_parameters"] = CocStatusParametersSchema(many=False).dump(character[2])
    skills = CocSkills.query.filter_by(character_id=id).all()
    c["coc_skills"] = CocSkillsSchema(many=True).dump(skills)
    return jsonify({"result": c}), 200


@bp.route('/character_all_info', methods=['POST'])
def create_character_info():
    # @login_required
    error = None
    req_json = request.get_json()

    # Create Character
    if not req_json["character"]:
        error = "character is required."
        flash(error)
    else:
        character_data = req_json["character"]
    character = Characters(
        user_id=character_data["user_id"],
        character_name=character_data["character_name"],
        player_name=character_data["player_name"],
        game_system=character_data["game_system"],
        prof_img_path=character_data["prof_img_path"],
        tags=character_data["tags"],
        create_time=datetime.now(),
        update_time=datetime.now(),
    )
    print(vars(character))
    # TODO: もしくは　character は作成済み前提でもいいかもしれない
    create_character(character)
    db.session.commit()
    id = character.id
    print("character_id", id)

    # Create coc_meta_info
    if not req_json["character"]["coc_meta_info"]:
        error = "coc meta info is required."
    else:
        coc_meta_info_data = req_json["character"]["coc_meta_info"]
    coc_meta_info = CocMetaInfo(
        character_id=id,
        job=coc_meta_info_data["job"],
        sex=coc_meta_info_data["sex"],
        age=coc_meta_info_data["age"],
        height=coc_meta_info_data["height"],
        weight=coc_meta_info_data["weight"],
        hair_color=coc_meta_info_data["hair_color"],
        eye_color=coc_meta_info_data["eye_color"],
        skin_color=coc_meta_info_data["skin_color"],
        home_place=coc_meta_info_data["home_place"],
        mental_disorder=coc_meta_info_data["mental_disorder"],
        edu_background=coc_meta_info_data["edu_background"],
        memo=coc_meta_info_data["memo"],
    )
    create_meta_info(coc_meta_info)

    # Create coc_status_params
    if not req_json["character"]["coc_status_parameters"]:
        error = "coc status parameters are required."
    else:
        coc_status_parameters = req_json["character"]["coc_status_parameters"]
    # TODO: VALIDATION
    if coc_status_parameters["max_job_point"] == "":
        coc_status_parameters["max_job_point"] = 0
    if coc_status_parameters["max_concern_point"] == "":
        coc_status_parameters["max_concern_point"] = 0

    coc_status_parameters = CocStatusParameters(
        character_id=id,
        str=coc_status_parameters["str"],
        con=coc_status_parameters["con"],
        pow=coc_status_parameters["pow"],
        dex=coc_status_parameters["dex"],
        app=coc_status_parameters["app"],
        size=coc_status_parameters["size"],
        inte=coc_status_parameters["int"],  # CAUTION
        edu=coc_status_parameters["edu"],
        hp=coc_status_parameters["hp"],
        mp=coc_status_parameters["mp"],
        init_san=coc_status_parameters["init_san"],
        current_san=coc_status_parameters["current_san"],
        idea=coc_status_parameters["idea"],
        knowledge=coc_status_parameters["knowledge"],
        damage_bonus=coc_status_parameters["damage_bonus"],
        luck=coc_status_parameters["luck"],
        max_job_point=coc_status_parameters["max_job_point"],
        max_concern_point=coc_status_parameters["max_concern_point"],
    )
    create_coc_status_parameters(coc_status_parameters)

    if not req_json["character"]["coc_skills"]:
        error = "coc skills are required."
    else:
        coc_skills = req_json["character"]["coc_skills"]
    for skill_data in coc_skills:
        skill = CocSkills(
            character_id=id,
            skill_name=skill_data["skill_name"],
            job_point=skill_data["job_point"],
            concern_point=skill_data["concern_point"],
            grow=skill_data["grow"],
            other=skill_data["other"],
            skill_type=skill_data.get("skill_type", 0),
        )
        create_skill(skill)

    if error is not None:
        return {"Failed to create character": error}, 500
    db.session.commit()
    character_data = req_json["character"]
    character_data["id"] = id
    return {"result": character_data}, HTTPStatus.OK


def create_character(character):
    print("create character")
    db.session.add(character)
    return


def create_meta_info(meta_info):
    print("create coc_meta_info create")
    db.session.add(meta_info)
    return


def create_coc_status_parameters(coc_status_parameters):
    print("create coc_status_parameters")
    db.session.add(coc_status_parameters)
    return


def create_skill(coc_skill):
    print("create coc_skill")
    db.session.add(coc_skill)
    return


def get_character(id, check_author=True):
    character_info = db.session.query(Characters, CocMetaInfo).join(
        CocMetaInfo, Characters.id == CocMetaInfo.character_id).filter(Characters.id == id).first()

    if character_info is None:
        abort(404, f"Post id {id} doesn't exist.")

    # ログインユーザーの user_id と一致したら返すそれ以外は 403
    # if check_author and character_info.user_id != str(g.user.id):
    #     abort(403)

    return character_info


@ bp.route('/character/<int:id>', methods=['PATCH'])
# @ login_required
def update(id):
    print(id)
    error = None
    req_json = request.get_json()
    # COC_SKILL は複数あるので別関数で取得・更新する
    if not req_json["character"]:
        error = "character is required."
        flash(error)
    else:
        req_character = req_json["character"]

    if not req_json["character"]["coc_meta_info"]:
        print("coc_meta_info is none.")
    else:
        req_meta = req_json["character"]["coc_meta_info"]

    if not req_json["character"]["coc_status_parameters"]:
        print("coc_status_parameters is none.")
    else:
        req_status = req_json["character"]["coc_status_parameters"]

    # TODO: 関数化
    c = db.session.query(Characters, CocMetaInfo, CocStatusParameters).\
        join(CocMetaInfo, Characters.id == CocMetaInfo.character_id).\
        join(CocStatusParameters, Characters.id == CocStatusParameters.character_id).\
        filter(Characters.id == id).first()
    chara = c[0]
    meta = c[1]
    status = c[2]

    if error is not None:
        flash(error)
        return jsonify({"result": '{}'.format(error)}), 500
    else:
        # Update character, meta_ifo, status_params
        chara.character_name = req_character.get('character_name')
        chara.player_name = req_character.get("player_name")
        chara.game_system = req_character.get("game_system")
        chara.prof_img_path = req_character.get("prof_img_path")
        chara.tags = req_character.get("tags")
        chara.create_time = req_character.get("create_time", chara.create_time)
        chara.update_time = datetime.now()
        chara.delete_time = req_character.get("delete_time")
        meta.job = req_meta.get("job")
        meta.sex = req_meta.get("sex")
        meta.age = req_meta.get("age")
        meta.height = req_meta.get("height")
        meta.weight = req_meta.get("weight")
        meta.hair_color = req_meta.get("hair_color")
        meta.eye_color = req_meta.get("eye_color")
        meta.skin_color = req_meta.get("skin_color")
        meta.home_place = req_meta.get("home_place")
        meta.mental_disorder = req_meta.get(
            "mental_disorder")
        meta.edu_background = req_meta.get(
            "edu_background")
        status.str = req_status.get("str")
        status.con = req_status.get("con")
        status.pow = req_status.get("pow")
        status.dex = req_status.get("dex")
        status.app = req_status.get("app")
        status.size = req_status.get("size")
        status.inte = req_status.get("inte")
        status.edu = req_status.get("edu")
        status.hp = req_status.get("hp")
        status.mp = req_status.get("mp")
        status.init_san = req_status.get(
            "init_san")
        status.current_san = req_status.get(
            "current_san")
        status.idea = req_status.get("idea")
        status.knowledge = req_status.get(
            "knowledge")
        status.damage_bonus = req_status.get(
            "damage_bonus")
        status.luck = req_status.get("luck")
        status.max_job_point = req_status.get(
            "max_job_point")
        status.max_concern_point = req_status.get(
            "max_concern_point")
        # TODO: COC_SKILL の Upsert

        if not req_json["character"]["coc_skills"]:
            print("coc_status_parameters is none.")
        else:
            req_skills = req_json["character"]["coc_skills"]
        update_skills(req_skills, id)

        db.session.commit()
        return jsonify({"result": "updated"}), HTTPStatus.OK


def update_skills(req_skills, id):
    db_skill = CocSkills.query.filter_by(character_id=id).all()
    for rs in req_skills:
        matched_db_data = list(filter(lambda skill: skill.skill_id == rs.get(
            "skill_id"), db_skill))
        if matched_db_data:
            # skill_id 合うものあったら更新
            print("update skill", rs.get("skill_name"), rs.get("skill_id"))
            mdb = matched_db_data[0]
            mdb.skill_name = rs.get("skill_name"),
            mdb.job_point = rs.get("job_point"),
            mdb.concern_point = rs.get("concern_point"),
            mdb.grow = rs.get("grow"),
            mdb.other = rs.get("other"),
            mdb.skill_type = rs.get("skill_type"),
        else:
            # character_id で絞って同じ skill_id のもの無いなら skill_id が間違っているとして
            # auto_increment する skill_id で新規に作成
            print("insert skill", rs.get("skill_name"))
            new_skill = CocSkills(
                character_id=id,
                skill_name=rs.get("skill_name"),
                job_point=rs.get("job_point"),
                concern_point=rs.get("concern_point"),
                grow=rs.get("grow"),
                other=rs.get("other"),
                skill_type=rs.get("skill_type"),
            )
            db.session.add(new_skill)
    return


@ bp.route('/<int:id>/delete', methods=['delete'])
# @login_required
def delete(id):
    character_meta_info = CocMetaInfo.query.filter_by(character_id=id).first()
    character_status_parameters = CocStatusParameters.query.filter_by(
        character_id=id).first()
    skills = CocSkills.query.filter_by(character_id=id).all()
    [db.session.delete(s) for s in skills]
    character = Characters.query.filter_by(id=id).first()
    db.session.delete(character_meta_info)
    db.session.delete(character_status_parameters)
    db.session.delete(character)
    db.session.commit()
    return jsonify({"deleted": id}), 200
