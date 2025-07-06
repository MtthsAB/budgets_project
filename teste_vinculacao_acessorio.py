#!/usr/bin/env python3
"""
Script para testar a vinculação de acessórios aos produtos
"""

import os
import sys
import django

# Configurar Django
sys.path.append('/home/matas/projetos/Project')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema_produtos.settings')
django.setup()

from produtos.models import Item, TipoItem

def testar_vinculacao():
    """Testa a vinculação de acessórios"""
    print("=== Teste de Vinculação de Acessórios ===\n")
    
    # Buscar acessórios e produtos
    try:
        tipo_acessorio = TipoItem.objects.get(nome__icontains='acessórios')
        acessorios = Item.objects.filter(id_tipo_produto=tipo_acessorio)
        
        print(f"Encontrados {acessorios.count()} acessórios:")
        for acessorio in acessorios:
            print(f"  - {acessorio.ref_produto} - {acessorio.nome_produto}")
            vinculados = acessorio.produtos_vinculados.all()
            if vinculados.exists():
                print(f"    Vinculado a {vinculados.count()} produto(s):")
                for vinculado in vinculados:
                    print(f"      * {vinculado.ref_produto} - {vinculado.nome_produto}")
            else:
                print("    Nenhum produto vinculado")
            print()
        
        # Buscar produtos que podem receber acessórios
        produtos_nao_acessorios = Item.objects.exclude(id_tipo_produto=tipo_acessorio).filter(ativo=True)
        print(f"Encontrados {produtos_nao_acessorios.count()} produtos disponíveis para vinculação:")
        for produto in produtos_nao_acessorios[:5]:  # Mostrar apenas os primeiros 5
            print(f"  - {produto.ref_produto} - {produto.nome_produto}")
            
        if produtos_nao_acessorios.count() > 5:
            print(f"  ... e mais {produtos_nao_acessorios.count() - 5} produtos")
            
    except TipoItem.DoesNotExist:
        print("ERRO: Tipo 'Acessórios' não encontrado no banco de dados")
        
    except Exception as e:
        print(f"ERRO: {str(e)}")

if __name__ == "__main__":
    testar_vinculacao()
