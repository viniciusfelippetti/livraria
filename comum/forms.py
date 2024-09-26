from django import forms

from comum.models import Livro, Autor, Categoria


class LivroForm(forms.ModelForm):
    categoria = forms.ModelChoiceField(queryset=Categoria.objects.all(),required=False)
    autor = forms.ModelChoiceField(queryset=Autor.objects.all(), required=False)

    class Meta:
        model = Livro
        fields = ("nome_livro", )