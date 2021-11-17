import unittest

from selenium import webdriver
from selenium.webdriver.common.keys import Keys


class FrLoginLogout(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Chrome()

    def test_valid_inputs(self):
        driver = self.driver
        driver.get("http://127.0.0.1:5000/")
        assert "ᗺolt Food" in driver.title
        driver.get("http://127.0.0.1:5000/login")
        username = driver.find_element_by_id("unm")
        username.send_keys("cus")
        password = driver.find_element_by_id("pwd")
        password.send_keys("123456")
        driver.find_element_by_name("submit").click()
        alert = driver.find_element_by_xpath("/html/body/div[1]")
        assert alert.text == 'Login succeeded'

    def test_invalid_username_valid_password(self):
        driver = self.driver
        driver.get("http://127.0.0.1:5000/")
        assert "ᗺolt Food" in driver.title
        driver.get("http://127.0.0.1:5000/login")
        username = driver.find_element_by_id("unm")
        username.send_keys("cust")
        password = driver.find_element_by_id("pwd")
        password.send_keys("123456")
        driver.find_element_by_name("submit").click()
        alert = driver.find_element_by_xpath("/html/body/div[1]")
        assert alert.text == 'Invalid username or password'

    def test_valid_username_invalid_password(self):
        driver = self.driver
        driver.get("http://127.0.0.1:5000/")
        assert "ᗺolt Food" in driver.title
        driver.get("http://127.0.0.1:5000/login")
        username = driver.find_element_by_id("unm")
        username.send_keys("cus")
        password = driver.find_element_by_id("pwd")
        password.send_keys("1234567")
        driver.find_element_by_name("submit").click()
        alert = driver.find_element_by_xpath("/html/body/div[1]")
        assert alert.text == 'Invalid username or password'

    def test_invalid_username_invalid_password(self):
        driver = self.driver
        driver.get("http://127.0.0.1:5000/")
        assert "ᗺolt Food" in driver.title
        driver.get("http://127.0.0.1:5000/login")
        username = driver.find_element_by_id("unm")
        username.send_keys("cusqwe")
        password = driver.find_element_by_id("pwd")
        password.send_keys("1234567123")
        driver.find_element_by_name("submit").click()
        alert = driver.find_element_by_xpath("/html/body/div[1]")
        assert alert.text == 'Invalid username or password'

    def test_empty_username_empty_password(self):
        driver = self.driver
        driver.get("http://127.0.0.1:5000/")
        assert "ᗺolt Food" in driver.title
        driver.get("http://127.0.0.1:5000/login")
        driver.find_element_by_name("submit").click()
        alert = driver.find_element_by_xpath("/html/body/div[1]")
        assert alert.text == 'Invalid input: Please enter a username'

    def tearDown(self):
        self.driver.close()


if __name__ == "__main__":
    unittest.main()
