from django.shortcuts import render, redirect
from django.db import transaction, IntegrityError
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Outfit, Garment, User
from django.http import HttpResponse


# Create your views here.
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
        user = request.POST.get('user', '')
        password = request.POST.get('password', '')
        if not user or user == '' or user == ' ' or not password or password == '' or password == ' ':
            messages.error(request, 'Invalid username or password.')
            return redirect('login')
        else:
            username = User.objects.get(Q(username=user) | Q(email=user)).username
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponse('OK')
        else:
            messages.error(request, 'Invalid username or password.')
            return redirect('login')


