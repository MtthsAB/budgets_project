#!/usr/bin/env python
"""
Script para testar o endpoint produtos_por_tipo corrigido
"""
import os
import django
from django.test import Client
from django.contrib.auth import get_user_model

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema_produtos.settings')
django.setup()

def test_produtos_por_tipo_endpoint():
    """Testa o endpoint produtos_por_tipo após as correções"""
    print("=== Testando endpoint produtos_por_tipo corrigido ===")
    
    # Fazer login
    client = Client()
    User = get_user_model()
    user = User.objects.filter(email='admin@essere.com').first()
    
    if not user:
        print("ERRO: Usuário admin não encontrado!")
        return
    
    client.force_login(user)
    print(f"Usuário logado: {user.email}")
    
    # Testar cada tipo de produto
    tipos_teste = ['sofa', 'banqueta', 'cadeira', 'poltrona', 'pufe', 'almofada', 'acessorio']
    
    for tipo in tipos_teste:
        print(f"\n--- Testando tipo: {tipo} ---")
        response = client.get(f'/orcamentos/produtos-por-tipo/?tipo={tipo}')
        
        if response.status_code == 200:
            data = response.json()
            produtos = data.get('produtos', [])
            print(f"Status: OK - {len(produtos)} produtos encontrados")
            
            # Mostrar todos os produtos encontrados
            for produto in produtos:
                print(f"  - {produto['nome_produto']} ({produto['ref_produto']}) - Preço: R$ {produto.get('preco', 'N/A')}")
        else:
            print(f"Status: ERRO {response.status_code}")
            print(f"Resposta: {response.content.decode()}")

if __name__ == "__main__":
    test_produtos_por_tipo_endpoint()
