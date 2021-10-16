from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from dolt import db


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32))
    username = db.Column(db.String(16), unique=True)
    password_hash = db.Column(db.String(128))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def validate_password(self, password):
        return check_password_hash(self.password_hash, password)


class Courier(db.Model, UserMixin):
    pass
