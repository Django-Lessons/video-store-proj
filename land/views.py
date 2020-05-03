import stripe
import logging
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.shortcuts import render
from django.http import (
    HttpResponse
)
from django.conf import settings
from land.payments import (VideosPlan, set_paid_until)
from land.models import Video

API_KEY = settings.STRIPE_SECRET_KEY
logger = logging.getLogger(__name__)


@require_POST
@csrf_exempt
def stripe_webhooks(request):

    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SIGNING_KEY
        )
        logger.info("Event constructed correctly")
    except ValueError:
        # Invalid payload
        logger.warning("Invalid Payload")
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError:
        # Invalid signature
        logger.warning("Invalid signature")
        return HttpResponse(status=400)

    # Handle the event
    if event.type == 'charge.succeeded':
        # object has  payment_intent attr
        set_paid_until(event.data.object)

    return HttpResponse(status=200)


def index(request):
    videos = Video.objects.all()
    return render(
        request,
        'land/index.html',
        {'videos': videos}
    )


def register(request):
    return render(
        request,
        'land/register.html'
    )


def video(request, id):
    video = Video.objects.filter(id=id).first()

    return render(
        request,
        'land/video.html',
        {'video': video}
    )


def about(request):
    return render(request, 'land/about.html')


def contact(request):
    return render(request, 'land/contact.html')


@login_required
def upgrade(request):
    logger.info("upgrade")
    return render(request, 'land/payments/upgrade.html')


@require_POST
@login_required
def payment_method(request):
    stripe.api_key = API_KEY
    plan = request.POST.get('plan', 'm')
    automatic = request.POST.get('automatic', 'on')
    payment_method = request.POST.get('payment_method', 'card')
    context = {}

    plan_inst = VideosPlan(plan_id=plan)
    #               plan_inst.amount
    # 'a' | 'm' =>  plan_inst.currency
    #               plan_inst.stripe_plan_id

    payment_intent = stripe.PaymentIntent.create(
        amount=plan_inst.amount,
        currency=plan_inst.currency,
        payment_method_types=['card']
    )

    if payment_method == 'card':

        context['secret_key'] = payment_intent.client_secret
        context['STRIPE_PUBLISHABLE_KEY'] = settings.STRIPE_PUBLISHABLE_KEY
        context['customer_email'] = request.user.email
        context['payment_intent_id'] = payment_intent.id
        context['automatic'] = automatic
        context['stripe_plan_id'] = plan_inst.stripe_plan_id

        return render(request, 'land/payments/card.html', context)


@login_required
def profile(request):
    logger.info("profile")
    return render(request, 'land/profile.html')


@login_required
def card(request):

    payment_intent_id = request.POST['payment_intent_id']
    payment_method_id = request.POST['payment_method_id']
    stripe_plan_id = request.POST['stripe_plan_id']
    automatic = request.POST['automatic']
    stripe.api_key = API_KEY

    if automatic == 'on':
        # create subs
        customer = stripe.Customer.create(
            email=request.user.email,
            payment_method=payment_method_id,
            invoice_settings={
                'default_payment_method': payment_method_id
            }
        )
        s = stripe.Subscription.create(
            customer=customer.id,
            items=[
                {
                    'plan': stripe_plan_id
                },
            ]
        )
        latest_invoice = stripe.Invoice.retrieve(s.latest_invoice)

        ret = stripe.PaymentIntent.confirm(
            latest_invoice.payment_intent
        )

        if ret.status == 'requires_action':
            pi = stripe.PaymentIntent.retrieve(
                latest_invoice.payment_intent
            )
            context = {}

            context['payment_intent_secret'] = pi.client_secret
            context['STRIPE_PUBLISHABLE_KEY'] = settings.STRIPE_PUBLISHABLE_KEY

            return render(request, 'land/payments/3dsec.html', context)
    else:
        stripe.PaymentIntent.modify(
            payment_intent_id,
            payment_method=payment_method_id
        )

    return render(request, 'land/payments/thank_you.html')
