import os
from sys import platform

from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
prefix = "sqlite:///" if platform.startswith("win") else "sqlite:////"
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "dev")
app.config["SQLALCHEMY_DATABASE_URI"] = f"{prefix}{os.path.join(app.root_path, 'data.db')}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
login_manager = LoginManager(app)


@login_manager.user_loader
def load_user(user_id):
    from dolt.models import User
    user = User.query.get(int(user_id))
    return user

from dolt import commands, models, views # noqa
