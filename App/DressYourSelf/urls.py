from django.urls import path
from .views import *

urlpatterns = [
    # Route for handling the login page
    path('login', login, name='login'),
]
