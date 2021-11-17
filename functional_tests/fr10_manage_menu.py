import unittest

from selenium import webdriver
from selenium.webdriver.common.keys import Keys


class FrManageMenu(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Chrome()

    def test_add_item_valid_name_valid_price(self):
        driver = self.driver
        driver.get("http://127.0.0.1:5000/")
        assert "ᗺolt Food" in driver.title
        driver.get("http://127.0.0.1:5000/login")
        username = driver.find_element_by_id("unm")
        username.send_keys("par")
        password = driver.find_element_by_id("pwd")
        password.send_keys("12345678")
        driver.find_element_by_name("submit").click()
        alert = driver.find_element_by_xpath("/html/body/div[1]")
        assert alert.text == 'Login succeeded'

        driver.get("http://127.0.0.1:5000/partner/menu")
        item_name = driver.find_element_by_id("inm")
        item_name.send_keys("Cookie")
        price = driver.find_element_by_id("price")
        price.send_keys("1.20")
        driver.find_element_by_name("submit").click()

        alert = driver.find_element_by_xpath("/html/body/div[1]")
        assert alert.text == 'Item added'

    def test_add_item_invalid_name_valid_price(self):
        driver = self.driver
        driver.get("http://127.0.0.1:5000/")
        assert "ᗺolt Food" in driver.title
        driver.get("http://127.0.0.1:5000/login")
        username = driver.find_element_by_id("unm")
        username.send_keys("par")
        password = driver.find_element_by_id("pwd")
        password.send_keys("12345678")
        driver.find_element_by_name("submit").click()
        alert = driver.find_element_by_xpath("/html/body/div[1]")
        assert alert.text == 'Login succeeded'

        driver.get("http://127.0.0.1:5000/partner/menu")
        price = driver.find_element_by_id("price")
        price.send_keys("1.20")
        driver.find_element_by_name("submit").click()

        alert = driver.find_element_by_xpath("/html/body/div[1]")
        assert alert.text == 'Invalid input: Please enter a name'


    def test_add_item_valid_name_invalid_price(self):
        driver = self.driver
        driver.get("http://127.0.0.1:5000/")
        assert "ᗺolt Food" in driver.title
        driver.get("http://127.0.0.1:5000/login")
        username = driver.find_element_by_id("unm")
        username.send_keys("par")
        password = driver.find_element_by_id("pwd")
        password.send_keys("12345678")
        driver.find_element_by_name("submit").click()
        alert = driver.find_element_by_xpath("/html/body/div[1]")
        assert alert.text == 'Login succeeded'

        driver.get("http://127.0.0.1:5000/partner/menu")
        item_name = driver.find_element_by_id("inm")
        item_name.send_keys("Cookie")
        driver.find_element_by_name("submit").click()

        alert = driver.find_element_by_xpath("/html/body/div[1]")
        assert alert.text == 'Invalid input: Please enter a valid price'


    def test_add_item_invalid_name_invalid_price(self):
        driver = self.driver
        driver.get("http://127.0.0.1:5000/")
        assert "ᗺolt Food" in driver.title
        driver.get("http://127.0.0.1:5000/login")
        username = driver.find_element_by_id("unm")
        username.send_keys("par")
        password = driver.find_element_by_id("pwd")
        password.send_keys("12345678")
        driver.find_element_by_name("submit").click()
        alert = driver.find_element_by_xpath("/html/body/div[1]")
        assert alert.text == 'Login succeeded'

        driver.get("http://127.0.0.1:5000/partner/menu")
        driver.find_element_by_name("submit").click()

        alert = driver.find_element_by_xpath("/html/body/div[1]")
        assert alert.text == 'Invalid input: Please enter a name'

    def test_update_existing_item_valid_name_valid_price(self):
        driver = self.driver
        driver.get("http://127.0.0.1:5000/")
        assert "ᗺolt Food" in driver.title
        driver.get("http://127.0.0.1:5000/login")
        username = driver.find_element_by_id("unm")
        username.send_keys("par")
        password = driver.find_element_by_id("pwd")
        password.send_keys("12345678")
        driver.find_element_by_name("submit").click()
        alert = driver.find_element_by_xpath("/html/body/div[1]")
        assert alert.text == 'Login succeeded'

        driver.get("http://127.0.0.1:5000/partner/menu/edit/1")
        item_name = driver.find_element_by_id("inm")
        item_name.clear()
        item_name.send_keys("Cookie")
        price = driver.find_element_by_id("price")
        price.clear()
        price.send_keys("1.99")
        driver.find_element_by_name("submit").click()

        alert = driver.find_element_by_xpath("/html/body/div[1]")
        assert alert.text == 'Item updated'

    def test_update_existing_item_invalid_name_valid_price(self):
        driver = self.driver
        driver.get("http://127.0.0.1:5000/")
        assert "ᗺolt Food" in driver.title
        driver.get("http://127.0.0.1:5000/login")
        username = driver.find_element_by_id("unm")
        username.send_keys("par")
        password = driver.find_element_by_id("pwd")
        password.send_keys("12345678")
        driver.find_element_by_name("submit").click()
        alert = driver.find_element_by_xpath("/html/body/div[1]")
        assert alert.text == 'Login succeeded'

        driver.get("http://127.0.0.1:5000/partner/menu/edit/1")
        item_name = driver.find_element_by_id("inm")
        item_name.clear()
        price = driver.find_element_by_id("price")
        price.clear()
        price.send_keys("1.99")
        driver.find_element_by_name("submit").click()

        alert = driver.find_element_by_xpath("/html/body/div[1]")
        assert alert.text == 'Invalid input: Please enter a name'

    def test_update_existing_item_valid_name_invalid_price(self):
        driver = self.driver
        driver.get("http://127.0.0.1:5000/")
        assert "ᗺolt Food" in driver.title
        driver.get("http://127.0.0.1:5000/login")
        username = driver.find_element_by_id("unm")
        username.send_keys("par")
        password = driver.find_element_by_id("pwd")
        password.send_keys("12345678")
        driver.find_element_by_name("submit").click()
        alert = driver.find_element_by_xpath("/html/body/div[1]")
        assert alert.text == 'Login succeeded'

        driver.get("http://127.0.0.1:5000/partner/menu/edit/1")
        item_name = driver.find_element_by_id("inm")
        item_name.clear()
        item_name.send_keys("Cookie")
        price = driver.find_element_by_id("price")
        price.clear()
        driver.find_element_by_name("submit").click()

        alert = driver.find_element_by_xpath("/html/body/div[1]")
        assert alert.text == 'Invalid input: Please enter a valid price'

    def test_update_existing_item_invalid_name_invalid_price(self):
        driver = self.driver
        driver.get("http://127.0.0.1:5000/")
        assert "ᗺolt Food" in driver.title
        driver.get("http://127.0.0.1:5000/login")
        username = driver.find_element_by_id("unm")
        username.send_keys("par")
        password = driver.find_element_by_id("pwd")
        password.send_keys("12345678")
        driver.find_element_by_name("submit").click()
        alert = driver.find_element_by_xpath("/html/body/div[1]")
        assert alert.text == 'Login succeeded'

        driver.get("http://127.0.0.1:5000/partner/menu/edit/1")
        item_name = driver.find_element_by_id("inm")
        item_name.clear()
        price = driver.find_element_by_id("price")
        price.clear()
        driver.find_element_by_name("submit").click()

        alert = driver.find_element_by_xpath("/html/body/div[1]")
        assert alert.text == 'Invalid input: Please enter a name'

    def test_delete_existing_item(self):
        driver = self.driver
        driver.get("http://127.0.0.1:5000/")
        assert "ᗺolt Food" in driver.title
        driver.get("http://127.0.0.1:5000/login")
        username = driver.find_element_by_id("unm")
        username.send_keys("par")
        password = driver.find_element_by_id("pwd")
        password.send_keys("12345678")
        driver.find_element_by_name("submit").click()
        alert = driver.find_element_by_xpath("/html/body/div[1]")
        assert alert.text == 'Login succeeded'

        driver.get("http://127.0.0.1:5000/partner/menu")
        driver.find_element_by_xpath("/html/body/div/ul[2]/li[1]/form/input").click()
        alert = driver.switch_to.alert
        alert.accept()

        alert = driver.find_element_by_xpath("/html/body/div[1]")
        assert alert.text == 'Item deleted'

    def test_delete_non_existing_item(self):
        driver = self.driver
        driver.get("http://127.0.0.1:5000/")
        assert "ᗺolt Food" in driver.title
        driver.get("http://127.0.0.1:5000/login")
        username = driver.find_element_by_id("unm")
        username.send_keys("par")
        password = driver.find_element_by_id("pwd")
        password.send_keys("12345678")
        driver.find_element_by_name("submit").click()
        alert = driver.find_element_by_xpath("/html/body/div[1]")
        assert alert.text == 'Login succeeded'
        driver.get("http://127.0.0.1:5000/partner/menu")
        invalid_post_request = '''var xhr = new XMLHttpRequest();
                xhr.open('POST', 'http://127.0.0.1:5000/partner/menu/delete/99999', false);
                xhr.setRequestHeader(
                    'Content-type', 'application/x-www-form-urlencoded');

                xhr.send();
                return xhr.response;'''
        result = driver.execute_script(invalid_post_request)
        assert "Invalid request: Item does not exist" in result





    def tearDown(self):
        self.driver.close()


if __name__ == "__main__":
    unittest.main()
