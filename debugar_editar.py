#!/usr/bin/env python3
"""
Script para debugar especificamente a view editar_orcamento
"""
import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema_produtos.settings')
django.setup()

from django.test import Client
from django.contrib.auth import get_user_model
from orcamentos.models import Orcamento
import json

User = get_user_model()

def debugar_editar():
    print("🐛 DEBUGANDO VIEW EDITAR_ORCAMENTO")
    print("=" * 50)
    
    # Buscar orçamento
    orcamento = Orcamento.objects.first()
    if not orcamento:
        print("❌ Nenhum orçamento encontrado!")
        return
    
    print(f"✅ Orçamento encontrado: ID {orcamento.pk}")
    print(f"  - Cliente: {orcamento.cliente.nome_empresa if orcamento.cliente else 'Nenhum'}")
    print(f"  - Vendedor: {orcamento.vendedor}")
    print(f"  - Status: {orcamento.status}")
    print(f"  - Desconto valor: {orcamento.desconto_valor}")
    print(f"  - Desconto %: {orcamento.desconto_percentual}")
    print(f"  - Acréscimo valor: {orcamento.acrescimo_valor}")
    print(f"  - Acréscimo %: {orcamento.acrescimo_percentual}")
    
    # Simular os dados que seriam gerados na view
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
    
    print(f"\n📊 Dados gerados para JSON:")
    for key, value in orcamento_data.items():
        print(f"  - {key}: {value}")
    
    # Tentar converter para JSON
    try:
        orcamento_data_json = json.dumps(orcamento_data)
        print(f"\n✅ JSON gerado com sucesso:")
        print(f"  Tamanho: {len(orcamento_data_json)} caracteres")
        print(f"  Primeiros 200 chars: {orcamento_data_json[:200]}...")
    except Exception as e:
        print(f"\n❌ Erro ao gerar JSON: {e}")
        return
    
    # Testar com cliente real
    client = Client()
    user = User.objects.filter(is_superuser=True).first()
    if not user:
        user = User.objects.first()
    
    client.force_login(user)
    
    print(f"\n🌐 Testando requisição real...")
    response = client.get(f'/orcamentos/{orcamento.pk}/editar/')
    
    if response.status_code == 200:
        content = response.content.decode('utf-8')
        
        # Procurar especificamente pelo JSON no HTML
        import re
        json_match = re.search(r'window\.orcamentoData = ({.*?});', content, re.DOTALL)
        
        if json_match:
            json_str = json_match.group(1)
            print(f"✅ JSON encontrado no HTML:")
            print(f"  Tamanho: {len(json_str)} caracteres")
            print(f"  Conteúdo: {json_str[:200]}...")
            
            # Tentar parsear o JSON
            try:
                parsed_data = json.loads(json_str)
                print(f"✅ JSON válido e parseável")
                print(f"  Cliente ID: {parsed_data.get('cliente_id')}")
                print(f"  Cliente nome: {parsed_data.get('cliente_nome')}")
            except Exception as e:
                print(f"❌ Erro ao parsear JSON: {e}")
        else:
            print(f"❌ JSON não encontrado no HTML")
            # Procurar por qualquer menção a orcamentoData
            if 'orcamentoData' in content:
                lines = content.split('\n')
                for i, line in enumerate(lines):
                    if 'orcamentoData' in line:
                        print(f"  Linha {i}: {line.strip()}")
            else:
                print(f"❌ Nenhuma menção a orcamentoData encontrada")
    else:
        print(f"❌ Erro na requisição: {response.status_code}")
    
    print("\n" + "=" * 50)
    print("🐛 DEBUG CONCLUÍDO")

if __name__ == '__main__':
    debugar_editar()
