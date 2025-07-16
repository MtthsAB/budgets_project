#!/usr/bin/env python
"""
Script para migrar dados de Item para Produto
"""

import os
import sys
import django

# Configurar Django
sys.path.append('/home/matas/projetos/Project')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema_produtos.settings')
django.setup()

from produtos.models import Item, Produto

def migrar_itens_para_produtos():
    """Migra todos os itens para a nova tabela produtos"""
    print("🔄 MIGRANDO DADOS DE ITEM PARA PRODUTO")
    print("=" * 50)
    
    itens = Item.objects.all()
    total_itens = itens.count()
    
    if total_itens == 0:
        print("ℹ️  Nenhum item encontrado para migrar.")
        return
    
    print(f"📦 Encontrados {total_itens} itens para migrar")
    
    migrados = 0
    erros = 0
    
    for item in itens:
        try:
            # Verificar se já existe um produto com a mesma referência
            produto_existente = Produto.objects.filter(ref_produto=item.ref_produto).first()
            
            if produto_existente:
                print(f"⚠️  Produto {item.ref_produto} já existe, pulando...")
                continue
            
            # Criar novo produto com dados básicos apenas
            produto = Produto.objects.create(
                ref_produto=item.ref_produto,
                nome_produto=item.nome_produto,
                id_tipo_produto=item.id_tipo_produto,
                ativo=item.ativo,
                imagem_principal=item.imagem_principal,
                imagem_secundaria=item.imagem_secundaria,
                created_at=item.created_at,
                created_by=item.created_by,
                updated_at=item.updated_at,
                updated_by=item.updated_by,
            )
            
            print(f"✅ Migrado: {produto.ref_produto} - {produto.nome_produto}")
            migrados += 1
            
        except Exception as e:
            print(f"❌ Erro ao migrar {item.ref_produto}: {str(e)}")
            erros += 1
    
    print("\n📊 RESULTADO DA MIGRAÇÃO")
    print("=" * 30)
    print(f"✅ Migrados com sucesso: {migrados}")
    print(f"❌ Erros: {erros}")
    print(f"📦 Total processados: {migrados + erros}")

def verificar_migracao():
    """Verifica se a migração foi bem-sucedida"""
    print("\n🔍 VERIFICANDO MIGRAÇÃO")
    print("=" * 30)
    
    total_itens = Item.objects.count()
    total_produtos = Produto.objects.count()
    
    print(f"📦 Itens na tabela antiga: {total_itens}")
    print(f"📦 Produtos na tabela nova: {total_produtos}")
    
    if total_produtos > 0:
        print("\n✅ MIGRAÇÃO CONCLUÍDA COM SUCESSO!")
        print("🔄 Dados básicos migrados para a nova tabela Produto")
        print("ℹ️  A tabela Item foi mantida temporariamente para compatibilidade")
    else:
        print("\n⚠️  Nenhum produto foi criado na nova tabela")

if __name__ == '__main__':
    migrar_itens_para_produtos()
    verificar_migracao()
