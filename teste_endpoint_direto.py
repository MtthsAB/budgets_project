#!/usr/bin/env python
"""
Script para testar o endpoint produtos-por-tipo via requests
"""
import os
import django
import requests
import json

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema_produtos.settings')
django.setup()

from django.contrib.auth import get_user_model
from django.test import Client

def test_endpoint():
    """Testar endpoint via Client do Django"""
    print("=== Testando endpoint produtos-por-tipo ===")
    
    # Criar cliente de teste
    client = Client()
    
    # Fazer login com usuário admin
    User = get_user_model()
    admin_user = User.objects.filter(email='admin@essere.com').first()
    
    if not admin_user:
        print("ERRO: Usuário admin não encontrado!")
        return
    
    client.force_login(admin_user)
    print(f"Usuário logado: {admin_user.email}")
    
    # Tipos para testar
    tipos = ['sofa', 'banqueta', 'cadeira', 'poltrona', 'pufe', 'almofada', 'acessorio']
    
    for tipo in tipos:
        print(f"\n--- Testando tipo: {tipo} ---")
        
        url = f'/orcamentos/produtos-por-tipo/?tipo={tipo}'
        response = client.get(url)
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            try:
                data = response.json()
                produtos = data.get('produtos', [])
                print(f"Produtos encontrados: {len(produtos)}")
                
                for produto in produtos:
                    print(f"  - {produto.get('nome', 'N/A')} (Ref: {produto.get('ref', 'N/A')})")
                    
            except Exception as e:
                print(f"Erro ao processar JSON: {e}")
                print(f"Conteúdo da resposta: {response.content.decode()[:200]}...")
        else:
            print(f"Erro na requisição: {response.status_code}")
            print(f"Conteúdo: {response.content.decode()[:200]}...")

if __name__ == "__main__":
    test_endpoint()
