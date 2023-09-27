from django.urls import path
from .views import *

urlpatterns = [
    path('', home, name='home'),
    # Garments
    path('garments/add', add_garment, name='add_garment'),
    path('garments/edit/<int:identification>', edit_garment, name='edit_garment'),
    path('garments', garments, name='garments'),
    # Outfits
    path('outfits/add', add_outfit, name='add_outfit'),
    # Route for handling the login page
    path('authentication/', authentication, name='authentication'),
    path('signin/', signin, name='signin'),
    path('logout/', signout, name='logout'),
    path('closet_outfits/', closet_outfits, name='closet_outfits'),    
    path('new-home/', new_home, name='new-home'),
    
]
