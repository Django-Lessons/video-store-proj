import logging
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from land.models import Video
from land.payments import (
    prepare_card_context,
    pay_with_card
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


@login_required
def paypal(request):
    pass


#    # accepts only GET and POST

#    # GET
#    if request.method == 'GET':
#
#        payment_method = request.GET.get('payment_method', 'card')
#
#        # paypal coming soon...
#        if payment_method == 'paypal':
#            return render(
#                request,
#                'lessons/checkout/paypal.html'
#            )
#
#        lesson_plan = LessonsPlan(
#            request.GET.get('plan', False)
#        )
#
#        secret_key = create_payment_intent(
#            lesson_plan=lesson_plan
#        )
#        return render(
#            request,
#            'lessons/checkout/card.html',
#            {
#                'plan_id': lesson_plan.id,
#                'secret_key': secret_key,
#                'customer_email': request.user.email,
#                'STRIPE_PUBLISHABLE_KEY': settings.STRIPE_PUBLISHABLE_KEY
#            }
#        )
#
#    if request.method != 'POST':
#        return HttpResponseBadRequest()
#
#    lesson_plan = LessonsPlan(
#        request.POST.get('plan_id', False)
#    )
#
#    # POST
#    create_payment_subscription(
#        email=request.user.email,
#        lesson_plan=lesson_plan,
#        payment_method_id=request.POST.get('payment_method_id', False)
#    )
#
#    return render(request, 'lessons/checkout/thank_you.html')#