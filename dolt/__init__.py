import os
from sys import platform

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
prefix = "sqlite:///" if platform.startswith("win") else "sqlite:////"
app.config["SQLALCHEMY_DATABASE_URI"] = f"{prefix}{os.path.join(app.root_path, 'data.db')}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

from dolt import views # noqa
