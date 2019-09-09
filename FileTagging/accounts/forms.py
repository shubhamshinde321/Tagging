from django import forms
from django.contrib.auth.models import User

class SignUpForm(forms.ModelForm):
    username = forms.CharField(label="Username", max_length=30, required=True)
    password = forms.CharField(label="Password", max_length=30, required=True, widget=forms.PasswordInput)
    confirm_password = forms.CharField(label="Confirm Password", max_length=30, required=True, widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'password', 'confirm_password')

class LoginForm(forms.ModelForm):
    username = forms.CharField(label="Username", max_length=30, required=True)
    password = forms.CharField(label="Password", max_length=30, required=True, widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'password')