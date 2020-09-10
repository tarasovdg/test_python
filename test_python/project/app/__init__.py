import secrets
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from werkzeug.wrappers import Request

db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    app.config.from_object("project.app.config.Config")
    app.secret_key = secrets.token_urlsafe(32)
    db.init_app(app)

    from project.app.main import main
    app.register_blueprint(main)

    return app


