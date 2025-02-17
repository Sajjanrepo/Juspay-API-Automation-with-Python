from selenium.webdriver.common.by import By
import time
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class TestSeleniumUPIPayment:
    def __init__(self):
        self.driver = None

    def complete_UPI_payment(self, payment_url, setup):
        """Automates the UPI payment process using Selenium."""

        self.driver = setup
        self.driver.get(payment_url)
        wait = WebDriverWait(self.driver, 10)

        try:
            success_key = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@value='SUCCESS']")))
            success_key.click()
        except Exception as e:
            print("Payment success button not found!", e)

        try:
            success_element = wait.until(
                EC.presence_of_element_located((By.XPATH, "//h1[normalize-space()='Payment Successful']")))
            success_message = success_element.text.strip()
            print("Success Message Found:", success_message)
            result = "Payment Successful" in success_message
        except Exception as e:
            print("Payment success message not found!", e)
            print("Page Source:", self.driver.page_source)
            result = False

        return result
