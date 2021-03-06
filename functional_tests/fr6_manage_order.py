import unittest

from selenium import webdriver
from selenium.webdriver.common.keys import Keys


class FrManageOrder(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Chrome()

    def test_manage_order_cancel_existing_item(self):
        driver = self.driver
        driver.get("http://127.0.0.1:5000/")
        assert "ᗺolt Food" in driver.title
        driver.get("http://127.0.0.1:5000/login")
        username = driver.find_element_by_id("unm")
        username.send_keys("emp")
        password = driver.find_element_by_id("pwd")
        password.send_keys("1234567")
        driver.find_element_by_name("submit").click()
        alert = driver.find_element_by_xpath("/html/body/div[1]")
        assert alert.text == 'Login succeeded'

        driver.find_element_by_xpath(
            "/html/body/div[2]/ul[1]/li[6]/form/input").click()
        alert = driver.switch_to.alert
        alert.accept()
        alert = driver.find_element_by_xpath("/html/body/div[1]")
        assert alert.text == 'Order cancelled'

    def test_manage_order_cancel_non_existing_item(self):
        driver = self.driver
        driver.get("http://127.0.0.1:5000/")
        assert "ᗺolt Food" in driver.title
        driver.get("http://127.0.0.1:5000/login")
        username = driver.find_element_by_id("unm")
        username.send_keys("emp")
        password = driver.find_element_by_id("pwd")
        password.send_keys("1234567")
        driver.find_element_by_name("submit").click()
        alert = driver.find_element_by_xpath("/html/body/div[1]")
        assert alert.text == 'Login succeeded'

        invalid_post_request = '''var xhr = new XMLHttpRequest();
          xhr.open('POST', 'http://127.0.0.1:5000/employee/cancel/2550', false);
          xhr.setRequestHeader(
              'Content-type', 'application/x-www-form-urlencoded');

          xhr.send('login=test&password=test');
          return xhr.response;'''
        result = driver.execute_script(invalid_post_request)
        assert "Invalid request" in result

    def tearDown(self):
        self.driver.close()


if __name__ == "__main__":
    unittest.main()
