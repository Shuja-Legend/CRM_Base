# Importing necessary modules and classes from Django
from django.core.mail import send_mail
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import *  # Importing the models module from the current directory
import re

# Custom SignUpForm that extends UserCreationForm
class SignUpForm(UserCreationForm):
    # Customizing the username field
    username = forms.CharField(
        label=('Username'),
        max_length=150,
        help_text=('Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'),
        error_messages={'unique': ("A user with that username already exists.")},
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    # Customizing the email field
    email = forms.EmailField(
        max_length=50,
        help_text='Required. Inform a valid email address.',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    # Customizing the password1 field
    password1 = forms.CharField(
        label=('Password'),
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )

    # Customizing the password2 field
    password2 = forms.CharField(
        label=('Password Confirmation'),
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        help_text=('Just Enter the same password, for confirmation')
    )

    class Meta:
        model = User
        # The fields attribute specifies the fields to be included in the form
        fields = ('username', 'email', 'password1', 'password2')


class CustomAuthenticationForm(AuthenticationForm):
    def clean_username(self):
        username = self.cleaned_data['username']
        try:
            validate_email(username)
        except ValidationError:
            raise forms.ValidationError("Please enter a valid email address.")
        print(username, type(username))
        return username

    def clean_password(self):
        password = self.cleaned_data['password']
        # Password length validation
        if len(password) < 16:
            raise forms.ValidationError("Password must be at least 16 characters long.")
        # Password complexity validation
        if not any(char.isdigit() for char in password):
            raise forms.ValidationError("Password must contain at least one digit.")
        if not any(char.isalpha() for char in password):
            raise forms.ValidationError("Password must contain at least one letter.")
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            raise forms.ValidationError("Password must contain at least one special character.")
        print(password, type(password))
        return password
