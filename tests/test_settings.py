import unittest

from dolt import app, db
from dolt.models import Courier, Customer


class DoltTestCaseSettings(unittest.TestCase):

    def setUp(self):
        app.config.update(
            TESTING=True,
            SQLALCHEMY_DATABASE_URI="sqlite:///:memory:"
        )
        db.create_all()

        courier = Courier(name="COU", username="cou") # noqa
        courier.set_password("12345")
        customer = Customer(name="CUS", username="cus")  # noqa
        customer.set_password("123456")

        db.session.add_all([courier, customer])
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

    def mock_login_role(self):
        self.client.post(
            "/login",
            data=dict(
                username="cou",
                password="12345",
            ),
            follow_redirects=True
        )

    def test_settings(self):
        self.mock_login()

        response = self.client.get("/settings")
        data = response.get_data(as_text=True)
        self.assertIn("Settings", data)
        self.assertIn("Your Name", data)

        response = self.client.post(
            "/settings",
            data=dict(
                name="Example Name"
            ),
            follow_redirects=True
        )
        data = response.get_data(as_text=True)
        self.assertIn("Settings saved", data)
        self.assertIn("Example Name", data)

        response = self.client.post(
            "/settings",
            data=dict(
                name=""
            ),
            follow_redirects=True
        )
        data = response.get_data(as_text=True)
        self.assertNotIn("Settings saved", data)
        self.assertIn("Input invalid: Please enter a name", data)

        response = self.client.post(
            "/settings",
            data=dict(
                name="a" * 33
            ),
            follow_redirects=True
        )
        data = response.get_data(as_text=True)
        self.assertNotIn("Settings saved", data)
        self.assertIn("Input invalid: the name must be at most 32 characters long", data)

    def test_settings_role(self):
        self.mock_login_role()

        response = self.client.post(
            "/settings",
            data=dict(
                name="Example Name"
            ),
            follow_redirects=True
        )
        data = response.get_data(as_text=True)
        self.assertIn("Settings saved", data)
        self.assertIn("Example Name", data)
        self.assertIn("Welcome, dear courier Example Name!", data)


if __name__ == '__main__':
    unittest.main()
