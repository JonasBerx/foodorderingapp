import unittest

from dolt import app, db
from dolt.models import Courier, Customer, Employee, Food, Order, Partner


class DoltTestCaseCourier(unittest.TestCase):

    def setUp(self):
        app.config.update(
            TESTING=True,
            SQLALCHEMY_DATABASE_URI="sqlite:///:memory:"
        )
        db.create_all()

        courier = Courier(name="Homer Simpson", username="cou")  # noqa
        courier.set_password("12345")
        customer = Customer(name="Bart Simpson", username="cus", address="Earth, the Solar System")  # noqa
        customer.set_password("123456")
        employee = Employee(name="Lisa Simpson", username="emp")  # noqa
        employee.set_password("1234567")
        partner = Partner(name="Marge's", username="par")  # noqa
        partner.set_password("12345678")

        food = Food(
            name="Burgers and Chicken",
            restaurant=partner,
            price=10.99
        )

        order = Order(
            status="ongoing",
            foods=[food],
            customer=customer,
            restaurant=food.restaurant
        )
        order.courier = courier

        db.session.add_all([courier, customer, employee, partner,
                            food,
                            order])
        db.session.commit()

        self.client = app.test_client()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def mock_login_employee(self):
        self.client.post(
            "/login",
            data=dict(
                username="emp",
                password="1234567"
            ),
            follow_redirects=True
        )

    def mock_login_courier(self):
        self.client.post(
            "/login",
            data=dict(
                username="cou",
                password="12345"
            ),
            follow_redirects=True
        )

    def test_get_unfinished_orders(self):
        self.mock_login_employee()
        response = self.client.get("/employee")
        data = response.get_data(as_text=True)
        self.assertIn("Welcome, dear employee Lisa Simpson!", data)
        self.assertIn("Marge&#39;s", data)
        self.assertIn("Ongoing", data)
        self.assertIn("Bart Simpson", data)
        self.assertIn("Earth, the Solar System", data)
        self.assertIn("Burgers and Chicken", data)
        self.assertIn("Homer Simpson", data)
        self.assertIn("Cancel", data)

    def test_cancel_order(self):
        self.mock_login_employee()
        response = self.client.post("/employee/cancel/1", follow_redirects=True)
        data = response.get_data(as_text=True)
        self.assertIn("Order cancelled", data)
        self.assertNotIn("Ongoing", data)

    def test_cancel_invalid_order(self):
        self.mock_login_employee()
        response = self.client.post("/employee/cancel/2", follow_redirects=True)
        data = response.get_data(as_text=True)
        self.assertIn("Invalid request: Order does not exist", data)
        self.assertNotIn("Order cancelled", data)

    def test_dashboard_auth_check(self):
        self.mock_login_courier()
        response = self.client.get("/employee", follow_redirects=True)
        data = response.get_data(as_text=True)
        self.assertIn("Invalid request: Unauthorized", data)
        self.assertNotIn("dear employee", data)

    def test_cancel_order_auth_check(self):
        self.mock_login_courier()
        response = self.client.post("/employee/cancel/1", follow_redirects=True)
        data = response.get_data(as_text=True)
        self.assertIn("Invalid request: Unauthorized", data)
        self.assertNotIn("Order cancelled", data)


if __name__ == "__main__":
    unittest.main()
