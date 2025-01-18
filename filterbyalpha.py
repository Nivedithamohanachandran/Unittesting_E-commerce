import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import HtmlTestRunner  # Import HtmlTestRunner

class SauceDemoTests(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.get("https://www.saucedemo.com/")
        self.driver.implicitly_wait(5)

    def login(self, username="standard_user", password="secret_sauce"):
        driver = self.driver
        driver.find_element(By.ID, "user-name").send_keys(username)
        driver.find_element(By.ID, "password").send_keys(password)
        driver.find_element(By.ID, "login-button").click()

    def sort_products_alphabetically(self, reverse=False):
        driver = self.driver
        
        # Wait until the sorting dropdown is visible and clickable
        if reverse:
            sort_option = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//*[contains(text(),'Name (Z to A)')]"))
            )
        else:
            sort_option = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//*[contains(text(),'Name (A to Z)')]"))
            )
        
        # Scroll the element into view using JavaScript
        driver.execute_script("arguments[0].scrollIntoView(true);", sort_option)
        time.sleep(1)  # Wait for scroll action to complete

        # Click on the sort option using JavaScript if ActionChains doesn't work
        driver.execute_script("arguments[0].click();", sort_option)

    def test_sort_products_alphabetically(self):
        self.login()  # Log in with default credentials
        
        # Perform sorting in ascending order (A to Z)
        self.sort_products_alphabetically(reverse=False)

        # Perform sorting in descending order (Z to A)
        self.sort_products_alphabetically(reverse=True)

    def tearDown(self):
        self.driver.quit()

if __name__ == "__main__":
    unittest.main(testRunner=HtmlTestRunner.HTMLTestRunner(output='reports'))  # Set up HTML report output