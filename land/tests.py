from django.test import TestCase
from land.models import User


class PaymentUnitTest(TestCase):

    def test_has_paid(self):
        user = User.objects.create(
            username="test"
        )
        user.save()

        self.assertFalse(
            user.has_paid(),
            "Initial user should have empty paid_until attr"
        )
