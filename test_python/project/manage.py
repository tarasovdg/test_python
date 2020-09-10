from project.app import create_app
from flask_login import LoginManager
from project.app.model import User

app = create_app()


def get_user(user_id):
    return User.query.filter(
        User.id == user_id,
        ).one()


def setup_login_manager(app):
    login_manager = LoginManager(app)
    login_manager.login_view = 'main.page_login'
    login_manager.init_app(app)
    login_manager.user_loader(get_user)

setup_login_manager(app)
