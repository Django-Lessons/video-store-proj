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

SUBSCRIPTION = 'subscription'
ORDER = 'order'


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


def create_order():
    order = get_order()
    return myapi.post("v2/checkout/orders", order)


def create_subscription():
    data = {
        'plan_id': settings.PAYPAL_PLAN_MONTHLY_ID,
    }
    return myapi.post("v1/billing/subscriptions", data)


def get_redirect_for(ret, what):
    for link in ret['links']:
        if link['rel'] == what:
            return link['href']


def set_paid_until(obj, from_what):

    if from_what == SUBSCRIPTION:
        billing_agreement_id = obj['billing_agreement_id']
        ret = myapi.get(f"v1/billing/subscriptions/{billing_agreement_id}")

        try:
            user = User.objects.get(order_id=ret['id'])
        except User.DoesNotExist:
            logger.error(f"User with order id={ret['id']} not found.")
            return False

        logger.debug(f"SUBSCRIPTION {obj} for user {user.email}")

    if from_what == ORDER:
        ret = get_redirect_for(obj['links'], 'self')
        try:
            user = User.objects.get(order_id=ret['id'])
        except User.DoesNotExist:
            logger.error(f"User with order id={ret['id']} not found.")
            return False

        logger.debug(f"ORDER {obj} for user {user.email}")

    return True
