import os
import yaml
import paypalrestsdk
import logging
from land.models import User

from django.conf import settings

logger = logging.getLogger(__name__)

BASE_DIR = os.path.join(
    "..",  # proj
    "..",  # land
    os.path.dirname(__file__)  # commands
)

PRODUCT_CONF_PATH = os.path.join("paypal", "product.yml")
PLAN_CONF_PATH = os.path.join("paypal", "plan.yml")
ORDER_CONF_PATH = os.path.join("paypal", "order.yml")

PRODUCT = "product"
PLAN = "plan"


def mode():
    if settings.DEBUG:
        return "sandbox"

    return "live"


myapi = paypalrestsdk.Api({
    "mode": mode(),  # noqa
    "client_id": settings.PAYPAL_CLIENT_ID,
    "client_secret": settings.PAYPAL_CLIENT_SECRET
})


def get_plan():
    data = None

    with open(PLAN_CONF_PATH, "r") as f:
        data = yaml.safe_load(f)
        logger.debug(data)

    return data


def get_product():
    data = None

    with open(PRODUCT_CONF_PATH, "r") as f:
        data = yaml.safe_load(f)
        logger.debug(data)

    return data


def get_order():
    data = None

    with open(ORDER_CONF_PATH, "r") as f:
        data = yaml.safe_load(f)
        logger.debug(data)

    return data


def place_order(user):
    # Perform one time payment, and save order id
    # on the user model
    order = {
        "intent": "CAPTURE",
        "purchase_units": [
            {
                "amount": {
                    "currency_code": "USD",
                    "value": "19.95"
                },
            }
        ],
        "application_context": {
            "shipping_preference": "NO_SHIPPING",
            "brand_name": "Video Store Demo"
        }
    }
    ret = myapi.post("v2/checkout/orders", order)


def set_paid_until(obj):
    logger.debug(f"OBJ = {obj}")
    billing_agreement_id = obj['billing_agreement_id']
    ret = myapi.get(f"v1/billing/subscriptions/{billing_agreement_id}")
    logger.debug("===================== Subsciption details =================")
    logger.debug(ret)
    if obj['amount']['total'] == "19.99":
        # hey, but how do I associat it to an user?
        pass
