#!/usr/bin/env python3
"""
Script para extrair e verificar especificamente os problemas de template literals
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

def verificar_template_literals():
    print("🔍 VERIFICANDO TEMPLATE LITERALS")
    print("=" * 50)
    
    # Preparar dados
    client = Client()
    user = User.objects.filter(is_superuser=True).first()
    client.force_login(user)
    
    # Buscar página novo orçamento
    response = client.get('/orcamentos/novo/')
    content = response.content.decode('utf-8')
    
    # Procurar por template literals problemáticos
    print("1️⃣ PROBLEMAS: Template literals não processados")
    
    # Extrair exemplos específicos
    problematic_patterns = [
        (r'id="\$\{[^}]+\}"', 'IDs com template literals'),
        (r'for="\$\{[^}]+\}"', 'Labels com template literals'),
        (r'data-[^=]+="\$\{[^}]+\}"', 'Atributos data com template literals'),
        (r'src="\$\{[^}]+\}"', 'Src com template literals'),
    ]
    
    total_problemas = 0
    for pattern, desc in problematic_patterns:
        matches = re.findall(pattern, content)
        if matches:
            print(f"  ❌ {desc}: {len(matches)} ocorrências")
            total_problemas += len(matches)
            for match in matches[:3]:  # Mostrar só as primeiras 3
                print(f"    - {match}")
        else:
            print(f"  ✅ {desc}: OK")
    
    print(f"\n📊 Total de problemas: {total_problemas}")
    
    # Procurar pelo contexto onde isso acontece
    print(f"\n2️⃣ CONTEXTO: Onde os problemas ocorrem")
    
    # Dividir o HTML em seções para encontrar onde está o problema
    script_blocks = re.findall(r'<script[^>]*>(.*?)</script>', content, re.DOTALL)
    
    for i, script in enumerate(script_blocks):
        problematic_literals = re.findall(r'\$\{[^}]+\}', script)
        
        if problematic_literals:
            print(f"\n  📄 Script block {i+1}:")
            print(f"    - Template literals encontrados: {len(problematic_literals)}")
            
            # Verificar se está dentro de uma string/template literal válido
            lines = script.split('\n')
            in_template_literal = False
            
            for line_num, line in enumerate(lines):
                if '${' in line:
                    # Verificar se a linha está dentro de um template literal válido
                    line_stripped = line.strip()
                    
                    # Contar backticks antes desta linha
                    before_text = '\n'.join(lines[:line_num])
                    backtick_count = before_text.count('`')
                    
                    # Se número ímpar de backticks, estamos dentro de template literal
                    inside_template = (backtick_count % 2) == 1
                    
                    if not inside_template:
                        print(f"    ⚠️  Linha {line_num + 1} (FORA de template literal): {line_stripped[:100]}")
                    else:
                        print(f"    ✅ Linha {line_num + 1} (dentro de template literal): OK")
    
    # Verificar problemas específicos
    print(f"\n3️⃣ DIAGNÓSTICO: Problemas específicos")
    
    # Verificar se há problemas de estrutura HTML que podem estar quebrando o JavaScript
    html_issues = [
        (r'<script[^>]*>\s*</script>', 'Scripts vazios'),
        (r'<script[^>]*>[^<]*\$\{[^}]+\}[^<]*</script>', 'Scripts com templates não processados'),
        (r'html \+= `[^`]*\$\{[^}]+\}[^`]*`[^;]*;', 'Template literals válidos'),
    ]
    
    for pattern, desc in html_issues:
        matches = re.findall(pattern, content, re.DOTALL)
        if matches:
            print(f"  🔍 {desc}: {len(matches)} encontrados")
        else:
            print(f"  ✅ {desc}: Nenhum")
    
    print(f"\n" + "=" * 50)
    print("🔍 VERIFICAÇÃO CONCLUÍDA")

if __name__ == '__main__':
    verificar_template_literals()
