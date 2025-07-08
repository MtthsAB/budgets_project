#!/usr/bin/env python
"""
Script para testar o endpoint produtos_por_tipo corrigido
"""
import os
import django
from django.test import Client
from django.contrib.auth import get_user_model
import json

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema_produtos.settings')
django.setup()

from produtos.models import Cadeira, Banqueta, Poltrona, Pufe, Almofada, Produto

def test_endpoint_produtos_por_tipo():
    """Testa o endpoint corrigido"""
    print("=== TESTANDO ENDPOINT PRODUTOS_POR_TIPO CORRIGIDO ===")
    
    # Verificar produtos disponíveis
    print(f"Cadeiras: {Cadeira.objects.count()}")
    print(f"Banquetas: {Banqueta.objects.count()}")
    print(f"Poltronas: {Poltrona.objects.count()}")
    print(f"Pufes: {Pufe.objects.count()}")
    print(f"Almofadas: {Almofada.objects.count()}")
    print(f"Produtos (Sofás/Acessórios): {Produto.objects.count()}")
    
    # Configurar cliente de teste
    client = Client()
    User = get_user_model()
    user = User.objects.filter(email='admin@essere.com').first()
    
    if not user:
        print("ERRO: Usuário admin não encontrado!")
        return
    
    client.force_login(user)
    print(f"Usuário logado: {user.email}")
    
    # Testar cada tipo
    tipos = ['sofa', 'cadeira', 'banqueta', 'poltrona', 'pufe', 'almofada', 'acessorio']
    
    for tipo in tipos:
        print(f"\n--- Testando tipo: {tipo} ---")
        
        try:
            response = client.get(f'/orcamentos/produtos-por-tipo/?tipo={tipo}')
            
            if response.status_code == 200:
                data = response.json()
                produtos = data.get('produtos', [])
                print(f"Status: OK - {len(produtos)} produtos encontrados")
                
                # Mostrar produtos encontrados
                for produto in produtos[:5]:  # Mostrar primeiros 5
                    print(f"  - {produto['nome_produto']} ({produto['ref_produto']}) - R$ {produto['preco']}")
                
                if len(produtos) > 5:
                    print(f"  ... e mais {len(produtos) - 5} produtos")
                    
            else:
                print(f"Status: ERRO {response.status_code}")
                if response.content:
                    try:
                        error_data = response.json()
                        print(f"Erro: {error_data}")
                    except:
                        print(f"Resposta: {response.content.decode()}")
                        
        except Exception as e:
            print(f"Erro ao testar tipo {tipo}: {e}")

if __name__ == "__main__":
    test_endpoint_produtos_por_tipo()
