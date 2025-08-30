#!/usr/bin/env python3
"""
Teste para verificar se a hidratação dos campos está funcionando corretamente
"""

import os
import sys
import django

# Setup do Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema_produtos.settings')
django.setup()

from orcamentos.models import Orcamento

def testar_hidratacao_orcamento_5():
    print("=== TESTE DE HIDRATAÇÃO - ORÇAMENTO 5 ===\n")
    
    try:
        # Buscar orçamento 5 com todas as relações
        orcamento = Orcamento.objects.select_related(
            'cliente', 'vendedor', 'faixa_preco', 'forma_pagamento'
        ).get(id=5)
        
        print("✓ Orçamento encontrado!")
        print(f"ID: {orcamento.id}")
        print(f"Número: {orcamento.numero}")
        print()
        
        print("=== DADOS QUE DEVEM APARECER NA TELA ===")
        
        # Cliente
        print(f"🔹 CLIENTE:")
        if orcamento.cliente:
            print(f"   ID: {orcamento.cliente.id}")
            print(f"   Nome: {orcamento.cliente.nome_empresa}")
            print(f"   Campo busca deve mostrar: '{orcamento.cliente.nome_empresa}'")
            print(f"   Select hidden deve ter valor: '{orcamento.cliente.id}'")
        else:
            print("   ✗ Nenhum cliente associado")
        print()
        
        # Vendedor
        print(f"🔹 VENDEDOR:")
        if orcamento.vendedor:
            print(f"   ID: {orcamento.vendedor.id}")
            print(f"   Nome: {orcamento.vendedor.first_name} {orcamento.vendedor.last_name}")
            print(f"   Email: {orcamento.vendedor.email}")
            print(f"   Campo readonly deve mostrar o nome do vendedor")
        else:
            print("   ✗ Nenhum vendedor associado")
        print()
        
        # Faixa de Preço
        print(f"🔹 FAIXA DE PREÇO:")
        if orcamento.faixa_preco:
            print(f"   ID: {orcamento.faixa_preco.id}")
            print(f"   Nome: {orcamento.faixa_preco.nome}")
            print(f"   Select deve ter valor: '{orcamento.faixa_preco.id}'")
        else:
            print("   ✗ Nenhuma faixa de preço associada")
        print()
        
        # Forma de Pagamento
        print(f"🔹 FORMA DE PAGAMENTO:")
        if orcamento.forma_pagamento:
            print(f"   ID: {orcamento.forma_pagamento.id}")
            print(f"   Nome: {orcamento.forma_pagamento.nome}")
            print(f"   Select deve ter valor: '{orcamento.forma_pagamento.id}'")
        else:
            print("   ✗ Nenhuma forma de pagamento associada")
        print()
        
        # Status
        print(f"🔹 STATUS:")
        print(f"   Valor: {orcamento.status}")
        print(f"   Select deve ter valor: '{orcamento.status}'")
        print()
        
        # Datas
        print(f"🔹 DATAS:")
        print(f"   Data Entrega: {orcamento.data_entrega}")
        print(f"   Input deve ter valor: '{orcamento.data_entrega}'")
        print(f"   Data Validade: {orcamento.data_validade}")
        print(f"   Input deve ter valor: '{orcamento.data_validade}'")
        print()
        
        # Descontos e Acréscimos
        print(f"🔹 DESCONTOS E ACRÉSCIMOS:")
        print(f"   Desconto Valor: R$ {orcamento.desconto_valor or 0}")
        print(f"   Desconto Percentual: {orcamento.desconto_percentual or 0}%")
        print(f"   Acréscimo Valor: R$ {orcamento.acrescimo_valor or 0}")
        print(f"   Acréscimo Percentual: {orcamento.acrescimo_percentual or 0}%")
        
        # Determinar qual campo deve estar ativo
        if orcamento.desconto_valor and float(orcamento.desconto_valor) > 0:
            print(f"   >>> Campo unificado desconto deve mostrar: {orcamento.desconto_valor} (R$)")
        elif orcamento.desconto_percentual and float(orcamento.desconto_percentual) > 0:
            print(f"   >>> Campo unificado desconto deve mostrar: {orcamento.desconto_percentual} (%)")
        else:
            print(f"   >>> Campo unificado desconto deve estar vazio")
        
        if orcamento.acrescimo_valor and float(orcamento.acrescimo_valor) > 0:
            print(f"   >>> Campo unificado acréscimo deve mostrar: {orcamento.acrescimo_valor} (R$)")
        elif orcamento.acrescimo_percentual and float(orcamento.acrescimo_percentual) > 0:
            print(f"   >>> Campo unificado acréscimo deve mostrar: {orcamento.acrescimo_percentual} (%)")
        else:
            print(f"   >>> Campo unificado acréscimo deve estar vazio")
        
        print()
        print("=== CHECKLIST DE TESTE MANUAL ===")
        print("1. ✓ Abrir http://localhost:8000/orcamentos/5/edit/")
        print("2. ✓ Campo 'Cliente' deve mostrar 'teste'")
        print("3. ✓ Campo 'Faixa de Preço' deve estar selecionado")
        print("4. ✓ Campo 'Forma de Pagamento' deve estar selecionado")
        print("5. ✓ Campo 'Status' deve mostrar 'rascunho'")
        print("6. ✓ Datas devem estar preenchidas")
        print("7. ✓ Desconto deve mostrar 15% no campo unificado")
        print("8. ✓ Acréscimo deve mostrar 50% no campo unificado")
        print("9. ✓ Sidebar deve calcular totais corretamente")
        print("10. ✓ Console do navegador deve mostrar logs de hidratação")
        
        print("\n=== JSON PARA JAVASCRIPT (view) ===")
        import json
        data_js = {
            'cliente_id': orcamento.cliente.id if orcamento.cliente else None,
            'cliente_nome': orcamento.cliente.nome_empresa if orcamento.cliente else '',
            'vendedor_id': orcamento.vendedor.id if orcamento.vendedor else None,
            'vendedor_nome': f"{orcamento.vendedor.first_name} {orcamento.vendedor.last_name}".strip() if orcamento.vendedor else '',
            'faixa_preco_id': orcamento.faixa_preco.id if orcamento.faixa_preco else None,
            'forma_pagamento_id': orcamento.forma_pagamento.id if orcamento.forma_pagamento else None,
            'status': orcamento.status,
            'data_entrega': orcamento.data_entrega.isoformat() if orcamento.data_entrega else None,
            'data_validade': orcamento.data_validade.isoformat() if orcamento.data_validade else None,
            'desconto_valor': float(orcamento.desconto_valor) if orcamento.desconto_valor else 0,
            'desconto_percentual': float(orcamento.desconto_percentual) if orcamento.desconto_percentual else 0,
            'acrescimo_valor': float(orcamento.acrescimo_valor) if orcamento.acrescimo_valor else 0,
            'acrescimo_percentual': float(orcamento.acrescimo_percentual) if orcamento.acrescimo_percentual else 0,
        }
        print(json.dumps(data_js, indent=2, ensure_ascii=False))
        
        return True
        
    except Orcamento.DoesNotExist:
        print("✗ Orçamento 5 não encontrado")
        return False
    except Exception as e:
        print(f"✗ Erro: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    sucesso = testar_hidratacao_orcamento_5()
    if sucesso:
        print("\n✅ Teste concluído - Verifique a tela no navegador!")
    else:
        print("\n❌ Teste falhou!")
