from django.shortcuts import render
from django.conf import settings


# Create your views here.
def homepage(request):
    return render(request, 'homepage.html')


def login(request):
    return render(request, 'login.html')


def signin(request):
    return render (request, 'Registrazione.html')


def home(request):
    return render(request, 'prova2.html')
