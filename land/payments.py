import logging
import stripe

from django.conf import settings
from land.models import User

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


def set_paid_until(invoice):
    """
    invoice = is stripe.invoice object instance
    from invoice.payment_succeeded webhook
    """
    # invoice['customer_email']
    # invoice['paid'] = true|false
    # invoice['current_period_end'] # timestamp of end of subscription
    email = invoice['customer_email']
    logger.info(f"email={email}")
    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        logger.warning(
            f"User with email {email} not found while trying to upgrade to PRO"
        )
        return False

    if invoice['subscription']:
        subscr = stripe.Subscription.retrieve(
            id=invoice['subscription']
        )

        current_period_end = subscr['current_period_end']

        if invoice['paid']:
            user.set_paid_until(current_period_end)
            logger.info(
                f"Profile with {current_period_end} saved for user {email}"
            )
        else:
            logger.info("Invoice is was NOT paid!")

    return True


def save_subscription(subscription):
    customer_id = subscription['customer']
    try:
        user = User.objects.get(customer_id=customer_id)
        user.subscription_id = subscription['id']
        user.save()
    except User.DoesNotExist:
        logger.error("Was unable to save subscription")
