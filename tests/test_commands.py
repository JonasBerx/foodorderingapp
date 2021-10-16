import unittest

from dolt import app, db
from dolt.commands import mock
from dolt.models import Customer


class DoltTestCaseCommands(unittest.TestCase):

    def setUp(self):
        app.config.update(
            TESTING=True,
            SQLALCHEMY_DATABASE_URI='sqlite:///:memory:'
        )
        self.client = app.test_client()
        self.runner = app.test_cli_runner()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_app_exist(self):
        self.assertIsNotNone(app)

    def test_app_is_testing(self):
        self.assertTrue(app.config["TESTING"])

    def test_mock_command(self):
        result = self.runner.invoke(mock)
        self.assertIn("Mock done", result.output)
        self.assertNotEqual(Customer.query.count(), 0)


if __name__ == '__main__':
    unittest.main()
