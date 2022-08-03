from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, session, jsonify
)
from werkzeug.exceptions import abort
from http import HTTPStatus
from . import model, db
from sqlalchemy import desc
from datetime import datetime
from flaskr.auth import login_required
from flaskr.model import (
    CharacterSchema, Characters, CocMetaInfo, CocMetaInfoSchema,
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


@bp.route('/character/<int:ch_id>')
def get_character(ch_id):
    character = Characters.query.filter_by(id=ch_id).first()
    print(character)
    return jsonify({'status': 'ok', 'character': CharacterSchema(many=False).dump(character)})


@bp.route('/character_info/<int:ch_id>')
def get_characters(ch_id):
    print(ch_id)
    character_info = db.session.query(Characters, CocMetaInfo).join(
        CocMetaInfo, Characters.id == CocMetaInfo.character_id).filter(Characters.id == ch_id).first()
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


@bp.route('/character_info_status/<int:ch_id>')
def get_characters_info_status(ch_id):
    print(ch_id)
    character = db.session.query(Characters, CocMetaInfo, CocStatusParameters).\
        join(CocMetaInfo, Characters.id == CocMetaInfo.character_id).\
        join(CocStatusParameters, Characters.id == CocStatusParameters.character_id).\
        filter(Characters.id == ch_id).first()
    c = CharacterSchema(many=False).dump(character[0])
    c['coc_meta_info'] = CocMetaInfoSchema(many=False).dump(character[1])
    c['coc_status_parameters'] = CocStatusParametersSchema(
        many=False).dump(character[2])
    return jsonify({"result": c}), 200


@bp.route('/character', methods=['POST'])
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
    coc_status_parameters = CocStatusParameters(
        character_id=id,
        str=coc_status_parameters["str"],
        con=coc_status_parameters["con"],
        pow=coc_status_parameters["pow"],
        dex=coc_status_parameters["dex"],
        app=coc_status_parameters["app"],
        size=coc_status_parameters["size"],
        inte=coc_status_parameters["inte"],
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
            skill_type=skill_data["skill_type"],
        )
        create_skill(skill)

    if error is not None:
        return {"Failed to create character": error}, 500
    db.session.commit()
    return {"res": character_data}, HTTPStatus.OK


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


@ bp.route('/<string:id>/update', methods=('GET', 'POST'))
# @ login_required
def update(id):
    character = get_character(id)

    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
            return jsonify({"result": '{}'.format(error)}), 500
        else:
            character.character_name = title
            character.player_name = body
            db.session.commit()
            return redirect(url_for('character.index'))

    return render_template('character/update.html', post=character)
    # return jsonify({'character': entries_schema.dump(character).data})


@bp.route('/<int:id>/delete', methods=('POST',))
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
