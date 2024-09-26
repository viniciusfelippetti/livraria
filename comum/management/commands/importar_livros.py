import requests
from django.core.management import BaseCommand

from comum.models import Livro, Autor, Categoria, Publicadora


class Command(BaseCommand):
    help = 'Importação dos parceiros'

    def handle(self, *args, **options):

        url = "https://openlibrary.org/search.json?q=the+lord+of+the+rings&page=2&fields=title,author_name,first_publish_year,subject,number_of_pages_median,publisher,cover_i"
        headers = {
            "User-Agent": "MyAppName/1.0 (myemail@example.com)"
        }

        response = requests.get(url, headers=headers)

        # Check for successful response
        if response.status_code == 200:
            # Load data as JSON (assuming response is JSON)
            data = response.json()
            docs = data['docs']
            print(len(docs))
            for doc in docs:

                publisher = doc.get("publisher")
                subject = doc.get("subject")
                title = doc.get("title")
                author_name = doc.get("author_name")
                first_publish_year = doc.get("first_publish_year")
                number_of_pages_median = doc.get("number_of_pages_median")
                capa_id = doc.get("cover_i")

                if publisher and title and author_name and first_publish_year and number_of_pages_median and capa_id and subject:
                    print(f"Primeiro ano de publicação: {first_publish_year}")
                    livro = Livro.objects.create(nome_livro=title,ano_publicacao=first_publish_year,numero_paginas=number_of_pages_median,capa_id=capa_id)
                    for nome in author_name:
                        autor, created = Autor.objects.get_or_create(nome=nome)
                        livro.autor.add(autor)

                    for nome in subject:
                        categoria, created = Categoria.objects.get_or_create(nome=nome)
                        livro.categoria.add(categoria)

                    for nome in publisher:
                        publicadora, created= Publicadora.objects.get_or_create(nome=nome)
                        livro.publicadora.add(publicadora)

                    livro.save()
                    print(f"Título: {title}")
                    print(f"Nome do Autor: {author_name}")
                    print(f"Número de páginas: {number_of_pages_median}")
                    print(f"Editor: {publisher}")
                    print(f"Editor: {subject}")

            # You can now use these variables (key, title, etc.) in your system
        else:
            print("Error:", response.status_code)
