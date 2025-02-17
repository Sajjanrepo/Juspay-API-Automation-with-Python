import json
import os

from tests.test_UPI_Payment import TestPaymentViaUPI
from tests.test_selenium_UPI_Payment import TestSeleniumUPIPayment


class TestPayment:

    def test_card_payment(self, setup, api_headers):
        """End-to-end test: API initiates payment, Selenium completes it, API verifies success."""

        # Step 1: API initiates payment
        self.payment_requests = TestPaymentViaUPI()
        self.payment_requests.test_txn_via_UPI_positive(api_headers)
        file_path = os.path.join(os.path.dirname(__file__), "..", "UPItxn_data.json")
        with open(file_path, "r") as file:
            data = json.load(file)
            payment_url = data["payment_url"]

        # Step 2: Selenium completes payment
        self.selenium_payment = TestSeleniumUPIPayment()
        is_successful = self.selenium_payment.complete_UPI_payment(payment_url, setup)
        assert is_successful, "Payment failed via UI"
