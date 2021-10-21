from flask import flash, redirect, render_template, request, url_for
from flask_login import current_user, login_user, login_required, logout_user

from dolt import app, db
from dolt.models import User


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/courier")
@login_required
def courier():
    return render_template("dashboards/courier.html")


@app.route("/orders")
@login_required
def orders():
    return render_template("dashboards/customer.html")


@app.route("/employee")
@login_required
def employee():
    return render_template("dashboards/employee.html")


@app.route("/partner")
@login_required
def partner():
    return render_template("dashboards/partner.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method != "POST":
        return render_template("login.html")

    # Get form data
    username = request.form["username"]
    password = request.form["password"]

    # Check input values
    if not username:
        flash("Invalid input: Please enter a username")
        redirect(url_for("login"))
    elif not password:
        flash("Invalid input: Please enter a password")
        redirect(url_for("login"))

    # Get the user
    user = User.query.filter(User.username == username).first()

    # Check password hash
    if not user:
        pass
    elif not user.validate_password(password):
        pass
    elif user.type in {"courier", "employee", "partner"}:
        login_user(user)
        flash("Login succeeded")
        return redirect(url_for(user.type))
    else:
        login_user(user)
        flash("Login succeeded")
        return redirect(url_for("index"))

    # Wrong login info
    flash("Invalid username or password")
    return redirect(url_for("login"))


@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Logout succeeded")
    return redirect(url_for("index"))


@app.route("/settings", methods=["GET", "POST"])
@login_required
def settings():
    if request.method != "POST":
        return render_template("settings.html")

    name = request.form["name"]

    if not name:
        flash("Invalid input: Please enter a name")
        return redirect(url_for("settings"))
    elif len(name) > 32:
        flash("Invalid input: the name must be at most 32 characters long")
        return redirect(url_for("settings"))

    current_user.name = name
    db.session.commit()
    flash("Settings saved")

    if current_user.type == "customer":
        return redirect(url_for("index"))
    else:
        return redirect(url_for(current_user.type))


@app.route("/courier/session/start", methods=["POST"])
@login_required
def start_new_session():
    if current_user.type == "courier":
        current_user.start_session()
        db.session.commit()
        flash("Session Started Successfully")
        return redirect(url_for("courier"))
    else:
        flash("Only courier's can access this route!")
        return redirect(redirect(url_for(current_user.type)))


@app.route("/courier/session/end", methods=["POST"])
@login_required
def end_current_session():
    if current_user.type == "courier":
        current_user.end_session()
        db.session.commit()
        flash("Session Ended Successfully")
        return redirect(url_for("courier"))
    else:
        flash("Only courier's can access this route!")
        return redirect(redirect(url_for(current_user.type)))
