from flask import flash, redirect, render_template, url_for
from flask_login import current_user, login_required

from dolt import app, db
from dolt.models import Order
from dolt.utils import get_unfinished_orders


@app.route("/employee")
@login_required
def employee():
    if current_user.type != "employee":
        return redirect(url_for("index"))

    available_orders = get_unfinished_orders()
    return render_template(
        "dashboards/employee/index.html",
        orders=available_orders
    )


@app.route("/employee/cancel/<int:order_id>", methods=["POST"])
@login_required
def employee_cancel(order_id: int):
    if current_user.type != "employee":
        return redirect(url_for("index"))

    order = Order.query.filter(Order.id == order_id).first()  # noqa

    if not order:
        flash("Invalid request: Order does not exist")
        return redirect(url_for("employee"))

    order.status = "cancelled"
    db.session.commit()
    flash("Order cancelled")

    return redirect(url_for("employee"))
