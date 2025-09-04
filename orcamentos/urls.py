from django.urls import path
from . import views

app_name = 'orcamentos'

urlpatterns = [
    # Listagem e CRUD básico
    path('', views.listar_orcamentos, name='listar'),
    path('novo/', views.novo_orcamento, name='novo'),
    path('<int:pk>/', views.visualizar_orcamento, name='visualizar'),
    path('<int:pk>/editar/', views.editar_orcamento, name='editar'),
    path('<int:pk>/excluir/', views.excluir_orcamento, name='excluir'),
    path('<int:pk>/duplicar/', views.duplicar_orcamento, name='duplicar'),
    
    # Funcionalidades especiais
    path('<int:pk>/pdf/', views.gerar_pdf, name='gerar_pdf'),
    path('<int:pk>/totais/', views.calcular_totais, name='calcular_totais'),
    
    # Itens do orçamento
    path('<int:orcamento_pk>/item/adicionar/', views.adicionar_item, name='adicionar_item'),
    path('<int:orcamento_pk>/item/<int:item_pk>/atualizar/', views.atualizar_item, name='atualizar_item'),
    path('<int:orcamento_pk>/item/<int:item_pk>/remover/', views.remover_item, name='remover_item'),
    
    # Buscas via AJAX
    path('buscar-cliente/', views.buscar_cliente, name='buscar_cliente'),
    path('buscar-produto/', views.buscar_produto, name='buscar_produto'),
    path('produtos-por-tipo/', views.produtos_por_tipo, name='produtos_por_tipo'),
    path('buscar-produtos-por-tipo/', views.buscar_produtos_por_tipo, name='buscar_produtos_por_tipo'),
    path('detalhes-produto/', views.obter_detalhes_produto, name='obter_detalhes_produto'),
    path('informacoes-produto/', views.obter_informacoes_produto, name='obter_informacoes_produto'),
    path('tamanhos-modulo/', views.obter_tamanhos_modulo, name='obter_tamanhos_modulo'),
    path('catalogo-produtos/', views.catalogo_produtos, name='catalogo_produtos'),
]
