import json
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from Utilities.configurations import getConfig
from src.helpers.api_requests_wrapper import post_request
from src.helpers.common_verification import verfiy_http_status_code, verify_response_key_should_not_be_none
from src.helpers.payload_manager import payload_create_order


class TestCreateOrder(object):
    config = getConfig()

    def test_create_order_positive(self, api_headers):
        """
        Verify that a valid order is created successfully.
        Expected: 200 OK, valid response body with a non-null 'id'
        """
        response = post_request(url=self.config['API']['endpoint'] + "orders",
                                headers=api_headers,
                                payload=payload_create_order(),
                                in_json=False)

        print("Response Code:", response.status_code)
        print("Response Body:", response.text)

        order_id = response.json()["order_id"]
        with open("order_data.json", "w") as file:
            json.dump({"order_id": order_id}, file)

        verfiy_http_status_code(response_data=response, expect_data=200)
        verify_response_key_should_not_be_none(order_id)
        verify_response_key_should_not_be_none(response.json()["status"])
        assert "CREATED" in response.text, "Expected 'CREATED' in response!"

    def test_create_order_missing_fields_negative(self, api_headers):
        """
        Verify API behavior when required fields are missing.
        Expected: 400 Bad Request, error message related to missing fields.
        """
        response = post_request(
            url=self.config['API']['endpoint'] + "orders",
            headers=api_headers,
            payload={}, in_json=False
        )

        print("Response Code:", response.status_code)
        print("Response Body:", response.text)

        verfiy_http_status_code(response, 400)
        assert "order_id is missing" in response.text, "Expected 'error_message:order_id is missing' in response!"

    def test_create_order_negative_amount_value_negative(self, api_headers):
        """
        Verify API response when an invalid amount format is provided.
        Expected: 400 Bad Request, validation error for 'negative amount'
        """
        invalid_payload = payload_create_order()
        invalid_payload["amount"] = -123456988

        response = post_request(
            url=self.config['API']['endpoint'] + "orders",
            headers=api_headers,
            payload=invalid_payload, in_json=False
        )

        print("Response Code:", response.status_code)
        print("Response Body:", response.text)

        verfiy_http_status_code(response, 400)
        assert "Invalid input data" in response.text, "Expected validation error for amount!"

    def test_create_order_zero_amount_value_negative(self, api_headers):
        """
        Verify API response when an zero amount value is provided.
        Expected: 400 Bad Request, validation error for 'zero amount'
        """
        invalid_payload = payload_create_order()
        invalid_payload["amount"] = 0

        response = post_request(
            url=self.config['API']['endpoint'] + "orders",
            headers=api_headers,
            payload=invalid_payload, in_json=False
        )

        print("Response Code:", response.status_code)
        print("Response Body:", response.text)

        verfiy_http_status_code(response, 400)
        assert "Invalid input data" in response.text, "Expected validation error for amount!"

    def test_create_order_unauthorized_negative(self, api_headers):
        """
        Verify API response when authorization is missing.
        Expected: 403 Unauthorized, error message.
        """
        response = post_request(
            url=self.config['API']['endpoint'] + "orders",
            headers={},
            payload=payload_create_order(), in_json=False
        )

        print("Response Code:", response.status_code)
        print("Response Body:", response.text)

        verfiy_http_status_code(response, 403)
        assert "Forbidden. No valid API key or client auth token is present in Authorization header or " \
               "client_auth_token query parameter" in response.text, "Expected 'Unauthorized' " \
                                                                                          "response!"
