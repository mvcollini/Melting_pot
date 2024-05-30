from django.urls import path
from.views import prova,home,login,signin
urlpatterns=[
    path("",prova,name="prova"),
    path("login/",login,name="login"),
    path("signin/",signin,name="signin"),
    path("home/",home, name="home" )
]
