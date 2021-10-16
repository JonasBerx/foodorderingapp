import unittest

from dolt import app


class DoltTestCasePages(unittest.TestCase):

    def setUp(self):
        app.config.update(
            TESTING=True,
            SQLALCHEMY_DATABASE_URI="sqlite:///:memory:"
        )
        self.client = app.test_client()
        self.runner = app.test_cli_runner()

    def tearDown(self):
        pass

    def test_index_page(self):
        response = self.client.get("/")
        data = response.get_data(as_text=True)
        self.assertIn("ᗺOlt Food", data)
        self.assertEqual(response.status_code, 200)

    def test_login_page(self):
        response = self.client.get("/login")
        data = response.get_data(as_text=True)
        self.assertIn("Enter your username", data)
        self.assertIn("Enter your password", data)
        self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()
