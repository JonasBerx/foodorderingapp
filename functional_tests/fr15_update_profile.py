import unittest

from selenium import webdriver
from selenium.webdriver.common.keys import Keys


class FrUpdateProfile(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Chrome()

    def test_valid_username_update(self):
        driver = self.driver
        driver.get("http://127.0.0.1:5000/login")
        username = driver.find_element_by_id("unm")
        username.send_keys("cus")
        password = driver.find_element_by_id("pwd")
        password.send_keys("123456")
        driver.find_element_by_name("submit").click()
        alert = driver.find_element_by_xpath("/html/body/div[1]")
        assert alert.text == 'Login succeeded'

        driver.get("http://127.0.0.1:5000/settings")
        username = driver.find_element_by_id("unm")
        username.clear()
        username.send_keys("Martin Martinovitsch")
        driver.find_element_by_name("submit").click()
        alert = driver.find_element_by_class_name("alert")
        assert alert.text == 'Settings saved'
        assert driver.find_element_by_tag_name(
            "h3").text == "Welcome, dear customer Martin Martinovitsch!"

    def test_empty_username_update(self):
        driver = self.driver
        driver.get("http://127.0.0.1:5000/login")
        username = driver.find_element_by_id("unm")
        username.send_keys("cus")
        password = driver.find_element_by_id("pwd")
        password.send_keys("123456")
        driver.find_element_by_name("submit").click()
        alert = driver.find_element_by_xpath("/html/body/div[1]")
        assert alert.text == 'Login succeeded'

        driver.get("http://127.0.0.1:5000/settings")
        username = driver.find_element_by_id("unm")
        username.clear()
        driver.find_element_by_name("submit").click()
        alert = driver.find_element_by_class_name("alert")
        assert alert.text == 'Invalid input: Please enter a name'

    def tearDown(self):
        self.driver.close()


if __name__ == "__main__":
    unittest.main()
