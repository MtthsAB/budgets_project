#!/usr/bin/env python
"""
Script para migrar acessórios de Produto para Acessorio
Execute: python migrar_acessorios.py
"""

import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema_produtos.settings')
django.setup()

from produtos.models import Produto, Acessorio, TipoItem, Item

def migrar_acessorios():
    """Migra os acessórios de Produto para Acessorio"""
    
    print("=== INICIANDO MIGRAÇÃO DE ACESSÓRIOS ===")
    
    try:
        # Buscar tipo acessório
        tipo_acessorio = TipoItem.objects.get(nome__icontains='acessório')
        print(f"✓ Tipo acessório encontrado: {tipo_acessorio.nome}")
        
        # Buscar produtos que são acessórios
        produtos_acessorios = Produto.objects.filter(id_tipo_produto=tipo_acessorio)
        print(f"✓ Encontrados {produtos_acessorios.count()} produtos do tipo acessório")
        
        acessorios_criados = 0
        
        for produto in produtos_acessorios:
            # Verificar se já existe acessório correspondente
            if not Acessorio.objects.filter(ref_acessorio=produto.ref_produto).exists():
                
                # Buscar dados específicos do acessório na tabela Item (se existir)
                preco = None
                descricao = None
                
                try:
                    item_acessorio = Item.objects.get(ref_produto=produto.ref_produto)
                    preco = item_acessorio.preco_acessorio
                    descricao = item_acessorio.descricao_acessorio
                except Item.DoesNotExist:
                    pass
                
                # Criar acessório
                acessorio = Acessorio(
                    ref_acessorio=produto.ref_produto,
                    nome=produto.nome_produto,
                    ativo=produto.ativo,
                    preco=preco,
                    descricao=descricao,
                    imagem_principal=produto.imagem_principal,
                    imagem_secundaria=produto.imagem_secundaria,
                    created_by=produto.created_by,
                    updated_by=produto.updated_by,
                    created_at=produto.created_at,
                    updated_at=produto.updated_at
                )
                acessorio.save()
                
                acessorios_criados += 1
                print(f"✓ Acessório criado: ID={acessorio.id} - {produto.ref_produto} - {produto.nome_produto}")
                
            else:
                print(f"⚠️ Acessório já existe: {produto.ref_produto}")
        
        print(f"\n=== MIGRAÇÃO CONCLUÍDA ===")
        print(f"✓ Acessórios criados: {acessorios_criados}")
        
        # Verificar resultado
        total_acessorios = Acessorio.objects.count()
        print(f"✓ Total de acessórios após migração: {total_acessorios}")
        
        return True
        
    except TipoItem.DoesNotExist:
        print("❌ Tipo 'acessório' não encontrado!")
        return False
    except Exception as e:
        print(f"❌ Erro durante a migração: {e}")
        return False

if __name__ == '__main__':
    try:
        if migrar_acessorios():
            print("\n🎉 Migração concluída com sucesso!")
        else:
            print("\n⚠️ Migração concluída com problemas!")
            
    except Exception as e:
        print(f"❌ Erro durante a migração: {e}")
        sys.exit(1)
