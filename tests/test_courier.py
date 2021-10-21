import unittest

from dolt import app, db
from dolt.models import User, Courier


class DoltTestCaseCourier(unittest.TestCase):

    def setUp(self):
        app.config.update(
            TESTING=True,
            SQLALCHEMY_DATABASE_URI="sqlite:///:memory:"
        )
        db.create_all()

        user = User(name="Test", username="test")  # noqa
        user.set_password("12345678")
        courier = Courier(name="COU", username="cou")  # noqa
        courier.set_password("12345")

        db.session.add_all([user, courier])
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

    def test_courier_session_displays_courier_status(self):
        self.mock_login_courier()
        response = self.client.get('/courier')
        data = response.get_data(as_text=True)
        self.assertIn("Welcome, dear courier COU!", data)
        self.assertIn("Session Status: Not In Session", data)


if __name__ == '__main__':
    unittest.main()
