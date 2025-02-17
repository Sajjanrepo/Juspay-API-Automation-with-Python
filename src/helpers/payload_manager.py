from src.resources import dynamic_variables
from Utilities.configurations import getConfig
import json
import os


def payload_create_customer():
    payload = {
        "first_name": "John",
        "last_name": dynamic_variables.dynamic_lastname(),
        "object_reference_id": dynamic_variables.dynamic_objectID(),
        "mobile_number": dynamic_variables.dynamic_mobile(),
        "email_address": dynamic_variables.dynamic_email()
    }
    return payload


def payload_create_order():
    file_path = os.path.join(os.path.dirname(__file__), "../..", "customer_data.json")

    with open(file_path, "r") as file:
        data = json.load(file)
        customer_id = data["customer_id"]
        mobile_number = data["mobile_number"]
        email = data["email_address"]
        lastname = data["last_name"]
    payload = {
        "order_id": dynamic_variables.dynamic_orderID(),
        "amount": dynamic_variables.dynamic_amount(),
        "customer_id": customer_id,
        "customer_email": email,
        "customer_phone": mobile_number,
        "product_id": dynamic_variables.dynamic_productID(),
        "gateway_id": "100",
        "billing_address_first_name": "John",
        "billing_address_last_name": lastname,
        "billing_address_city": 'Bangalore',
        "billing_address_state": "Karnataka",
        "billing_address_country": "India",
        "billing_address_postal_code": "506103"
    }

    return payload


def payload_txns_via_card():
    file_path = os.path.join(os.path.dirname(__file__), "../..", "order_data.json")
    config = getConfig()
    with open(file_path, "r") as file:
        data = json.load(file)
        order_id = data["order_id"]

    payload = {
        "order_id": order_id,
        "merchant_id": config['API']['merchantID'],
        "payment_method_type": "CARD",
        "payment_method": "VISA",
        "card_number": config['CARD']['card_number'],
        "card_exp_month": config['CARD']['card_exp_month'],
        "card_exp_year": config['CARD']['card_exp_year'],
        "name_on_card": "John",
        "card_security_code": config['CARD']['card_security_code'],
        "save_to_locker": 'true',
        "tokenize": "true",
        "redirect_after_payment": "true",
        "format": "json"
    }
    return payload
