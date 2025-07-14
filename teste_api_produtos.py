#!/usr/bin/env python
"""
Script de diagnóstico para verificar se os sofás estão sendo retornados corretamente pela API
"""
import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema_produtos.settings')
django.setup()

from produtos.models import TipoItem, Produto

def testar_api_busca_produtos():
    """Simula a busca de produtos por tipo como a API faz"""
    print("🔍 TESTE DA API DE BUSCA DE PRODUTOS")
    print("=" * 50)
    
    # 1. Buscar tipo sofá
    try:
        tipo_sofa = TipoItem.objects.filter(nome__icontains='Sofás').first()
        print(f"✅ Tipo Sofás encontrado: {tipo_sofa.nome} (ID: {tipo_sofa.id})")
    except Exception as e:
        print(f"❌ Erro ao buscar tipo sofás: {e}")
        return
    
    # 2. Buscar produtos desse tipo
    try:
        sofas = Produto.objects.filter(id_tipo_produto=tipo_sofa, ativo=True)
        print(f"✅ Sofás encontrados: {sofas.count()}")
        
        for sofa in sofas:
            print(f"   - {sofa.nome_produto} (ID: {sofa.id}, Ref: {sofa.ref_produto})")
            
            # Simular estrutura retornada pela API
            produto_api = {
                'id': f'produto_{sofa.id}',  # Aqui está o problema!
                'nome_produto': sofa.nome_produto,
                'ref_produto': sofa.ref_produto,
                'display_name': f'{sofa.ref_produto} - {sofa.nome_produto}',
                'preco': 0.0  # Produtos sofás não têm preço direto
            }
            print(f"     API ID: {produto_api['id']}")
            print(f"     Display Name: {produto_api['display_name']}")
            
    except Exception as e:
        print(f"❌ Erro ao buscar sofás: {e}")
        return
    
    # 3. Testar se a detecção de sofá funciona
    print(f"\n🧪 TESTE DE DETECÇÃO DE SOFÁ:")
    for sofa in sofas:
        produto_id = f'produto_{sofa.id}'
        is_sofa = produto_id.startsWith('produto_')
        print(f"   - {sofa.nome_produto}: ID={produto_id}, É sofá? {is_sofa}")

def verificar_tipos_disponiveis():
    """Verifica todos os tipos de produto disponíveis"""
    print(f"\n📋 TIPOS DE PRODUTO DISPONÍVEIS:")
    tipos = TipoItem.objects.all()
    for tipo in tipos:
        count = Produto.objects.filter(id_tipo_produto=tipo, ativo=True).count()
        print(f"   - {tipo.nome}: {count} produtos")

if __name__ == '__main__':
    try:
        verificar_tipos_disponiveis()
        testar_api_busca_produtos()
        
    except Exception as e:
        print(f"❌ Erro durante teste: {e}")
        import traceback
        traceback.print_exc()
