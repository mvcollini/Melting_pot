from django.urls import path
from.views import prova,home
urlpatterns=[
    path("",prova,name="prova"),
    path("home/",home, name="home" )
]
#problem