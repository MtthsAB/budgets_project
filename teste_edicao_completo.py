#!/usr/bin/env python3
"""
Teste completo da tela de edição com autenticação
"""

import os
import sys
import django

# Setup do Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema_produtos.settings')
django.setup()

from django.test import Client
from django.contrib.auth import get_user_model
from orcamentos.models import Orcamento

def testar_tela_edicao_com_auth():
    print("=== TESTE COMPLETO DA TELA DE EDIÇÃO ===\n")
    
    # Criar cliente de teste do Django
    client = Client()
    
    # Fazer login com usuário
    User = get_user_model()
    try:
        user = User.objects.first()
        if not user:
            print("✗ Nenhum usuário encontrado no sistema")
            return False
            
        print(f"Usuário encontrado: {user.email}")
        
        # Simular login
        client.force_login(user)
        print("✓ Login simulado com sucesso")
        
        # Testar acesso à página de edição
        url = '/orcamentos/5/editar/'
        print(f"Testando URL: {url}")
        
        response = client.get(url)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            print("✓ Página acessível")
            
            # Verificar contexto
            context = response.context
            if context:
                print("✓ Contexto disponível")
                
                # Verificar se orcamento está no contexto
                if 'orcamento' in context:
                    orcamento = context['orcamento']
                    print(f"✓ Orçamento no contexto: ID {orcamento.id}")
                    print(f"  Cliente: {orcamento.cliente.nome_empresa if orcamento.cliente else 'None'}")
                    print(f"  Status: {orcamento.status}")
                else:
                    print("✗ Orçamento não encontrado no contexto")
                
                # Verificar se orcamento_data_json está no contexto
                if 'orcamento_data_json' in context:
                    print("✓ orcamento_data_json presente no contexto")
                    json_data = context['orcamento_data_json']
                    print(f"  JSON: {json_data}")
                else:
                    print("✗ orcamento_data_json NÃO encontrado no contexto")
                
                # Verificar se form está no contexto
                if 'form' in context:
                    form = context['form']
                    print("✓ Form presente no contexto")
                    print(f"  Campos do form: {list(form.fields.keys())}")
                    
                    # Verificar valores iniciais do form
                    if hasattr(form, 'instance') and form.instance:
                        instance = form.instance
                        print("✓ Form tem instância do orçamento")
                        print(f"  Cliente no form: {instance.cliente}")
                        print(f"  Status no form: {instance.status}")
                    else:
                        print("✗ Form não tem instância")
                else:
                    print("✗ Form não encontrado no contexto")
            else:
                print("✗ Nenhum contexto disponível")
            
            # Verificar conteúdo HTML
            content = response.content.decode('utf-8')
            
            # Procurar por elementos específicos
            checks = [
                ('window.orcamentoData', 'Dados JavaScript'),
                ('id="id_cliente"', 'Campo cliente'),
                ('id="id_faixa_preco"', 'Campo faixa preço'),
                ('id="id_forma_pagamento"', 'Campo forma pagamento'),
                ('id="id_status"', 'Campo status'),
                ('function hidratarCamposOrcamento', 'Função hidratação'),
            ]
            
            print("\n--- Verificação do HTML ---")
            for search_term, description in checks:
                if search_term in content:
                    print(f"✓ {description} encontrado")
                else:
                    print(f"✗ {description} NÃO encontrado")
                    
            return True
            
        elif response.status_code == 404:
            print("✗ Orçamento não encontrado (404)")
        elif response.status_code == 403:
            print("✗ Acesso negado (403)")
        else:
            print(f"✗ Status inesperado: {response.status_code}")
            
        return False
        
    except Exception as e:
        print(f"✗ Erro: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    sucesso = testar_tela_edicao_com_auth()
    if sucesso:
        print("\n✅ Teste concluído com sucesso!")
    else:
        print("\n❌ Teste falhou!")
