import logging
from django.core.management.base import BaseCommand
from land.models import User

logger = logging.getLogger(__name__)


class Command(BaseCommand):

    help = """
    List all users
"""

    def handle(self, *args, **options):
        for u in User.objects.order_by("username"):
            logger.info(f"username={u.username}")
