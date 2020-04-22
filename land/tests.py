from datetime import date, timedelta
from django.test import TestCase
from land.models import User


class PaymentUnitTest(TestCase):

    def setUp(self):
        self.user = User.objects.create(
            username="test"
        )
        self.user.save()

    def test_has_paid(self):
        self.assertFalse(
            self.user.has_paid(),
            "Initial user should have empty paid_until attr"
        )

    def test_diffrent_date_values(self):
        current_date = date(2020, 1, 4)  # 1st of April 2020
        _30days = timedelta(days=30)

        self.user.set_paid_until(current_date + _30days)

        self.assertTrue(
            self.user.has_paid(
                current_date=current_date
            )
        )

        self.user.set_paid_until(current_date - _30days)

        self.assertFalse(
            self.user.has_paid(
                current_date=current_date
            )
        )
