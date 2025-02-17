import json
import os

from tests.test_Payment_via_CARD import TestPaymentViaCard
from tests.test_selenium_CARDpayment import TestSeleniumPayment


class TestPayment:

    def test_card_payment(self, setup, api_headers):
        """End-to-end test: API initiates payment, Selenium completes it, API verifies success."""

        # Step 1: API initiates payment
        self.payment_requests = TestPaymentViaCard()
        self.payment_requests.test_txn_via_CARD_positive(api_headers)
        file_path = os.path.join(os.path.dirname(__file__), "..", "txn_data.json")
        with open(file_path, "r") as file:
            data = json.load(file)
            payment_url = data["payment_url"]

        # Step 2: Selenium completes payment
        self.selenium_payment = TestSeleniumPayment()
        is_successful = self.selenium_payment.complete_payment(payment_url, setup)
        assert is_successful, "Payment failed via UI"
