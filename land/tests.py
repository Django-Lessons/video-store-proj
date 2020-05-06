from datetime import date, datetime, timedelta
from django.test import TestCase
from land.models import User
from land.payments.paypal import plus_days


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

    def test_different_date_values(self):
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

    def test_different_input_types(self):
        current_date = datetime(2020, 4, 1)
        _30days = timedelta(days=30)

        ts_in_future = datetime.timestamp(current_date + _30days)

        self.user.set_paid_until(
            int(ts_in_future)
        )

        self.user.set_paid_until(
            '1212344545'
        )

    def test_plus_31_days(self):
        current_date = datetime(2020, 1, 1)
        _15days = timedelta(days=15)

        self.user.set_paid_until(
            current_date - _15days
        )
        self.assertFalse(
            self.user.has_paid(
                current_date=current_date
            )
        )
        self.user.set_paid_until(
            plus_days(count=31)
        )
        self.assertTrue(
            self.user.has_paid(
                current_date=current_date
            )
        )



