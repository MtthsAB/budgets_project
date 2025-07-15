#!/usr/bin/env python3
"""
Script para testar endpoints de produtos por tipo
"""

import os
import sys
import django
import requests
from django.test import Client

# Configurar Django
sys.path.append('/home/matas/projetos/Project')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema_produtos.settings')
django.setup()

from authentication.models import CustomUser

def testar_endpoints():
    # Criar cliente de teste
    client = Client()
    
    # Fazer login
    try:
        user = CustomUser.objects.get(username='admin')
        client.force_login(user)
        print("✅ Login realizado com sucesso")
    except CustomUser.DoesNotExist:
        print("❌ Usuário admin não encontrado")
        return
    
    # Tipos para testar
    tipos = ['acessorio', 'almofada', 'banqueta', 'cadeira', 'poltrona', 'pufe', 'sofa']
    
    print("\n=== TESTE DE ENDPOINTS ===")
    
    for tipo in tipos:
        print(f"\n🔸 Testando tipo: {tipo}")
        
        # Testar endpoint produtos-por-tipo
        response1 = client.get(f'/orcamentos/produtos-por-tipo/?tipo={tipo}')
        if response1.status_code == 200:
            data1 = response1.json()
            print(f"   produtos-por-tipo: {len(data1.get('produtos', []))} produtos")
        else:
            print(f"   produtos-por-tipo: ERRO {response1.status_code}")
        
        # Testar endpoint buscar-produtos-por-tipo (sem busca)
        response2 = client.get(f'/orcamentos/buscar-produtos-por-tipo/?tipo={tipo}')
        if response2.status_code == 200:
            data2 = response2.json()
            print(f"   buscar-produtos-por-tipo: {len(data2.get('produtos', []))} produtos")
            # Mostrar alguns exemplos
            if data2.get('produtos'):
                for produto in data2['produtos'][:2]:
                    print(f"      - {produto['display_name']} (R$ {produto['preco']})")
        else:
            print(f"   buscar-produtos-por-tipo: ERRO {response2.status_code}")

if __name__ == '__main__':
    testar_endpoints()
