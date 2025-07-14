#!/usr/bin/env python
"""
Script para testar o fluxo de seleção de sofás no sistema de orçamentos.
Verifica se os dados estão sendo corretamente enviados e processados.
"""

import os
import django
import json
from django.test import Client
from django.contrib.auth import get_user_model

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema_produtos.settings')
django.setup()

from orcamentos.models import Orcamento, OrcamentoItem
from produtos.models import Produto, Modulo, Acessorio

def testar_endpoint_detalhes_produto():
    """Testa se o endpoint de detalhes do produto retorna os dados corretos para sofás."""
    print("=== Testando endpoint de detalhes do produto ===")
    
    client = Client()
    
    # Buscar um produto do tipo sofá
    try:
        # Buscar produtos que são sofás
        produtos = Produto.objects.filter(
            id_tipo_produto__nome__icontains='sofá'
        ) | Produto.objects.filter(
            id_tipo_produto__nome__icontains='sofa'
        )
        sofa = produtos.first()
        
        if not sofa:
            print("❌ Nenhum sofá encontrado no banco de dados")
            return False
            
        print(f"✅ Sofá encontrado: {sofa.nome_produto}")
        
        # Fazer requisição ao endpoint
        response = client.get(f'/orcamentos/detalhes-produto/', {'produto_id': sofa.id})
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Endpoint respondeu com status 200")
            print(f"📦 Dados retornados: {json.dumps(data, indent=2, ensure_ascii=False)}")
            
            # Verificar se contém os campos esperados
            campos_esperados = ['produto', 'modulos', 'acessorios']
            for campo in campos_esperados:
                if campo in data:
                    print(f"✅ Campo '{campo}' presente")
                else:
                    print(f"❌ Campo '{campo}' ausente")
                    
            return True
        else:
            print(f"❌ Endpoint retornou status {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Erro ao testar endpoint: {e}")
        return False

def verificar_modelos_sofa():
    """Verifica se existem módulos e acessórios para sofás."""
    print("\n=== Verificando dados de sofás ===")
    
    # Buscar produtos que são sofás usando o método eh_sofa()
    produtos = Produto.objects.all()
    sofas = [p for p in produtos if p.eh_sofa()]
    print(f"📊 Total de sofás: {len(sofas)}")
    
    for sofa in sofas[:3]:  # Verificar os primeiros 3
        print(f"\n🛋️  Sofá: {sofa.nome_produto}")
        
        modulos = Modulo.objects.filter(produto=sofa)
        print(f"   📦 Módulos: {modulos.count()}")
        for modulo in modulos[:2]:
            print(f"      - {modulo.nome}")
            
        acessorios = Acessorio.objects.filter(produtos=sofa)
        print(f"   🎨 Acessórios: {acessorios.count()}")
        for acessorio in acessorios[:2]:
            print(f"      - {acessorio.nome}")

def verificar_estrutura_orcamento():
    """Verifica se a estrutura de orçamentos suporta os dados dinâmicos."""
    print("\n=== Verificando estrutura de orçamentos ===")
    
    # Verificar se existe pelo menos um orçamento para análise
    orcamento = Orcamento.objects.first()
    if orcamento:
        print(f"✅ Orçamento exemplo encontrado: {orcamento.id}")
        
        itens = OrcamentoItem.objects.filter(orcamento=orcamento)
        print(f"📋 Itens no orçamento: {itens.count()}")
        
        for item in itens[:2]:
            print(f"   📦 Item: {item.produto.nome if item.produto else 'N/A'}")
            if hasattr(item, 'dados_dinamicos') and item.dados_dinamicos:
                print(f"      📊 Dados dinâmicos: {json.dumps(item.dados_dinamicos, indent=6, ensure_ascii=False)}")
    else:
        print("⚠️  Nenhum orçamento encontrado no banco")

if __name__ == "__main__":
    print("🔧 Iniciando testes do fluxo de sofás...\n")
    
    # Executar testes
    testar_endpoint_detalhes_produto()
    verificar_modelos_sofa()
    verificar_estrutura_orcamento()
    
    print("\n✅ Testes concluídos!")
