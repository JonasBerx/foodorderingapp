import unittest

from dolt import app, db


class DoltTestCasePages(unittest.TestCase):

    def setUp(self):
        app.config.update(
            TESTING=True,
            SQLALCHEMY_DATABASE_URI="sqlite:///:memory:"
        )
        db.create_all()
        db.session.commit()

        self.client = app.test_client()

    def tearDown(self):
        pass

    def test_error_pages(self):
        # 401
        response = self.client.get("/courier")
        data = response.get_data(as_text=True)
        self.assertIn("Unauthorized - 401", data)
        self.assertIn("Go Back", data)
        self.assertEqual(response.status_code, 401)

        # 404
        response = self.client.get("/abracadabra")
        data = response.get_data(as_text=True)
        self.assertIn("Page Not Found - 404", data)
        self.assertIn("Go Back", data)
        self.assertEqual(response.status_code, 404)

    def test_index_page(self):
        response = self.client.get("/")
        data = response.get_data(as_text=True)
        self.assertIn("ᗺolt Food", data)
        self.assertEqual(response.status_code, 200)

    def test_login_page(self):
        response = self.client.get("/login")
        data = response.get_data(as_text=True)
        self.assertIn("Enter your username", data)
        self.assertIn("Enter your password", data)
        self.assertEqual(response.status_code, 200)

    def test_orders_page(self):
        response = self.client.get("/orders")
        self.assertEqual(response.status_code, 401)


if __name__ == '__main__':
    unittest.main()
