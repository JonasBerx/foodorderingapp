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

    def test_app_exist(self):
        self.assertIsNotNone(app)

    def test_index_page(self):
        response = self.client.get("/")
        data = response.get_data(as_text=True)
        self.assertIn("ᗺOlt Food", data)
        self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()
