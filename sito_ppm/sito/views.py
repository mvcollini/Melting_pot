from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib import messages
from .models import CustomUser
from django.core.files.storage import FileSystemStorage


# Create your views here.
def homepage(request):
    return render(request, 'homepage.html')


def login(request):
    return render(request, 'login.html')


def signin(request):
    return render(request, 'Registrazione.html')


def home(request):
    return render(request, 'prova2.html')

def registra(request):
    if request.method == 'POST':
        print("POST request received")
        print(request.POST)  # Print the POST data for debugging
        print(request.FILES)

        username = request.POST.get('username')
        password = request.POST.get('password')

        print(f"Username: {username}")
        print(f"Password: {password}")

        if not username or not password:
            messages.error(request, 'All fields except profile image are required.')
            return redirect('signin')

        if CustomUser.objects.filter(username=username).exists():
            messages.error(request, 'Username already taken')
            return redirect('signin')
        user = CustomUser.objects.create_user(username=username, password=password)

        user.save()

        return redirect('login')
    return render(request, 'registrazione.html')
