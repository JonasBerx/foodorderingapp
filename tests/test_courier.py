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


if __name__ == '__main__':
    unittest.main()
