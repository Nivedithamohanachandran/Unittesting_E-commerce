import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import HtmlTestRunner  # Import HtmlTestRunner for HTML reports

class SauceDemoTests(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.get("https://www.saucedemo.com/")
        self.driver.implicitly_wait(5)

    def login(self):
        driver = self.driver
        driver.find_element(By.ID, "user-name").send_keys("standard_user")
        driver.find_element(By.ID, "password").send_keys("secret_sauce")
        driver.find_element(By.ID, "login-button").click()
        time.sleep(2)

    def add_to_cart_and_verify(self):
        driver = self.driver
        driver.find_element(By.CSS_SELECTOR, ".inventory_item:nth-child(1) .btn_inventory").click()
        time.sleep(2)
        driver.get("https://www.saucedemo.com/inventory.html")
        driver.find_element(By.CSS_SELECTOR, ".inventory_item:nth-child(2) .btn_inventory").click()
        time.sleep(2)

        # Verify cart total
        cart_total = driver.find_element(By.CLASS_NAME, "shopping_cart_badge").text
        self.assertEqual(cart_total, "2", "Cart item count mismatch")

        # Open cart and validate items
        driver.find_element(By.CLASS_NAME, "shopping_cart_link").click()
        time.sleep(2)
        items_in_cart = driver.find_elements(By.CLASS_NAME, "cart_item")
        self.assertEqual(len(items_in_cart), 2, "Cart items count mismatch")

    def checkout_with_empty_cart(self):
        driver = self.driver
        driver.find_element(By.CLASS_NAME, "shopping_cart_link").click()
        driver.find_element(By.CLASS_NAME, "checkout_button").click()
        error_message = driver.find_element(By.CLASS_NAME, "error-message-container").text
        self.assertIn("Your cart is empty", error_message, "Empty cart error not displayed")

    def checkout_with_missing_shipping_details(self):
        driver = self.driver
        self.add_to_cart_and_verify()
        driver.find_element(By.CLASS_NAME, "shopping_cart_link").click()
        driver.find_element(By.CLASS_NAME, "checkout_button").click()
        driver.find_element(By.ID, "continue").click()
        error_message = driver.find_element(By.CLASS_NAME, "error-message-container").text
        self.assertIn("Error: First Name is required", error_message, "Missing shipping details error not displayed")

    def checkout_with_valid_shipping_details(self):
        driver = self.driver
        self.add_to_cart_and_verify()
        driver.find_element(By.CLASS_NAME, "shopping_cart_link").click()
        driver.find_element(By.CLASS_NAME, "checkout_button").click()
        driver.find_element(By.ID, "first-name").send_keys("John")
        driver.find_element(By.ID, "last-name").send_keys("Doe")
        driver.find_element(By.ID, "postal-code").send_keys("12345")
        driver.find_element(By.ID, "continue").click()
        time.sleep(2)
        # Verify if the next page is the overview page (checking for Finish button)
        finish_button = driver.find_element(By.ID, "finish")
        self.assertTrue(finish_button.is_displayed(), "Finish button not displayed, checkout incomplete")

    def checkout_with_invalid_payment_details(self):
        driver = self.driver
        self.add_to_cart_and_verify()
        driver.find_element(By.CLASS_NAME, "shopping_cart_link").click()
        driver.find_element(By.CLASS_NAME, "checkout_button").click()
        driver.find_element(By.ID, "first-name").send_keys("John")
        driver.find_element(By.ID, "last-name").send_keys("Doe")
        driver.find_element(By.ID, "postal-code").send_keys("12345")
        driver.find_element(By.ID, "continue").click()
        driver.find_element(By.ID, "finish").click()
        # Invalid payment isn't explicitly simulated, so assuming payment failure message is displayed
        error_message = driver.find_element(By.CLASS_NAME, "error-message-container").text
        self.assertIn("Error: Payment declined", error_message, "Invalid payment details error not displayed")

    def test_cart_functionality(self):
        self.login()
        self.add_to_cart_and_verify()

    def test_missing_shipping_details(self):
        self.login()
        self.checkout_with_missing_shipping_details()

    def test_valid_shipping_details(self):
        self.login()
        self.checkout_with_valid_shipping_details()

    def test_invalid_payment_details(self):
        self.login()
        self.checkout_with_invalid_payment_details()

    def tearDown(self):
        self.driver.quit()

if __name__ == "__main__":
    unittest.main(testRunner=HtmlTestRunner.HTMLTestRunner(output='reports'))
