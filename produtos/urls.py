from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('teste/', views.teste_view, name='teste'),
    path('teste-imagem/', views.teste_imagem_view, name='teste_imagem'),
    path('teste-cadastro/', views.teste_cadastro_view, name='teste_cadastro'),
    path('produtos/', views.produtos_list_view, name='produtos_lista'),
    path('produtos/cadastro/', views.produto_cadastro_view, name='produto_cadastro'),
    path('produtos/debug-cadastro/', views.debug_cadastro_view, name='debug_cadastro'),
    path('produtos/<int:produto_id>/', views.produto_detalhes_view, name='produto_detalhes'),
    path('produtos/<int:produto_id>/editar/', views.produto_editar_view, name='produto_editar'),
    path('produtos/<int:produto_id>/excluir/', views.produto_excluir_view, name='produto_excluir'),
    path('teste-tamanhos-edicao/', views.teste_tamanhos_edicao_view, name='teste_tamanhos_edicao'),
    
    # Teste temporário para imagens de banquetas
    path('banquetas/<int:banqueta_id>/teste-imagem/', views.banqueta_teste_imagem_view, name='banqueta_teste_imagem'),
    
    # APIs
    path('api/produtos/', views.api_produtos_disponiveis, name='api_produtos_disponiveis'),
    
    # URLs para acessórios (manter temporariamente para não quebrar)
    path('acessorios/', views.acessorios_list_view, name='acessorios_lista'),
    path('acessorios/cadastro/', views.acessorio_cadastro_view, name='acessorio_cadastro'),
    path('acessorios/<int:acessorio_id>/', views.acessorio_detalhes_view, name='acessorio_detalhes'),
    path('acessorios/<int:acessorio_id>/editar/', views.acessorio_editar_view, name='acessorio_editar'),
    path('acessorios/<int:acessorio_id>/excluir/', views.acessorio_excluir_view, name='acessorio_excluir'),
    
    # URLs para banquetas - COMENTADAS: agora integradas na listagem de produtos
    # path('banquetas/', views.banquetas_list_view, name='banquetas_lista'),
    path('banquetas/cadastro/', views.banqueta_cadastro_view, name='banqueta_cadastro'),
    path('banquetas/<int:banqueta_id>/', views.banqueta_detalhes_view, name='banqueta_detalhes'),
    path('banquetas/<int:banqueta_id>/editar/', views.banqueta_editar_view, name='banqueta_editar'),
    path('banquetas/<int:banqueta_id>/excluir/', views.banqueta_excluir_view, name='banqueta_excluir'),
    
    # URLs para cadeiras
    path('cadeiras/', views.cadeiras_list_view, name='cadeiras_lista'),
    path('cadeiras/cadastro/', views.cadeira_cadastro_view, name='cadeira_cadastro'),
    path('cadeiras/<int:cadeira_id>/', views.cadeira_detalhes_view, name='cadeira_detalhes'),
    path('cadeiras/<int:cadeira_id>/editar/', views.cadeira_editar_view, name='cadeira_editar'),
    path('cadeiras/<int:cadeira_id>/excluir/', views.cadeira_excluir_view, name='cadeira_excluir'),
    path('cadeiras/<int:cadeira_id>/teste-imagem/', views.cadeira_teste_imagem_view, name='cadeira_teste_imagem'),
]
