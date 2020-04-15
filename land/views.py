from django.shortcuts import render
from land.models import Video


def index(request):
    videos = Video.objects.all()
    return render(
        request,
        'land/index.html',
        {'videos': videos}
    )


def video(request, id):
    video = Video.find(id=id)

    return render(
        request,
        'land/index.html',
        {'video': video}
    )


def about(request):
    return render(request, 'land/about.html')


def contact(request):
    return render(request, 'land/contact.html')
 