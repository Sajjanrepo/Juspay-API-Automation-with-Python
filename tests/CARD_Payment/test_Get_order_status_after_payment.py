import json
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from Utilities.configurations import getConfig
from src.helpers.api_requests_wrapper import get_request
from src.helpers.common_verification import verfiy_http_status_code, verify_response_key


class TestAfterPaymentStatus:
    config = getConfig()

    def test_AfterPaymentStatus_positive(self, api_headers):
        """
        Verify that a valid txns via card is created successfully.
        Expected: 200 OK, valid response body with a non-null 'id'
        """
        file_path = os.path.join(os.path.dirname(__file__), "..", "order_data.json")
        with open(file_path, "r") as file:
            data = json.load(file)
            order_id = data["order_id"]

        response = get_request(url=self.config['API']['endpoint'] + "orders/" + f"{order_id}",
                               headers=api_headers
                               )
        print(response)
        print("Response Code:", response.status_code)
        print("Response Body:", response.text)

        order_id_resp = response.json()["order_id"]
        payment_status = response.json()["status"]
        verfiy_http_status_code(response_data=response, expect_data=200)
        verify_response_key(order_id_resp, order_id)
        verify_response_key(payment_status, "CHARGED")
        assert "CHARGED" in response.text, "Expected 'status:CHARGED' in response!"
