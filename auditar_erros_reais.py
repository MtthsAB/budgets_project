#!/usr/bin/env python3
"""
Script para auditar erros reais nas páginas de orçamentos
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
import json

User = get_user_model()

def auditar_erros():
    print("🔍 AUDITORIA DE ERROS - PÁGINAS DE ORÇAMENTOS")
    print("=" * 60)
    
    # Preparar dados
    client = Client()
    user = User.objects.filter(is_superuser=True).first()
    if not user:
        print("❌ Nenhum usuário encontrado!")
        return
    
    client.force_login(user)
    print(f"✅ Login realizado: {user.email}")
    
    # URLs para testar
    orcamento_existente = Orcamento.objects.order_by('-created_at').first()
    urls_teste = [
        ('/orcamentos/novo/', 'NOVO'),
        (f'/orcamentos/{orcamento_existente.pk}/editar/' if orcamento_existente else None, 'EDITAR'),
    ]
    
    for url, nome in urls_teste:
        if not url:
            print(f"\n❌ {nome}: Nenhum orçamento para testar")
            continue
            
        print(f"\n{'='*20} PÁGINA {nome} {'='*20}")
        print(f"URL: {url}")
        
        try:
            response = client.get(url)
            print(f"Status HTTP: {response.status_code}")
            
            if response.status_code == 200:
                content = response.content.decode('utf-8')
                
                # 1. Verificar elementos críticos
                print(f"\n📋 ELEMENTOS CRÍTICOS:")
                elementos = {
                    'cliente-busca': 'Campo busca cliente',
                    'id_cliente': 'Select cliente oculto',
                    'desconto_valor_unificado': 'Campo desconto unificado',
                    'desconto_tipo_btn': 'Botão tipo desconto',
                    'acrescimo_valor_unificado': 'Campo acréscimo unificado',
                    'acrescimo_tipo_btn': 'Botão tipo acréscimo',
                    'btn-adicionar-item': 'Botão adicionar item',
                    'modal-adicionar-item': 'Modal adicionar item',
                }
                
                for element_id, desc in elementos.items():
                    presente = f'id="{element_id}"' in content
                    status = "✅" if presente else "❌"
                    print(f"  {status} {desc}")
                
                # 2. Verificar JavaScript crítico
                print(f"\n⚡ FUNÇÕES JAVASCRIPT:")
                funcoes_js = [
                    'inicializarCamposUnificados',
                    'hidratarCamposOrcamento',
                    'buscarClientes',
                    'mostrarModulosSofa',
                    'atualizarTotaisSidebar',
                ]
                
                for funcao in funcoes_js:
                    presente = f'function {funcao}' in content or f'{funcao} =' in content
                    status = "✅" if presente else "❌"
                    print(f"  {status} {funcao}")
                
                # 3. Verificar erros de template literal
                print(f"\n🔧 TEMPLATE LITERALS:")
                template_errors = content.count('${')
                if template_errors > 0:
                    print(f"  ⚠️  {template_errors} template literals não processados")
                else:
                    print(f"  ✅ Nenhum template literal não processado")
                
                # 4. Verificar estrutura de chaves/parênteses
                print(f"\n🏗️  ESTRUTURA JAVASCRIPT:")
                import re
                script_matches = re.findall(r'<script[^>]*>(.*?)</script>', content, re.DOTALL)
                
                if script_matches:
                    script_content = script_matches[-1]  # Script principal
                    open_braces = script_content.count('{')
                    close_braces = script_content.count('}')
                    open_parens = script_content.count('(')
                    close_parens = script_content.count(')')
                    
                    print(f"  Chaves: {open_braces} abertas, {close_braces} fechadas")
                    print(f"  Parênteses: {open_parens} abertos, {close_parens} fechados")
                    
                    if open_braces == close_braces and open_parens == close_parens:
                        print(f"  ✅ Estrutura JavaScript válida")
                    else:
                        print(f"  ❌ Estrutura JavaScript inválida")
                
                # 5. Verificar hidratação (só para editar)
                if nome == 'EDITAR':
                    print(f"\n💧 HIDRATAÇÃO:")
                    hidratacao = [
                        f'window.orcamentoPk = {orcamento_existente.pk}',
                        'window.orcamentoData = {',
                        'hidratarCamposOrcamento()',
                    ]
                    
                    for item in hidratacao:
                        presente = item in content
                        status = "✅" if presente else "❌"
                        print(f"  {status} {item}")
                
                # 6. Verificar imports de CSS/JS
                print(f"\n📦 RECURSOS ESTÁTICOS:")
                recursos = [
                    'bootstrap.min.css',
                    'bootstrap.bundle.min.js',
                    'static/css/',
                    '<script>',
                ]
                
                for recurso in recursos:
                    presente = recurso in content
                    status = "✅" if presente else "❌"
                    print(f"  {status} {recurso}")
                    
            else:
                print(f"❌ Erro HTTP: {response.status_code}")
                
        except Exception as e:
            print(f"❌ Exceção: {e}")
    
    print(f"\n{'='*60}")
    print("🔍 AUDITORIA CONCLUÍDA")

if __name__ == '__main__':
    auditar_erros()
