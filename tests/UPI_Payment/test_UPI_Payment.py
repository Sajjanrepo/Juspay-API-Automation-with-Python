import json
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from Utilities.configurations import getConfig
from src.helpers.api_requests_wrapper import post_request
from src.helpers.common_verification import verfiy_http_status_code, verify_response_key_should_not_be_none
from src.helpers.payload_manager import payload_UPI_Payment


class TestPaymentViaUPI:
    config = getConfig()

    def test_txn_via_UPI_positive(self, api_headers):
        """
        Verify that a valid txns via card is created successfully.
        Expected: 200 OK, valid response body with a non-null 'id'
        """
        response = post_request(url=self.config['API']['endpoint'] + "txns",
                                headers=api_headers,
                                payload=payload_UPI_Payment(),
                                in_json=False)

        print("Response Code:", response.status_code)
        print("Response Body:", response.text)

        if response.status_code == 200:
            payment_url = response.json()["payment"]["authentication"]["url"]
            with open("UPItxn_data.json", "w") as file:
                json.dump({"payment_url": payment_url}, file)
        else:
            raise Exception(f"Payment initiation failed: {response.text}")

        verify_response_key_should_not_be_none(payment_url)
        verify_response_key_should_not_be_none(response.json()["status"])
        assert "PENDING_VBV" in response.text, "Expected 'status:PENDING_VBV' in response!"

    def test_txn_via_UPI_missing_fields_negative(self, api_headers):
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
        assert "MISSING_MANDATORY_PARAMETER" in response.text, "Expected 'error_message:order_id is missing' in " \
                                                               "response!"

    def test_txn_via_UPI_InvalidUPI_ID_negative(self, api_headers):
        """
        Verify API response when an invalid card number format is provided.
        Expected: 400 Bad Request, validation error for 'invalid upi id'
        """
        invalid_payload = payload_UPI_Payment()
        invalid_payload["upi_vpa"] = -12345698

        response = post_request(
            url=self.config['API']['endpoint'] + "txns",
            headers=api_headers,
            payload=invalid_payload, in_json=False
        )

        print("Response Code:", response.status_code)
        print("Response Body:", response.text)

        verfiy_http_status_code(response, 400)
        assert "INVALID_INPUT" in response.text, "Expected validation error for wrong UPI id"

