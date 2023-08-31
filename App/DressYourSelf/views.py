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
def home(request):
    return HttpResponse('This is the home page!')


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

def upload_show_image(request):
    image = None

    if request.method == 'POST':
        image = request.FILES.get('image')
        if image:
            uploaded_image = UploadedImage.objects.create(image=image)
            return redirect('upload_show_image')

    return render(request, 'upload_show_image.html', {'image': image})
