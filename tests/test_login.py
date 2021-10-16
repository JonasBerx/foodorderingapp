import unittest

from dolt import app, db
from dolt.models import User


class DoltTestCaseLogin(unittest.TestCase):

    def setUp(self):
        app.config.update(
            TESTING=True,
            SQLALCHEMY_DATABASE_URI="sqlite:///:memory:"
        )
        db.create_all()

        user = User(name="Test", username="test") # noqa
        user.set_password("12345678")

        db.session.add_all([user])
        db.session.commit()

        self.client = app.test_client()
        self.runner = app.test_cli_runner()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def mock_login(self):
        self.client.post("/login", data=dict(
            username="test",
            password="12345678",
        ), follow_redirects=True)

    def test_login(self):
        response = self.client.post("/login", data=dict(
            username="test",
            password="12345678"
        ), follow_redirects=True)
        data = response.get_data(as_text=True)
        self.assertIn("Login succeeded", data)
        self.assertIn("Logout", data)
        self.assertIn("Settings", data)

        response = self.client.post("/login", data=dict(
            username="test",
            password="87654321"
        ), follow_redirects=True)
        data = response.get_data(as_text=True)
        self.assertNotIn("Login succeeded", data)
        self.assertIn("Invalid username or password", data)

        response = self.client.post("/login", data=dict(
            username="test123",
            password="12345678"
        ), follow_redirects=True)
        data = response.get_data(as_text=True)
        self.assertNotIn("Login succeeded", data)
        self.assertIn("Invalid username or password", data)

        response = self.client.post("/login", data=dict(
            username="",
            password="12345678"
        ), follow_redirects=True)
        data = response.get_data(as_text=True)
        self.assertNotIn("Login succeeded", data)
        self.assertIn("Input invalid: Please enter a username", data)

        response = self.client.post("/login", data=dict(
            username="test",
            password=""
        ), follow_redirects=True)
        data = response.get_data(as_text=True)
        self.assertNotIn("Login succeeded", data)
        self.assertIn("Input invalid: Please enter a password", data)

    def test_logout(self):
        self.mock_login()
        response = self.client.get("/logout", follow_redirects=True)
        data = response.get_data(as_text=True)
        self.assertIn("Logout succeeded", data)


if __name__ == '__main__':
    unittest.main()
