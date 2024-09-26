from django.urls import path

from comum.views import LivroListView, LivroInfoView

urlpatterns = [
    path('', LivroListView.as_view(), name='livros'),
    path('info/<pk>', LivroInfoView.as_view(), name='livros_info'),
]