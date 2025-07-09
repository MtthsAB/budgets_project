
from django.urls import path
from debug_cliente_view import cliente_cadastro_debug

urlpatterns = [
    path('debug-cliente/', cliente_cadastro_debug, name='debug_cliente'),
]
