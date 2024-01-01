from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, AbstractUser

class UserRegistrationForm(UserCreationForm):
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'shipping_address', 'billing_address']
