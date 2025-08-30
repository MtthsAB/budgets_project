#!/usr/bin/env python3
"""
Script para encontrar a chave extra que está quebrando o JavaScript
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

def encontrar_chave_extra():
    print("🔍 PROCURANDO CHAVE EXTRA NO JAVASCRIPT")
    print("=" * 50)
    
    # Preparar dados
    client = Client()
    user = User.objects.filter(is_superuser=True).first()
    client.force_login(user)
    
    # Buscar página novo orçamento
    response = client.get('/orcamentos/novo/')
    content = response.content.decode('utf-8')
    
    # Extrair o script principal
    script_matches = re.findall(r'<script[^>]*>(.*?)</script>', content, re.DOTALL)
    
    if not script_matches:
        print("❌ Nenhum script encontrado")
        return
    
    script_content = script_matches[-1]  # Script principal
    
    print(f"📊 Análise do script:")
    print(f"  - Tamanho: {len(script_content)} caracteres")
    print(f"  - Linhas: {len(script_content.split(chr(10)))}")
    
    # Analisar chaves linha por linha
    lines = script_content.split('\n')
    balance = 0
    problematic_lines = []
    
    for i, line in enumerate(lines):
        line_balance = line.count('{') - line.count('}')
        balance += line_balance
        
        # Se balance fica negativo, há chave extra
        if balance < 0:
            problematic_lines.append((i+1, line.strip(), balance))
        
        # Verificar se há padrões suspeitos
        if balance < -1:  # Muito negativo
            break
    
    if problematic_lines:
        print(f"\n❌ Linhas problemáticas encontradas:")
        for line_num, line_content, bal in problematic_lines:
            print(f"  Linha {line_num} (balance: {bal}): {line_content[:80]}")
    
    # Verificar final do script
    print(f"\n📊 Balance final: {balance}")
    
    if balance == -1:
        print("🎯 PROBLEMA: Exatamente 1 chave de fechamento extra")
        
        # Procurar onde pode estar a chave extra
        last_lines = lines[-20:]  # Últimas 20 linhas
        
        print(f"\n🔍 Verificando últimas 20 linhas:")
        for i, line in enumerate(last_lines):
            line_num = len(lines) - 20 + i + 1
            closes = line.count('}')
            opens = line.count('{')
            if closes > opens:
                print(f"  ⚠️  Linha {line_num}: {closes - opens} chaves extras: {line.strip()}")
            elif line.strip() == '}':
                print(f"  🎯 Linha {line_num}: Chave solitária: {line.strip()}")
            elif '}' in line:
                print(f"  📍 Linha {line_num}: Tem chave: {line.strip()}")
    
    # Verificar se há estruturas de função não fechadas
    print(f"\n🔍 Verificando estruturas de função:")
    
    function_patterns = [
        r'function\s+\w+\s*\([^)]*\)\s*\{',
        r'\w+\s*=\s*function\s*\([^)]*\)\s*\{',
        r'document\.addEventListener\s*\([^{]*\{',
        r'if\s*\([^)]*\)\s*\{',
        r'else\s*\{',
        r'for\s*\([^)]*\)\s*\{',
        r'while\s*\([^)]*\)\s*\{',
    ]
    
    for pattern in function_patterns:
        matches = re.finditer(pattern, script_content)
        for match in matches:
            start = match.start()
            # Encontrar linha
            lines_before = script_content[:start].count('\n')
            line_content = lines[lines_before] if lines_before < len(lines) else "N/A"
            print(f"  📍 Estrutura na linha {lines_before + 1}: {line_content.strip()[:60]}")
    
    print(f"\n" + "=" * 50)
    print("🔍 BUSCA CONCLUÍDA")

if __name__ == '__main__':
    encontrar_chave_extra()
