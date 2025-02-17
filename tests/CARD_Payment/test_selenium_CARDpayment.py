from selenium.webdriver.common.by import By
import time
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class TestSeleniumPayment:
    def __init__(self):
        self.driver = None

    def complete_payment(self, payment_url, setup):
        """Automates the payment process using Selenium."""

        self.driver = setup
        self.driver.get(payment_url)
        wait = WebDriverWait(self.driver, 10)

        time.sleep(3)

        try:
            txn_dropdown = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@id='txnStateDropdownToggle']")))
            txn_dropdown.click()

            dropdown_list = self.driver.find_elements(By.XPATH, "//ul[@id='txnStateDropdownMenu']/li")
            for value in dropdown_list:
                print("Dropdown Option:", value.text)
                if value.text.strip().upper() == "CHARGED":
                    value.click()
                    break
        except Exception as e:
            print("Dropdown selection failed:", e)

        try:
            submit_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@id='submitButton']")))
            submit_button.click()
        except Exception as e:
            print("Submit button issue:", e)

        try:
            success_element = wait.until(
                EC.presence_of_element_located((By.XPATH, "//h1[contains(text(), 'Payment Successful')]")))
            success_message = success_element.text.strip()
            print("Success Message Found:", success_message)
            result = "Payment Successful" in success_message
        except Exception as e:
            print("Payment success message not found!", e)
            print("Page Source:", self.driver.page_source)
            result = False

        return result
