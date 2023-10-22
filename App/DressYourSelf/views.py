from django.db import transaction, IntegrityError
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Outfit, Garment, CustomUser
# from django.http import HttpResponse
from django.shortcuts import render, redirect
from .forms import UserProfileForm
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash

# Create your views here.
@login_required
# Create your views here.
def add_garment(request):
    if request.method == 'GET':
        categories = Garment.Category.choices
        return render(request, 'add_garment.html', {
            'categories': categories,
            'cssBootstrap': False,
            'jsBootstrap': True,
            'cssName': '/css/add_garment.css',
            'jsName': '/js/add_garment.js'
        })
    elif request.method == 'POST':
        try:
            if request.POST.get('name') == '' or request.POST.get('name') is None or request.POST.get('name') == ' ':
                raise IntegrityError('Name is required')
            else:
                name = request.POST.get('name')
            if request.POST.get('category') == '' or request.POST.get('category') is None or request.POST.get(
                    'category') == ' ':
                raise IntegrityError('Category is required')
            else:
                category = request.POST.get('category')
            image = request.FILES.get('image')
            if request.POST.get('description') == '' or request.POST.get('description') is None or request.POST.get(
                    'description') == ' ':
                description = None
            else:
                description = request.POST.get('description')
            if request.POST.get('brand') == '' or request.POST.get('brand') is None or request.POST.get('brand') == ' ':
                brand = None
            else:
                brand = request.POST.get('brand')
            if request.POST.get('size') == '' or request.POST.get('size') is None or request.POST.get('size') == ' ':
                size = None
            else:
                size = request.POST.get('size')
            if request.POST.get('color') == '' or request.POST.get('color') is None or request.POST.get('color') == ' ':
                color = None
            else:
                color = request.POST.get('color')
            user = request.user

            garment = Garment.objects.create(
                name=name,
                image=image,
                description=description,
                category=category,
                brand=brand,
                size=size,
                color=color,
                user=user
            )

            garment.save()

            return redirect('garments')
        except IntegrityError as e:
            messages.error(request, "The name of the garment is already taken")
            return redirect('add_garment')


@login_required
@transaction.atomic
def garments(request):
    garments_clothes = Garment.objects.filter(user=request.user)
    if request.method == 'GET':
        return render(request, 'garments.html', {
            'cssBootstrap': False,
            'jsBootstrap': False,
            'garments': garments_clothes,
            'cssName': '/css/garments.css',
            'jsName': '/js/garments.js'
        })
    elif request.method == 'POST':
        try:
            identification = request.POST.get('id')
            garment = Garment.objects.get(id=identification)
            garment.delete()
            return redirect('garments')
        except IntegrityError as e:
            messages.error(request, e)
            return redirect('garments')


@login_required
@transaction.atomic
def edit_garment(request, identification):
    garment = Garment.objects.get(id=identification)
    if request.method == 'GET':
        categories = Garment.Category.choices
        return render(request, 'edit_garment.html', {
            'categories': categories,
            'cssBootstrap': False,
            'jsBootstrap': True,
            'garment': garment,
            'cssName': '/css/add_garment.css',
            'jsName': '/js/add_garment.js'
        })
    elif request.method == 'POST':
        try:
            if request.POST.get('name') == '' or request.POST.get('name') is None or request.POST.get('name') == ' ':
                raise IntegrityError('Name is required')
            else:
                name = request.POST.get('name')
            if request.POST.get('category') == '' or request.POST.get('category') is None or request.POST.get(
                    'category') == ' ':
                raise IntegrityError('Category is required')
            else:
                category = request.POST.get('category')
            if request.FILES.get('image') is None:
                image = garment.image
            else:
                image = request.FILES.get('image')
            if request.POST.get('description') == '' or request.POST.get('description') is None or request.POST.get(
                    'description') == ' ':
                description = None
            else:
                description = request.POST.get('description')
            if request.POST.get('brand') == '' or request.POST.get('brand') is None or request.POST.get('brand') == ' ':
                brand = None
            else:
                brand = request.POST.get('brand')
            if request.POST.get('size') == '' or request.POST.get('size') is None or request.POST.get('size') == ' ':
                size = None
            else:
                size = request.POST.get('size')
            if request.POST.get('color') == '' or request.POST.get('color') is None or request.POST.get('color') == ' ':
                color = None
            else:
                color = request.POST.get('color')
            user = request.user

            garment.name = name
            garment.image = image
            garment.description = description
            garment.category = category
            garment.brand = brand
            garment.size = size
            garment.color = color
            garment.user = user

            garment.save()

            return redirect('garments')
        except IntegrityError as e:
            messages.error(request, "The name of the garment is already taken")
            return redirect('edit_garment')


@login_required
# Create your views here.
def add_outfit(request):
    tops = Garment.objects.filter(user=request.user, category="Top")
    bottoms = Garment.objects.filter(user=request.user, category="Bottom")
    footwears = Garment.objects.filter(user=request.user, category="Footwear")
    others = Garment.objects.filter(user=request.user).exclude(category="Top").exclude(category="Bottom").exclude(
        category="Footwear")
    if request.method == 'GET':
        return render(request, 'add_outfit.html', {
            'cssBootstrap': False,
            'jsBootstrap': True,
            'cssName': '/css/add_outfit.css',
            'jsName': '/js/add_outfit.js',
            'tops': tops,
            'bottoms': bottoms,
            'footwears': footwears,
            'others': others
        })
    elif request.method == 'POST':
        try:
            if request.POST.get('name') == '' or request.POST.get('name') is None or request.POST.get('name') == ' ':
                raise IntegrityError('Name is required')
            else:
                name = request.POST.get('name')

            image = request.FILES.get('outfitImage')

            if request.POST.get('description') == '' or request.POST.get('description') is None or request.POST.get(
                    'description') == ' ':
                description = None
            else:
                description = request.POST.get('description')

            if request.POST.get('tops') == '' or request.POST.get('tops') is None or request.POST.get('tops') == ' ':
                tops = None
            else:
                tops = request.POST.get('tops')
                tops = tops.split(',')
                tops = Garment.objects.filter(id__in=tops)

            if request.POST.get('bottoms') == '' or request.POST.get('bottoms') is None or request.POST.get(
                    'bottoms') == ' ':
                bottoms = None
            else:
                bottoms = request.POST.get('bottoms')
                bottoms = bottoms.split(',')
                bottoms = Garment.objects.filter(id__in=bottoms)

            if request.POST.get('footwears') == '' or request.POST.get('footwears') is None or request.POST.get(
                    'footwears') == ' ':
                footwears = None
            else:
                footwears = request.POST.get('footwears')
                footwears = footwears.split(',')
                footwears = Garment.objects.filter(id__in=footwears)

            if request.POST.get('others') == '' or request.POST.get('others') is None or request.POST.get(
                    'others') == ' ':
                others = None
            else:
                others = request.POST.get('others')
                others = others.split(',')
                others = Garment.objects.filter(id__in=others)

            user = request.user
            outfit = Outfit.objects.create(
                name=name,
                image=image,
                description=description,
                user=user
            )

            if tops is not None:
                outfit.garments.add(*tops)
            if bottoms is not None:
                outfit.garments.add(*bottoms)
            if footwears is not None:
                outfit.garments.add(*footwears)
            if others is not None:
                outfit.garments.add(*others)

            outfit.save()

            return redirect('closet_outfits')
        except IntegrityError as e:
            messages.error(request, "The name of the outfit is already taken")
            return redirect('add_outfit')


# transaction.atomic() is used to rollback the database if an error occurs
@transaction.atomic
def signin(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'GET':
        return render(request, 'signin.html')
    elif request.method == 'POST':
        try:
            username = CustomUser.objects.all().get(
                Q(username=request.POST.get('username')) | Q(email=request.POST.get('username'))).username
            user = authenticate(username=username, password=request.POST.get('password'))
            if user is None:
                messages.error(request, 'Invalid username or password')
                return redirect('signin')
            else:
                login(request, user)
                return redirect('home')
        except CustomUser.DoesNotExist:
            messages.error(request, 'User does not exist')
            return redirect('authentication')
    else:
        return 404


@transaction.atomic
def authentication(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'GET':
        return render(request, 'signup.html')
    elif request.method == 'POST':
        if request.POST['password'] == request.POST['passwordc']:
            try:
                # Creates a new user object
                user = CustomUser.objects.create(username=request.POST['username'], password=request.POST['password'],
                                                 email=request.POST['email'], first_name=request.POST['name'],
                                                 last_name=request.POST['lastname'])
                # Saves the user object
                user.save()
                login(request, user)
                return redirect('home')
            except IntegrityError:
                messages.info(request, 'Username already taken or email already registered')
                return redirect('authentication')
        else:
            messages.error(request, 'Passwords must match')
            return redirect('authentication')


def home(request):
    if request.user.is_authenticated:
        return render(request, 'new-home.html')
    return render(request, 'home.html')


def signout(request):
    logout(request)
    return redirect('home')


def closet_outfits(request):
    # Obtener el parámetro de búsqueda desde la URL
    search_query = request.GET.get('search')

    # Recuperar todos los outfits del usuario actual
    outfits = Outfit.objects.filter(user=request.user)

    if search_query:
        # Si se proporciona un parámetro de búsqueda, filtrar los outfits por nombre
        outfits = outfits.filter(name__icontains=search_query)

    if request.method == 'POST':
        # Si se envía una solicitud POST, significa que se solicitó eliminar un outfit
        outfit_id = request.POST.get('outfit_id')
        outfit_to_delete = Outfit.objects.get(id=outfit_id)
        outfit_to_delete.delete()
        return redirect('closet_outfits')

    return render(request, 'closet_outfits.html', {'outfits': outfits, 'search_query': search_query})


#vista de profile

@login_required
def profile(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=request.user)
        password_change_form = PasswordChangeForm(request.user, request.POST)

        if form.is_valid() and password_change_form.is_valid():
            form.save()
            password_change_form.save()
            update_session_auth_hash(request, password_change_form.user)
            messages.success(request, 'Tu perfil y contraseña se han actualizado correctamente.')
            return redirect('home')
        else:
            messages.error(request, 'Hubo un error al actualizar el perfil y/o la contraseña.')
    else:
        form = UserProfileForm(instance=request.user)
        password_change_form = PasswordChangeForm(request.user)

    return render(request, 'profile.html', {'form': form, 'password_change_form': password_change_form})