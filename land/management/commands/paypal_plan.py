import logging
from django.core.management.base import BaseCommand

logger = logging.getLogger(__name__)


class Command(BaseCommand):

    help = """
    Manages Paypal Plans
"""

    def add_arguments(self, parser):
        parser.add_argument(
            "create",
            help="Creates Paypal plan"
        )
        parser.add_argument(
            "list",
            help="List Paypal plans"
        )

    def handle(self, *args, **options):
        pass
