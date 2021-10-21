import unittest

from dolt import app, db
from dolt.models import Partner, Food


class DoltTestCasePartner(unittest.TestCase):

    def setUp(self):
        app.config.update(
            TESTING=True,
            SQLALCHEMY_DATABASE_URI="sqlite:///:memory:"
        )
        db.create_all()

        partner1 = Partner(name="Restaurant 1", username="par")  # noqa
        partner1.set_password("12345678")

        food_1 = Food(name="Food 1", restaurant=partner1)
        food_2 = Food(name="Food 2", restaurant=partner1)

        partner2 = Partner(name="Restaurant 2", username="par2")  # noqa
        partner2.set_password("12345678")

        food_a = Food(name="Food A", restaurant=partner2)
        food_b = Food(name="Food B", restaurant=partner2)

        db.session.add_all([partner1, partner2, food_1, food_2, food_a, food_b])
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

    def test_index_restaurants(self):
        response = self.client.get("/")
        data = response.get_data(as_text=True)
        self.assertIn("ᗺolt Food", data)
        self.assertIn("Restaurant 1", data)
        self.assertIn("Food 1", data)
        self.assertIn("Food 2", data)
        self.assertIn("Restaurant 2", data)
        self.assertIn("Food A", data)
        self.assertIn("Food B", data)
        self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()
