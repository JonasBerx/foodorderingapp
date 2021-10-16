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

    def test_login(self):
        response = self.client.post("/login", data=dict(
            username="test",
            password="12345678"
        ), follow_redirects=True)
        data = response.get_data(as_text=True)
        self.assertIn("Login succeeded", data)


if __name__ == '__main__':
    unittest.main()
