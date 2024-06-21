from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import CustomUser, Recipe, Category, SavedRecipe, Follow
from django.http import JsonResponse
from django.core.files.storage import FileSystemStorage
from django.contrib.auth import logout, authenticate, login


# Create your views here.
def homepage(request):
    last_4_recipes = Recipe.objects.order_by('-id')[:4]
    recipe = Recipe.objects.all()
    context = {
        'last_4_recipes': last_4_recipes,
        'recipes': recipe
    }
    return render(request, 'homepage.html', context)


def mylogin(request):
    return render(request, 'login.html')


def signin(request):
    return render(request, 'Registrazione.html')


def profilo(request):
    recipes = Recipe.objects.filter(user=request.user)
    return render(request, 'profile.html', {'recipes': recipes})


def mysetting(request):
    return render(request, 'settings.html')


def crea(request):
    categories = Category.objects.all()
    return render(request, 'ricette.html', {'categories': categories})


def registra(request):
    if request.method == 'POST':

        username = request.POST.get('username')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        profile_image = request.FILES.get('profile_image')

        if not username or not password or not password2:
            messages.error(request, 'Tutti i campi tranne Immagine Profilo sono obbligatori')
            return redirect('signin')

        if CustomUser.objects.filter(username=username).exists():
            messages.error(request, 'Username già in uso')
            return redirect('signin')

        if password2 != password:
            messages.error(request, 'Le due password inserite sono diverse')
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
            messages.error(request, 'Username o Password invalidi')
            return redirect('mylogin')

    return render(request, 'login.html')


@login_required
def esci(request):
    logout(request)
    return redirect('mylogin')


@login_required
def impostazioni(request):
    if request.method == 'POST':

        username = request.POST.get('username')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        profile_image = request.FILES.get('profile_image')

        if not username and not password and not profile_image:
            messages.error(request, 'Non ci sono stati cambiamenti')
            return redirect('mysetting')

        user = request.user  # prendi lo user loggato

        if not username:
            username = user.username

        if not password:
            password = None  # se non è cambiata la metto nulla
        elif password2 != password:
            messages.error(request, 'Le due password inserite sono diverse')
            return redirect('signin')

        if not profile_image:
            profile_image = user.profile_image

        if CustomUser.objects.filter(username=username).exclude(pk=user.pk).exists():
            messages.error(request, 'Username già in uso')
            return redirect('mysetting')

        if user.check_password(password):
            messages.error(request, 'La nuova password non può essere la stessa della password attuale')
            return redirect('mysetting')

        # aggiorna username e password solo se è cambiata
        user.username = username
        if password:
            user.set_password(password)

        # aggiorna immagine
        if profile_image:
            user.profile_image = profile_image

        user.save()

        # riautentica lo user con il nuovo username
        user = authenticate(username=user.username, password=password)
        if user is not None:
            login(request, user)

        return redirect('profilo')

    return render(request, 'settings.html')


@login_required
def create_recipe(request):
    if request.method == 'POST':
        titolo = request.POST.get('titolo')
        ingredienti = request.POST.get('ingredienti')
        foto = request.FILES.get('foto')
        istruzioni = request.POST.get('istruzioni')
        tempo = request.POST.get('tempo')
        categoria = request.POST.get('category')

        if not titolo or not categoria or not ingredienti or not istruzioni:
            messages.error(request, 'All fields except photo and preparation time are required.')
            return redirect('create_recipe')

        try:
            category = Category.objects.get(id=categoria)
        except Category.DoesNotExist:
            messages.error(request, 'Invalid category.')
            return redirect('create_recipe')

        recipe = Recipe(
            title=titolo,
            photo=foto,
            preparationtime=tempo,
            category=category,
            user=request.user,
            ingredients=ingredienti,
            instructions=istruzioni
        )
        recipe.save()
        return redirect('profilo')
    categories = Category.objects.all()
    return render(request, 'ricette.html', {'categories': categories})


def recipe_detail(request, id):
    recipe = get_object_or_404(Recipe, id=id)
    return render(request, 'recipe_detail.html', {'recipe': recipe})


@login_required
def delete_recipe(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id, user=request.user)
    if request.method == 'POST':
        recipe.delete()
        return redirect('profilo')
    return render(request, 'recipes/recipe_detail.html', {'recipe': recipe})


def delete_profile(request):
    user = request.user
    if request.method == 'POST':
        user.delete()
        return redirect('homepage')

    return render(request, 'profile.html')


@login_required
def modifica_ricetta(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    categories = Category.objects.all()
    return render(request, 'modifica_ricetta.html', {'recipe': recipe, 'categories': categories})


@login_required
def update_ricetta(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id, user=request.user)
    if request.method == 'POST':
        titolo = request.POST.get('titolo')
        ingredienti = request.POST.get('ingredienti')
        foto = request.FILES.get('foto')
        istruzioni = request.POST.get('istruzioni')
        tempo = request.POST.get('tempo')
        categoria = request.POST.get('category')
        categories = Category.objects.all()
        if not titolo and not ingredienti and not istruzioni and not tempo and not foto:
            messages.error(request, 'Non ci sono stati cambiamenti')
            return redirect('modifica_ricetta', recipe_id=recipe.id)
        if titolo:
            recipe.title = titolo
        if ingredienti:
            recipe.ingredients = ingredienti
        if foto:
            recipe.photo = foto
        if istruzioni:
            recipe.instructions = istruzioni
        if tempo:
            recipe.preparationtime = tempo

        try:
            category = Category.objects.get(id=categoria)
        except Category.DoesNotExist:
            messages.error(request, 'Invalid category.')
            return redirect('modifica_ricetta', recipe_id=recipe.id)
        recipe.category = category

        recipe.save()
        return redirect('profilo')
        categories = Category.objects.all()
        return render(request, 'recipe_detail.html', {'recipe': recipe, 'categories': categories})


def searchuser(request):
    query = request.GET.get('q2')
    if query:
        if request.user in CustomUser.objects.all():
            results = CustomUser.objects.filter(username__icontains=query).exclude(id=request.user.id)
        else:
            results = CustomUser.objects.filter(username__icontains=query)

    else:
        results = CustomUser.objects.none()
    if request.user in CustomUser.objects.all():
        followed_user_ids = Follow.objects.filter(utente=request.user).values_list('followee_id', flat=True)
    else:
        followed_user_ids = None
    context = {
        'results': results,
        'query': query,
        'followed_user_ids': followed_user_ids,
    }
    return render(request, 'ricerca_utente.html', context)


def search(request):
    query = request.GET.get('q')
    if query:
        results = Recipe.objects.filter(title__icontains=query) | Recipe.objects.filter(
            ingredients__icontains=query)
    else:
        results = Recipe.objects.none()

    context = {
        'results': results,
        'query': query,
    }

    return render(request, 'risultati_ricerca.html', context)


@login_required
def toggle_save_recipe(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    saved_recipe, created = SavedRecipe.objects.get_or_create(user=request.user, recipe=recipe)

    if created:
        message = 'Recipe saved successfully!'
        status = 'saved'
    else:
        saved_recipe.delete()
        message = 'Recipe removed'
        status = 'removed'

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({'message': message, 'status': status})

    return redirect('recipe_detail', recipe_id=recipe.id)


@login_required
def ricette_salvate(request):
    saved_recipes = SavedRecipe.objects.filter(user=request.user)
    return render(request, 'ricette_salvate.html', {'saved_recipes': saved_recipes})


def ricerca_utente(request):
    if request.user in CustomUser.objects.all():
        users = CustomUser.objects.exclude(id=request.user.id)
        follows = Follow.objects.filter(utente=request.user).values_list('followee_id', flat=True)
    else:
        users = CustomUser.objects.all()
        follows = None
    context = {
        'users': users,
        'follows': follows
    }
    return render(request, 'ricerca_utente.html', context)


def user_profile(request, user_id):
    recipes = Recipe.objects.filter(user=user_id)
    user = get_object_or_404(CustomUser, id=user_id)

    if request.user in CustomUser.objects.all():
        followed_user_ids = Follow.objects.filter(utente=request.user).values_list('followee_id', flat=True)
        currentuser = request.user
    else:
        followed_user_ids = None
        currentuser = None
    context = {'user': user,
               'recipes': recipes,
               'currentuser': currentuser,
               'followed_user_ids': followed_user_ids}
    return render(request, 'pagina_utente.html', context)


@login_required
def follow_user(request, user_id):
    followee = get_object_or_404(CustomUser, id=user_id)
    follow, created = Follow.objects.get_or_create(utente=request.user, followee=followee)

    status = 'followed' if created else 'already_followed'

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({'status': status, 'user_id': user_id})

    return redirect('ricerca_utente')


@login_required
def unfollow_user(request, user_id):
    followee = get_object_or_404(CustomUser, id=user_id)
    follow = Follow.objects.filter(utente=request.user, followee=followee).first()

    if follow:
        follow.delete()
        status = 'unfollowed'
    else:
        status = 'not_following'

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({'status': status, 'user_id': user_id})

    return redirect('ricerca_utente')


def followers(request):
    follower = Follow.objects.filter(followee=request.user)
    followed_user_ids = Follow.objects.filter(utente=request.user).values_list('followee_id', flat=True)
    context = {
        'follower': follower,
        'followed_user_ids': followed_user_ids,
    }
    return render(request, 'follower.html', context)


def seguiti(request):
    seguito = Follow.objects.filter(utente=request.user)
    followed_user_ids = Follow.objects.filter(utente=request.user).values_list('followee_id', flat=True)
    context = {
        'seguito': seguito,
        'followed_user_ids': followed_user_ids,
    }
    return render(request, 'seguiti.html', context)


def primi(request):
    category = Category.objects.get(name='Primi')
    recipes = Recipe.objects.filter(category=category)

    context = {
        'recipes': recipes
    }
    return render(request, 'primi.html', context)

def secondi(request):
    category = Category.objects.get(name='Secondi')
    recipes = Recipe.objects.filter(category=category)

    context = {
        'recipes': recipes
    }
    return render(request, 'secondi.html', context)

def antipasti(request):
    category = Category.objects.get(name='Antipasti')
    recipes = Recipe.objects.filter(category=category)

    context = {
        'recipes': recipes
    }
    return render(request, 'antipasti.html', context)
def contorni(request):
    category = Category.objects.get(name='Contorni')
    recipes = Recipe.objects.filter(category=category)

    context = {
        'recipes': recipes
    }
    return render(request, 'contorni.html', context)

def dolci(request):
    category = Category.objects.get(name='Dolci')
    recipes = Recipe.objects.filter(category=category)

    context = {
        'recipes': recipes
    }
    return render(request, 'dolci.html', context)