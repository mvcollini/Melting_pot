from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib import messages
from .models import CustomUser
from django.core.files.storage import FileSystemStorage
from django.contrib.auth import logout, authenticate, login


# Create your views here.
def homepage(request):
    return render(request, 'homepage.html')


def mylogin(request):
    return render(request, 'login.html')


def signin(request):
    return render(request, 'Registrazione.html')


def home(request):
    return render(request, 'prova2.html')


def profilo(request):
    return render(request, 'profile.html')


def registra(request):
    if request.method == 'POST':

        username = request.POST.get('username')
        password = request.POST.get('password')
        profile_image = request.FILES.get('profile_image')

        if not username or not password:
            messages.error(request, 'All fields except profile image are required.')
            return redirect('signin')

        if CustomUser.objects.filter(username=username).exists():
            messages.error(request, 'Username already taken')
            return redirect('signin')
        user = CustomUser.objects.create_user(username=username, password=password)
        if profile_image:
            user.profile_image = profile_image

        user.save()

        return redirect('mylogin')
    return render(request, 'registrazione.html')


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            return redirect('homepage')
        else:
            messages.error(request, 'Invalid username or password')
            return redirect('mylogin')

    return render(request, 'login.html')


def esci(request):
    logout(request)
    return redirect('mylogin')
