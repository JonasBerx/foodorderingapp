from typing import Optional, Tuple

from flask import flash, redirect, render_template, url_for
from flask_login import current_user, login_required

from dolt import app, db
from dolt.models import Order


def check_order_authentication(order_id: int) -> Tuple[bool, Optional[Order]]:
    the_order = Order.query.filter(Order.id == order_id).first()  # noqa

    if not the_order:
        flash("Invalid request: Item does not exist")
        return False, None
    elif the_order.courier != current_user:
        flash("Invalid request: Unauthorized")
        return False, None

    return True, the_order


@app.route("/courier")
@login_required
def courier():
    if current_user.type != "courier":
        return redirect(url_for("index"))

    return render_template("dashboards/courier/index.html")


@app.route("/courier/missions", methods=["GET"])
@login_required
def missions():
    if current_user.type != "courier":
        return redirect(url_for("index"))

    return render_template("dashboards/courier/missions.html")


@app.route("/courier/missions/<int:order_id>/accept", methods=["POST"])
@login_required
def accept_mission(order_id: id):
    if current_user.type != "courier":
        return redirect(url_for("index"))

    auth, the_order = check_order_authentication(order_id)

    if not auth:
        return redirect(url_for("missions"))

    the_order.status = "delivering"
    db.session.commit()

    flash("Mission Accepted successfully")
    flash(f"Pick up {the_order.foods[0].name} from {the_order.restaurant.name}")

    return redirect(url_for("missions"))


@app.route("/courier/missions/<int:order_id>/reject", methods=["POST"])
@login_required
def reject_mission(order_id: id):
    if current_user.type != "courier":
        return redirect(url_for("index"))

    auth, the_order = check_order_authentication(order_id)

    if not auth:
        return redirect(url_for("missions"))

    the_order = Order.query.filter(Order.id == order_id).first()

    if not the_order:
        flash("Invalid request: Item does not exist")
        return redirect(url_for("missions"))
    elif the_order.courier != current_user:
        flash("Invalid request: Unauthorized")
        return redirect(url_for("missions"))

    the_order.courier_id = None
    db.session.commit()
    flash("Mission Rejected successfully")

    return redirect(url_for("missions"))


@app.route("/courier/session/start", methods=["POST"])
@login_required
def start_new_session():
    if current_user.type != "courier":
        return redirect(url_for("index"))

    current_user.start_session()
    db.session.commit()
    flash("Session Started Successfully")

    return redirect(url_for("courier"))


@app.route("/courier/session/end", methods=["POST"])
@login_required
def end_current_session():
    if current_user.type != "courier":
        return redirect(url_for("index"))

    current_user.end_session()
    db.session.commit()
    flash("Session Ended Successfully")

    return redirect(url_for("courier"))
