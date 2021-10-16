from flask_login import UserMixin

from dolt import db


class User(db.Model, UserMixin):
    pass
