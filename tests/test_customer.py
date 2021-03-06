import unittest

from dolt import app, db
from dolt.models import Customer, Partner, Food


class DoltTestCaseCourier(unittest.TestCase):

    def setUp(self):
        app.config.update(
            TESTING=True,
            SQLALCHEMY_DATABASE_URI="sqlite:///:memory:"
        )
        db.create_all()

        customer = Customer(name="CUS", username="cus", address="Earth, the Solar System")  # noqa
        customer.set_password("123456")

        partner1 = Partner(name="Restaurant 1", username="par")  # noqa
        partner1.set_password("12345678")

        food_1 = Food(name="Food 1", restaurant=partner1, price=6.99)
        food_2 = Food(name="Food 2", restaurant=partner1, price=7.99)

        db.session.add_all([customer, partner1, food_1, food_2])
        db.session.commit()

        self.client = app.test_client()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def mock_login(self):
        self.client.post(
            "/login",
            data=dict(
                username="cus",
                password="123456",
            ),
            follow_redirects=True
        )

    def mock_login_partner(self):
        self.client.post(
            "/login",
            data=dict(
                username="par",
                password="12345678"
            ),
            follow_redirects=True
        )

    def test_order_food(self):
        self.mock_login()
        response = self.client.post("/order/new/1", follow_redirects=True)
        data = response.get_data(as_text=True)
        self.assertIn("Order created", data)
        self.assertIn("Restaurant 1", data)
        self.assertIn("Food 1", data)
        self.assertIn("Ongoing", data)

    def test_invalid_order(self):
        self.mock_login()
        response = self.client.post("/order/new/3", follow_redirects=True)
        data = response.get_data(as_text=True)
        self.assertNotIn("Order created", data)
        self.assertIn("Invalid request", data)

    def test_show_order_button_without_login(self):
        response = self.client.get("/", follow_redirects=True)
        data = response.get_data(as_text=True)
        self.assertIn('input class="order"', data)

    def test_login_redirect(self):
        response = self.client.post("/order/new/1", follow_redirects=True)
        data = response.get_data(as_text=True)
        self.assertNotIn("Unauthorized", data)
        self.assertIn("Please login first", data)

    def test_orders_template(self):
        self.mock_login()
        self.client.post("/order/new/1", follow_redirects=True)
        response = self.client.get("/orders", follow_redirects=True)
        data = response.get_data(as_text=True)
        self.assertIn("Restaurant 1", data)
        self.assertIn("Ongoing", data)
        self.assertIn("Food 1", data)

    def test_order_auth_check(self):
        self.mock_login_partner()
        response = self.client.post("/order/new/1", follow_redirects=True)
        data = response.get_data(as_text=True)
        self.assertIn("Invalid request: Unauthorized", data)
        self.assertNotIn("Order created", data)

    def test_orders_auth_check(self):
        self.mock_login_partner()
        response = self.client.get("/orders", follow_redirects=True)
        data = response.get_data(as_text=True)
        self.assertIn("Invalid request: Unauthorized", data)
        self.assertNotIn("Orders List", data)


if __name__ == "__main__":
    unittest.main()
