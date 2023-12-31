from django.shortcuts import render

from django.http import HttpResponse
from django.shortcuts import render


def index(request):
    return HttpResponse('Hello, world. You\'re at the polls index.')


def harry(request):
    return render(request, 'hello.html', {'name': 'Harry'})
