import stripe
import datetime
from datetime import date
from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser

API_KEY = settings.STRIPE_SECRET_KEY


class StripeCustomer(models.Model):
    customer_id = models.CharField(max_length=64)
    email = models.CharField(max_length=64)
    payment_method_id = models.CharField(max_length=64)


class StripeSubscription(models.Model):
    subscription_id = models.CharField(max_length=64)


class User(AbstractUser):
    paid_until = models.DateField(
        null=True,
        blank=True
    )

    def set_paid_until(self, date_or_timestamp):
        if isinstance(date_or_timestamp, int):
            # input date as timestamp integer
            paid_until = date.fromtimestamp(date_or_timestamp)
        elif isinstance(date_or_timestamp, str):
            # input date as timestamp string
            paid_until = date.fromtimestamp(int(date_or_timestamp))
        else:
            paid_until = date_or_timestamp

        self.paid_until = paid_until
        self.save()

    def has_paid(
        self,
        current_date=datetime.date.today()
    ):
        if self.paid_until is None:
            return False

        return current_date < self.paid_until

    def get_or_create_customer(self, payment_method_id):
        customer_id = None
        try:
            customer = StripeCustomer.objects.get(
                email=self.email,
                payment_method_id=payment_method_id
            )
            customer_id = customer.customer_id
        except StripeCustomer.DoesNotExist:
            customer = stripe.Customer.create(
                email=self.email,
                payment_method=payment_method_id,
                invoice_settings={
                    'default_payment_method': payment_method_id,
                },
            )
            StripeCustomer.objects.create(
                email=self.email,
                payment_method_id=payment_method_id,
                customer_id=customer.id
            )
            customer_id = customer.id

        return customer_id

    def create_or_update_subscription(
        self,
        customer_id,
        stripe_plan_id
    ):
        try:
            StripeSubscription.objects.get(
                customer_id=customer_id
            )
        except StripeSubscription.DoesNotExist:
            stripe.api_key = API_KEY
            stripe.Subscription.create(
                customer=customer_id,
                items=[
                    {
                        'plan': stripe_plan_id,
                    },
                ]
            )


class Video(models.Model):

    title = models.CharField(max_length=30)
    thumbnail = models.FileField()
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        default=1
    )

    class Meta:
        verbose_name = "Video"
        verbose_name_plural = "Videos"

    def __str__(self):
        return f"{self.title}"
