from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, session
)
from werkzeug.exceptions import abort

from . import model, db
from sqlalchemy import desc
from datetime import datetime
from flaskr.auth import login_required
from flaskr.db import get_db
from flaskr.model import Characters


bp = Blueprint('character', __name__)


@bp.route('/')
def index():
    characters = Characters.query.order_by(desc(model.Characters.id))
    return render_template('character/index.html', characters=characters)


@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        character_name = request.form['character_name']
        player_name = request.form['player_name']
        tags = request.form['tags']
        error = None
        print(session['user_id'])
        if not character_name:
            error = 'character name is required.'

        if error is not None:
            flash(error)
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

    return render_template('character/create.html')


def get_post(id, check_author=True):
    character = Characters.query.filter_by(id=id).first()

    if character is None:
        abort(404, f"Post id {id} doesn't exist.")

    print(character)
    if check_author and character.user_id != str(g.user.id):
        abort(403)

    return character


@ bp.route('/<string:id>/update', methods=('GET', 'POST'))
@ login_required
def update(id):
    character = get_post(id)

    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            character.character_name = title
            character.player_name = body
            db.session.commit()
            return redirect(url_for('character.index'))

    return render_template('character/update.html', post=character)


@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    get_post(id)
    db = get_db()
    db.execute(f'DELETE FROM post WHERE id = {id}')
    db.commit()
    return redirect(url_for('character.index'))
