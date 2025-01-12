1. Install Necessary Dependencies
Make sure you have the necessary Python libraries installed for the tests. Run the following commands in your terminal:

bash
Copy code
pip install selenium
pip install html-testRunner
These dependencies will help you run the unit tests using Selenium for web automation and generate test reports.

2. Files to be Executed
input.py: This file is used to test the login functionality with valid credentials as well as edge cases like invalid credentials, password errors, and any other login-related scenarios.

To run this test, execute the following in your terminal:

bash
Copy code
python input.py
cartest.py: This script tests various cart-related functionalities. It ensures the cart behaves correctly, including edge cases like empty carts, adding/removing items, and handling bugs that may arise during cart operations.

To execute this file:

bash
Copy code
python cartest.py
checkout.py: This script tests the checkout process. It covers edge cases such as trying to checkout with an empty cart, missing payment details, or any other issues that may arise during the checkout process.

Run this script as follows:

bash
Copy code
python checkout.py
3. Test Report Generation
The tests will generate reports through html-testRunner. Make sure your test suite is set up to include this report generation, which can be referenced in the README file for easy access and tracking.
