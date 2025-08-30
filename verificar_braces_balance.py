#!/usr/bin/env python
"""
Script para encontrar desequilíbrio de chaves no JavaScript do template
"""
import os
import django
import re

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema_produtos.settings')
django.setup()

def verificar_balance_braces():
    """Verifica o balanceamento de chaves no template"""
    template_path = "/home/matas/projetos/Project/templates/orcamentos/form.html"
    
    with open(template_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Extrair apenas o JavaScript (entre <script> e </script>)
    js_pattern = r'<script[^>]*>(.*?)</script>'
    js_matches = re.findall(js_pattern, content, re.DOTALL)
    
    for i, js_code in enumerate(js_matches):
        print(f"\n=== BLOCO JAVASCRIPT {i+1} ===")
        
        # Rastrear chaves linha por linha
        lines = js_code.split('\n')
        balance = 0
        open_positions = []
        
        for line_num, line in enumerate(lines, 1):
            for char_pos, char in enumerate(line):
                if char == '{':
                    balance += 1
                    open_positions.append((line_num, char_pos, line.strip()))
                elif char == '}':
                    balance -= 1
                    if open_positions:
                        open_positions.pop()
                    
                    # Se ficou negativo, tem chave de fechamento extra
                    if balance < 0:
                        print(f"❌ LINHA {line_num}: Chave de fechamento extra")
                        print(f"   Linha: {line.strip()}")
                        return False
        
        # Verificar se sobrou chave aberta
        if balance > 0:
            print(f"❌ CHAVES ABERTAS NÃO FECHADAS: {balance}")
            print("\n📍 Últimas chaves abertas:")
            for line_num, char_pos, line_content in open_positions[-5:]:
                print(f"   Linha {line_num}: {line_content}")
        elif balance < 0:
            print(f"❌ CHAVES DE FECHAMENTO EXTRAS: {abs(balance)}")
        elif balance == 0:
            print("✅ Chaves balanceadas neste bloco")
        
        return balance == 0

if __name__ == "__main__":
    print("🔍 VERIFICANDO BALANCEAMENTO DE CHAVES")
    print("=" * 50)
    
    result = verificar_balance_braces()
    
    if result:
        print("\n✅ TODAS AS CHAVES ESTÃO BALANCEADAS")
    else:
        print("\n❌ PROBLEMA DE BALANCEAMENTO ENCONTRADO")
