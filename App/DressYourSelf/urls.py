from django.urls import path
from .views import *
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', home, name='home'),
    # Garments
    path('garments/add', add_garment, name='add_garment'),
    path('garments/edit/<int:identification>', edit_garment, name='edit_garment'),
    path('garments', garments, name='garments'),
    # Outfits
    path('outfits/add', add_outfit, name='add_outfit'),
    path('outfits/add/generated', add_outfit_generated, name='add_outfit_generated'),
    path('outfits/add/save', save_outfit_generated, name='save_outfit_generated'),
    path('closet_outfits/', closet_outfits, name='closet_outfits'),
    path('random_outfits/', generate_random_outfit, name='random_outfits'),
    # Route for handling the login page
    path('authentication/', authentication, name='authentication'),
    path('signin/', signin, name='signin'),
    path('logout/', signout, name='logout'),
    #modify password
    path("reset_password/", auth_views.PasswordResetView.as_view(template_name="password/password_reset.html"), name="reset_password"),
    path("reset_password_sent/",auth_views.PasswordResetDoneView.as_view(template_name="password/password_reset_sent.html"), name="password_reset_done"),
    path("reset/<uidb64>/<token>/",auth_views.PasswordResetConfirmView.as_view(template_name="password/change_password.html"), name="password_reset_confirm"),
    path("reset_password_complete/",auth_views.PasswordResetCompleteView.as_view(template_name="password/password_reset_done.html"), name="password_reset_complete"), 
    #profile
    path('edit_user/', edit_user, name='edit_user'),
    path('change_password/', change_password, name='change_password'),

]
