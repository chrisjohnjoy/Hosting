from django.test import TestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class HostTest(TestCase):
    
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.implicitly_wait(10)
        self.live_server_url = 'http://127.0.0.1:8000/login/login'

    def tearDown(self):
        self.driver.quit()

    def test_login_page(self):
        driver = self.driver
        driver.get(self.live_server_url)
        driver.maximize_window()
        time.sleep(2)

        username = driver.find_element(By.CSS_SELECTOR,"#id_username")
        password = driver.find_element(By.CSS_SELECTOR, "#id_password")
        submit_button = driver.find_element(By.CSS_SELECTOR, "input[type='submit']")

        username.send_keys('customer1')
        password.send_keys('Admin123@')
        submit_button.click()

       

        time.sleep(2)  
# Logout
        logout_button = driver.find_element(By.CSS_SELECTOR, "#dropdownMenuButton")
        logout_button.click()
        time.sleep(2)  # Wait for dropdown to open

        logout_link = driver.find_element(By.CSS_SELECTOR, "a[href*='logout']")
        logout_link.click()

        time.sleep(2)  # Wait for logout to complete



    def test_phamacist_edit(self):
        driver = self.driver
        driver.get(self.live_server_url)
        driver.maximize_window()
        time.sleep(2)

        username = driver.find_element(By.CSS_SELECTOR,"#id_username")
        password = driver.find_element(By.CSS_SELECTOR, "#id_password")
        submit_button = driver.find_element(By.CSS_SELECTOR, "input[type='submit']")

        username.send_keys('admin')
        password.send_keys('Admin123@')
        submit_button.click()

    
        time.sleep(5) 

    def test_purchase_flow(self):
        driver = self.driver
        driver.get(self.live_server_url)
        driver.maximize_window()
        time.sleep(2)

        # Login as customer1
        username = driver.find_element(By.CSS_SELECTOR, "#id_username")
        password = driver.find_element(By.CSS_SELECTOR, "#id_password")
        submit_button = driver.find_element(By.CSS_SELECTOR, "input[type='submit']")

        username.send_keys('customer1')
        password.send_keys('Admin123@')
        submit_button.click()

        time.sleep(5)  # Wait for login to complete

        # Select medicine from nav bar search for Dolo 650
        search_input = driver.find_element(By.ID, "search-query")

        search_input.send_keys("Dolo 650")
        time.sleep(2)

        # Select Dolo 650 from the dropdown
        search_result = driver.find_element(By.XPATH, "//a[contains(text(), 'Dolo 650 Tablet')]")
        search_result.click()   
        time.sleep(2)

        # Scroll down the page
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)

        # Click add to cart
        add_to_cart_button = driver.find_element(By.CSS_SELECTOR, ".add-to-cart-form button")
        add_to_cart_button.click()
        time.sleep(2)

        # Click cart in nav bar
        cart_button = driver.find_element(By.XPATH, "//a[contains(@href, 'cart')]")
        cart_button.click()
        time.sleep(2)

        # Click checkout
        checkout_button = driver.find_element(By.CLASS_NAME, "btn.btn-primary.btn-lg")
        checkout_button.click()
        time.sleep(2)

        # Click proceed to pay
        # Wait for the "Proceed to Pay" button to be visible
        proceed_to_pay_button = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, "//button[contains(text(), 'Proceed to Pay')]")))
        time.sleep(2)
       

        # Click logout
        logout_button = driver.find_element(By.CSS_SELECTOR, "#dropdownMenuButton")
        logout_button.click()
        time.sleep(2)

        logout_link = driver.find_element(By.CSS_SELECTOR, "a[href*='logout']")
        logout_link.click()

        time.sleep(2)  

    def test_customer_registration(self):
        driver = self.driver
        driver.get(self.live_server_url)
        driver.maximize_window()
        time.sleep(2)

        # Click the dropdown menu
        dropdown_menu = driver.find_element(By.XPATH, "//button[@id='dropdownMenuButton']")
        dropdown_menu.click()

        # Click the customer register link
        customer_register_link = driver.find_element(By.LINK_TEXT, "Customer Register")
        customer_register_link.click()

        # Fill in registration form
        email_field = driver.find_element(By.ID, "id_email")
        email_field.send_keys("test@example.com")

        username_field = driver.find_element(By.ID, "id_username")
        username_field.send_keys("test_user")

        password_field = driver.find_element(By.ID, "id_password1")
        password_field.send_keys("test_password")

        confirm_password_field = driver.find_element(By.ID, "id_password2")
        confirm_password_field.send_keys("test_password")

        name_field = driver.find_element(By.ID, "id_name")
        name_field.send_keys("Test")

        phone_number_field = driver.find_element(By.ID, "id_phone_number")
        phone_number_field.send_keys("1234567890")

        address_field = driver.find_element(By.ID, "id_address")
        address_field.send_keys("123 Test Street")
        time.sleep(3)
        # Click register button
        register_button = driver.find_element(By.XPATH, "//button[@type='submit']")
        register_button.click()

        # Wait for registration to complete
        time.sleep(3)
        dropdown_menu = driver.find_element(By.XPATH, "//button[@id='dropdownMenuButton']")
        dropdown_menu.click()

        # Click the Login link in the dropdown menu
        login_link = driver.find_element(By.LINK_TEXT, "Login")
        login_link.click()

        # Wait for login page to load
        time.sleep(2)

        # Log in using registered credentials
        username_login_field = driver.find_element(By.ID, "id_username")
        username_login_field.send_keys("test_user")

        password_login_field = driver.find_element(By.ID, "id_password")
        password_login_field.send_keys("test_password")

        submit_button = driver.find_element(By.CSS_SELECTOR, "input[type='submit']")
        submit_button.click()
        # Wait for login to complete
        time.sleep(3)

        # Click the dropdown menu again
        dropdown_menu = driver.find_element(By.XPATH, "//button[@id='dropdownMenuButton']")
        dropdown_menu.click()

        # Click logout link
        logout_link = driver.find_element(By.LINK_TEXT, "Logout")
        logout_link.click()

        # Wait for logout to complete
        time.sleep(3)

if __name__ == '__main__':
    import unittest
    unittest.main()
