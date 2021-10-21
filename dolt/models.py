from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from dolt import db


class User(db.Model, UserMixin):
    type = db.Column(db.String(20))

    __mapper_args__ = {
        "polymorphic_identity": "user",
        'polymorphic_on': type
    }

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32))
    username = db.Column(db.String(16), unique=True)
    password_hash = db.Column(db.String(128))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def validate_password(self, password):
        return check_password_hash(self.password_hash, password)


class Courier(User):
    __mapper_args__ = {
        "polymorphic_identity": "courier",
    }
    id = db.Column(db.Integer, db.ForeignKey("user.id"), primary_key=True)
    session_status = db.Column(db.Enum("0", "1"), nullable=False, server_default="0")
    missions = db.relationship("Order", backref="courier", lazy=True)

    def in_session(self):
        return self.session_status == "1"

    def set_session_status(self, status):
        self.session_status = status

    def start_session(self):
        self.set_session_status("1")
        return self.in_session()

    def end_session(self):
        self.set_session_status("0")
        return self.in_session()


class Customer(User):
    __mapper_args__ = {
        "polymorphic_identity": "customer",
    }
    id = db.Column(db.Integer, db.ForeignKey("user.id"), primary_key=True)
    orders = db.relationship("Order", backref="customer", lazy=True)


class Employee(User):
    __mapper_args__ = {
        "polymorphic_identity": "employee",
    }
    id = db.Column(db.Integer, db.ForeignKey("user.id"), primary_key=True)


class Partner(User):
    __mapper_args__ = {
        "polymorphic_identity": "partner",
    }
    id = db.Column(db.Integer, db.ForeignKey("user.id"), primary_key=True)
    menu = db.relationship("Food", backref="restaurant", lazy=True)
    orders = db.relationship("Order", backref="restaurant", lazy=True)


class Food(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32))
    partner_id = db.Column(db.Integer(), db.ForeignKey("partner.id"))
    order_id = db.Column(db.Integer(), db.ForeignKey("order.id"))


class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32))
    food = db.relationship("Food", backref="order", lazy=True)
    partner_id = db.Column(db.Integer(), db.ForeignKey("partner.id"))
    customer_id = db.Column(db.Integer(), db.ForeignKey("customer.id"))
    courier_id = db.Column(db.Integer(), db.ForeignKey("courier.id"))
