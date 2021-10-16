from flask import render_template, request

from dolt import app


@app.route("/")
def index():
    return render_template("index.html"), 200


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        return  # Do login
    else:
        return render_template("login.html"), 200
