#!/usr/bin/env python3
"""
Script para extrair e analisar os erros JavaScript
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
import re

User = get_user_model()

def analisar_erros_js():
    print("🐛 ANALISANDO ERROS JAVASCRIPT")
    print("=" * 50)
    
    # Criar cliente de teste
    client = Client()
    user = User.objects.filter(is_superuser=True).first()
    if not user:
        user = User.objects.first()
    
    client.force_login(user)
    
    print("--- Página NOVO orçamento ---")
    response = client.get('/orcamentos/novo/')
    
    if response.status_code == 200:
        content = response.content.decode('utf-8')
        
        # Procurar por diferentes tipos de problemas
        problemas = []
        
        # 1. Procurar por elementos que podem estar faltando
        elementos_criticos = [
            ('desconto_valor_unificado', 'id="desconto_valor_unificado"'),
            ('desconto_tipo_btn', 'id="desconto_tipo_btn"'),
            ('acrescimo_valor_unificado', 'id="acrescimo_valor_unificado"'),
            ('acrescimo_tipo_btn', 'id="acrescimo_tipo_btn"'),
            ('cliente-busca', 'id="cliente-busca"'),
            ('id_cliente', 'id="id_cliente"'),
            ('id_faixa_preco', 'id="id_faixa_preco"'),
            ('id_forma_pagamento', 'id="id_forma_pagamento"'),
            ('id_status', 'id="id_status"'),
            ('id_data_entrega', 'id="id_data_entrega"'),
            ('id_data_validade', 'id="id_data_validade"'),
        ]
        
        print("Verificando elementos críticos:")
        for nome, selector in elementos_criticos:
            presente = selector in content
            status = "✅" if presente else "❌"
            print(f"  {status} {nome}: {presente}")
            if not presente:
                problemas.append(f"Elemento {nome} não encontrado")
        
        # 2. Procurar por problemas de sintaxe JavaScript
        script_matches = re.findall(r'<script[^>]*>(.*?)</script>', content, re.DOTALL)
        
        print(f"\n{len(script_matches)} blocos de script encontrados")
        
        for i, script in enumerate(script_matches):
            if 'inicializarCamposUnificados' in script or 'hidratarCamposOrcamento' in script:
                print(f"\nAnalisando script principal (bloco {i+1}):")
                
                # Verificar problemas comuns
                if 'getElementById(' in script:
                    # Extrair todas as chamadas getElementById
                    get_element_calls = re.findall(r"getElementById\(['\"]([^'\"]+)['\"]\)", script)
                    print(f"  IDs buscados pelo JavaScript: {len(get_element_calls)}")
                    
                    for element_id in get_element_calls[:10]:  # Mostrar só os primeiros 10
                        presente = f'id="{element_id}"' in content
                        status = "✅" if presente else "❌"
                        print(f"    {status} {element_id}")
                        if not presente:
                            problemas.append(f"JavaScript busca elemento '{element_id}' que não existe")
                
                # Procurar por possíveis erros de sintaxe
                lines = script.split('\n')
                for line_num, line in enumerate(lines):
                    line = line.strip()
                    if line and not line.startswith('//') and not line.startswith('/*'):
                        # Verificar problemas comuns
                        if 'undefined' in line.lower():
                            problemas.append(f"Possível undefined na linha {line_num}: {line[:50]}")
                        if 'null.' in line:
                            problemas.append(f"Possível acesso a null na linha {line_num}: {line[:50]}")
        
        # 3. Verificar se há elementos duplicados
        id_matches = re.findall(r'id="([^"]+)"', content)
        id_counts = {}
        for id_val in id_matches:
            id_counts[id_val] = id_counts.get(id_val, 0) + 1
        
        duplicados = {k: v for k, v in id_counts.items() if v > 1}
        if duplicados:
            print(f"\n❌ IDs duplicados encontrados:")
            for id_dup, count in duplicados.items():
                print(f"  - {id_dup}: {count} vezes")
                problemas.append(f"ID duplicado: {id_dup}")
        else:
            print(f"\n✅ Nenhum ID duplicado")
        
        print(f"\n📋 RESUMO DOS PROBLEMAS ENCONTRADOS:")
        if problemas:
            for i, problema in enumerate(problemas, 1):
                print(f"  {i}. {problema}")
        else:
            print("  ✅ Nenhum problema obvio encontrado!")
            
    else:
        print(f"❌ Erro ao carregar página: {response.status_code}")
    
    print("\n" + "=" * 50)
    print("🐛 ANÁLISE CONCLUÍDA")

if __name__ == '__main__':
    analisar_erros_js()
