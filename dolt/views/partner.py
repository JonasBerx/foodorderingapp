from typing import Optional, Tuple

from flask import flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from dolt import app, db
from dolt.models import Food
from dolt.utils import get_float


def check_food_authentication(food_id: int) -> Tuple[bool, Optional[Food]]:
    food = Food.query.filter(Food.id == food_id).first()  # noqa

    if not food:
        flash("Invalid request: Item does not exist")
        return False, None
    elif food.restaurant != current_user:
        flash("Invalid request: Unauthorized")
        return False, None

    return True, food


@app.route("/partner")
@login_required
def partner():
    if current_user.type != "partner":
        return redirect(url_for("index"))

    return render_template("dashboards/partner/index.html")


@app.route("/partner/menu", methods=["GET", "POST"])
@login_required
def partner_menu():
    if current_user.type != "partner":
        return redirect(url_for("index"))

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
    if current_user.type != "partner":
        return redirect(url_for("index"))

    auth, food = check_food_authentication(food_id)

    if not auth:
        return redirect(url_for("partner_menu"))

    db.session.delete(food)
    db.session.commit()
    flash("Item deleted")
    return redirect(url_for("partner_menu"))


@app.route("/partner/menu/edit/<int:food_id>", methods=["GET", "POST"])
@login_required
def partner_menu_edit(food_id: int):
    if current_user.type != "partner":
        return redirect(url_for("index"))

    auth, food = check_food_authentication(food_id)

    if not auth:
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
