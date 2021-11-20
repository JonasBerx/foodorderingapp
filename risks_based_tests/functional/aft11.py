import unittest

import chromedriver_binary  # noqa
from selenium import webdriver
from selenium.webdriver.common.by import By


class FrManageMenu(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Chrome()

    def test(self):
        driver = self.driver
        driver.get("http://127.0.0.1:5000/")

        assert "ᗺolt Food" in driver.title

        driver.get("http://127.0.0.1:5000/login")
        username = driver.find_element(By.ID, "unm")
        username.send_keys("cou")
        password = driver.find_element(By.ID, "pwd")
        password.send_keys("12345")
        driver.find_element(By.NAME, "submit").click()
        alert = driver.find_element(By.XPATH, "/html/body/div[1]")

        assert alert.text == "Login succeeded"

        invalid_post_request = """
            var xhr = new XMLHttpRequest();
            xhr.open("POST", "http://127.0.0.1:5000/partner/menu", false);
            xhr.setRequestHeader(
                "Content-type", "application/x-www-form-urlencoded");

            xhr.send();
            return xhr.response;
        """
        result = driver.execute_script(invalid_post_request)
        assert "Invalid request: Unauthorized" in result

    def tearDown(self):
        self.driver.close()


if __name__ == "__main__":
    unittest.main()
