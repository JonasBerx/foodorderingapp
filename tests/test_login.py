import unittest

from dolt import app, db
from dolt.models import User, Courier, Customer, Employee, Partner


class DoltTestCaseLogin(unittest.TestCase):

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
        customer = Customer(name="CUS", username="cus")  # noqa
        customer.set_password("123456")
        employee = Employee(name="EMP", username="emp")  # noqa
        employee.set_password("1234567")
        partner = Partner(name="PAR", username="par")  # noqa
        partner.set_password("12345678")

        db.session.add_all([user, courier, customer, employee, partner])
        db.session.commit()

        self.client = app.test_client()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def mock_login(self):
        self.client.post(
            "/login",
            data=dict(
                username="test",
                password="12345678"
            ),
            follow_redirects=True
        )

    def mock_login_courier(self):
        self.client.post(
            "/login",
            data=dict(
                username="cou",
                password="87654321"
            ),
            follow_redirects=True
        )

    def test_logout_status(self):
        response = self.client.get("/")
        data = response.get_data(as_text=True)
        self.assertNotIn("Logout", data)
        self.assertNotIn("Settings", data)

    def test_logout_status_role(self):
        response = self.client.get("/courier")
        data = response.get_data(as_text=True)
        self.assertNotIn("Logout", data)
        self.assertNotIn("Settings", data)
        self.assertNotIn("Welcome, dear courier!", data)

    def test_login(self):
        # Correct login
        response = self.client.post(
            "/login",
            data=dict(
                username="test",
                password="12345678"
            ),
            follow_redirects=True
        )
        data = response.get_data(as_text=True)
        self.assertIn("Login succeeded", data)
        self.assertIn("Logout", data)
        self.assertIn("Settings", data)

        # Wrong password
        response = self.client.post(
            "/login",
            data=dict(
                username="test",
                password="87654321"
            ),
            follow_redirects=True
        )
        data = response.get_data(as_text=True)
        self.assertNotIn("Login succeeded", data)
        self.assertIn("Invalid username or password", data)

        # User does not exist
        response = self.client.post(
            "/login",
            data=dict(
                username="test123",
                password="12345678"
            ),
            follow_redirects=True
        )
        data = response.get_data(as_text=True)
        self.assertNotIn("Login succeeded", data)
        self.assertIn("Invalid username or password", data)

        # Username is empty
        response = self.client.post(
            "/login",
            data=dict(
                username="",
                password="12345678"
            ),
            follow_redirects=True
        )
        data = response.get_data(as_text=True)
        self.assertNotIn("Login succeeded", data)
        self.assertIn("Invalid input: Please enter a username", data)

        # Password is empty
        response = self.client.post(
            "/login",
            data=dict(
                username="test",
                password=""
            ), follow_redirects=True
        )
        data = response.get_data(as_text=True)
        self.assertNotIn("Login succeeded", data)
        self.assertIn("Invalid input: Please enter a password", data)

    def test_logout(self):
        self.mock_login()
        response = self.client.get("/logout", follow_redirects=True)
        data = response.get_data(as_text=True)
        self.assertIn("Logout succeeded", data)
        self.assertNotIn("Logout</a>", data)
        self.assertNotIn("Settings", data)

    def test_login_role(self):
        # Test different roles' login
        roles = {
            "courier": "12345",
            "customer": "123456",
            "employee": "1234567",
            "partner": "12345678"
        }

        for role in roles:
            response = self.client.post(
                "/login",
                data=dict(
                    username=role[:3],
                    password=roles[role]
                ),
                follow_redirects=True
            )
            data = response.get_data(as_text=True)
            self.assertIn("Login succeeded", data)
            self.assertIn("Logout", data)
            self.assertIn("Settings", data)
            self.assertIn(f"Welcome, dear {role}", data)

            if role == "customer":
                self.assertIn("Orders", data)
                response = self.client.get("/orders")
                data = response.get_data(as_text=True)
                self.assertIn("Orders List", data)
            else:
                self.assertIn("Dashboard", data)

            response = self.client.get("/logout", follow_redirects=True)
            data = response.get_data(as_text=True)
            self.assertIn("Logout succeeded", data)
            self.assertNotIn("Logout</a>", data)
            self.assertNotIn("Settings", data)


if __name__ == '__main__':
    unittest.main()
