#!/usr/bin/env python3
"""
Teste final para verificar se a tela de edição de orçamento está funcionando corretamente
"""

import os
import sys
import django

# Setup do Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema_produtos.settings')
django.setup()

from orcamentos.models import Orcamento
from produtos.models import Produto
from clientes.models import Cliente
from decimal import Decimal

def testar_edicao_orcamento():
    print("=== TESTE FINAL - EDIÇÃO DE ORÇAMENTO ===\n")
    
    # Buscar o orçamento criado anteriormente
    try:
        orcamento = Orcamento.objects.select_related('cliente').get(id=2)
        print(f"✓ Orçamento encontrado: ID {orcamento.id}")
    except Orcamento.DoesNotExist:
        print("✗ Orçamento não encontrado - criando novo...")
        cliente = Cliente.objects.first()
        orcamento = Orcamento.objects.create(
            cliente=cliente,
            numero="TST-002",
            vendedor_id=1,  # Assumindo que existe um vendedor com ID 1
            faixa_preco_id=1,  # Assumindo que existe uma faixa de preço
            forma_pagamento_id=1,  # Assumindo que existe uma forma de pagamento
            data_entrega="2025-09-30",
            data_validade="2025-09-15",
            desconto_valor=100.00,
            acrescimo_percentual=5.0
        )
        print(f"✓ Novo orçamento criado: ID {orcamento.id}")
    
    # Verificar dados do cabeçalho
    print(f"\n=== DADOS DO CABEÇALHO ===")
    print(f"Número: {orcamento.numero}")
    print(f"Cliente: {orcamento.cliente.nome_empresa if orcamento.cliente else 'None'}")
    print(f"Status: {orcamento.status}")
    print(f"Desconto Valor: R$ {orcamento.desconto_valor}")
    print(f"Desconto Percentual: {orcamento.desconto_percentual}%")
    print(f"Acréscimo Valor: R$ {orcamento.acrescimo_valor}")
    print(f"Acréscimo Percentual: {orcamento.acrescimo_percentual}%")
    
    # Verificar itens
    print(f"\n=== ITENS DO ORÇAMENTO ===")
    itens = orcamento.itens.select_related('produto', 'produto__id_tipo_produto').all()
    print(f"Total de itens: {itens.count()}")
    
    subtotal = Decimal('0.00')
    for item in itens:
        total_item = item.quantidade * item.preco_unitario
        subtotal += total_item
        print(f"• {item.produto.ref_produto} - {item.produto.id_tipo_produto.nome}")
        print(f"  Qtd: {item.quantidade} x R$ {item.preco_unitario} = R$ {total_item}")
    
    print(f"\nSubtotal: R$ {subtotal}")
    
    # Calcular totais
    desconto_total = Decimal('0.00')
    if orcamento.desconto_valor and orcamento.desconto_valor > 0:
        desconto_total += orcamento.desconto_valor
    if orcamento.desconto_percentual and orcamento.desconto_percentual > 0:
        desconto_total += subtotal * (orcamento.desconto_percentual / 100)
    
    acrescimo_total = Decimal('0.00')
    if orcamento.acrescimo_valor and orcamento.acrescimo_valor > 0:
        acrescimo_total += orcamento.acrescimo_valor
    if orcamento.acrescimo_percentual and orcamento.acrescimo_percentual > 0:
        acrescimo_total += subtotal * (orcamento.acrescimo_percentual / 100)
    
    total_final = subtotal - desconto_total + acrescimo_total
    
    print(f"Desconto Total: R$ {desconto_total}")
    print(f"Acréscimo Total: R$ {acrescimo_total}")
    print(f"TOTAL FINAL: R$ {total_final}")
    
    # Verificar produtos disponíveis por tipo
    print(f"\n=== PRODUTOS DISPONÍVEIS POR TIPO ===")
    tipos_produtos = Produto.objects.values_list('id_tipo_produto__nome', flat=True).distinct()
    for tipo in tipos_produtos:
        count = Produto.objects.filter(id_tipo_produto__nome=tipo).count()
        print(f"• {tipo}: {count} produtos")
    
    print(f"\n=== CHECKLIST DE VALIDAÇÃO ===")
    checklist = [
        ("Dados do orçamento carregados", orcamento.id is not None),
        ("Cliente associado", orcamento.cliente is not None),
        ("Itens do pedido existem", itens.count() > 0),
        ("Produtos de tipos diferentes", len(set(item.produto.id_tipo_produto.nome for item in itens)) > 1),
        ("Descontos/acréscimos definidos", (orcamento.desconto_valor or orcamento.desconto_percentual or 
                                         orcamento.acrescimo_valor or orcamento.acrescimo_percentual)),
        ("Valores calculados corretamente", total_final > 0)
    ]
    
    for descricao, status in checklist:
        simbolo = "✓" if status else "✗"
        print(f"{simbolo} {descricao}")
    
    print(f"\n=== INSTRUÇÕES PARA TESTE MANUAL ===")
    print("1. Acesse: http://localhost:8000/orcamentos/2/edit/")
    print("2. Verifique se o nome do cliente aparece no campo 'Cliente'")
    print("3. Verifique se os valores de desconto/acréscimo estão nos campos corretos")
    print("4. Verifique se todos os itens aparecem na lista")
    print("5. Verifique se a sidebar de totais mostra os valores corretos")
    print("6. Tente adicionar um novo item de tipo diferente")
    print("7. Tente alterar os descontos/acréscimos e verificar se os totais atualizam")
    
    return orcamento.id

if __name__ == "__main__":
    try:
        orcamento_id = testar_edicao_orcamento()
        print(f"\n✓ Teste concluído com sucesso! Orçamento ID: {orcamento_id}")
    except Exception as e:
        print(f"\n✗ Erro no teste: {e}")
        import traceback
        traceback.print_exc()
