import unittest

from dolt import app, db
from dolt.models import Customer


class DoltTestCaseSettings(unittest.TestCase):

    def setUp(self):
        app.config.update(
            TESTING=True,
            SQLALCHEMY_DATABASE_URI="sqlite:///:memory:"
        )
        db.create_all()

        customer = Customer(name="CUS", username="cus")  # noqa
        customer.set_password("123456")

        db.session.add(customer)
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


if __name__ == '__main__':
    unittest.main()
