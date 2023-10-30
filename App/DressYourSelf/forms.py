from django import forms
from django.contrib.auth.forms import UserChangeForm, PasswordChangeForm 
from django.contrib.auth import get_user_model
from .models import CustomUser

User = get_user_model()

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ['email', 'first_name', 'last_name']

    def __init__(self, *args, **kwargs):
        super(CustomUserChangeForm, self).__init__(*args, **kwargs)
        self.fields.pop('password')
        
class CustomPasswordChangeForm(PasswordChangeForm):
    class Meta:
        model = CustomUser 