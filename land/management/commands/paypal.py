import logging
from django.core.management.base import BaseCommand

logger = logging.getLogger(__name__)


PRODUCT = "product"
PLAN = "plan"

class Command(BaseCommand):

    help = """
    Manages Paypal Plans
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

    def handle(self, *args, **options):
        create_what = options.get("create")
        list_what = options.get("list")

        if create_what:
            logger.debug(f"Create a {create_what}")
            self.create(create_what)
        elif list_what:
            logger.debug(f"List {list_what}")
            self.list(list_what)
