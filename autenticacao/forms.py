from django.contrib.auth.forms import AuthenticationForm
from django import forms


class LoginForm(AuthenticationForm):
    username = forms.CharField(label='CPF', max_length=11)
    password = forms.CharField(label='Senha', widget=forms.PasswordInput)