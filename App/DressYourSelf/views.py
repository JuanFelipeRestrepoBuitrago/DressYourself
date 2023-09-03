from django.db import transaction, IntegrityError
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Outfit, Garment, CustomUser
from django.http import HttpResponse
from django.shortcuts import render, redirect


# Create your views here.
@login_required
# Create your views here.
def add_garment(request):
    if request.method == 'GET':
        categories = Garment.Category.choices
        return render(request, 'add_garment.html', {
            'cssBootstrap': False,
            'jsBootstrap': True,
            'categories': categories,
            'cssName': '/css/add_garment.css',
            'jsName': '/js/add_garment.js'
        })
    elif request.method == 'POST':
        try:
            if request.POST.get('name') == '' or request.POST.get('name') is None or request.POST.get('name') == ' ':
                raise IntegrityError('Name is required')
            else:
                name = request.POST.get('name')
            if request.POST.get('category') == '' or request.POST.get('category') is None or request.POST.get('category') == ' ':
                raise IntegrityError('Category is required')
            else:
                category = request.POST.get('category')
            image = request.FILES.get('image')
            if request.POST.get('description') == '' or request.POST.get('description') is None or request.POST.get('description') == ' ':
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

            return redirect('garments')
        except IntegrityError as e:
            messages.error(request, e)
            return redirect('add_garment')


@login_required
def garments(request):
    garments = Garment.objects.filter(user=request.user)
    if request.method == 'GET':
        return render(request, 'garments.html', {
            'garments': garments,
            'cssName': '/css/garments.css',
            'jsName': '/js/garments.js'
        })

# transaction.atomic() is used to rollback the database if an error occurs
@transaction.atomic
def signin(request):
    if request.method == 'GET':
        return render(request, 'signin.html')
    elif request.method == 'POST':
        username = CustomUser.objects.all().get(
            Q(username=request.POST.get('username')) | Q(email=request.POST.get('username'))).username
        user = authenticate(username=username, password=request.POST.get('password'))
        if user is None:
            messages.error(request, 'Usuario o contraseña incorrecta')
            return redirect('signin')
        else:
            login(request, user)
            return redirect('home')


@transaction.atomic
def signUp(request):
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
                messages.warning(request, 'Username already taken or email already registered')
                return redirect('signUp')
        else:
            messages.error(request, 'Passwords must match')
            return redirect('signUp')


def home(request):
    return render(request, 'home.html')


def signout(request):
    logout(request)
    return redirect('home')
