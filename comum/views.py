from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.views.generic import ListView
import json
from comum.forms import LivroForm
from comum.models import Livro, Compra, ItemCompra

from openpyxl.workbook import Workbook

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer


# Create your views here.
class LivroListView(ListView):
    model = Livro
    context_object_name = 'livros'
    template_name = 'livros_list.html'
    paginate_by = 12

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
        context = {'livro': livro}
        return render(request, 'livro_detail.html', context)


class ComprasInfoView(LoginRequiredMixin,View):

    def get(self, request, *args, **kwargs):
        compras = Compra.objects.filter(usuario=request.user)
        context = {'compras': compras}

        if 'exportar_pdf' in request.GET:
            pdf = self.exportar_pdf()
            return pdf
        if 'exportar_xlsx' in request.GET:
            xlsx = self.exportar_xlsx()
            return xlsx
        return render(request, 'compras_detail.html', context)

    def exportar_pdf(self):

        compras = Compra.objects.filter(usuario=self.request.user)
        # Cria um buffer para armazenar o PDF
        buffer = HttpResponse(content_type='application/pdf')
        buffer['Content-Disposition'] = f'attachment; filename="compras_{self.request.user}.pdf"'

        doc = SimpleDocTemplate(buffer, pagesize=letter)
        styles = getSampleStyleSheet()

        elements = []

        data = [
            [Paragraph("Quantidade", styles['Normal']),
             Paragraph("Livro", styles['Normal'])]
        ]

        for compra in compras:
            for item in compra.itens.all():
                quantidade = str(item.quantidade)
                livro = str(item.livro)

                data.append([
                    Paragraph(quantidade, styles['Normal']),
                    Paragraph(livro, styles['Normal'])
                ])

        # Cria a tabela no PDF
        table = Table(data)
        table.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                                   ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                                   ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                                   ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                                   ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                                   ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                                   ('GRID', (0, 0), (-1, -1), 1, colors.black)]))

        elements.append(table)  # Adiciona a tabela aos elementos do PDF

        # Gera o PDF
        doc.build(elements)
        return buffer

    def exportar_xlsx(self):
        compras = Compra.objects.filter(usuario=self.request.user)

        wb = Workbook()
        ws = wb.active


        headers = ["Quantidade", "Livro"]
        ws.append(headers)

        for compra in compras:
            for item in compra.itens.all():
                quantidade = str(item.quantidade)
                livro = str(item.livro)

                ws.append([quantidade, livro])

        # Cria um HttpResponse com o conteúdo do arquivo Excel
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = f'attachment; filename="compras_{self.request.user}.xlsx"'

        # Salva o Workbook no HttpResponse
        wb.save(response)
        return response


def add_to_cart_ajax(request):
    if request.method == 'POST':
        livro_id = request.POST.get('livro_id')
        quantity = int(request.POST.get('quantity', 1))
        livro = get_object_or_404(Livro, id=livro_id)
        cart = request.session.get("cart", {})  # Add or update cart
        if str(livro_id) in cart:
            cart[str(livro_id)]['quantity'] += quantity
        else:
            cart[str(livro_id)] = {
                'name': livro.nome_livro,
                'price': str(livro.preco),  # Assuming you have a price field
                'quantity': quantity
            }

        request.session['cart'] = cart
        return JsonResponse({'status': 'success', 'cart': cart})

    return JsonResponse({'status': 'error'}, status=400)

def remove_from_cart_ajax(request):
    if request.method == 'POST':
        livro_id = request.POST.get('livro_id')

        cart = request.session.get('cart', {})

        # Remove item from cart
        if livro_id in cart:
            del cart[livro_id]
            request.session['cart'] = cart
            return JsonResponse({'status': 'success'})

    return JsonResponse({'status': 'error'}, status=400)


def finalizar_compra(request):
    if request.method == 'POST':
        itens = request.POST.get('items')
        if itens:
            # Carregar itens em formato JSON
            itens_list = json.loads(itens)

            # Lista para armazenar os detalhes dos livros
            livros = []

            # Para cada item, buscar o livro e criar um dicionário com os detalhes relevantes
            for item in itens_list:
                livro = Livro.objects.get(id=item[0])
                livros.append({
                    'id': livro.id,
                    'nome': livro.nome_livro,
                    'preco': livro.preco,  # Exemplo de campo de preço, se existir
                    'quantidade': item[1]  # Assumindo que o segundo valor da lista é a quantidade
                })

            # Passar o contexto com os detalhes dos livros
            context = {
                "livros": livros,
                "itens": itens_list,
            }

            # Armazenar o contexto na sessão (JSON serializável)
            request.session['finalizar_compra_context'] = context
            # Redirecionar para a URL do carrinho
            return JsonResponse({'status': 'success', 'message': 'POR FAVOR'}, status=200)

    # Caso a requisição não seja POST ou não haja itens, retornar erro
    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)

@login_required
def carrinho_detail_view(request):
    context = request.session.get('finalizar_compra_context', {})
    return render(request, 'carrinho_detail.html', context)

def pagamento_view(request):
    quantidade = request.POST.getlist("quantidade")
    nome = request.POST.getlist("nome")

    for i in range(len(quantidade)):
        livro = Livro.objects.get(nome_livro=nome[i])
        itemcompra = ItemCompra.objects.create(quantidade=quantidade[i], livro=livro)
        compra = Compra.objects.create(usuario=request.user)
        compra.itens.add(itemcompra)

    request.session['cart'] = {}
    return redirect('compras_detail')
