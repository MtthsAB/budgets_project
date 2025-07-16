#!/usr/bin/env python
"""
Teste da API de busca de produtos - simulando chamada interna
"""
import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema_produtos.settings')
django.setup()

from django.test import RequestFactory
from authentication.models import CustomUser
from orcamentos.views import buscar_produtos_por_tipo

def testar_api_interna():
    """Testa a API internamente"""
    print("🔍 TESTE DA API INTERNA - BUSCA DE PRODUTOS")
    print("=" * 50)
    
    # Criar factory de request
    factory = RequestFactory()
    
    # Criar um usuário para o teste
    user = CustomUser.objects.first()
    if not user:
        print("❌ Nenhum usuário encontrado no sistema")
        return
    
    print(f"✅ Usuário encontrado: {user.email}")
    
    # Teste 1: Buscar sofás
    print(f"\n🛋️  Testando busca de sofás...")
    request = factory.get('/orcamentos/buscar-produtos-por-tipo/?tipo=sofa')
    request.user = user
    
    try:
        response = buscar_produtos_por_tipo(request)
        
        if response.status_code == 200:
            data = response.content.decode('utf-8')
            import json
            result = json.loads(data)
            
            print(f"✅ Resposta da API (código {response.status_code}):")
            print(f"   - Produtos encontrados: {len(result.get('produtos', []))}")
            
            for produto in result.get('produtos', []):
                print(f"     • {produto['display_name']} (ID: {produto['id']})")
        else:
            print(f"❌ Erro na API (código {response.status_code})")
            
    except Exception as e:
        print(f"❌ Erro ao testar API: {e}")
        import traceback
        traceback.print_exc()
    
    # Teste 2: Buscar cadeiras (para comparação)
    print(f"\n🪑 Testando busca de cadeiras...")
    request2 = factory.get('/orcamentos/buscar-produtos-por-tipo/?tipo=cadeira')
    request2.user = user
    
    try:
        response2 = buscar_produtos_por_tipo(request2)
        
        if response2.status_code == 200:
            data2 = response2.content.decode('utf-8')
            result2 = json.loads(data2)
            
            print(f"✅ Resposta da API (código {response2.status_code}):")
            print(f"   - Produtos encontrados: {len(result2.get('produtos', []))}")
            
    except Exception as e:
        print(f"❌ Erro ao testar API cadeiras: {e}")

if __name__ == '__main__':
    try:
        testar_api_interna()
        
    except Exception as e:
        print(f"❌ Erro durante teste: {e}")
        import traceback
        traceback.print_exc()
