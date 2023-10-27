from django import forms
from django.contrib.auth.forms import UserChangeForm 
from django.contrib.auth import get_user_model
from .models import CustomUser

#User = get_user_model()

class CustomUserChangeForm(UserChangeForm):
    new_password = forms.CharField(
        label="Nueva contraseña",
        widget=forms.PasswordInput(),
        required=False,
    )
    class Meta:
        model = CustomUser
        fields = ['email', 'first_name', 'last_name', 'new_password']
