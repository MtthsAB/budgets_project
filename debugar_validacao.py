#!/usr/bin/env python3
"""
Script para testar e debugar a validação do formulário
"""
import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema_produtos.settings')
django.setup()

from django.test import Client
from django.contrib.auth import get_user_model
from orcamentos.models import Orcamento, FaixaPreco, FormaPagamento
from orcamentos.forms import OrcamentoForm
from clientes.models import Cliente

User = get_user_model()

def debugar_validacao():
    print("🐛 DEBUGANDO VALIDAÇÃO DO FORMULÁRIO")
    print("=" * 50)
    
    # Preparar dados
    client = Client()
    user = User.objects.filter(is_superuser=True).first()
    if not user:
        user = User.objects.first()
    
    client.force_login(user)
    
    # Buscar dados necessários
    cliente = Cliente.objects.first()
    faixa_preco = FaixaPreco.objects.first()
    forma_pagamento = FormaPagamento.objects.first()
    
    print(f"📊 Dados disponíveis:")
    print(f"  - Cliente: {cliente.nome_empresa if cliente else 'NENHUM'}")
    print(f"  - Faixa preço: {faixa_preco.nome if faixa_preco else 'NENHUMA'}")
    print(f"  - Forma pagamento: {forma_pagamento.nome if forma_pagamento else 'NENHUMA'}")
    
    if not cliente:
        print("❌ Sem cliente para teste!")
        return
    
    # Teste 1: Validar formulário diretamente
    print(f"\n1️⃣ TESTE: Validação direta do formulário")
    
    form_data = {
        'cliente': cliente.id,
        'data_entrega': '2025-09-30',
        'data_validade': '2025-09-15',
        'status': 'rascunho',
        'desconto_valor': '',
        'desconto_percentual': '',
        'acrescimo_valor': '',
        'acrescimo_percentual': '',
    }
    
    if faixa_preco:
        form_data['faixa_preco'] = faixa_preco.id
    if forma_pagamento:
        form_data['forma_pagamento'] = forma_pagamento.id
    
    form = OrcamentoForm(form_data)
    
    if form.is_valid():
        print("✅ Formulário válido")
    else:
        print("❌ Formulário inválido:")
        for field, errors in form.errors.items():
            print(f"  - {field}: {errors}")
    
    # Teste 2: POST real para ver a resposta
    print(f"\n2️⃣ TESTE: POST real")
    
    response = client.post('/orcamentos/novo/', data=form_data)
    
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        # Forma de novo com erros
        content = response.content.decode('utf-8')
        
        # Procurar por mensagens de erro
        if 'alert-danger' in content or 'is-invalid' in content:
            print("❌ Erros encontrados na resposta")
            
            # Extrair erros específicos
            import re
            error_matches = re.findall(r'<div[^>]*alert-danger[^>]*>(.*?)</div>', content, re.DOTALL)
            for error in error_matches:
                clean_error = re.sub(r'<[^>]+>', '', error).strip()
                if clean_error:
                    print(f"  Erro: {clean_error}")
            
            # Procurar campos com erro
            invalid_matches = re.findall(r'<[^>]*is-invalid[^>]*name="([^"]*)"', content)
            for field in invalid_matches:
                print(f"  Campo inválido: {field}")
        else:
            print("⚠️  Sem erros visuais óbvios, mas formulário não foi processado")
            
            # Verificar se o formulário tem dados
            if 'value=""' in content:
                print("  🔍 Formulário parece estar vazio (valores em branco)")
    
    elif response.status_code == 302:
        print("✅ Redirect - provavelmente criado com sucesso")
        print(f"  URL: {response.url}")
    else:
        print(f"❌ Status inesperado: {response.status_code}")
    
    # Teste 3: Verificar requisitos mínimos
    print(f"\n3️⃣ TESTE: Campos obrigatórios")
    
    # Verificar quais campos são obrigatórios no form
    form_empty = OrcamentoForm({})
    
    if not form_empty.is_valid():
        print("Campos obrigatórios:")
        for field, errors in form_empty.errors.items():
            print(f"  - {field}: {errors}")
    
    print("\n" + "=" * 50)
    print("🐛 DEBUG CONCLUÍDO")

if __name__ == '__main__':
    debugar_validacao()
