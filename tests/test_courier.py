import unittest

from dolt import app, db
from dolt.models import Courier, Food,  Customer, Order, Partner


class DoltTestCaseCourier(unittest.TestCase):

    def setUp(self):
        app.config.update(
            TESTING=True,
            SQLALCHEMY_DATABASE_URI="sqlite:///:memory:"
        )
        db.create_all()

        courier = Courier(name="Test Courier", username="cou")  # noqa
        courier.set_password("12345")
        customer = Customer(name="CUS", username="cus", address="Earth, the Solar System")  # noqa
        customer.set_password("123456")

        partner1 = Partner(name="Restaurant 1", username="par")  # noqa
        partner1.set_password("12345678")
        partner2 = Partner(name="Restaurant 2", username="par2")  # noqa
        partner2.set_password("12345678")

        food_a = Food(
            name="Burgers and Chicken",
            restaurant=partner1,
            price=10.99
        )
        food_b = Food(name="Pancakes", restaurant=partner2, price=12.99)

        order1 = Order(
            status="ongoing",
            foods=[food_a],
            customer=customer,
            restaurant=food_a.restaurant
        )
        order1.courier = courier

        order2 = Order(
            status="ongoing",
            foods=[food_b],
            customer=customer,
            restaurant=food_b.restaurant
        )
        order2.courier = courier

        order3 = Order(
            status="finished",
            foods=[food_b],
            customer=customer,
            restaurant=food_b.restaurant
        )
        order3.courier = courier

        db.session.add_all([courier, customer, partner1, partner2,
                            food_a, food_b,
                            order1, order2, order3])
        db.session.commit()

        self.client = app.test_client()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def mock_login_courier(self):
        self.client.post(
            "/login",
            data=dict(
                username="cou",
                password="12345"
            ),
            follow_redirects=True
        )

    def test_a_courier_can_see_their_session_status(self):
        self.mock_login_courier()
        response = self.client.get("/courier")
        data = response.get_data(as_text=True)
        self.assertIn("Welcome, dear courier Test Courier!", data)
        self.assertIn("Not In Session", data)

    def test_a_courier_can_start_a_session(self):
        self.mock_login_courier()
        response = self.client.post(
            "/courier/session/start",
            follow_redirects=True
        )
        data = response.get_data(as_text=True)
        self.assertIn("Session Started Successfully", data)
        self.assertIn("Session in Progress", data)

    def test_a_courier_can_end_a_session(self):
        self.mock_login_courier()
        response = self.client.post(
            "/courier/session/end",
            follow_redirects=True
        )
        data = response.get_data(as_text=True)
        self.assertIn("Session Ended Successfully", data)
        self.assertIn("Not In Session", data)

    def test_a_courier_can_see_the_missions_page(self):
        self.mock_login_courier()
        response = self.client.get("/courier/missions", follow_redirects=True)
        data = response.get_data(as_text=True)
        self.assertIn("Here are your pending missions", data)

    def test_a_courier_can_see_the_missions_assigned_to_him(self):
        self.mock_login_courier()
        response = self.client.get("/courier/missions", follow_redirects=True)
        data = response.get_data(as_text=True)
        self.assertIn("Delivery of Burgers and Chicken", data)
        self.assertIn("Delivery of Pancakes", data)
        self.assertIn("At Restaurant 2", data)
        self.assertIn("At Restaurant 1", data)
        self.assertIn("Accept Mission", data)
        self.assertIn("Reject Mission", data)

    def test_a_courier_can_only_see_the_pending_missions_assigned_to_him(self):
        self.mock_login_courier()
        response = self.client.get("/courier/missions", follow_redirects=True)
        data = response.get_data(as_text=True)
        self.assertNotIn("Finished", data)

    def test_a_courier_can_accept_a_mission(self):
        self.mock_login_courier()
        response = self.client.post(
            "/courier/missions/1/accept",
            follow_redirects=True
        )
        data = response.get_data(as_text=True)
        self.assertIn("Mission Accepted successfully", data)
        self.assertIn("Pick up Burgers and Chicken from Restaurant 1", data)
        self.assertIn("Delivering", data)
        self.assertIn("Order Delivered", data)

    def test_a_courier_cannot_accept_an_invalid_mission(self):
        self.mock_login_courier()
        response = self.client.post(
            "/courier/missions/100/accept",
            follow_redirects=True
        )
        data = response.get_data(as_text=True)
        self.assertIn("Invalid request: Item does not exist", data)
        self.assertIn("Ongoing", data)

    def test_a_courier_can_reject_a_mission(self):
        self.mock_login_courier()
        response = self.client.post(
            "/courier/missions/1/reject",
            follow_redirects=True
        )
        data = response.get_data(as_text=True)
        self.assertIn("Mission Rejected successfully", data)
        self.assertNotIn("Delivery of Burgers and Chicken", data)
        self.assertNotIn("Delivering", data)
        self.assertNotIn("Order Delivered", data)

    def test_a_courier_cannot_reject_an_invalid_mission(self):
        self.mock_login_courier()
        response = self.client.post(
            "/courier/missions/100/reject",
            follow_redirects=True
        )
        data = response.get_data(as_text=True)
        self.assertIn("Invalid request: Item does not exist", data)
        self.assertIn("Ongoing", data)


if __name__ == "__main__":
    unittest.main()
