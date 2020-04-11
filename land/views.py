from django.shortcuts import render


def index(request):
    return render(request, 'land/index.html')


def about(request):
    return render(request, 'land/about.html')


def contact(request):
    return render(request, 'land/contact.html')
 