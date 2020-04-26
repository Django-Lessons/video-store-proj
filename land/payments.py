from django.conf import settings
import stripe

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


def create_subscription(email, plan, payment_method_id):
    stripe.api_key = API_KEY

    customer = stripe.Customer.create(
        email=email,
        payment_method=payment_method_id,
        invoice_settings={
            'default_payment_method': payment_method_id,
        },
    )

    stripe.Subscription.create(
        customer=customer.id,
        items=[
            {
                'plan': plan.stripe_plan_id,
            },
        ]
    )


def pay_with_card(request):

    payment_method_id = request.POST.get('payment_method_id')
    automatic = request.POST.get('automatic', 'on')

    stripe.api_key = API_KEY
    stripe.PaymentIntent.retrieve(
        request.POST.get('payment_intent_id')
    )
    stripe_plan_id = request.POST.get('plan_id', False)

    stripe.PaymentIntent.modify(
        request.POST.get('payment_intent_id'),
        payment_method=payment_method_id
    )

    stripe.PaymentIntent.confirm(
        request.POST.get('payment_intent_id'),
        payment_method=payment_method_id
    )

    if automatic == 'on':
        create_subscription(
            request.user.email,
            stripe_plan_id,
            payment_method_id
        )


def prepare_card_context(request):
    context = {}
    stripe.api_key = API_KEY

    automatic = request.GET.get('automatic', 'on')

    plan = VideosPlan(
        plan_id=request.GET.get('plan', False)
    )

    payment_intent = stripe.PaymentIntent.create(
        amount=plan.amount,
        currency=plan.currency,
        payment_method_types=["card"],
    )
    secret_key = payment_intent.client_secret
    context = {
        'plan_id': plan.stripe_plan_id,
        'secret_key': secret_key,
        'payment_intent_id': payment_intent.id,
        'automatic': automatic,
        'customer_email': request.user.email,
        'STRIPE_PUBLISHABLE_KEY': settings.STRIPE_PUBLISHABLE_KEY
    }
    return context
