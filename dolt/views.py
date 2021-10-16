from flask import flash, redirect, render_template, request, url_for
from flask_login import login_user, login_required, logout_user

from dolt import app
from dolt.models import User


@app.route("/")
def index():
    return render_template("index.html"), 200


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        # Get form data
        username = request.form["username"]
        password = request.form["password"]

        # Get the user
        user = User.query.filter(User.username == username).first()

        # Check password hash
        if user.validate_password(password):
            login_user(user)
            flash("Login succeeded")
            return redirect(url_for("index"))

        # Wrong password
        flash("Invalid username or password")
        return redirect(url_for("login"))

    return render_template("login.html"), 200


@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Logout succeeded")
    return redirect(url_for("index"))
