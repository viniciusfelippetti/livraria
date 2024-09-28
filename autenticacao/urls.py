from django.urls import path

from autenticacao.views import LoginView, LogoutView, UserCreateView

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('usuarios/add', UserCreateView.as_view(), name='usuarios_add'),
]
