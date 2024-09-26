from django.shortcuts import render
from django.views import View
from django.views.generic import ListView

from comum.forms import LivroForm
from comum.models import Livro


# Create your views here.
class LivroListView(ListView):
    model = Livro
    context_object_name = 'livros'
    template_name = 'livros_list.html'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["livro_filtro_form"] = LivroForm()
        return context

    def get_queryset(self):

        queryset = super().get_queryset()
        nome_livro_filtro = self.request.GET.get("nome_livro")
        autor_filtro = self.request.GET.get("autor")
        categoria_filtro = self.request.GET.get("categoria")

        if nome_livro_filtro:
            queryset = queryset.filter(nome_livro__icontains=nome_livro_filtro)
        if autor_filtro:
            queryset = queryset.filter(autor__id=autor_filtro)
        if categoria_filtro:
            queryset = queryset.filter(categoria__id=categoria_filtro)

        return queryset

class LivroInfoView(View):

    def get(self, request, *args, **kwargs):
        id = self.kwargs['pk']
        livro = Livro.objects.get(id=id)
        return render(request, )
