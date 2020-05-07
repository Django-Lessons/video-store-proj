import os
import yaml
import paypalrestsdk
import logging

from django.core.management.base import BaseCommand
from django.conf import settings

from land.payments.paypal import mode

PRODUCT = "product"
PLAN = "plan"

BASE_DIR = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),  # commands
    "../",  # management
    "../",  # land
    "../",  # videoproj
)

PRODUCT_CONF_PATH = os.path.join(
    BASE_DIR, "paypal", "product.yml"
)
PLAN_CONF_PATH = os.path.join(
    BASE_DIR, "paypal", "plan.yml"
)

logger = logging.getLogger(__name__)

myapi = paypalrestsdk.Api({
    "mode": mode(),  # noqa "sandbox" or "live"
    "client_id": settings.PAYPAL_CLIENT_ID,
    "client_secret": settings.PAYPAL_CLIENT_SECRET
})


class Command(BaseCommand):

    help = """
    Manages Paypal Plans and Products
"""

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
            data = yaml.load(f, Loader=yaml.FullLoader)
            ret = myapi.post("v1/catalogs/products", data)
            logger.debug(ret)

    def create_plan(self):
        with open(PLAN_CONF_PATH, "r") as f:
            data = yaml.load(f, Loader=yaml.FullLoader)
            ret = myapi.post("v1/billing/plans", data)
            logger.debug(ret)

    def list_product(self):
        ret = myapi.get("v1/catalogs/products")
        logger.debug(ret)

    def list_plan(self):
        ret = myapi.get("v1/billing/plans")
        logger.debug(ret)

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
