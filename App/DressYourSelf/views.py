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
from django.contrib.auth.models import User
from django.db import IntegrityError


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
        return render(request,'signin.html', {
            'form': AuthenticationForm
        })
    else: 
        user = authenticate(
            request, username=request.POST['username'], password =request.POST['password'])
        if user is None: 
            return render(request,'signin.html', {
                'form': AuthenticationForm,
                'error': 'Usuario o contraseña incorrecta'
            })
        else:
            login(request, user)
            return redirect('home')
    
def signUp(request):
    if request.method == 'GET':
        return render(request, 'signup.html',{
        'form' : UserCreationForm
        })
        
    else:
        if request.POST['password1'] == request.POST['password2']:
            #usamos try por si hay errores
            try:
                #registrar usuario
                user=User.objects.create_user(username=request.POST['username'], password=request.POST['password1'])
                #aca se guarda en la base de datos
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
