import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import HtmlTestRunner  # Import HTMLTestRunner for HTML reports
import time

class CheckoutWithEmptyCartTests(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.get("https://www.saucedemo.com/")  # Sauce Labs demo site
        self.driver.implicitly_wait(5)

    def login(self, username="standard_user", password="secret_sauce"):
        driver = self.driver
        driver.find_element(By.ID, "user-name").send_keys(username)  # Enter username
        driver.find_element(By.ID, "password").send_keys(password)  # Enter password
        driver.find_element(By.ID, "login-button").click()  # Click login button

    def go_to_cart(self):
        driver = self.driver
        driver.find_element(By.CLASS_NAME, "shopping_cart_link").click()  # Go to cart
        time.sleep(2)  # Wait for the cart page to load

    def checkout(self):
        driver = self.driver
        driver.find_element(By.ID, "checkout").click()  # Click checkout button
        time.sleep(2)  # Wait for the checkout page to load

    def test_checkout_with_empty_cart(self):
        self.login()  # Log in with default credentials
        self.go_to_cart()  # Navigate to the cart page

        # Ensure that the cart is empty
        empty_cart_message = self.driver.find_element(By.CLASS_NAME, "cart_footer").text
        self.assertEqual(empty_cart_message, "Your cart is empty", "Cart is not empty.")

        # Proceed to checkout
        self.checkout()

        # Check for an error message or indication that the cart is empty
        try:
            error_message = self.driver.find_element(By.CLASS_NAME, "error-message-container").text
            self.assertIn("empty", error_message.lower(), "No error message for empty cart.")
        except:
            # If no error message, assert that the checkout process is blocked (button disabled or not clickable)
            checkout_button_disabled = self.driver.find_element(By.ID, "checkout").get_attribute("disabled")
            self.assertIsNotNone(checkout_button_disabled, "Checkout button is not disabled for empty cart.")

    def tearDown(self):
        self.driver.quit()  # Close the browser after the test

if __name__ == "__main__":
    unittest.main(testRunner=HtmlTestRunner.HTMLTestRunner(output='reports'))  # Generate HTML report