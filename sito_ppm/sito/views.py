from django.shortcuts import render
from django.conf import settings

# Create your views here.
def prova(request):
    return render(request,'ciao.html')
def home(request):
    return render(request,'prova2.html')