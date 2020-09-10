from flask import Blueprint
import hashlib

from flask import render_template, request, redirect, url_for
from flask_login import login_user
from sqlalchemy import func
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound

from project.app.model import User
from project.app.main.view import main


@main.route("/")
def page_login():
    """
    Страница логина
    :return:
    """
    return render_template('login.html')


@main.route('/api/signIn', methods=['POST'])
def sign_in():
    """
    Api логина
    :return:
    """
    name = request.values.get('name', '')
    pwd = request.values.get('password', '')

    try:
        u = User.query.filter(
                func.lower(User.name) == name.lower(),
                ).one()
        if u.password != hashlib.md5(pwd.encode('utf-8')).hexdigest():
            raise InvalidRequestError('Password is wrong')
    except MultipleResultsFound as ex:
        return render_template("login.html", error='Internal error')
    except NoResultFound as ex:
        return render_template("login.html", error='No User found')
    except InvalidRequestError as ex:
        return render_template("login.html", error='Password is wrong')

    login_user(u)

    return redirect(url_for('main.users'))
