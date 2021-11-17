import unittest

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException



class FrAcceptDeliveryMission(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Chrome()

    def test_take_unassinged_open_mission(self):
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
                True

        except NoSuchElementException:
            start_session = '''var xhr = new XMLHttpRequest();
                xhr.open('POST', 'http://127.0.0.1:5000/courier/session/start', false);
                xhr.setRequestHeader(
                    'Content-type', 'application/x-www-form-urlencoded');

                xhr.send();
                return xhr.response;'''
            driver.execute_script(start_session)
        driver.get("http://127.0.0.1:5000/courier/missions")
        # We assume that there is open missions
        driver.find_element_by_xpath("/html/body/div/ul/li[5]/form[1]/input").click()
        alert = driver.find_element_by_xpath("/html/body/div[1]")
        assert alert.text == 'Mission Accepted successfully'

    # def test_take_non_existent_mission(self):
    #     driver = self.driver
    #     driver.get("http://127.0.0.1:5000/")
    #     assert "ᗺolt Food" in driver.title
    #     driver.get("http://127.0.0.1:5000/login")
    #     username = driver.find_element_by_id("unm")
    #     username.send_keys("cou")
    #     password = driver.find_element_by_id("pwd")
    #     password.send_keys("12345")
    #     driver.find_element_by_name("submit").click()
    #     alert = driver.find_element_by_xpath("/html/body/div[1]")
    #     assert alert.text == 'Login succeeded'
    #     try:
    #         driver.get("http://127.0.0.1:5000/courier")
    #         if driver.find_element_by_xpath("/html/body/div/div/text()").text == "Session in Progress":
    #             True

    #     except NoSuchElementException:
    #         start_session = '''var xhr = new XMLHttpRequest();
    #             xhr.open('POST', 'http://127.0.0.1:5000/courier/session/start', false);
    #             xhr.setRequestHeader(
    #                 'Content-type', 'application/x-www-form-urlencoded');

    #             xhr.send();
    #             return xhr.response;'''
    #         driver.execute_script(start_session)
    #     driver.get("http://127.0.0.1:5000/courier/missions")
    #     # We assume that there is open missions
    #     non_existent = '''var xhr = new XMLHttpRequest();
    #             xhr.open('POST', 'http://127.0.0.1:5000/courier/missions/99999999/accept', false);
    #             xhr.setRequestHeader(
    #                 'Content-type', 'application/x-www-form-urlencoded');

    #             xhr.send();
    #             return xhr.response;'''
    #     driver.execute_script(non_existent)
    #     alert = driver.find_element_by_xpath("/html/body/div[1]")
    #     assert alert.text == 'Invalid request'

    def tearDown(self):
        self.driver.close()


if __name__ == "__main__":
    unittest.main()
