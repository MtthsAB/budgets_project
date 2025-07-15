#!/usr/bin/env python3
"""
Script para testar adição de item com preço
"""

import os
import sys
import django

# Configurar Django
sys.path.append('/home/matas/projetos/Project')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema_produtos.settings')
django.setup()

from orcamentos.models import Orcamento, OrcamentoItem
from produtos.models import Produto, Cadeira, TipoItem
from decimal import Decimal

def main():
    print("=== TESTE DE ADIÇÃO DE ITEM COM PREÇO ===")
    
    # Buscar o último orçamento
    orcamento = Orcamento.objects.order_by('-id').first()
    print(f"📋 Último orçamento: {orcamento.numero}")
    
    # Buscar uma cadeira específica
    cadeira = Cadeira.objects.filter(ativo=True).first()
    if not cadeira:
        print("❌ Nenhuma cadeira encontrada")
        return
        
    print(f"🪑 Cadeira encontrada: {cadeira.nome} - R$ {cadeira.preco}")
    
    # Verificar se existe produto correspondente na tabela Produto
    try:
        tipo_cadeira = TipoItem.objects.filter(nome__icontains='Cadeira').first()
        if not tipo_cadeira:
            print("❌ Tipo 'Cadeira' não encontrado")
            return
            
        # Buscar ou criar produto na tabela genérica
        produto, created = Produto.objects.get_or_create(
            ref_produto=cadeira.ref_cadeira,
            defaults={
                'nome_produto': cadeira.nome,
                'id_tipo_produto': tipo_cadeira,
                'preco': cadeira.preco,
                'ativo': True
            }
        )
        
        if created:
            print(f"✅ Produto criado na tabela genérica: {produto.nome_produto}")
        else:
            print(f"📦 Produto já existe na tabela genérica: {produto.nome_produto}")
            
        # Criar item no orçamento
        item = OrcamentoItem.objects.create(
            orcamento=orcamento,
            produto=produto,
            quantidade=1,
            preco_unitario=cadeira.preco,
            observacoes="Teste automatizado de adição de item"
        )
        
        print(f"✅ Item adicionado com sucesso!")
        print(f"   Produto: {item.produto.nome_produto}")
        print(f"   Quantidade: {item.quantidade}")
        print(f"   Preço Unitário: R$ {item.preco_unitario}")
        print(f"   Total: R$ {item.get_total()}")
        
    except Exception as e:
        print(f"❌ Erro ao criar item: {e}")

if __name__ == '__main__':
    main()
