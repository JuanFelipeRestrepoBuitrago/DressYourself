from django.shortcuts import render, redirect
from django.db import transaction, IntegrityError
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Outfit, Garment, User
from django.http import HttpResponse
from django.shortcuts import render, redirect


# Create your views here.
def home(request):
    return HttpResponse('This is the home page!')


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
        user = User.objects.get(username='root')
        
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
def login(request):
    """
    Login view for the application
    :param request: request object
    :return: response with the login page
    """
    if request.method == 'GET':
        return render(request, 'login.html')
    else:
        user = request.POST.get('user')
        password = request.POST.get('password')
        if not user or user == '' or user == ' ' or not password or password == '' or password == ' ':
            messages.error(request, 'Invalid username or password.')
            return redirect('login')
        else:
            username = User.objects.get(Q(username=user) | Q(email=user)).username
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request=request, user=user)
            return HttpResponse('OK')
        else:
            messages.error(request, 'Invalid username or password.')
            return redirect('login')

def upload_show_image(request):
    image = None

    if request.method == 'POST':
        image = request.FILES.get('image')
        if image:
            uploaded_image = UploadedImage.objects.create(image=image)
            return redirect('upload_show_image')

    return render(request, 'upload_show_image.html', {'image': image})
