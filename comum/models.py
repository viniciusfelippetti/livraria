from django.db import models

from autenticacao.models import Usuario


# Create your models here.
class Categoria(models.Model):
    nome = models.CharField(max_length=150)

    def __str__(self):
        return f"{self.nome}"

class Publicadora(models.Model):
    nome = models.CharField(max_length=150)

    def __str__(self):
        return f"{self.nome}"

class Autor(models.Model):
    nome = models.CharField(max_length=150)

    def __str__(self):
        return f"{self.nome}"

class Livro(models.Model):
    nome_livro = models.CharField(max_length=200)
    preco = models.FloatField(default=10.0)
    ano_publicacao = models.IntegerField()
    numero_paginas = models.IntegerField()
    autor = models.ManyToManyField(Autor, verbose_name="Autores")
    categoria = models.ManyToManyField(Categoria, verbose_name="Categorias")
    publicadora = models.ManyToManyField(Publicadora, verbose_name="Publicadoras")
    capa_id = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.nome_livro} - {self.ano_publicacao}"

    class Meta:
        ordering = ('nome_livro',)

class ItemCompra(models.Model):
    quantidade = models.IntegerField()
    livro = models.ForeignKey(Livro, on_delete=models.CASCADE)

class Compra(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    itens = models.ManyToManyField(ItemCompra, verbose_name="Itens da compra")
