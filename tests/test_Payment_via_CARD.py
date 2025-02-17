import json
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from Utilities.configurations import getConfig
from src.helpers.api_requests_wrapper import post_request
from src.helpers.common_verification import verfiy_http_status_code, verify_response_key_should_not_be_none
from src.helpers.payload_manager import payload_txns_via_card


class TestPaymentViaCard:
    config = getConfig()

    def test_txn_via_CARD_positive(self, api_headers):
        """
        Verify that a valid txns via card is created successfully.
        Expected: 200 OK, valid response body with a non-null 'id'
        """
        response = post_request(url=self.config['API']['endpoint'] + "txns",
                                headers=api_headers,
                                payload=payload_txns_via_card(),
                                in_json=False)

        print("Response Code:", response.status_code)
        print("Response Body:", response.text)

        if response.status_code == 200:
            payment_url = response.json()["payment"]["authentication"]["url"]
            with open("txn_data.json", "w") as file:
                json.dump({"payment_url": payment_url}, file)
        else:
            raise Exception(f"Payment initiation failed: {response.text}")

        verify_response_key_should_not_be_none(payment_url)
        verify_response_key_should_not_be_none(response.json()["status"])
        assert "PENDING_VBV" in response.text, "Expected 'status:PENDING_VBV' in response!"

    def test_txn_via_CARD_missing_fields_negative(self, api_headers):
        """
        Verify API behavior when required fields are missing.
        Expected: 400 Bad Request, error message related to missing fields.
        """
        response = post_request(
            url=self.config['API']['endpoint'] + "txns",
            headers=api_headers,
            payload={}, in_json=False
        )

        print("Response Code:", response.status_code)
        print("Response Body:", response.text)

        verfiy_http_status_code(response, 400)
        assert "MISSING_MANDATORY_PARAMETER" in response.text, "Expected 'error_message:order_id is missing' in response!"

    def test_txn_via_card_invalidcardnumber_negative(self, api_headers):
        """
        Verify API response when an invalid card number format is provided.
        Expected: 400 Bad Request, validation error for 'invalid card number'
        """
        invalid_payload = payload_txns_via_card()
        invalid_payload["card_number"] = "1234569886595698649469499548484545944959654894445488"

        response = post_request(
            url=self.config['API']['endpoint'] + "txns",
            headers=api_headers,
            payload=invalid_payload, in_json=False
        )

        print("Response Code:", response.status_code)
        print("Response Body:", response.text)

        verfiy_http_status_code(response, 400)
        assert "invalid_card_number" in response.text, "Expected validation error for card number!"

    def test_txn_via_card_cardnumber_specialcharacter_negative(self, api_headers):
        """
        Verify API response when an invalid card number format is provided.It contains special character
        Expected: 400 Bad Request, validation error for 'invalid card number'
        """
        invalid_payload = payload_txns_via_card()
        invalid_payload["card_number"] = "123456984@!^&@88"

        response = post_request(
            url=self.config['API']['endpoint'] + "txns",
            headers=api_headers,
            payload=invalid_payload, in_json=False
        )

        print("Response Code:", response.status_code)
        print("Response Body:", response.text)

        verfiy_http_status_code(response, 400)
        assert "Invalid card number. Card number should contain only digits and should pass luhn check." in response.text, "Expected validation error for card number!"

    def test_txn_via_card_expired_card_negative(self, api_headers):
        """
        Verify API response when an invalid expired date is provided.
        Expected: 400 Bad Request, validation error for 'expired card date'
        """
        invalid_payload = payload_txns_via_card()
        invalid_payload["card_exp_year"] = "1288"

        response = post_request(
            url=self.config['API']['endpoint'] + "txns",
            headers=api_headers,
            payload=invalid_payload, in_json=False
        )
        print("Response Code:", response.status_code)
        print("Response Body:", response.text)

        verfiy_http_status_code(response, 400)
        assert "Card expired. Card expiry year/month cannot be less than current year/month." in response.text, "Expected validation error for card expired date!"

    def test_txn_via_card_incorrect_cvv_negative(self, api_headers):
        """
        Verify API response when an incorrect CVV value is provided.
        Expected: 400 Bad Request, validation error for 'incorrect CVV'
        """
        invalid_payload = payload_txns_via_card()
        invalid_payload["card_security_code"] = "-123"

        response = post_request(
            url=self.config['API']['endpoint'] + "txns",
            headers=api_headers,
            payload=invalid_payload, in_json=False
        )

        print("Response Code:", response.status_code)
        print("Response Body:", response.text)

        verfiy_http_status_code(response, 400)
        assert "invalid card cvv." in response.text, "Expected validation error for CVV!"

    def test_txn_via_card_long_cvv_negative(self, api_headers):
        """
        Verify API response when an incorrect CVV value is provided.
        Expected: 400 Bad Request, validation error for 'incorrect CVV'
        """
        invalid_payload = payload_txns_via_card()
        invalid_payload["card_security_code"] = "1234567"

        response = post_request(
            url=self.config['API']['endpoint'] + "txns",
            headers=api_headers,
            payload=invalid_payload, in_json=False
        )

        print("Response Code:", response.status_code)
        print("Response Body:", response.text)

        verfiy_http_status_code(response, 400)
        assert "Invalid card security code. Invalid card security code length for provided card brand." in response.text, "Expected validation error for CVV!"
