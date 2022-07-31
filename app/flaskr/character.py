from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, session, jsonify
)
from werkzeug.exceptions import abort
from http import HTTPStatus
from . import model, db
from sqlalchemy import create_engine, desc
from datetime import datetime
from flaskr.auth import login_required
from flaskr.model import (
    CharacterSchema, Characters, CocMetaInfo, CocMetaInfoSchema,
    CocStatusParameters, CocStatusParametersSchema, CocSkills, CocSkillsSchema
)

bp = Blueprint('character', __name__)


@bp.route('/')
def index():
    characters = Characters.query.order_by(desc(model.Characters.id))
    return render_template('character/index.html', characters=characters)


@bp.route('/test', methods=['POST'])
def create_character_info():
    req_json = request.get_json()
    print(req_json["character"].keys())
    if not req_json["character"]:
        error = 'character value name is required.'
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
    create_character(character)
    return {"res": character_data}, HTTPStatus.OK


def create_character(character):
    print("create_character")
    db.session.add(character)
    db.session.commit()
    return {"res": character}, HTTPStatus.OK


def create_meta_info(meta_info):
    return {"res": meta_info}, HTTPStatus.OK


def create_coc_status_parameters(coc_status_parameters):
    return {"res": coc_status_parameters}, HTTPStatus.OK


def create_skill(coc_skill):
    return {"res": coc_skill}, HTTPStatus.OK


@bp.route('/characters')
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
@login_required
def create():
    character_name = request.form['character_name']
    player_name = request.form['player_name']
    tags = request.form['tags']
    error = None
    print(session['user_id'])
    if not character_name:
        error = 'character name is required.'

    if error is not None:
        flash(error)
        return jsonify({"result": "unknown error"}), HTTPStatus.INTERNAL_SERVER_ERROR
    else:
        character = Characters(
            id=None,
            user_id=session['user_id'],
            character_name=character_name,
            player_name=player_name,
            game_system="CoC",
            prof_img_path="",
            tags=tags,
            create_time=datetime.now(),
            update_time=datetime.now(),
            delete_time=None,
        )
        db.session.add(character)
        db.session.commit()

        return redirect(url_for('character.index'))


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
