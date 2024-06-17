from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import CustomUser, Recipe, Category
from django.core.files.storage import FileSystemStorage
from django.contrib.auth import logout, authenticate, login


# Create your views here.
def homepage(request):
    return render(request, 'homepage.html')


def mylogin(request):
    return render(request, 'login.html')


def signin(request):
    return render(request, 'Registrazione.html')


# da eliminare
def home(request):
    return render(request, 'prova2.html')


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
        foto = request.POST.get('foto')
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


@login_required
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


@login_required
def modifica_ricetta(request, id):
    recipe = get_object_or_404(Recipe, id=id)
    return render(request, 'modifica_ricetta.html', {'recipe': recipe})


@login_required
def update_ricetta(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id, user=request.user)
    if request.method == 'POST':
        titolo = request.POST.get('titolo')
        ingredienti = request.POST.get('ingredienti')
        foto = request.POST.get('foto')
        istruzioni = request.POST.get('istruzioni')
        tempo = request.POST.get('tempo')
        categoria = request.POST.get('category')

        if not titolo or not categoria or not ingredienti or not istruzioni or not tempo or not foto:
            messages.error(request, 'Non ci sono stati cambiamenti')
            return redirect('modifica_ricetta', {'recipe': recipe})
        if not titolo:
            titolo = recipe.title
        if not ingredienti:
            ingredienti = recipe.ingredients
        if not foto:
            foto = recipe.photo
        if not istruzioni:
            istruzioni = recipe.instructions
        if not tempo:
            tempo = recipe.preparationtime

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
        return render(request, 'recipes/recipe_detail.html', {'recipe': recipe})
