import unittest

from selenium import webdriver
from selenium.webdriver.common.keys import Keys


class FrManageMenu(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Chrome()

    def test_existing_item(self):
        driver = self.driver
        driver.get("http://127.0.0.1:5000/")
        assert "ᗺolt Food" in driver.title

    def tearDown(self):
        self.driver.close()


if __name__ == "__main__":
    unittest.main()
