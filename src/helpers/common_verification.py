def verfiy_http_status_code(response_data, expect_data):
    assert response_data.status_code == expect_data, "Failed ER!=AR"


def verify_response_key_should_not_be_none(key):
    assert key is not None, "Failed - Key is None"
    assert key != "", "Failed - Key is an empty string"


def verify_response(response):
    assert "Created" in response


def verify_response_key(key, expected_data):
    assert key == expected_data

# Common Verfication
# HTTP Status Code
# Headers
# Data Verification
# JSON schema
