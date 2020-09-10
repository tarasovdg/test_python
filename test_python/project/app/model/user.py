import hashlib
from sqlalchemy.ext.hybrid import hybrid_property

from project.app import db


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    permission = db.Column(db.Boolean, default=True, nullable=False)

    def __init__(self, name, user_password, permission):
        self.name = name
        self.password = hashlib.md5(user_password.encode()).hexdigest()
        self.permission = permission

    @property
    def is_active(self):
        return True

    def get_id(self):
        return self.id

    @property
    def user_password(self):
        return self.password

    @user_password.setter
    def user_password(self, pwd):
        self.password = hashlib.md5(pwd.encode()).hexdigest()
        return self.id

    @property
    def is_authenticated(self):
        return True

    @hybrid_property
    def is_permission(self):
        return self.permission == True
