from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('add_garment/', views.add_garment, name='add_garment'),
]
