import logging
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login
from land.models import Video


logger = logging.getLogger(__name__)


def index(request):
    videos = Video.objects.all()
    return render(
        request,
        'land/index.html',
        {'videos': videos}
    )


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            logger.debug("Authentication successful")
            auth_login(request, user)
            return redirect('index')
        else:
            logger.debug("Authentication failed")
            pass

    return render(
        request,
        'land/login.html'
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
 