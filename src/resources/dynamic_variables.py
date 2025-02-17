import random
import string


def dynamic_objectID():
    objectVar = random.randint(100000, 999999)
    return "object" + str(objectVar)


def dynamic_lastname():
    lastnameVar = ''.join(random.choices(string.ascii_letters, k=7))
    return "Smith" + lastnameVar


def dynamic_email():
    emailVar = ''.join(random.choices(string.ascii_letters, k=6))
    return "John" + emailVar + "@gmail.com"


def dynamic_mobile():
    mobileVar = random.randint(1000000000, 9999999999)
    return str(mobileVar)


def dynamic_amount():
    amountVar = random.randint(100000, 999999)
    return amountVar


def dynamic_refundID():
    refundVar = random.randint(100000, 999999)
    return "refund" + str(refundVar)


def dynamic_orderID():
    orderIDVar = random.randint(10000000000, 99999999999)
    return "order" + str(orderIDVar)


def dynamic_productID():
    productDVar = random.randint(10000000000, 99999999999)
    return "product" + str(productDVar)
