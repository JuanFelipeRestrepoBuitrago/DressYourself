from django.urls import path
from .views import *
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('garments/add', views.add_garment, name='add_garment'),
    path('garments', views.garments, name='garments'),
    # Route for handling the login page
    path('login', signin, name='login'),
    path('signUp/', signUp, name='signUp'),
    path('logout/', signout, name='logout'),
    path('signin/', signin, name='signin')
]
