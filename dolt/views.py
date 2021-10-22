from flask import flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user

from dolt import app, db, login_manager
from dolt.errors import bad_request
from dolt.models import Food, Order, Partner, User
from dolt.utils import get_float


@app.route("/")
def index():
    restaurants = Partner.query.all()
    return render_template("index.html", restaurants=restaurants)


@app.route("/courier")
@login_required
def courier():
    return render_template("dashboards/courier/index.html")


@app.route("/order/new/<int:food_id>", methods=["POST"])
@login_required
def order(food_id: int):
    food = Food.query.filter(Food.id == food_id).first()

    if not food:
        flash("Invalid request")
        return redirect(url_for("index"))

    restaurant = food.restaurant
    new_order = Order(
        status="ongoing",
        customer=current_user,
        restaurant=restaurant,
        foods=[food]
    )
    db.session.add(new_order)
    db.session.commit()
    flash("Order created")
    return redirect(url_for("orders"))


@app.route("/orders")
@login_required
def orders():
    return render_template("dashboards/customer/index.html")


@app.route("/employee")
@login_required
def employee():
    return render_template("dashboards/employee/index.html")


@app.route("/partner")
@login_required
def partner():
    return render_template("dashboards/partner/index.html")


@app.route("/partner/menu", methods=["GET", "POST"])
@login_required
def partner_menu():
    if request.method != "POST":
        return render_template("dashboards/partner/menu.html")

    name = request.form["name"]
    price = get_float(request.form["price"])

    # Check input values
    if not name:
        flash("Invalid input: Please enter a name")
        return redirect(url_for("partner_menu"))
    elif price is None:
        flash("Invalid input: Please enter a valid price")
        return redirect(url_for("partner_menu"))

    food = Food(name=name, price=price, restaurant=current_user)
    db.session.add(food)
    db.session.commit()
    flash("Item added")
    return redirect(url_for("partner_menu"))


@app.route("/partner/menu/delete/<int:food_id>", methods=["POST"])
@login_required
def partner_menu_delete(food_id: int):
    food = Food.query.filter(Food.id == food_id).first()  # noqa

    if not food:
        flash("Invalid request: Item does not exist")
        return redirect(url_for("partner_menu"))
    elif food.restaurant != current_user:
        flash("Invalid request: Unauthorized")
        return redirect(url_for("partner_menu"))

    db.session.delete(food)
    db.session.commit()
    flash("Item deleted")
    return redirect(url_for("partner_menu"))


@app.route("/partner/menu/edit/<int:food_id>", methods=["GET", "POST"])
@login_required
def partner_menu_edit(food_id: int):
    food = Food.query.filter(Food.id == food_id).first()  # noqa

    if not food:
        flash("Invalid request: Item does not exist")
        return redirect(url_for("partner_menu"))
    elif food.restaurant != current_user:
        flash("Invalid request: Unauthorized")
        return redirect(url_for("partner_menu"))

    if request.method != "POST":
        return render_template("dashboards/partner/edit.html", food=food)

    name = request.form["name"]
    price = get_float(request.form["price"])

    # Check input values
    if not name:
        flash("Invalid input: Please enter a name")
        return redirect(url_for("partner_menu_edit", food_id=food.id))
    elif price is None:
        flash("Invalid input: Please enter a valid price")
        return redirect(url_for("partner_menu_edit", food_id=food.id))

    food.name = name
    food.price = price
    db.session.commit()
    flash("Item updated")
    return redirect(url_for("partner_menu"))


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
    current_user.start_session()
    db.session.commit()
    flash("Session Started Successfully")
    return redirect(url_for("courier"))


@app.route("/courier/session/end", methods=["POST"])
@login_required
def end_current_session():
    current_user.end_session()
    db.session.commit()
    flash("Session Ended Successfully")
    return redirect(url_for("courier"))


@login_manager.unauthorized_handler
def unauthorized():
    if request.path.startswith("/employee"):
        return bad_request(None)

    flash("Please login first")
    return redirect("/login")
