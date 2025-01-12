import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import HtmlTestRunner  # Import html-testRunner

class SauceDemoTests(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.get("https://www.saucedemo.com/")
        self.driver.implicitly_wait(5)

    def test_valid_login(self):
        driver = self.driver
        driver.find_element(By.ID, "user-name").send_keys("standard_user")
        driver.find_element(By.ID, "password").send_keys("secret_sauce")
        driver.find_element(By.ID, "login-button").click()
        self.assertIn("Products", driver.page_source, "Login Failed")

    def test_invalid_login(self):
        driver = self.driver
        driver.find_element(By.ID, "user-name").send_keys("invalid_user")
        driver.find_element(By.ID, "password").send_keys("wrong_password")
        driver.find_element(By.ID, "login-button").click()
        self.assertIn("Epic sadface", driver.page_source, "Invalid Login Test Failed")

    def test_missing_username(self):
        driver = self.driver
        driver.find_element(By.ID, "password").send_keys("secret_sauce")
        driver.find_element(By.ID, "login-button").click()
        error_message = driver.find_element(By.CSS_SELECTOR, ".error-message-container").text
        self.assertIn("Username is required", error_message, "Missing Username Test Failed")

    def test_missing_password(self):
        driver = self.driver
        driver.find_element(By.ID, "user-name").send_keys("standard_user")
        driver.find_element(By.ID, "login-button").click()
        error_message = driver.find_element(By.CSS_SELECTOR, ".error-message-container").text
        self.assertIn("Password is required", error_message, "Missing Password Test Failed")

    def tearDown(self):
        self.driver.quit()

if __name__ == "__main__":
    unittest.main(testRunner=HtmlTestRunner.HTMLTestRunner(output='reports'))
