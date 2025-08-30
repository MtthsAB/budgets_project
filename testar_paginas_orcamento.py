#!/usr/bin/env python3
"""
Script para testar se as páginas de orçamento estão funcionando
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

def testar_paginas():
    print("🧪 TESTANDO PÁGINAS DE ORÇAMENTO")
    print("=" * 50)
    
    # Criar cliente de teste
    client = Client()
    
    # Criar usuário de teste
    try:
        user = User.objects.filter(is_superuser=True).first()
        if not user:
            user = User.objects.first()
        print(f"✅ Usuário encontrado: {user.email if user else 'Nenhum'}")
    except Exception as e:
        print(f"❌ Erro ao buscar usuário: {e}")
        return
    
    if not user:
        print("❌ Nenhum usuário encontrado!")
        return
    
    # Fazer login
    login_success = client.force_login(user)
    print(f"✅ Login realizado")
    
    # Testar página de listagem
    print("\n--- Testando página de listagem ---")
    response = client.get('/orcamentos/')
    print(f"Status listagem: {response.status_code}")
    if response.status_code == 200:
        print("✅ Página de listagem OK")
    else:
        print(f"❌ Erro na listagem: {response.status_code}")
    
    # Testar página novo orçamento
    print("\n--- Testando página novo orçamento ---")
    response = client.get('/orcamentos/novo/')
    print(f"Status novo: {response.status_code}")
    if response.status_code == 200:
        print("✅ Página novo orçamento OK")
        
        # Verificar se tem contexto correto
        context = response.context
        if context:
            print(f"✅ Contexto disponível:")
            print(f"  - form: {'SIM' if 'form' in context else 'NÃO'}")
            print(f"  - titulo: {'SIM' if 'titulo' in context else 'NÃO'}")
            if 'titulo' in context:
                print(f"  - titulo valor: {context['titulo']}")
        else:
            print("❌ Sem contexto")
    else:
        print(f"❌ Erro na página novo: {response.status_code}")
        if hasattr(response, 'content'):
            print(f"Conteúdo do erro: {response.content[:500]}")
    
    # Testar página editar (se existir orçamento)
    print("\n--- Testando página editar orçamento ---")
    try:
        orcamento = Orcamento.objects.first()
        if orcamento:
            response = client.get(f'/orcamentos/{orcamento.pk}/editar/')
            print(f"Status editar (ID {orcamento.pk}): {response.status_code}")
            if response.status_code == 200:
                print("✅ Página editar orçamento OK")
                
                # Verificar contexto
                context = response.context
                if context:
                    print(f"✅ Contexto disponível:")
                    print(f"  - form: {'SIM' if 'form' in context else 'NÃO'}")
                    print(f"  - orcamento: {'SIM' if 'orcamento' in context else 'NÃO'}")
                    print(f"  - orcamento_data_json: {'SIM' if 'orcamento_data_json' in context else 'NÃO'}")
                    print(f"  - titulo: {'SIM' if 'titulo' in context else 'NÃO'}")
                    if 'titulo' in context:
                        print(f"  - titulo valor: {context['titulo']}")
                else:
                    print("❌ Sem contexto")
            else:
                print(f"❌ Erro na página editar: {response.status_code}")
        else:
            print("❌ Nenhum orçamento encontrado para testar edição")
    except Exception as e:
        print(f"❌ Erro ao testar edição: {e}")
    
    print("\n" + "=" * 50)
    print("🧪 TESTE CONCLUÍDO")

if __name__ == '__main__':
    testar_paginas()
