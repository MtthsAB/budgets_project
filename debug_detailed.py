#!/usr/bin/env python3
"""
Debug detalhado da página de cadastro
"""

import os
import django
import sys
import requests

# Configurar Django
sys.path.append('/home/matas/projetos/Project')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema_produtos.settings')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

def debug_detailed():
    """Debug detalhado da página"""
    # Criar sessão
    session = requests.Session()
    
    # Pegar CSRF token da página de login
    login_page = session.get('http://localhost:8000/auth/login/')
    csrf_token = None
    
    for line in login_page.text.split('\n'):
        if 'csrfmiddlewaretoken' in line and 'value=' in line:
            start = line.find('value="') + 7
            end = line.find('"', start)
            csrf_token = line[start:end]
            break
    
    # Fazer login
    login_data = {
        'username': 'test@example.com',
        'password': 'testpass123',
        'csrfmiddlewaretoken': csrf_token
    }
    
    login_response = session.post('http://localhost:8000/auth/login/', data=login_data)
    
    # Testar a página de cadastro
    cadastro_response = session.get('http://localhost:8000/produtos/cadastro/')
    
    print(f"Status: {cadastro_response.status_code}")
    print(f"URL final: {cadastro_response.url}")
    
    content = cadastro_response.text
    
    # Salvar conteúdo para análise
    with open('/home/matas/projetos/Project/debug_page_content.html', 'w', encoding='utf-8') as f:
        f.write(content)
    print("📄 Conteúdo salvo em debug_page_content.html")
    
    # Verificar se há título da página
    if '<title>' in content:
        start = content.find('<title>') + 7
        end = content.find('</title>', start)
        title = content[start:end]
        print(f"Título da página: {title}")
    
    # Verificar alguns elementos básicos
    basic_checks = {
        'Formulário de cadastro': '<form' in content and 'produtoForm' in content,
        'Extends base.html': "{% extends 'base.html' %}" in content,
        'Template de sofas': 'produtos/sofas/cadastro.html' in content,
        'Div secao-imagens': 'id="secao-imagens"' in content,
        'Include secao_imagens': 'produtos/includes/secao_imagens.html' in content,
        'Select tipo_produto': 'id="tipo_produto"' in content,
        'JavaScript toggleCamposPorTipo': 'toggleCamposPorTipo' in content,
    }
    
    print("\n=== VERIFICAÇÕES BÁSICAS ===")
    for check, result in basic_checks.items():
        status = "✅" if result else "❌"
        print(f"{status} {check}")
    
    # Mostrar primeiros 2000 caracteres
    print("\n=== PRIMEIROS 2000 CARACTERES ===")
    print(content[:2000])

if __name__ == '__main__':
    debug_detailed()
