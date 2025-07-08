from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),
    # URLs para gerenciamento de usuários
    path('usuarios/', views.usuarios_lista, name='usuarios_lista'),
    path('usuarios/novo/', views.usuario_novo, name='usuario_novo'),
    path('usuarios/<int:pk>/', views.usuario_detalhe, name='usuario_detalhe'),
    path('usuarios/<int:pk>/editar/', views.usuario_editar, name='usuario_editar'),
    path('usuarios/<int:pk>/alterar-senha/', views.usuario_alterar_senha, name='usuario_alterar_senha'),
    path('usuarios/<int:pk>/toggle-ativo/', views.usuario_toggle_ativo, name='usuario_toggle_ativo'),
    # URL temporária para orçamentos
    path('orcamentos/', views.orcamentos_em_desenvolvimento, name='orcamentos_em_desenvolvimento'),
]
