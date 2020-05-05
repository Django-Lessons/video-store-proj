import yaml
import requests
import paypalrestsdk
import os
import logging
from django.conf import settings
from django.core.management.base import BaseCommand

logger = logging.getLogger(__name__)


def mode():
    if settings.DEBUG:
        return "sandbox"

    return "live"


myapi = paypalrestsdk.Api({
    "mode": mode(),  # noqa
    "client_id": settings.PAYPAL_CLIENT_ID,
    "client_secret": settings.PAYPAL_CLIENT_SECRET
})


PRODUCT = "product"
PLAN = "plan"

BASE_DIR = os.path.join(
    "..",  # proj
    "..",  # land
    "..",  # management
    os.path.dirname(__file__)  # commands
)

PRODUCT_CONF_PATH = os.path.join("paypal", "product.yml")
PLAN_CONF_PATH = os.path.join("paypal", "plan.yml")

class Command(BaseCommand):

    help = """
    Manages Paypal Plans
"""

    @property
    def headers(self):
        return {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {settings.PAYPAL_ACCESS_TOKEN}"
        }

    def add_arguments(self, parser):
        parser.add_argument(
            "--create",
            "-c",
            choices=[PRODUCT, PLAN],
            help="Creates Paypal product or plan"
        )
        parser.add_argument(
            "--list",
            "-l",
            choices=[PRODUCT, PLAN],
            help="List Paypal products or plans"
        )

    def create_product(self):
        with open(PRODUCT_CONF_PATH, "r") as f:
            data = yaml.safe_load(f)
            logger.debug(data)
            ret = myapi.post("v1/catalogs/products", data)
            logger.debug(ret)

    def create_plan(self):
        with open(PLAN_CONF_PATH, "r") as f:
            data = yaml.safe_load(f)
            logger.debug(data)
            ret = myapi.post("v1/billing/plans", data)
            logger.debug(ret)

    def list_product(self):
        ret = myapi.get("v1/catalogs/products")
        logger.debug(ret)

    def list_plan(self):
        pass

    def create(self, what):
        if what == PRODUCT:
            self.create_product()
        else:
            self.create_plan()

    def list(self, what):
        if what == PRODUCT:
            self.list_product()
        else:
            self.list_plan()

    def handle(self, *args, **options):
        create_what = options.get("create")
        list_what = options.get("list")

        if create_what:
            logger.debug(f"Create a {create_what}")
            self.create(create_what)
        elif list_what:
            logger.debug(f"List {list_what}")
            self.list(list_what)
