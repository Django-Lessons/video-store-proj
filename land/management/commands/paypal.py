import logging
from django.core.management.base import BaseCommand

PRODUCT = "product"
PLAN = "plan"

logger = logging.getLogger(__name__)


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
        pass

    def create_plan(self):
        pass

    def list_product(self):
        pass

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
