from django.urls import path
from .views import *

urlpatterns = [
    path('', home, name='home'),
    path('garments/add', add_garment, name='add_garment'),
    path('garments', garments, name='garments'),
    # Route for handling the login page
    path('authentication/', authentication, name='authentication'),
    path('signin/', signin, name='signin'),
    path('logout/', signout, name='logout'),
]
