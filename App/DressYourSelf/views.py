from django.shortcuts import render, redirect
from django.db import transaction, IntegrityError
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Outfit, Garment, User
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.db import IntegrityError


# Create your views here.
@login_required
# Create your views here.
def add_garment(request):
    if request.method == 'GET':
        categories = Garment.Category.choices
        return render(request, 'add_garment.html', {
            'categories': categories,
            'cssName': '/css/add_garment.css',
            'jsName': '/js/add_garment.js'
        })
    elif request.method == 'POST':
        name = request.POST.get('name')
        image = request.FILES.get('image')
        description = request.POST.get('description')
        category = request.POST.get('category')
        brand = request.POST.get('brand')
        size = request.POST.get('size')
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

        return HttpResponse(f'Garment {garment.name} added successfully!')
    

# transaction.atomic() is used to rollback the database if an error occurs
@transaction.atomic
def signin(request):
    if request.method == 'GET':
        return render(request,'signin.html',)
    elif request.method == 'POST':
        username = User.objects.all().get(Q(username=request.POST.get('username')) | Q(email=request.POST.get('username'))).username
        user = authenticate(username=username, password=request.POST.get('password'))
        if user is None: 
            return render(request, 'signin.html', {
                'error': 'Usuario o contraseña incorrecta'
            })
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
                user = User.objects.create_user(username=request.POST['username'], password=request.POST['password'], email=request.POST['email'], first_name=request.POST['first_name'], last_name=request.POST['last_name'])
                # Saves the user object
                user.save()
                login(request, user)
                return redirect('home')
            except IntegrityError:
                return render(request, 'signup.html',{ 
                    'form' : UserCreationForm,
                    "error": 'El usuario ya existe'
                })
                
        return render(request, 'signup.html',{
            'form': UserCreationForm,
            "error": 'Las contraseñas no coinciden'
        })
    
    
    
def home(request):
    return render(request,'home.html')

def tasks(request):
    return render(request,'tasks.html')

def signout(request):
    logout(request)
    return redirect('home')
