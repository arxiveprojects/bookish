from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm,UserChangeForm
from django import forms

class CustomUserCreationForm(UserCreationForm):
    bio=forms.CharField(widget=forms.Textarea(attrs={"rows":2 }),required=False)
    class Meta:
        model= get_user_model()
        fields= ('email', 'username', 'image', 'bio',)
        

class CustomUserChangeForm(UserChangeForm):
    bio=forms.CharField(widget=forms.Textarea(attrs={"rows":2 }),required=False)
    password = None
    class Meta:
        model= get_user_model()
        fields= ('email', 'username', 'image', 'bio',)
