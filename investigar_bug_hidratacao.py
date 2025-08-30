#!/usr/bin/env python3
"""
Script para investigar o bug de hidratação dos campos na edição
"""

import os
import sys
import django
import requests
import re
import json

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema_produtos.settings')
django.setup()

from django.test import Client
from authentication.models import CustomUser
from orcamentos.models import Orcamento

def investigar_bug_hidratacao():
    """Investigar detalhadamente o bug de hidratação"""
    
    print("🔍 === INVESTIGAÇÃO DO BUG DE HIDRATAÇÃO ===")
    
    # 1. Verificar dados no banco
    print("\n1️⃣ VERIFICANDO DADOS NO BANCO:")
    try:
        orcamento = Orcamento.objects.select_related('cliente', 'vendedor').get(id=5)
        print(f"   ✅ Orçamento encontrado: ID {orcamento.id}")
        print(f"   📋 Cliente: {orcamento.cliente.nome_empresa if orcamento.cliente else 'NENHUM'}")
        print(f"   💰 Desconto valor: R$ {orcamento.desconto_valor or 0}")
        print(f"   📊 Desconto %: {orcamento.desconto_percentual or 0}%")
        print(f"   💰 Acréscimo valor: R$ {orcamento.acrescimo_valor or 0}")
        print(f"   📊 Acréscimo %: {orcamento.acrescimo_percentual or 0}%")
    except Exception as e:
        print(f"   ❌ Erro ao buscar orçamento: {e}")
        return False
    
    # 2. Fazer login e acessar página
    print("\n2️⃣ ACESSANDO PÁGINA DE EDIÇÃO:")
    user = CustomUser.objects.get(email='teste@teste.com')
    client = Client()
    client.force_login(user)
    
    response = client.get('/orcamentos/5/editar/')
    
    if response.status_code != 200:
        print(f"   ❌ Erro ao acessar página: {response.status_code}")
        return False
    
    print(f"   ✅ Página acessada: status {response.status_code}")
    
    content = response.content.decode('utf-8')
    
    # 3. Verificar contexto da view
    print("\n3️⃣ VERIFICANDO CONTEXTO DA VIEW:")
    
    # Verificar se window.orcamentoData está sendo injetado
    if 'window.orcamentoData' in content:
        print("   ✅ window.orcamentoData encontrado")
        
        # Extrair e analisar JSON
        pattern = r'window\.orcamentoData = ({.*?});'
        match = re.search(pattern, content, re.DOTALL)
        
        if match:
            json_str = match.group(1)
            try:
                data = json.loads(json_str)
                print("   ✅ JSON parseado com sucesso")
                print("   📋 Dados extraídos:")
                for key, value in data.items():
                    print(f"      {key}: {value}")
            except json.JSONDecodeError as e:
                print(f"   ❌ Erro ao parsear JSON: {e}")
                print(f"   📄 JSON bruto: {json_str[:200]}...")
        else:
            print("   ❌ Não foi possível extrair JSON")
    else:
        print("   ❌ window.orcamentoData NÃO encontrado no HTML")
    
    # 4. Verificar elementos HTML
    print("\n4️⃣ VERIFICANDO ELEMENTOS HTML:")
    
    elementos_essenciais = [
        ('id="cliente-busca"', 'Campo de busca do cliente'),
        ('id="id_cliente"', 'Select hidden do cliente'),
        ('id="desconto_valor_unificado"', 'Input unificado de desconto'),
        ('id="acrescimo_valor_unificado"', 'Input unificado de acréscimo'),
        ('id="desconto_tipo_btn"', 'Botão tipo desconto'),
        ('id="acrescimo_tipo_btn"', 'Botão tipo acréscimo'),
    ]
    
    for elemento, descricao in elementos_essenciais:
        if elemento in content:
            print(f"   ✅ {descricao}")
        else:
            print(f"   ❌ {descricao} - NÃO ENCONTRADO")
    
    # 5. Verificar JavaScript
    print("\n5️⃣ VERIFICANDO JAVASCRIPT:")
    
    funcoes_js = [
        ('function hidratarCamposOrcamento', 'Função principal de hidratação'),
        ('function hidratarDescontoAcrescimo', 'Função específica desc/acr'),
        ('hidratarCamposOrcamento();', 'Chamada da hidratação'),
        ('document.addEventListener(\'DOMContentLoaded\'', 'Event listener DOMContentLoaded'),
    ]
    
    for funcao, descricao in funcoes_js:
        if funcao in content:
            print(f"   ✅ {descricao}")
        else:
            print(f"   ❌ {descricao} - NÃO ENCONTRADO")
    
    # 6. Verificar estrutura específica de hidratação
    print("\n6️⃣ VERIFICANDO ESTRUTURA DE HIDRATAÇÃO:")
    
    # Procurar pela condição de hidratação
    if 'if (window.orcamentoData)' in content:
        print("   ✅ Condição de hidratação encontrada")
    else:
        print("   ❌ Condição de hidratação NÃO encontrada")
    
    # Procurar timeout de hidratação
    if 'setTimeout' in content and 'hidratarCamposOrcamento' in content:
        print("   ✅ Timeout de hidratação encontrado")
    else:
        print("   ❌ Timeout de hidratação NÃO encontrado")
    
    # 7. Extrair e analisar seção crítica do HTML
    print("\n7️⃣ EXTRAINDO SEÇÕES CRÍTICAS:")
    
    # Procurar seção do cliente
    cliente_match = re.search(r'<div[^>]*cliente-expandido[^>]*>.*?</div>', content, re.DOTALL)
    if cliente_match:
        print("   ✅ Seção do cliente encontrada")
        cliente_html = cliente_match.group(0)
        if 'cliente-busca' in cliente_html:
            print("   ✅ Input cliente-busca dentro da seção")
        else:
            print("   ❌ Input cliente-busca NÃO encontrado na seção")
    else:
        print("   ❌ Seção do cliente NÃO encontrada")
    
    # Procurar seções de desconto/acréscimo
    desconto_match = re.search(r'<div[^>]*col-md-6[^>]*>.*?Desconto.*?</div>', content, re.DOTALL)
    if desconto_match:
        print("   ✅ Seção de desconto encontrada")
    else:
        print("   ❌ Seção de desconto NÃO encontrada")
    
    # 8. Salvar HTML para análise detalhada
    print("\n8️⃣ SALVANDO PARA ANÁLISE:")
    
    with open('/tmp/orcamento_edicao_debug.html', 'w', encoding='utf-8') as f:
        f.write(content)
    print("   💾 HTML completo salvo em: /tmp/orcamento_edicao_debug.html")
    
    # Extrair apenas a seção do formulário
    form_match = re.search(r'<form[^>]*orcamento-form[^>]*>.*?</form>', content, re.DOTALL)
    if form_match:
        with open('/tmp/form_section_debug.html', 'w', encoding='utf-8') as f:
            f.write(form_match.group(0))
        print("   💾 Seção do formulário salva em: /tmp/form_section_debug.html")
    
    # Extrair apenas o JavaScript
    script_matches = re.findall(r'<script[^>]*>(.*?)</script>', content, re.DOTALL)
    with open('/tmp/javascript_debug.js', 'w', encoding='utf-8') as f:
        for i, script in enumerate(script_matches):
            f.write(f"\n\n/* === SCRIPT {i+1} === */\n")
            f.write(script)
    print("   💾 JavaScript salvo em: /tmp/javascript_debug.js")
    
    # 9. Comparar com página de novo orçamento
    print("\n9️⃣ COMPARANDO COM PÁGINA NOVO:")
    
    response_novo = client.get('/orcamentos/novo/')
    if response_novo.status_code == 200:
        content_novo = response_novo.content.decode('utf-8')
        
        # Verificar diferenças estruturais
        elementos_novo = []
        elementos_edicao = []
        
        for elemento, _ in elementos_essenciais:
            if elemento in content_novo:
                elementos_novo.append(elemento)
            if elemento in content:
                elementos_edicao.append(elemento)
        
        print(f"   📊 Elementos na página NOVO: {len(elementos_novo)}")
        print(f"   📊 Elementos na página EDIÇÃO: {len(elementos_edicao)}")
        
        faltando = set(elementos_novo) - set(elementos_edicao)
        if faltando:
            print(f"   ⚠️  Elementos faltando na edição: {faltando}")
        else:
            print("   ✅ Todos os elementos presentes em ambas as páginas")
    else:
        print(f"   ❌ Erro ao acessar página novo: {response_novo.status_code}")
    
    print(f"\n🔍 INVESTIGAÇÃO CONCLUÍDA")
    print(f"📄 Verifique os arquivos gerados em /tmp/ para análise detalhada")
    
    return True

if __name__ == '__main__':
    sucesso = investigar_bug_hidratacao()
    if sucesso:
        print("\n💡 PRÓXIMOS PASSOS:")
        print("   1. Analise os arquivos em /tmp/")
        print("   2. Verifique o console do navegador")
        print("   3. Compare as diferenças entre novo e edição")
    else:
        print("\n❌ INVESTIGAÇÃO FALHOU")
