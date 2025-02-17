import json
import os
import sys
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from Utilities.configurations import getConfig
from src.helpers.api_requests_wrapper import post_request
from src.helpers.common_verification import verfiy_http_status_code, verify_response_key_should_not_be_none
from src.helpers.payload_manager import payload_create_customer


class TestCreateCustomer:
    config = getConfig()

    def test_create_customer_positive(self, api_headers):
        """
        Verify that a valid customer is created successfully.
        Expected: 200 OK, valid response body with a non-null 'id'
        """
        response = post_request(url=self.config['API']['endpoint'] + "customers",
                                headers=api_headers,
                                payload=payload_create_customer(),
                                in_json=False)

        print("Response Code:", response.status_code)
        print("Response Body:", response.text)

        customer_id = response.json()["id"]
        mobile_number = response.json()["mobile_number"]
        email_address = response.json()["email_address"]
        last_name = response.json()["last_name"]
        with open("customer_data.json", "w") as file:
            json.dump({"customer_id": customer_id,"mobile_number": mobile_number,"email_address": email_address,"last_name":last_name}, file)

        verfiy_http_status_code(response_data=response, expect_data=200)
        verify_response_key_should_not_be_none(customer_id)

    def test_create_customer_missing_fields_negative(self, api_headers):
        """
        Verify API behavior when required fields are missing.
        Expected: 400 Bad Request, error message related to missing fields.
        """
        response = post_request(
            url=self.config['API']['endpoint'] + "customers",
            headers=api_headers,
            payload={}, in_json=False
        )

        print("Response Code:", response.status_code)
        print("Response Body:", response.text)

        verfiy_http_status_code(response, 400)
        assert "error_message" in response.json(), "Expected 'error_message' in response!"

    def test_create_customer_invalid_mobile_number_negative(self, api_headers):
        """
        Verify API response when an invalid mobile number is provided.
        Expected: 400 Bad Request, validation error for 'mobile_number'
        """
        invalid_payload = payload_create_customer()
        invalid_payload["mobile_number"] = "ABC123"  # Invalid mobile number format

        response = post_request(
            url=self.config['API']['endpoint'] + "customers",
            headers=api_headers,
            payload=invalid_payload, in_json=False
        )

        print("Response Code:", response.status_code)
        print("Response Body:", response.text)

        verfiy_http_status_code(response, 400)
        assert "Wrong value in mobile_number" in response.text, "Expected validation error for mobile number!"

    def test_create_customer_invalid_email_format_negative(self, api_headers):
        """
        Verify API response when an invalid email format is provided.
        Expected: 400 Bad Request, validation error for 'email_address'
        """
        invalid_payload = payload_create_customer()
        invalid_payload["email_address"] = 1234569887  # Invalid email format

        response = post_request(
            url=self.config['API']['endpoint'] + "customers",
            headers=api_headers,
            payload=invalid_payload, in_json=False
        )

        print("Response Code:", response.status_code)
        print("Response Body:", response.text)

        verfiy_http_status_code(response, 400)
        assert "Invalid value passed, expected String" in response.text, "Expected validation error for email!"

    def test_create_customer_unauthorized_negative(self, api_headers):
        """
        Verify API response when authorization is missing.
        Expected: 403 Unauthorized, error message.
        """
        response = post_request(
            url=self.config['API']['endpoint'] + "customers",
            headers={},
            payload=payload_create_customer(), in_json=False
        )

        print("Response Code:", response.status_code)
        print("Response Body:", response.text)

        verfiy_http_status_code(response, 403)
        assert "Forbidden. API key not present in Authorization header" in response.text, "Expected 'Unauthorized' " \
                                                                                          "response!"
