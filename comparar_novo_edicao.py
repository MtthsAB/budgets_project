#!/usr/bin/env python3
"""
Script para comparar as páginas novo vs edição
"""

import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema_produtos.settings')
django.setup()

from django.test import Client
from authentication.models import CustomUser
import re

def comparar_paginas():
    """Comparar páginas novo vs edição"""
    
    print("🔍 === COMPARAÇÃO DETALHADA: NOVO VS EDIÇÃO ===")
    
    # Fazer login
    user = CustomUser.objects.get(email='teste@teste.com')
    client = Client()
    client.force_login(user)
    
    # Acessar ambas as páginas
    print("📄 Acessando páginas...")
    response_novo = client.get('/orcamentos/novo/')
    response_edicao = client.get('/orcamentos/5/editar/')
    
    if response_novo.status_code != 200 or response_edicao.status_code != 200:
        print(f"❌ Erro de acesso: novo={response_novo.status_code}, edição={response_edicao.status_code}")
        return False
    
    content_novo = response_novo.content.decode('utf-8')
    content_edicao = response_edicao.content.decode('utf-8')
    
    print("✅ Ambas as páginas acessadas")
    
    # 1. Comparar presença de elementos essenciais
    print("\n1️⃣ ELEMENTOS ESSENCIAIS:")
    
    elementos = [
        ('id="cliente-busca"', 'Campo busca cliente'),
        ('id="desconto_valor_unificado"', 'Input desconto unificado'),
        ('id="acrescimo_valor_unificado"', 'Input acréscimo unificado'),
        ('id="desconto_tipo_btn"', 'Botão tipo desconto'),
        ('id="acrescimo_tipo_btn"', 'Botão tipo acréscimo'),
        ('hidratarCamposOrcamento', 'Função hidratação'),
        ('hidratarDescontoAcrescimo', 'Função desc/acr'),
        ('document.addEventListener', 'Event listeners'),
    ]
    
    for elemento, descricao in elementos:
        novo_tem = elemento in content_novo
        edicao_tem = elemento in content_edicao
        
        if novo_tem and edicao_tem:
            print(f"   ✅ {descricao}")
        elif novo_tem and not edicao_tem:
            print(f"   ❌ {descricao} - FALTA NA EDIÇÃO")
        elif not novo_tem and edicao_tem:
            print(f"   ⚠️ {descricao} - SÓ NA EDIÇÃO")
        else:
            print(f"   ❌ {descricao} - FALTA EM AMBAS")
    
    # 2. Comparar estrutura dos campos
    print("\n2️⃣ ESTRUTURA DOS CAMPOS:")
    
    # Extrair seção do cliente
    cliente_novo = re.search(r'<div[^>]*cliente-expandido[^>]*>.*?</div>', content_novo, re.DOTALL)
    cliente_edicao = re.search(r'<div[^>]*cliente-expandido[^>]*>.*?</div>', content_edicao, re.DOTALL)
    
    if cliente_novo and cliente_edicao:
        print("   ✅ Seção cliente encontrada em ambas")
        # Comparar estrutura interna
        if 'cliente-busca' in cliente_novo.group(0) and 'cliente-busca' in cliente_edicao.group(0):
            print("   ✅ Input cliente-busca presente em ambas")
        else:
            print("   ❌ Input cliente-busca com diferenças")
    else:
        print("   ❌ Seção cliente com problemas")
    
    # 3. Comparar JavaScript de hidratação
    print("\n3️⃣ JAVASCRIPT DE HIDRATAÇÃO:")
    
    # Verificar se a página novo tem hidratação (não deveria ter)
    if 'window.orcamentoData' in content_novo:
        print("   ⚠️ Página NOVO tem window.orcamentoData (inesperado)")
    else:
        print("   ✅ Página NOVO sem dados de hidratação (correto)")
    
    if 'window.orcamentoData' in content_edicao:
        print("   ✅ Página EDIÇÃO tem window.orcamentoData")
        
        # Extrair e validar dados
        pattern = r'window\.orcamentoData = ({.*?});'
        match = re.search(pattern, content_edicao, re.DOTALL)
        if match:
            import json
            try:
                data = json.loads(match.group(1))
                print(f"   ✅ JSON válido com {len(data)} campos")
                
                # Verificar campos específicos
                campos_importantes = ['cliente_id', 'cliente_nome', 'desconto_valor', 'desconto_percentual', 'acrescimo_valor', 'acrescimo_percentual']
                for campo in campos_importantes:
                    if campo in data:
                        print(f"      ✅ {campo}: {data[campo]}")
                    else:
                        print(f"      ❌ {campo}: AUSENTE")
            except json.JSONDecodeError as e:
                print(f"   ❌ JSON inválido: {e}")
    else:
        print("   ❌ Página EDIÇÃO sem window.orcamentoData")
    
    # 4. Verificar ordem de execução do JavaScript
    print("\n4️⃣ ORDEM DE EXECUÇÃO:")
    
    # Procurar pela sequência de inicialização
    init_patterns = [
        (r'document\.addEventListener\(\'DOMContentLoaded\'.*?{', 'DOMContentLoaded listener'),
        (r'if \(window\.orcamentoData\)', 'Verificação de dados'),
        (r'hidratarCamposOrcamento\(\);', 'Chamada de hidratação'),
        (r'setTimeout.*hidratarCamposOrcamento', 'Timeout de hidratação'),
    ]
    
    for pattern, descricao in init_patterns:
        matches_edicao = re.findall(pattern, content_edicao, re.DOTALL)
        if matches_edicao:
            print(f"   ✅ {descricao} - {len(matches_edicao)} ocorrência(s)")
        else:
            print(f"   ❌ {descricao} - NÃO ENCONTRADO")
    
    # 5. Salvar comparação detalhada
    print("\n5️⃣ SALVANDO COMPARAÇÃO:")
    
    with open('/tmp/comparacao_novo.html', 'w', encoding='utf-8') as f:
        f.write(content_novo)
    
    with open('/tmp/comparacao_edicao.html', 'w', encoding='utf-8') as f:
        f.write(content_edicao)
    
    # Criar diff básico das seções importantes
    diff_report = f"""
=== RELATÓRIO DE COMPARAÇÃO ===

ELEMENTOS ESSENCIAIS:
- Novo: {len([e for e, _ in elementos if e in content_novo])} de {len(elementos)}
- Edição: {len([e for e, _ in elementos if e in content_edicao])} de {len(elementos)}

DADOS DE HIDRATAÇÃO:
- Novo: {'SIM' if 'window.orcamentoData' in content_novo else 'NÃO'}
- Edição: {'SIM' if 'window.orcamentoData' in content_edicao else 'NÃO'}

TAMANHOS:
- Novo: {len(content_novo)} caracteres
- Edição: {len(content_edicao)} caracteres

ESTRUTURA:
- Ambas usam o mesmo template: {content_novo.count('<form') == content_edicao.count('<form')}
- Script blocks novo: {content_novo.count('<script')}
- Script blocks edição: {content_edicao.count('<script')}
"""
    
    with open('/tmp/diff_report.txt', 'w', encoding='utf-8') as f:
        f.write(diff_report)
    
    print("   💾 Arquivos salvos:")
    print("      - /tmp/comparacao_novo.html")
    print("      - /tmp/comparacao_edicao.html")
    print("      - /tmp/diff_report.txt")
    
    return True

if __name__ == '__main__':
    comparar_paginas()
    print("\n🔍 PRÓXIMOS PASSOS:")
    print("1. Compare os arquivos HTML gerados")
    print("2. Procure por diferenças estruturais")
    print("3. Verifique se o JavaScript está sendo executado na ordem correta")
