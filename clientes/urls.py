from django.urls import path
from . import views

urlpatterns = [
    path('', views.cliente_lista, name='cliente_lista'),
    path('cadastro/', views.cliente_cadastro, name='cliente_cadastro'),
    path('<int:pk>/', views.cliente_detalhes, name='cliente_detalhes'),
    path('<int:pk>/editar/', views.cliente_editar, name='cliente_editar'),
    path('<int:pk>/deletar/', views.cliente_deletar, name='cliente_deletar'),
]
