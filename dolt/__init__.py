from flask import Flask

app = Flask(__name__)

from dolt import views
