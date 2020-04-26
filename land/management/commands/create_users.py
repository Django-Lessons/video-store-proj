import logging
from django.core.management.base import BaseCommand
from land.models import User

logger = logging.getLogger(__name__)


class Command(BaseCommand):

    help = """
    Creates a couple of users
"""

    def add_arguments(self, parser):
        parser.add_argument(
            '--start',
            '-s',
            type=int,
            default=1,
            help="Number to start with"
        )
        parser.add_argument(
            '--count',
            '-c',
            type=int,
            help="Number/Count of users to create"
        )
        parser.add_argument(
            '--password',
            '-p',
            help="Password"
        )

    def handle(self, *args, **options):
        count = options.get('count', 10)
        password = options.get('password')
        start = options.get('start')

        for n in range(start, start + count + 1):
            u = User.objects.create(
                username=f"user{n}",
                email=f"user{n}@mail.com"
            )
            u.set_password(password)
            u.save()
