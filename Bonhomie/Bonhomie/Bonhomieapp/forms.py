from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, AbstractUser
from django.contrib.auth import get_user_model


class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    class Meta:
        model = CustomUser
        fields = ['username','email', 'password1', 'password2']