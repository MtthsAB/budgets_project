#!/usr/bin/env python3
"""
Script para verificar se as funções JavaScript específicas estão funcionando
"""
import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema_produtos.settings')
django.setup()

from django.test import Client
from django.contrib.auth import get_user_model
import re

User = get_user_model()

def testar_execucao_js():
    print("⚡ TESTANDO EXECUÇÃO DO JAVASCRIPT")
    print("=" * 50)
    
    # Preparar dados
    client = Client()
    user = User.objects.filter(is_superuser=True).first()
    client.force_login(user)
    
    # Buscar página novo orçamento
    response = client.get('/orcamentos/novo/')
    content = response.content.decode('utf-8')
    
    print("1️⃣ VERIFICAÇÃO: Estrutura das funções JavaScript")
    
    # Verificar se as funções críticas estão definidas corretamente
    funcoes_criticas = [
        ('mostrarModulosSofa', r'function mostrarModulosSofa\([^)]*\)\s*\{'),
        ('inicializarCamposUnificados', r'function inicializarCamposUnificados\([^)]*\)\s*\{'),
        ('hidratarCamposOrcamento', r'function hidratarCamposOrcamento\([^)]*\)\s*\{'),
        ('atualizarTotais', r'function atualizarTotais\([^)]*\)\s*\{'),
    ]
    
    for nome, pattern in funcoes_criticas:
        if re.search(pattern, content):
            print(f"  ✅ Função {nome}: Definida corretamente")
        else:
            print(f"  ❌ Função {nome}: PROBLEMA na definição")
    
    print(f"\n2️⃣ VERIFICAÇÃO: Sintaxe de template literals")
    
    # Verificar se os template literals estão dentro de blocos válidos
    script_content = ""
    script_matches = re.findall(r'<script[^>]*>(.*?)</script>', content, re.DOTALL)
    
    if script_matches:
        script_content = script_matches[-1]  # Pegar o script principal (último)
        
        # Verificar problemas de sintaxe
        problemas_sintaxe = []
        
        # 1. Template literals não fechados
        backtick_count = script_content.count('`')
        if backtick_count % 2 != 0:
            problemas_sintaxe.append("Template literal não fechado (número ímpar de backticks)")
        
        # 2. Strings não fechadas
        single_quote_count = len(re.findall(r"(?<!\\)'", script_content))
        double_quote_count = len(re.findall(r'(?<!\\)"', script_content))
        
        if single_quote_count % 2 != 0:
            problemas_sintaxe.append("String com aspas simples não fechada")
        if double_quote_count % 2 != 0:
            problemas_sintaxe.append("String com aspas duplas não fechada")
        
        # 3. Chaves não balanceadas
        open_braces = script_content.count('{')
        close_braces = script_content.count('}')
        if open_braces != close_braces:
            problemas_sintaxe.append(f"Chaves não balanceadas: {open_braces} abertas, {close_braces} fechadas")
        
        # 4. Parênteses não balanceados
        open_parens = script_content.count('(')
        close_parens = script_content.count(')')
        if open_parens != close_parens:
            problemas_sintaxe.append(f"Parênteses não balanceados: {open_parens} abertos, {close_parens} fechados")
        
        if problemas_sintaxe:
            print("  ❌ Problemas de sintaxe encontrados:")
            for problema in problemas_sintaxe:
                print(f"    - {problema}")
        else:
            print("  ✅ Sintaxe parece OK")
    
    print(f"\n3️⃣ VERIFICAÇÃO: Chamadas das funções")
    
    # Verificar se as funções são chamadas
    chamadas_funcoes = [
        ('mostrarModulosSofa', r'mostrarModulosSofa\s*\('),
        ('inicializarCamposUnificados', r'inicializarCamposUnificados\s*\('),
        ('hidratarCamposOrcamento', r'hidratarCamposOrcamento\s*\('),
    ]
    
    for nome, pattern in chamadas_funcoes:
        calls = re.findall(pattern, content)
        if calls:
            print(f"  ✅ {nome}: Chamada {len(calls)} vez(es)")
        else:
            print(f"  ❌ {nome}: NÃO é chamada")
    
    print(f"\n4️⃣ DIAGNÓSTICO: Área problemática específica")
    
    # Procurar especificamente onde os ${} estão aparecendo no HTML final
    problema_lines = []
    lines = content.split('\n')
    
    for i, line in enumerate(lines):
        if '${' in line and '<script>' not in line and '</script>' not in line:
            # Está fora de script
            problema_lines.append((i+1, line.strip()))
    
    if problema_lines:
        print(f"  ❌ Template literals no HTML (fora de scripts): {len(problema_lines)} linhas")
        for line_num, line_content in problema_lines[:5]:  # Mostrar só as primeiras 5
            print(f"    Linha {line_num}: {line_content[:80]}...")
    else:
        print(f"  ✅ Nenhum template literal problemático no HTML")
    
    print(f"\n5️⃣ VERIFICAÇÃO: Elementos que deveriam ser criados dinamicamente")
    
    # Verificar se elementos esperados estão sendo criados
    elementos_esperados = [
        ('modulos-lista', 'Container para lista de módulos'),
        ('sofa-modulos', 'Container para módulos de sofá'),
        ('acessorios-lista', 'Container para lista de acessórios'),
    ]
    
    for id_elemento, desc in elementos_esperados:
        if f'id="{id_elemento}"' in content:
            print(f"  ✅ {desc}: Container presente")
        else:
            print(f"  ❌ {desc}: Container AUSENTE")
    
    print(f"\n" + "=" * 50)
    print("⚡ TESTE DE EXECUÇÃO CONCLUÍDO")

if __name__ == '__main__':
    testar_execucao_js()
