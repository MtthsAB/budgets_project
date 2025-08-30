#!/usr/bin/env python3
"""
Script para testar especificamente o HTML gerado pelas páginas
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

def testar_html():
    print("🧪 TESTANDO HTML DAS PÁGINAS")
    print("=" * 50)
    
    # Criar cliente de teste
    client = Client()
    
    # Buscar usuário
    user = User.objects.filter(is_superuser=True).first()
    if not user:
        user = User.objects.first()
    
    if not user:
        print("❌ Nenhum usuário encontrado!")
        return
    
    # Fazer login
    client.force_login(user)
    print(f"✅ Login realizado com {user.email}")
    
    # Testar página novo orçamento
    print("\n--- Analisando página novo orçamento ---")
    response = client.get('/orcamentos/novo/')
    
    if response.status_code == 200:
        content = response.content.decode('utf-8')
        
        # Verificar elementos críticos
        checks = {
            'form tag': '<form' in content,
            'campo cliente': 'cliente-busca' in content or 'id_cliente' in content,
            'campos desconto': 'desconto_valor_unificado' in content,
            'campos acrescimo': 'acrescimo_valor_unificado' in content,
            'script tag': '<script>' in content,
            'hidratação script': 'hidratarCamposOrcamento' in content,
            'campos unificados script': 'inicializarCamposUnificados' in content,
        }
        
        print("Verificações de elementos:")
        for check, result in checks.items():
            status = "✅" if result else "❌"
            print(f"  {status} {check}: {result}")
        
        # Procurar por erros JavaScript
        if 'Uncaught' in content or 'Error' in content:
            print("❌ Possíveis erros JavaScript encontrados no HTML")
        else:
            print("✅ Nenhum erro JavaScript óbvio no HTML")
        
        # Verificar se tem dados de orçamento (deve ser None para novo)
        if 'window.orcamentoData = null' in content:
            print("✅ Dados de orçamento corretos para página nova")
        elif 'window.orcamentoData =' in content:
            print("❌ Dados de orçamento presentes em página nova (erro)")
        else:
            print("⚠️  Não foi possível verificar dados de orçamento")
    
    # Testar página editar orçamento
    print("\n--- Analisando página editar orçamento ---")
    orcamento = Orcamento.objects.first()
    if orcamento:
        response = client.get(f'/orcamentos/{orcamento.pk}/editar/')
        
        if response.status_code == 200:
            content = response.content.decode('utf-8')
            
            # Verificar elementos críticos para edição
            checks = {
                'form tag': '<form' in content,
                'campo cliente': 'cliente-busca' in content or 'id_cliente' in content,
                'dados do orçamento': f'window.orcamentoPk = {orcamento.pk}' in content,
                'dados JSON': 'window.orcamentoData =' in content and 'null' not in content,
                'hidratação script': 'hidratarCamposOrcamento' in content,
                'função hidratação': 'function hidratarCamposOrcamento' in content,
            }
            
            print("Verificações de elementos para edição:")
            for check, result in checks.items():
                status = "✅" if result else "❌"
                print(f"  {status} {check}: {result}")
            
            # Procurar dados específicos do orçamento
            if orcamento.cliente:
                cliente_presente = orcamento.cliente.nome_empresa in content
                print(f"  {'✅' if cliente_presente else '❌'} Cliente '{orcamento.cliente.nome_empresa}' no HTML: {cliente_presente}")
        else:
            print(f"❌ Erro ao carregar página editar: {response.status_code}")
    else:
        print("❌ Nenhum orçamento encontrado para testar edição")
    
    print("\n" + "=" * 50)
    print("🧪 ANÁLISE CONCLUÍDA")

if __name__ == '__main__':
    testar_html()
