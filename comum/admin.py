from django.contrib import admin

from comum.models import Livro, Autor, Categoria, Compra, ItemCompra

# Register your models here.
admin.site.register(Livro)
admin.site.register(Autor)
admin.site.register(Categoria)
admin.site.register(ItemCompra)
admin.site.register(Compra)