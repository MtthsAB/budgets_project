#!/usr/bin/env python3
"""
Script para investigar item específico do orçamento
"""

import os
import sys
import django

# Configurar Django
sys.path.append('/home/matas/projetos/Project')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema_produtos.settings')
django.setup()

from orcamentos.models import Orcamento, OrcamentoItem
from produtos.models import Produto, Cadeira

def main():
    print("=== INVESTIGANDO ITEM MIA BR ===")
    
    # Buscar o item específico
    item = OrcamentoItem.objects.filter(produto__nome_produto__icontains='MIA').first()
    
    if item:
        print(f"\n📋 ITEM ENCONTRADO:")
        print(f"   ID: {item.id}")
        print(f"   Produto: {item.produto}")
        print(f"   Produto ID: {item.produto.id}")
        print(f"   Quantidade: {item.quantidade}")
        print(f"   Preço Unitário: R$ {item.preco_unitario}")
        print(f"   Total: R$ {item.get_total()}")
        
        print(f"\n🔍 DETALHES DO PRODUTO:")
        produto = item.produto
        print(f"   Nome: {produto.nome_produto}")
        print(f"   Referência: {produto.ref_produto}")
        print(f"   Tipo: {produto.id_tipo_produto}")
        print(f"   Preço na tabela Produto: R$ {produto.preco}")
        print(f"   Ativo: {produto.ativo}")
        
        # Verificar se existe na tabela específica
        try:
            cadeira = Cadeira.objects.get(ref_cadeira=produto.ref_produto)
            print(f"\n🪑 CADEIRA ESPECÍFICA:")
            print(f"   Nome: {cadeira.nome}")
            print(f"   Referência: {cadeira.ref_cadeira}")
            print(f"   Preço: R$ {cadeira.preco}")
            print(f"   Ativo: {cadeira.ativo}")
        except Cadeira.DoesNotExist:
            print(f"\n❌ Cadeira não encontrada na tabela específica")
            
    else:
        print("❌ Item MIA BR não encontrado")
        
    # Verificar todos os itens do orçamento
    print(f"\n📊 TODOS OS ITENS DE TODOS OS ORÇAMENTOS:")
    orcamentos = Orcamento.objects.all()
    
    for orcamento in orcamentos:
        print(f"\n🔢 ORÇAMENTO {orcamento.numero}:")
        itens = orcamento.itens.all()
        total_orcamento = 0
        
        if not itens:
            print("   Nenhum item encontrado")
            continue
            
        for item in itens:
            print(f"   {item.produto.nome_produto} - Qtd: {item.quantidade} - Preço: R$ {item.preco_unitario} - Total: R$ {item.get_total()}")
            total_orcamento += item.get_total() or 0
            
        print(f"💰 TOTAL CALCULADO: R$ {total_orcamento}")
        print(f"💰 TOTAL NO ORÇAMENTO: R$ {getattr(orcamento, 'total', 'N/A')}")
        
    # Procurar por itens que contenham "MIA" ou "CD120"
    print(f"\n🔍 PROCURANDO ITENS COM 'MIA' OU 'CD120':")
    itens_mia = OrcamentoItem.objects.filter(
        produto__nome_produto__icontains='MIA'
    ) | OrcamentoItem.objects.filter(
        produto__ref_produto__icontains='CD120'
    )
    
    for item in itens_mia:
        print(f"   Encontrado: {item.produto.nome_produto} - {item.produto.ref_produto}")
        print(f"   Preço: R$ {item.preco_unitario} - Total: R$ {item.get_total()}")

if __name__ == '__main__':
    main()
