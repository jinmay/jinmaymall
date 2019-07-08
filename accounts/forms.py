from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

User = get_user_model()

class UserCreationForm(UserCreationForm):
    
    class Meta:
        model = User
        fields = ('username', 'email', )