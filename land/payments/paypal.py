import os
import yaml
import paypalrestsdk
import logging
from datetime import datetime, timedelta
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


myapi = paypalrestsdk.Api({
    "mode": mode(),  # noqa
    "client_id": settings.PAYPAL_CLIENT_ID,
    "client_secret": settings.PAYPAL_CLIENT_SECRET
})


from django.conf import settings


def mode():
    if settings.DEBUG:
        return "sandbox"

    return "live"


def get_url_from(iterator, what):
    for link in iterator:
        if link['rel'] == what:
            return link['href']


def plus_days(count):
    _date = datetime.now()
    return _date + timedelta(days=count)


def set_paid_until(obj, from_what):

    if from_what == SUBSCRIPTION:
        billing_agreement_id = obj['billing_agreement_id']
        ret = myapi.get(f"v1/billing/subscriptions/{billing_agreement_id}")

        try:
            user = User.objects.get(paypal_subscription_id=ret['id'])
        except User.DoesNotExist:
            logger.error(f"User with order id={ret['id']} not found.")
            return False

        logger.debug(f"SUBSCRIPTION {obj} for user {user.email}")
        if obj['amount']['total'] == '19.95':
            user.set_paid_until(plus_days(count=31))

    if from_what == ORDER:
        url = get_url_from(obj['links'], 'self')
        ret = myapi.get(url)
        try:
            user = User.objects.get(paypal_order_id=ret['id'])
        except User.DoesNotExist:
            logger.error(f"User with order id={ret['id']} not found.")
            return False

        logger.debug(f"ORDER {obj} for user {user.email}")

    return True
