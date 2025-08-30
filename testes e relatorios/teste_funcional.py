#!/usr/bin/env python3
"""
Script para testar o funcionamento atual das páginas e identificar problemas críticos
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
from clientes.models import Cliente

User = get_user_model()

def teste_funcional():
    print("🧪 TESTE FUNCIONAL DAS PÁGINAS")
    print("=" * 50)
    
    # Preparar dados de teste
    client = Client()
    user = User.objects.filter(is_superuser=True).first()
    if not user:
        user = User.objects.first()
    
    client.force_login(user)
    print(f"✅ Login realizado: {user.email}")
    
    # Teste 1: Carregar página novo orçamento
    print("\n1️⃣ TESTE: Carregar página novo orçamento")
    response = client.get('/orcamentos/novo/')
    
    if response.status_code == 200:
        print("✅ Página carregada com sucesso")
        
        # Verificar elementos críticos no HTML
        content = response.content.decode('utf-8')
        
        elementos_criticos = [
            ('Form tag', '<form'),
            ('Campo cliente', 'id="cliente-busca"'),
            ('Campo desconto', 'id="desconto_valor_unificado"'),
            ('Campo acréscimo', 'id="acrescimo_valor_unificado"'),
            ('Script de hidratação', 'hidratarCamposOrcamento'),
            ('Script de campos unificados', 'inicializarCamposUnificados'),
        ]
        
        for nome, busca in elementos_criticos:
            presente = busca in content
            status = "✅" if presente else "❌"
            print(f"  {status} {nome}: {presente}")
    else:
        print(f"❌ Erro ao carregar página: {response.status_code}")
        return
    
    # Teste 2: Tentar criar orçamento via POST
    print("\n2️⃣ TESTE: Submeter novo orçamento")
    
    # Buscar cliente de teste
    cliente = Cliente.objects.first()
    if not cliente:
        print("❌ Nenhum cliente encontrado para teste")
        return
    
    # Dados mínimos para criar orçamento
    post_data = {
        'cliente': cliente.id,
        'data_entrega': '2025-09-30',
        'data_validade': '2025-09-15',
        'status': 'rascunho',
        'desconto_valor': '',
        'desconto_percentual': '',
        'acrescimo_valor': '',
        'acrescimo_percentual': '',
        'itens_pedido_json': '[]',  # Sem itens por enquanto
    }
    
    response = client.post('/orcamentos/novo/', data=post_data)
    
    if response.status_code == 302:  # Redirect esperado após sucesso
        print("✅ Orçamento criado com sucesso (redirect)")
        # Pegar a URL de redirecionamento
        redirect_url = response.url
        print(f"  Redirecionado para: {redirect_url}")
        
        # Verificar se foi criado um novo orçamento
        novo_orcamento = Orcamento.objects.filter(cliente=cliente).order_by('-created_at').first()
        if novo_orcamento:
            print(f"  ✅ Orçamento #{novo_orcamento.numero} criado com sucesso")
            
            # Teste 3: Carregar página de edição
            print(f"\n3️⃣ TESTE: Carregar página de edição (ID {novo_orcamento.pk})")
            response = client.get(f'/orcamentos/{novo_orcamento.pk}/editar/')
            
            if response.status_code == 200:
                print("✅ Página de edição carregada com sucesso")
                
                content = response.content.decode('utf-8')
                
                # Verificar se os dados estão sendo injetados
                verificacoes_edicao = [
                    ('Dados do orçamento', f'window.orcamentoPk = {novo_orcamento.pk}'),
                    ('JSON de dados', 'window.orcamentoData = {'),
                    ('Nome do cliente', cliente.nome_empresa),
                    ('Função de hidratação', 'function hidratarCamposOrcamento'),
                ]
                
                for nome, busca in verificacoes_edicao:
                    presente = busca in content
                    status = "✅" if presente else "❌"
                    print(f"  {status} {nome}: {presente}")
                
                # Teste 4: Tentar salvar edição
                print(f"\n4️⃣ TESTE: Salvar edição do orçamento")
                
                edit_data = {
                    'cliente': cliente.id,
                    'data_entrega': '2025-10-01',
                    'data_validade': '2025-09-16',
                    'status': 'aprovado',
                    'desconto_valor': '',
                    'desconto_percentual': '10',
                    'acrescimo_valor': '',
                    'acrescimo_percentual': '',
                }
                
                response = client.post(f'/orcamentos/{novo_orcamento.pk}/editar/', data=edit_data)
                
                if response.status_code == 302:
                    print("✅ Edição salva com sucesso")
                    
                    # Verificar se as mudanças foram aplicadas
                    novo_orcamento.refresh_from_db()
                    if novo_orcamento.status == 'aprovado':
                        print("  ✅ Status atualizado corretamente")
                    if novo_orcamento.desconto_percentual == 10:
                        print("  ✅ Desconto atualizado corretamente")
                else:
                    print(f"❌ Erro ao salvar edição: {response.status_code}")
                    if response.content:
                        print(f"  Conteúdo: {response.content.decode('utf-8')[:200]}...")
            else:
                print(f"❌ Erro ao carregar página de edição: {response.status_code}")
        else:
            print("❌ Orçamento não foi criado no banco de dados")
    else:
        print(f"❌ Erro ao criar orçamento: {response.status_code}")
        if response.content:
            print(f"  Conteúdo: {response.content.decode('utf-8')[:200]}...")
    
    print("\n" + "=" * 50)
    print("🧪 TESTE FUNCIONAL CONCLUÍDO")

if __name__ == '__main__':
    teste_funcional()
