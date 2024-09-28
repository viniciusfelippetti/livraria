from django.urls import path

from comum.views import LivroListView, LivroInfoView, ComprasInfoView, add_to_cart_ajax, remove_from_cart_ajax, \
    finalizar_compra, carrinho_detail_view, pagamento_view

urlpatterns = [
    path('', LivroListView.as_view(), name='livros'),
    path('info/<pk>', LivroInfoView.as_view(), name='livros_detail'),
    path('compras/', ComprasInfoView.as_view(), name='compras_detail'),
    path('add_to_cart_ajax/', add_to_cart_ajax, name='add_to_cart_ajax'),
    path('remove_from_cart_ajax/', remove_from_cart_ajax, name='remove_from_cart_ajax'),
    path('finalizar-compra/', finalizar_compra, name='finalizar_compra_url'),
    path('carrinho/', carrinho_detail_view, name='carrinho'),
    path('pagamento/', pagamento_view, name='pagamento'),
]