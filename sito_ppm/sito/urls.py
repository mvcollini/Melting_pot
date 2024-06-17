from django.urls import path
from .views import (homepage, home, mylogin, signin, registra, esci, login_view, profilo,
                    mysetting, impostazioni, crea, create_recipe, recipe_detail, delete_recipe,
                    modifica_ricetta, update_ricetta)
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path("", homepage, name="homepage"),
    path("mylogin/", mylogin, name="mylogin"),
    path("signin/", signin, name="signin"),
    path("home/", home, name="home"),
    path("registra/", registra, name="registra"),
    path("esci/", esci, name="esci"),
    path("login_view/", login_view, name="login_view"),
    path("profilo/", profilo, name='profilo'),
    path("mysetting/", mysetting, name='mysetting'),
    path("impostazioni/", impostazioni, name="impostazioni"),
    path("crea/", crea, name='crea'),
    path('create/', create_recipe, name='create_recipe'),
    path('recipe/<int:id>/', recipe_detail, name='recipe_detail'),
    path('recipe/<int:recipe_id>/delete/', delete_recipe, name='delete_recipe'),
    path('recipe/<int:id>/modifica', modifica_ricetta, name='modifica_ricetta'),
    path("modificaricetta/<int:id>/", update_ricetta, name='update_ricetta')

]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
