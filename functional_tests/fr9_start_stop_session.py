import unittest

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException


class FrStartStopSession(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Chrome()

    def test_start_session_successful(self):
        driver = self.driver
        driver.get("http://127.0.0.1:5000/")
        assert "ᗺolt Food" in driver.title
        driver.get("http://127.0.0.1:5000/login")
        username = driver.find_element_by_id("unm")
        username.send_keys("cou")
        password = driver.find_element_by_id("pwd")
        password.send_keys("12345")
        driver.find_element_by_name("submit").click()
        alert = driver.find_element_by_xpath("/html/body/div[1]")
        assert alert.text == 'Login succeeded'
        try:
            driver.get("http://127.0.0.1:5000/courier")
            if driver.find_element_by_xpath("/html/body/div/div/text()").text == "Session in Progress":
                # print("Already in session, stopping session")
                driver.find_element_by_xpath(
                    "/html/body/div[2]/div/form[2]/input").click()

        except NoSuchElementException:
            invalid_post_request = '''var xhr = new XMLHttpRequest();
                xhr.open('POST', 'http://127.0.0.1:5000/courier/session/start', false);
                xhr.setRequestHeader(
                    'Content-type', 'application/x-www-form-urlencoded');

                xhr.send();
                return xhr.response;'''
            result = driver.execute_script(invalid_post_request)
            assert "Session Started Successfully" in result

    def test_stop_session_successful(self):
        driver = self.driver
        driver.get("http://127.0.0.1:5000/")
        assert "ᗺolt Food" in driver.title
        driver.get("http://127.0.0.1:5000/login")
        username = driver.find_element_by_id("unm")
        username.send_keys("cou")
        password = driver.find_element_by_id("pwd")
        password.send_keys("12345")
        driver.find_element_by_name("submit").click()
        alert = driver.find_element_by_xpath("/html/body/div[1]")
        assert alert.text == 'Login succeeded'
        try:
            driver.get("http://127.0.0.1:5000/courier")
            if driver.find_element_by_xpath("/html/body/div/div/text()") == "Not In Session":
                driver.find_element_by_xpath(
                    "/html/body/div[2]/div/form/input").click()
        except NoSuchElementException:
            invalid_post_request = '''var xhr = new XMLHttpRequest();
                xhr.open('POST', 'http://127.0.0.1:5000/courier/session/end', false);
                xhr.setRequestHeader(
                    'Content-type', 'application/x-www-form-urlencoded');

                xhr.send();
                return xhr.response;'''
            result = driver.execute_script(invalid_post_request)
            assert "Session Ended Successfully" in result


def tearDown(self):
    self.driver.close()


if __name__ == "__main__":
    unittest.main()
