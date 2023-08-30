from django.urls import path
from .views import *
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('add_garment/', views.add_garment, name='add_garment'),
    # Route for handling the login page
    path('login', signin, name='login'),
    path('upload_image/', views.upload_show_image, name='upload_show_image'),
]
