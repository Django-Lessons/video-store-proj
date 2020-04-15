from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from land import views

urlpatterns = [
    path('', views.index, name='index'),
    path('video', views.video, name='video'),
    path('about', views.about, name='about'),
    path('contact', views.contact, name='contact'),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )
