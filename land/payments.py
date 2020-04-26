from django.conf import settings
from stripe import (
    Customer,
    Subscription,
    PaymentIntent
)

MONTH = 'm'
ANNUAL = 'a'

PLAN_DICT = {
    MONTH: settings.STRIPE_PLAN_MONTHLY_ID,
    ANNUAL: settings.STRIPE_PLAN_ANNUAL_ID
}

API_KEY = settings.STRIPE_SECRET_KEY


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


def prepare_card_context(request):
    context = {}

    plan = VideosPlan(
        plan_id=request.GET.get('plan_id', False)
    )

    payment_intent = PaymentIntent.create(
        api_key=API_KEY,
        amount=plan.amount,
        currency=plan.currency,
        payment_method_types=["card"],
    )
    secret_key = payment_intent.client_secret
    context = {
        'plan_id': plan.stripe_plan_id,
        'secret_key': secret_key,
        'customer_email': request.user.email,
        'STRIPE_PUBLISHABLE_KEY': settings.STRIPE_PUBLISHABLE_KEY
    }
    return context
