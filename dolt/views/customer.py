from flask import flash, redirect, render_template, url_for
from flask_login import current_user, login_required

from dolt import app, db
from dolt.models import Food, Order


@app.route("/order/new/<int:food_id>", methods=["POST"])
@login_required
def order(food_id: int):
    if current_user.type != "customer":
        return redirect(url_for("index"))

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
    if current_user.type != "customer":
        return redirect(url_for("index"))

    return render_template("dashboards/customer/index.html")
