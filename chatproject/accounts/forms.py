# accounts/forms.py

from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    profile_picture = forms.ImageField(required=False)
    bio = forms.CharField(widget=forms.Textarea, required=False)
    
    class Meta:
        model = CustomUser
        fields = ('email', 'password1', 'password2', 'first_name', 'last_name', 'profile_picture', 'bio')

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'profile_picture', 'bio')