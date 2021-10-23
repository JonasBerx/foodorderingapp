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

        food_1 = Food(name="Food 1", restaurant=partner1, price=6.99)
        food_2 = Food(name="Food 2", restaurant=partner1, price=7.99)

        partner2 = Partner(name="Restaurant 2", username="par2")  # noqa
        partner2.set_password("12345678")

        food_a = Food(name="Food A", restaurant=partner2, price=10.99)
        food_b = Food(name="Food B", restaurant=partner2, price=12.99)

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

    def mock_login_breaker(self):
        self.client.post(
            "/login",
            data=dict(
                username="par2",
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

    def test_add_item(self):
        self.mock_login_partner()

        response = self.client.post(
            "/partner/menu",
            data=dict(
                name="New Food",
                price=11.99
            ),
            follow_redirects=True
        )
        data = response.get_data(as_text=True)
        self.assertIn("Item added", data)
        self.assertIn("New Food", data)

        response = self.client.post(
            "/partner/menu",
            data=dict(
                name="",
                price=11.99
            ),
            follow_redirects=True
        )
        data = response.get_data(as_text=True)
        self.assertNotIn("Item added", data)
        self.assertIn("Invalid input: Please enter a name", data)

        response = self.client.post(
            "/partner/menu",
            data=dict(
                name="New Food",
                price="price?"
            ),
            follow_redirects=True
        )
        data = response.get_data(as_text=True)
        self.assertNotIn("Item added", data)
        self.assertIn("Invalid input: Please enter a valid price", data)

    def test_update_item(self):
        self.mock_login_partner()

        response = self.client.get("/partner/menu/edit/1")
        data = response.get_data(as_text=True)
        self.assertIn("Edit item", data)
        self.assertIn("Food 1", data)
        self.assertIn("6.99", data)

        response = self.client.post(
            "/partner/menu/edit/1",
            data=dict(
                name="New Food 1",
                price=8.99
            ),
            follow_redirects=True
        )
        data = response.get_data(as_text=True)
        self.assertIn("Item updated", data)
        self.assertIn("New Food 1", data)
        self.assertIn("8,99", data)

        response = self.client.post(
            "/partner/menu/edit/1",
            data=dict(
                name="",
                price=8.99
            ),
            follow_redirects=True
        )
        data = response.get_data(as_text=True)
        self.assertNotIn("Item updated", data)
        self.assertIn("Invalid input: Please enter a name", data)

        response = self.client.post(
            "/partner/menu/edit/1",
            data=dict(
                name="Newer Food 1",
                price="price?"
            ),
            follow_redirects=True
        )
        data = response.get_data(as_text=True)
        self.assertNotIn("Item updated", data)
        self.assertNotIn("Newer Food 1", data)
        self.assertIn("Invalid input: Please enter a valid price", data)

    def test_delete_item(self):
        self.mock_login_partner()

        response = self.client.post("/partner/menu/delete/1", follow_redirects=True)
        data = response.get_data(as_text=True)
        self.assertIn("Item deleted", data)
        self.assertNotIn("Food 1", data)

    def test_invalid_management_item_does_not_exist(self):
        self.mock_login_partner()

        response = self.client.post("/partner/menu/edit/8", follow_redirects=True)
        data = response.get_data(as_text=True)
        self.assertNotIn("Edit item", data)
        self.assertIn("Invalid request: Item does not exist", data)

        response = self.client.post("/partner/menu/delete/8", follow_redirects=True)
        data = response.get_data(as_text=True)
        self.assertNotIn("Item deleted", data)
        self.assertNotIn("Page Not Found - 404", data)
        self.assertIn("Invalid request: Item does not exist", data)

    def test_invalid_management_unauthorized(self):
        self.mock_login_breaker()

        response = self.client.post(
            "/partner/menu/edit/1",
            data=dict(
                name="New Food 1",
                price=8.99
            ),
            follow_redirects=True
        )
        data = response.get_data(as_text=True)
        self.assertNotIn("Item updated", data)
        self.assertNotIn("New Food 1", data)
        self.assertNotIn("8,99", data)
        self.assertIn("Invalid request: Unauthorized", data)

        response = self.client.post("/partner/menu/delete/1", follow_redirects=True)
        data = response.get_data(as_text=True)
        self.assertNotIn("Item deleted", data)
        self.assertNotIn("Page Not Found - 404", data)
        self.assertIn("Invalid request: Unauthorized", data)


if __name__ == "__main__":
    unittest.main()
