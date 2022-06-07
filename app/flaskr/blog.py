from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, session
)
from werkzeug.exceptions import abort

from . import model
from sqlalchemy import desc
from datetime import datetime
from flaskr.auth import login_required
from flaskr.db import get_db

bp = Blueprint('blog', __name__)


@bp.route('/')
def index():
    db = get_db()
    characters = db.query(model.Characters).order_by(desc(model.Characters.id))
    print(characters)
    return render_template('blog/index.html', characters=characters)


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
            db = get_db()
            character = model.Characters()
            character.id = None
            character.user_id = session['user_id']
            character.character_name = character_name
            character.player_name = player_name
            character.game_system = "CoC"
            character.prof_img_path = ""
            character.tags = tags
            character.create_time = datetime.now()
            character.update_time = datetime.now()
            character.delete_time = None
            db.add(character)
            db.commit()
            return redirect(url_for('blog.index'))

    return render_template('blog/create.html')


def get_post(id, check_author=True):
    post = get_db().execute(
        'SELECT p.id, title, body, created, author_id, username'
        ' FROM post p JOIN user u ON p.author_id = u.id'
        f' WHERE p.id = {id}'
    ).fetchone()

    if post is None:
        abort(404, f"Post id {id} doesn't exist.")

    if check_author and post['author_id'] != g.user['id']:
        abort(403)

    return post


@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    post = get_post(id)

    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                f"UPDATE post SET title = '{title}', body = '{body}' WHERE id = {id}"
            )
            db.commit()
            return redirect(url_for('blog.index'))

    return render_template('blog/update.html', post=post)


@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    get_post(id)
    db = get_db()
    db.execute(f'DELETE FROM post WHERE id = {id}')
    db.commit()
    return redirect(url_for('blog.index'))
