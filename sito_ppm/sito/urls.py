from django.urls import path
from.views import homepage,home,login,signin


urlpatterns=[
    path("",homepage,name="homepage"),
    path("login/",login,name="login"),
    path("signin/",signin,name="signin"),
    path("home/",home, name="home"),

]
