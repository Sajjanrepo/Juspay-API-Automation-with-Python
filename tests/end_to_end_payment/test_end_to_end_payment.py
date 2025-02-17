import pytest
from tests.CARD_Payment.test_create_customer import TestCreateCustomer
from tests.CARD_Payment.test_create_order import TestCreateOrder
from tests.CARD_Payment.test_Get_order_status_before_payment import TestBeforePaymentStatus
from tests.CARD_Payment.test_CARDpayment_complete import TestPayment
from tests.CARD_Payment.test_Get_order_status_after_payment import TestAfterPaymentStatus


@pytest.mark.usefixtures("setup")
class TestSequentialPayments:

    def test_full_payment_flow(self, setup, api_headers):
        """Runs the full payment process in sequence."""

        print("\n🚀 Step 1: Creating Customer")
        customer_test = TestCreateCustomer()
        customer_test.test_create_customer_positive(api_headers)

        print("\n🚀 Step 2: Creating Order")
        order_test = TestCreateOrder()
        order_test.test_create_order_positive(api_headers)

        print("\n🚀 Step 3: Checking Order Status Before Payment")
        before_payment_test = TestBeforePaymentStatus()
        before_payment_test.test_BeforePaymentStatus_positive(api_headers)

        print("\n🚀 Step 4: Processing Payment")
        payment_test = TestPayment()
        payment_test.test_card_payment(setup, api_headers)

        print("\n🚀 Step 5: Checking Order Status After Payment")
        after_payment_test = TestAfterPaymentStatus()
        after_payment_test.test_AfterPaymentStatus_positive(api_headers)

        print("\nAll tests executed successfully!")

