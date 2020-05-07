from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include

from land import views

urlpatterns = [
    path('', views.index, name='index'),
    path('video/<int:id>/', views.video, name='video'),
    path('about', views.about, name='about'),
    path('upgrade', views.upgrade, name='upgrade'),
    path('payment-method', views.payment_method, name='payment_method'),
    path('stripe-webhooks', views.stripe_webhooks, name='stripe_webhooks'),
    path('paypal-webhooks', views.paypal_webhooks, name='paypal_webhooks'),
    path('card', views.card, name='card'),
    path('profile', views.profile, name='profile'),
    path('contact', views.contact, name='contact'),
    path('register', views.register, name='register'),
    path('accounts/', include('django.contrib.auth.urls')),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )
