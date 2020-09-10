from flask import render_template, request, redirect, url_for
from flask_login import current_user, login_required
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import NoResultFound
from werkzeug.exceptions import InternalServerError, BadRequest

from project.app.model import User
from project.app import db
from project.app.main.view import main


@main.route("/users")
@login_required
def users():
    """
    Страница списка с юзерами
    :return:
    """
    users = User.query.all()
    res = {
             'total': len(users),
             'objects': [
               {
                 'id': u.id,
                 'name': u.name,
                 'permission': u.permission,
               } for u in users
             ]
           }
    return render_template('users.html', res=res, perm=current_user.is_permission)


@main.route("/create_user")
@login_required
def create_user():
    """
    Страница создания юзера
    :return:
    """
    if not current_user.is_permission:
        return render_template('login.html', error='Not enough permissions')

    return render_template('edit_user.html')


@main.route('/api/create_user', methods=['POST'])
@login_required
def api_create_user():
    """
    Api создания юзера
    :return:
    """
    name = request.values.get('name', '').strip()
    pwd = request.values.get('password', '')
    permission = bool(request.values.get('permission', False))

    if not name or not pwd:
        return render_template("edit_user.html", error='Fill in all the fields')
    try:
        db.session.add(User(name=name, user_password=pwd, permission=permission))
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        raise InternalServerError()

    return redirect(url_for('main.users'))


# На самом деле должен быть put, но формами его нельзя отправить
@main.route('/api/edit_user', methods=['POST'])
@login_required
def api_edit_user():
    """
    Api редактирования юзера
    :return:
    """
    user_id = request.values.get('id', '')
    name = request.values.get('name', '').strip()
    pwd = request.values.get('password', '')
    permission = bool(request.values.get('permission', False))

    if not current_user.is_permission:
        return render_template('login.html', error='Not enough permissions')

    try:
        u = User.query.filter(
            User.id == user_id,
            ).one()
    except NoResultFound as ex:
        return redirect(url_for('main.users'))

    if name:
        u.name = name
    if pwd:
        u.user_password = pwd
    u.permission = permission
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        raise InternalServerError()

    return redirect(url_for('main.users'))


@main.route('/edit/<user_id>')
@login_required
def page_edit_user(user_id: int):
    """
    Стрница редактирования юзера
    :param user_id:
    :return:
    """
    if not current_user.is_permission:
        return render_template('login.html', error='Not enough permissions')

    try:
        u = User.query.filter(
            User.id == user_id,
            ).one()
    except NoResultFound as ex:
        return redirect(url_for('main.users'))

    return render_template('edit_user.html', id=u.id, name=u.name, permission='checked' if u.permission else '')


# На самом деле должен быть delete, но формами его нельзя отправить
# Так же удалять юзера полностью плоззая практика, но в задание написано так
@main.route('/delete/<user_id>', methods=['POST'])
@login_required
def delete_user(user_id):
    """
    Api удаления юзера
    :param user_id:
    :return:
    """
    if not current_user.is_permission:
        return render_template('login.html', error='Not enough permissions')

    if str(current_user.id) == user_id:
        return BadRequest('You can\'t delete yourself')

    try:
        User.query.filter(
            User.id == user_id,
            ).one()
    except NoResultFound as ex:
        return redirect(url_for('main.users'))

    db.session.execute(f'DELETE FROM users WHERE ID = {user_id}')
    db.session.commit()

    return redirect(url_for('main.users'))
