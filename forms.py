from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class RegisterForm(UserCreationForm):
    email = forms.EmailField()


class Meta:
    model = User
    fields = ["new_username", "email", "new_password", "new_password_repeat"]
