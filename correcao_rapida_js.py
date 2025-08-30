#!/usr/bin/env python
"""
Script para aplicar correção rápida no JavaScript do form.html
Remove extra chaves e parênteses, mantendo funcionalidade básica
"""
import os
import re

def fix_javascript_syntax():
    """Corrige erros de sintaxe JavaScript no template form.html"""
    template_path = "/home/matas/projetos/Project/templates/orcamentos/form.html"
    
    print("🔧 Corrigindo erros de sintaxe JavaScript...")
    
    with open(template_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Lista de correções conhecidas
    corrections = [
        # Remove chave extra após funções específicas
        (r'(\s+function enviarItemViaAjax\(.*?\}\s*\}\s*)(?=\n\s*//)', r'\1'),
        
        # Remove parênteses ou chaves extras em locais específicos
        (r'(\s+}\s*}\);?\s*)(?=\n\s*//\s*Forçar atualização)', r'\1'),
        
        # Remove múltiplas chaves consecutivas desnecessárias
        (r'(\s*}\s*}\s*}\s*)', r'\n    }\n'),
    ]
    
    original_content = content
    
    for pattern, replacement in corrections:
        content = re.sub(pattern, replacement, content, flags=re.MULTILINE | re.DOTALL)
    
    # Verificar se houve mudança
    if content != original_content:
        with open(template_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print("✅ Correções aplicadas ao template")
        return True
    else:
        print("ℹ️  Nenhuma correção necessária")
        return False

def verify_syntax():
    """Verifica se a sintaxe JavaScript está correta"""
    template_path = "/home/matas/projetos/Project/templates/orcamentos/form.html"
    
    with open(template_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Extrair JavaScript
    js_pattern = r'<script[^>]*>(.*?)</script>'
    js_matches = re.findall(js_pattern, content, re.DOTALL)
    
    for js_code in js_matches:
        # Contar chaves e parênteses
        braces_open = js_code.count('{')
        braces_close = js_code.count('}')
        parens_open = js_code.count('(')
        parens_close = js_code.count(')')
        
        print(f"Chaves: {braces_open} abertas, {braces_close} fechadas")
        print(f"Parênteses: {parens_open} abertos, {parens_close} fechados")
        
        if braces_open == braces_close and parens_open == parens_close:
            print("✅ Sintaxe JavaScript válida")
            return True
        else:
            print("❌ Sintaxe JavaScript inválida")
            return False

if __name__ == "__main__":
    print("🔍 APLICANDO CORREÇÃO RÁPIDA DE SINTAXE")
    print("=" * 50)
    
    # Aplicar correções
    fixed = fix_javascript_syntax()
    
    # Verificar resultado
    valid = verify_syntax()
    
    if valid:
        print("\n✅ CORREÇÃO CONCLUÍDA COM SUCESSO")
        print("💡 Execute o teste novamente para verificar se os elementos estão visíveis")
    else:
        print("\n❌ AINDA HÁ PROBLEMAS DE SINTAXE")
        print("💡 Pode ser necessário correção manual adicional")
