from django.contrib.auth import login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import CreateView

from autenticacao.forms import LoginForm, UsuarioForm
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
                if request.GET.get("next"):
                    return redirect(f'{request.GET.get("next")}')
                else:
                    return redirect('livros')
        return render(request, 'login.html', {'form': form})

class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('livros')

class UserCreateView(CreateView):
    login_url = '/autenticacao/login/'
    model = Usuario
    form_class = UsuarioForm
    template_name = 'usuario_create_update.html'
    success_url = '/livros/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
