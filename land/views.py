import logging
import stripe
from django.conf import settings
from django.http import (
    HttpResponse
)
from django.shortcuts import render
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from land.models import Video
from land.payments import (
    prepare_card_context,
    pay_with_card,
    set_paid_until
)


logger = logging.getLogger(__name__)


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


@login_required
def payment_method(request):
    if request.method != 'GET':
        return render(request, 'land/payments/upgrade.html')

    payment_method = request.GET.get('payment_method', 'card')

    if payment_method == 'card':
        context = prepare_card_context(request)
        return render(
            request,
            'land/payments/card.html',
            context
        )
    return render(request, 'land/payments/upgrade.html')


@login_required
def card(request):
    pay_with_card(request)

    return render(request, 'land/payments/thank_you.html')


@require_POST
@csrf_exempt
def stripe_webhooks(request):
    logger.info("Stripe webhook received")

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
    if event.type == 'invoice.payment_succeeded':
        # ... handle other event types
        set_paid_until(invoice=event.data.object)

    return HttpResponse(status=200)


@login_required
def paypal(request):
    pass
