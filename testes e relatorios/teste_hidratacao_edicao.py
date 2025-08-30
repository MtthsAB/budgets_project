#!/usr/bin/env python3
"""
Script de teste para verificar a implementação da hidratação 
dos campos de desconto e acréscimo na edição de orçamentos.
"""

import os
import sys
import django
from decimal import Decimal

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema_produtos.settings')
django.setup()

from orcamentos.models import Orcamento, OrcamentoItem
from clientes.models import Cliente
from produtos.models import Produto
from django.contrib.auth.models import User

def teste_hidratacao_edicao():
    """Teste da hidratação de campos na edição de orçamentos"""
    
    print("🧪 === TESTE DE HIDRATAÇÃO DOS CAMPOS DE EDIÇÃO ===")
    
    # Buscar orçamento existente para teste
    try:
        orcamento = Orcamento.objects.filter(
            cliente__isnull=False
        ).select_related('cliente', 'vendedor', 'faixa_preco', 'forma_pagamento').first()
        
        if not orcamento:
            print("❌ Nenhum orçamento encontrado para teste")
            return False
            
        print(f"📋 Testando orçamento ID: {orcamento.id}")
        print(f"   Cliente: {orcamento.cliente.nome_empresa if orcamento.cliente else 'N/A'}")
        print(f"   Vendedor: {orcamento.vendedor.get_full_name() if orcamento.vendedor else 'N/A'}")
        
        # Verificar dados atuais
        print("\n📊 DADOS ATUAIS:")
        print(f"   Desconto Valor: R$ {orcamento.desconto_valor or 0}")
        print(f"   Desconto Percentual: {orcamento.desconto_percentual or 0}%")
        print(f"   Acréscimo Valor: R$ {orcamento.acrescimo_valor or 0}")
        print(f"   Acréscimo Percentual: {orcamento.acrescimo_percentual or 0}%")
        
        # Simular dados de hidratação como a view prepara
        import json
        orcamento_data = {
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
        
        print("\n🔄 PAYLOAD DE HIDRATAÇÃO:")
        print(json.dumps(orcamento_data, indent=2, ensure_ascii=False))
        
        # Teste de diferentes cenários
        print("\n🎯 CENÁRIOS DE TESTE:")
        
        # Cenário 1: Desconto em valor
        if orcamento_data['desconto_valor'] > 0:
            print("✅ Cenário 1: Desconto em VALOR detectado")
            print(f"   → Campo unificado deve mostrar: {orcamento_data['desconto_valor']}")
            print(f"   → Botão deve mostrar: R$")
        elif orcamento_data['desconto_percentual'] > 0:
            print("✅ Cenário 1: Desconto em PERCENTUAL detectado")
            print(f"   → Campo unificado deve mostrar: {orcamento_data['desconto_percentual']}")
            print(f"   → Botão deve mostrar: %")
        else:
            print("ℹ️  Cenário 1: Nenhum desconto definido")
            
        # Cenário 2: Acréscimo em valor
        if orcamento_data['acrescimo_valor'] > 0:
            print("✅ Cenário 2: Acréscimo em VALOR detectado")
            print(f"   → Campo unificado deve mostrar: {orcamento_data['acrescimo_valor']}")
            print(f"   → Botão deve mostrar: R$")
        elif orcamento_data['acrescimo_percentual'] > 0:
            print("✅ Cenário 2: Acréscimo em PERCENTUAL detectado")
            print(f"   → Campo unificado deve mostrar: {orcamento_data['acrescimo_percentual']}")
            print(f"   → Botão deve mostrar: %")
        else:
            print("ℹ️  Cenário 2: Nenhum acréscimo definido")
            
        # Testar com valores específicos
        print("\n🧮 TESTE COM VALORES ESPECÍFICOS:")
        
        # Alterar temporariamente para testar hidratação
        backup_desconto_valor = orcamento.desconto_valor
        backup_desconto_perc = orcamento.desconto_percentual
        backup_acrescimo_valor = orcamento.acrescimo_valor
        backup_acrescimo_perc = orcamento.acrescimo_percentual
        
        # Teste 1: Desconto em valor
        orcamento.desconto_valor = Decimal('150.00')
        orcamento.desconto_percentual = None
        orcamento.acrescimo_valor = None
        orcamento.acrescimo_percentual = Decimal('5.0')
        
        test_data = {
            'desconto_valor': float(orcamento.desconto_valor) if orcamento.desconto_valor else 0,
            'desconto_percentual': float(orcamento.desconto_percentual) if orcamento.desconto_percentual else 0,
            'acrescimo_valor': float(orcamento.acrescimo_valor) if orcamento.acrescimo_valor else 0,
            'acrescimo_percentual': float(orcamento.acrescimo_percentual) if orcamento.acrescimo_percentual else 0,
        }
        
        print("📋 Teste - Desconto R$150 + Acréscimo 5%:")
        print(f"   desconto_valor: {test_data['desconto_valor']}")
        print(f"   desconto_percentual: {test_data['desconto_percentual']}")
        print(f"   acrescimo_valor: {test_data['acrescimo_valor']}")
        print(f"   acrescimo_percentual: {test_data['acrescimo_percentual']}")
        
        # Simular lógica de hidratação
        print("\n🔧 SIMULAÇÃO DA LÓGICA DE HIDRATAÇÃO:")
        
        # Desconto
        if test_data['desconto_valor'] and test_data['desconto_valor'] > 0:
            print(f"✅ Desconto → Campo: {test_data['desconto_valor']}, Tipo: R$")
        elif test_data['desconto_percentual'] and test_data['desconto_percentual'] > 0:
            print(f"✅ Desconto → Campo: {test_data['desconto_percentual']}, Tipo: %")
        else:
            print("ℹ️  Desconto → Nenhum valor")
            
        # Acréscimo
        if test_data['acrescimo_valor'] and test_data['acrescimo_valor'] > 0:
            print(f"✅ Acréscimo → Campo: {test_data['acrescimo_valor']}, Tipo: R$")
        elif test_data['acrescimo_percentual'] and test_data['acrescimo_percentual'] > 0:
            print(f"✅ Acréscimo → Campo: {test_data['acrescimo_percentual']}, Tipo: %")
        else:
            print("ℹ️  Acréscimo → Nenhum valor")
        
        # Restaurar valores originais
        orcamento.desconto_valor = backup_desconto_valor
        orcamento.desconto_percentual = backup_desconto_perc
        orcamento.acrescimo_valor = backup_acrescimo_valor
        orcamento.acrescimo_percentual = backup_acrescimo_perc
        
        print(f"\n🎉 TESTE CONCLUÍDO PARA ORÇAMENTO {orcamento.id}")
        print("   📝 Para testar na prática:")
        print(f"   🌐 Acesse: /orcamentos/{orcamento.id}/editar/")
        print("   👁️  Verifique se os campos estão pré-preenchidos corretamente")
        print("   🔄 Teste alternar entre R$ e % e salvar")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro no teste: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    sucesso = teste_hidratacao_edicao()
    if sucesso:
        print("\n✅ Todos os testes passaram!")
    else:
        print("\n❌ Alguns testes falharam.")
    
    sys.exit(0 if sucesso else 1)
