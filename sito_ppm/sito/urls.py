from django.urls import path
from .views import (homepage, mylogin, signin, registra, esci, login_view, profilo,
                    mysetting, impostazioni, crea, create_recipe, recipe_detail, delete_recipe,
                    modifica_ricetta, update_ricetta, search, toggle_save_recipe, ricette_salvate,
                    ricerca_utente,searchuser, user_profile, follow_user, unfollow_user,
                    delete_profile,followers)
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path("", homepage, name="homepage"),
    path("mylogin/", mylogin, name="mylogin"),
    path("signin/", signin, name="signin"),
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
    path('recipe/<int:recipe_id>/modifica/', modifica_ricetta, name='modifica_ricetta'),
    path("recipe/<int:recipe_id>/update/", update_ricetta, name='update_ricetta'),
    path('search/', search, name='search'),
    path('toggle-save-recipe/<int:recipe_id>/', toggle_save_recipe, name='toggle_save_recipe'),
    path("ricette_salvate/", ricette_salvate, name='ricette_salvate'),
    path("ricerca_utente/", ricerca_utente, name ='ricerca_utente'),
    path("searchuser/",searchuser,name='searchuser'),
    path('user/<int:user_id>/', user_profile, name='user_profile'),
    path('follow/<int:user_id>/', follow_user, name='follow_user'),
    path('unfollow/<int:user_id>/', unfollow_user, name='unfollow_user'),
    path('delete_profile/', delete_profile, name='delete_profile'),
    path('followers/',followers, name='followers'),

]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
