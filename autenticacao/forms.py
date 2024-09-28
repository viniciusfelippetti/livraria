from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django import forms

from autenticacao.models import Usuario


class LoginForm(AuthenticationForm):
    username = forms.CharField(label='CPF', max_length=11)
    password = forms.CharField(label='Senha', widget=forms.PasswordInput)

class UsuarioForm(UserCreationForm):
    class Meta:
        model = Usuario
        fields = ('cpf', 'email', 'nome', 'password1', 'password2', 'endereco', 'is_active')