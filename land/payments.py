import logging
import stripe
from land.models import User

from django.conf import settings

MONTH = 'm'
ANNUAL = 'a'

API_KEY = settings.STRIPE_SECRET_KEY
logger = logging.getLogger(__name__)


class VideosMonthPlan:
    def __init__(self):
        self.stripe_plan_id = settings.STRIPE_PLAN_MONTHLY_ID
        self.amount = 1995


class VideosAnnualPlan:
    def __init__(self):
        self.stripe_plan_id = settings.STRIPE_PLAN_ANNUAL_ID
        self.amount = 19950


class VideosPlan:
    def __init__(self, plan_id):
        """
        plan_id is either string 'm' (stands for monthly)
        or a string letter 'a' (which stands for annual)
        """
        if plan_id == MONTH:
            self.plan = VideosMonthPlan()
            self.id = MONTH
        elif plan_id == ANNUAL:
            self.plan = VideosAnnualPlan()
            self.id = ANNUAL
        else:
            raise ValueError('Invalid plan_id value')

        self.currency = 'usd'

    @property
    def stripe_plan_id(self):
        return self.plan.stripe_plan_id

    @property
    def amount(self):
        return self.plan.amount


def set_paid_until(charge):
    logger.info(f"set_paid_until with {charge}")

    stripe.api_key = API_KEY
    pi = stripe.PaymentIntent.retrieve(charge.payment_intent)

    if pi.customer:
        customer = stripe.Customer.retrieve(pi.customer)
        email = customer.email

        if customer:
            subscr = stripe.Subscription.retrieve(
                customer['subscriptions'].data[0].id
            )
            current_period_end = subscr['current_period_end']

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            logger.warning(
                f"User with email {email} not found"
            )
            return False

        user.set_paid_until(current_period_end)
        logger.info(
            f"Profile with {current_period_end} saved for user {email}"
        )
    else:
        pass
        # charge.amount  1990 | 19995
        # this was one time payment, update
        # paid_until (e.g. paid_until = current_date + 31 days) using
        # charge.paid + charge.amount attrs
