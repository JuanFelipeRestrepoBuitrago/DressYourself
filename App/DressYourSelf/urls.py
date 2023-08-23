from django.urls import path
from .views import *
from . import views

urlpatterns = [
    # Route for handling the login page
    path('login', login, name='login'),
    path('upload_image/', views.upload_show_image, name='upload_show_image'),
]
