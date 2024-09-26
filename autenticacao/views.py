from django.contrib.auth import login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views import View

from autenticacao.forms import LoginForm
from autenticacao.models import Usuario


# Create your views here.
class LoginView(View):
    def get(self, request):
        form = LoginForm()
        return render(request, 'login.html', {'form': form})

    def post(self, request):
        form = LoginForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = Usuario.objects.get(cpf=username)
            if user.check_password(password):
                login(request, user)
                return redirect('livros')
        return render(request, 'login.html', {'form': form})

class LogoutView(LoginRequiredMixin, View):
    def get(self, request):
        logout(request)
        return redirect('livros')