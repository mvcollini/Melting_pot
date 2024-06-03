from django.urls import path
from .views import homepage, home, login, signin, registra
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path("", homepage, name="homepage"),
    path("login/", login, name="login"),
    path("signin/", signin, name="signin"),
    path("home/", home, name="home"),
    path("registra/", registra, name="registra")

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
