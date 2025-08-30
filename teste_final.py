#!/usr/bin/env python3
"""
Script para testar se o problema foi realmente corrigido
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

User = get_user_model()

def teste_final():
    print("🎯 TESTE FINAL: FUNCIONAMENTO DAS PÁGINAS")
    print("=" * 50)
    
    # Preparar dados
    client = Client()
    user = User.objects.filter(is_superuser=True).first()
    client.force_login(user)
    
    print("📋 Verificando status atual...")
    
    # Teste 1: Verificar se páginas carregam
    urls_teste = [
        ('/orcamentos/', 'Listagem'),
        ('/orcamentos/novo/', 'Novo orçamento'),
    ]
    
    for url, nome in urls_teste:
        response = client.get(url)
        status = "✅" if response.status_code == 200 else "❌"
        print(f"  {status} {nome}: {response.status_code}")
    
    # Teste 2: Verificar se há orçamentos para editar
    ultimo_orcamento = Orcamento.objects.order_by('-created_at').first()
    if ultimo_orcamento:
        print(f"\n📊 Testando edição do orçamento ID {ultimo_orcamento.pk}")
        
        response = client.get(f'/orcamentos/{ultimo_orcamento.pk}/editar/')
        status = "✅" if response.status_code == 200 else "❌"
        print(f"  {status} Página de edição: {response.status_code}")
        
        if response.status_code == 200:
            content = response.content.decode('utf-8')
            
            # Verificar elementos específicos críticos
            verificacoes = [
                ('window.orcamentoPk', 'ID do orçamento no JS'),
                ('window.orcamentoData', 'Dados do orçamento no JS'),
                ('hidratarCamposOrcamento()', 'Chamada de hidratação'),
                ('function hidratarCamposOrcamento', 'Função de hidratação'),
                ('desconto_valor_unificado', 'Campo desconto unificado'),
                ('acrescimo_valor_unificado', 'Campo acréscimo unificado'),
            ]
            
            print(f"\n🔍 Verificação de elementos críticos:")
            for busca, desc in verificacoes:
                presente = busca in content
                status = "✅" if presente else "❌"
                print(f"  {status} {desc}: {presente}")
    else:
        print(f"\n❌ Nenhum orçamento para testar edição")
    
    # Teste 3: Verificar console de browser (simulado)
    print(f"\n🌐 Status do navegador (simulado):")
    response = client.get('/orcamentos/novo/')
    
    if response.status_code == 200:
        content = response.content.decode('utf-8')
        
        # Verificar se há erros óbvios
        erros_potenciais = content.count('${')
        if erros_potenciais > 0:
            print(f"  ⚠️  {erros_potenciais} template literals não processados (ainda presente)")
        else:
            print(f"  ✅ Nenhum template literal não processado")
        
        # Verificar estrutura JavaScript
        if 'function inicializarCamposUnificados' in content:
            print(f"  ✅ Função de campos unificados presente")
        else:
            print(f"  ❌ Função de campos unificados ausente")
            
        if 'function hidratarCamposOrcamento' in content:
            print(f"  ✅ Função de hidratação presente")
        else:
            print(f"  ❌ Função de hidratação ausente")
    
    # Teste 4: Verificar se principal problema foi corrigido
    print(f"\n🎯 PRINCIPAL PROBLEMA (chaves balanceadas):")
    response = client.get('/orcamentos/novo/')
    content = response.content.decode('utf-8')
    
    # Contar chaves no JavaScript
    import re
    script_matches = re.findall(r'<script[^>]*>(.*?)</script>', content, re.DOTALL)
    
    if script_matches:
        script_content = script_matches[-1]  # Script principal
        open_braces = script_content.count('{')
        close_braces = script_content.count('}')
        
        if open_braces == close_braces:
            print(f"  ✅ Chaves balanceadas: {open_braces} abertas, {close_braces} fechadas")
        else:
            print(f"  ❌ Chaves NÃO balanceadas: {open_braces} abertas, {close_braces} fechadas")
    
    print(f"\n" + "=" * 50)
    
    # Conclusão
    if open_braces == close_braces:
        print("🎉 SUCESSO: Problema principal do JavaScript CORRIGIDO!")
        print("📝 Próximos passos:")
        print("   1. Teste manual no navegador")
        print("   2. Verificar se hidratação funciona")
        print("   3. Testar criação/edição de orçamentos")
        print("   4. Verificar alternância R$/% dos campos unificados")
    else:
        print("❌ PROBLEMA: Ainda há erros de sintaxe JavaScript")
    
    print("🎯 TESTE FINAL CONCLUÍDO")

if __name__ == '__main__':
    teste_final()
