from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('teste/', views.teste_view, name='teste'),
    path('produtos/', views.produtos_list_view, name='produtos_lista'),
    path('produtos/cadastro/', views.produto_cadastro_view, name='produto_cadastro'),
    path('produtos/<int:produto_id>/', views.produto_detalhes_view, name='produto_detalhes'),
    path('produtos/<int:produto_id>/editar/', views.produto_editar_view, name='produto_editar'),
    path('produtos/<int:produto_id>/excluir/', views.produto_excluir_view, name='produto_excluir'),
]
