import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import HtmlTestRunner  # Import HtmlTestRunner for HTML reports
import time

class ProductFilterTests(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.get("https://www.saucedemo.com/")  # Update with your website URL
        self.driver.implicitly_wait(5)

    def login(self, username="standard_user", password="secret_sauce"):
        driver = self.driver
        driver.find_element(By.ID, "user-name").send_keys(username)
        driver.find_element(By.ID, "password").send_keys(password)
        driver.find_element(By.ID, "login-button").click()

    def filter_products_alphabetically(self, reverse=False):
        driver = self.driver
        # Assuming there's a button or clickable element for sorting by Name (A to Z)
        if reverse:
            driver.find_element(By.XPATH, "//*[contains(text(),'Name (Z to A)')]").click()
        else:
            driver.find_element(By.XPATH, "//*[contains(text(),'Name (A to Z)')]").click()

    def filter_products_by_price(self, reverse=False):
        driver = self.driver
        # Assuming there's a button or clickable element for sorting by Price (low to high)
        if reverse:
            driver.find_element(By.XPATH, "//*[contains(text(),'Price (high to low)')]").click()
        else:
            driver.find_element(By.XPATH, "//*[contains(text(),'Price (low to high)')]").click()

    def test_filter_products_alphabetically(self):
        self.login()
        self.filter_products_alphabetically()  # Sort alphabetically A-Z
        time.sleep(2)  # Wait for sorting to take effect
        product_names = [element.text for element in self.driver.find_elements(By.CLASS_NAME, "inventory_item_name")]
        self.assertEqual(product_names, sorted(product_names), "Products are not sorted alphabetically A-Z")

        # Reverse sorting (Z-A)
        self.filter_products_alphabetically(reverse=True)
        time.sleep(2)
        product_names_reverse = [element.text for element in self.driver.find_elements(By.CLASS_NAME, "inventory_item_name")]
        self.assertEqual(product_names_reverse, sorted(product_names_reverse, reverse=True), "Products are not sorted alphabetically Z-A")

    def test_filter_products_by_price(self):
        self.login()
        self.filter_products_by_price()  # Sort by price low to high
        time.sleep(2)  # Wait for sorting to take effect
        product_prices = [float(element.text.strip('$')) for element in self.driver.find_elements(By.CLASS_NAME, "inventory_item_price")]
        self.assertEqual(product_prices, sorted(product_prices), "Products are not sorted by price low to high")

        # Reverse sorting (high to low)
        self.filter_products_by_price(reverse=True)
        time.sleep(2)
        product_prices_reverse = [float(element.text.strip('$')) for element in self.driver.find_elements(By.CLASS_NAME, "inventory_item_price")]
        self.assertEqual(product_prices_reverse, sorted(product_prices_reverse, reverse=True), "Products are not sorted by price high to low")

    def tearDown(self):
        self.driver.quit()

if __name__ == "__main__":
    unittest.main(testRunner=HtmlTestRunner.HTMLTestRunner(output='reports'))
