#!/usr/bin/env python3
"""
Teste para verificar se a funcionalidade de ordenação de produtos está funcionando
"""

import os
import sys
import django
from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse

# Configurar Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema_produtos.settings')
django.setup()

from produtos.models import Item, TipoItem, Banqueta, Cadeira

def test_ordenacao_produtos():
    """Teste básico da funcionalidade de ordenação"""
    print("🧪 Testando funcionalidade de ordenação de produtos...")
    
    client = Client()
    
    # Testar acesso à página sem autenticação (deve redirecionar)
    response = client.get('/produtos/')
    print(f"📋 Status sem autenticação: {response.status_code}")
    
    # Testar parâmetros de ordenação na URL
    test_urls = [
        '/produtos/?ordenar_por=referencia&direcao=asc',
        '/produtos/?ordenar_por=nome&direcao=desc', 
        '/produtos/?ordenar_por=status&direcao=asc',
        '/produtos/?ordenar_por=created_at&direcao=desc',
        '/produtos/?ordenar_por=created_by&direcao=asc',
    ]
    
    for url in test_urls:
        response = client.get(url)
        print(f"📋 URL: {url} - Status: {response.status_code}")
    
    print("✅ Teste básico de ordenação concluído!")

def verificar_estrutura_view():
    """Verificar se a view tem a estrutura correta para ordenação"""
    print("🔍 Verificando estrutura da view...")
    
    # Importar e verificar se a view tem os parâmetros necessários
    from produtos.views import produtos_list_view
    import inspect
    
    # Verificar código fonte da função
    source_lines = inspect.getsourcelines(produtos_list_view)[0]
    source_code = ''.join(source_lines)
    
    checks = [
        ('ordenar_por', 'ordenar_por' in source_code),
        ('direcao', 'direcao' in source_code),
        ('order_by', 'order_by' in source_code),
        ('campos_ordenacao', 'campos_ordenacao' in source_code)
    ]
    
    for check_name, resultado in checks:
        status = "✅" if resultado else "❌"
        print(f"{status} {check_name}: {'Presente' if resultado else 'Ausente'}")
    
    print("🏁 Verificação de estrutura concluída!")

if __name__ == "__main__":
    test_ordenacao_produtos()
    verificar_estrutura_view()
