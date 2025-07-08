#!/usr/bin/env python
"""
Teste do endpoint produtos_por_tipo
"""
import os
import django
from django.test import Client
from django.contrib.auth import get_user_model

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema_produtos.settings')
django.setup()

def test_endpoint_produtos_por_tipo():
    """Testa o endpoint produtos_por_tipo"""
    print("=== Testando endpoint produtos_por_tipo ===")
    
    client = Client()
    
    # Fazer login
    User = get_user_model()
    user = User.objects.filter(email='admin@essere.com').first()
    if not user:
        print("ERRO: Usuário admin não encontrado!")
        return
    
    client.force_login(user)
    print(f"Usuário logado: {user.email}")
    
    # Testar tipos
    tipos_teste = ['cadeira', 'banqueta', 'poltrona', 'sofa', 'pufe', 'almofada', 'acessorio']
    
    for tipo in tipos_teste:
        print(f"\n--- Testando tipo: {tipo} ---")
        try:
            response = client.get(f'/orcamentos/produtos-por-tipo/?tipo={tipo}')
            
            if response.status_code == 200:
                data = response.json()
                produtos = data.get('produtos', [])
                print(f"✓ Status: OK - {len(produtos)} produtos encontrados")
                
                # Mostrar primeiros 3 produtos
                for produto in produtos[:3]:
                    print(f"  - {produto['nome_produto']} ({produto['ref_produto']}) - R$ {produto['preco']}")
                    
                if len(produtos) > 3:
                    print(f"  ... e mais {len(produtos) - 3} produtos")
            else:
                print(f"✗ Status: ERRO {response.status_code}")
                print(f"Resposta: {response.content.decode()}")
                
        except Exception as e:
            print(f"✗ Erro na requisição: {e}")

if __name__ == "__main__":
    test_endpoint_produtos_por_tipo()
