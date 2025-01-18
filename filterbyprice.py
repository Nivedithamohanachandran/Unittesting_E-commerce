import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import HtmlTestRunner  # Import HtmlTestRunner for HTML reports
import time

class ProductFilterTests(unittest.TestCase):
    def setUp(self):
        """Set up the web driver and open the application"""
        self.driver = webdriver.Chrome()
        self.driver.get("https://www.saucedemo.com/")  # Update with your website URL
        self.driver.implicitly_wait(5)

    def login(self, username="standard_user", password="secret_sauce"):
        """Helper method to log in to the application"""
        driver = self.driver
        driver.find_element(By.ID, "user-name").send_keys(username)
        driver.find_element(By.ID, "password").send_keys(password)
        driver.find_element(By.ID, "login-button").click()

    def filter_products_by_price(self, reverse=False):
        """Helper method to filter products by price (low to high or high to low)"""
        driver = self.driver
        # Click the sorting dropdown for price
        if reverse:
            driver.find_element(By.XPATH, "//*[contains(text(),'Price (high to low)')]").click()
        else:
            driver.find_element(By.XPATH, "//*[contains(text(),'Price (low to high)')]").click()

    def test_filter_products_by_price(self):
        """Test case to filter products by price in both low to high and high to low order"""
        self.login()  # Log in with default credentials
        
        # Sort products by price low to high
        self.filter_products_by_price(reverse=False)
        time.sleep(2)  # Wait for sorting to take effect
        product_prices = [float(element.text.strip('$')) for element in self.driver.find_elements(By.CLASS_NAME, "inventory_item_price")]
        self.assertEqual(product_prices, sorted(product_prices), "Products are not sorted by price low to high")

        # Reverse sorting (high to low)
        self.filter_products_by_price(reverse=True)
        time.sleep(2)
        product_prices_reverse = [float(element.text.strip('$')) for element in self.driver.find_elements(By.CLASS_NAME, "inventory_item_price")]
        self.assertEqual(product_prices_reverse, sorted(product_prices_reverse, reverse=True), "Products are not sorted by price high to low")

    def tearDown(self):
        """Close the browser after the test"""
        self.driver.quit()

if __name__ == "__main__":
    unittest.main(testRunner=HtmlTestRunner.HTMLTestRunner(output='reports'))  # Generate HTML report
