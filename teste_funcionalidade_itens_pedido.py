#!/usr/bin/env python
"""
Script para testar a funcionalidade de Itens do Pedido
"""
import os
import django
import requests
from django.test import Client
from django.contrib.auth import get_user_model

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema_produtos.settings')
django.setup()

from produtos.models import Produto, TipoItem
from orcamentos.models import Orcamento, OrcamentoItem
from clientes.models import Cliente

def test_produtos_por_tipo():
    """Testa o endpoint de produtos por tipo"""
    print("=== Testando endpoint produtos-por-tipo ===")
    
    # Verificar tipos disponíveis
    print("\nTipos de produto disponíveis:")
    tipos = TipoItem.objects.all()
    for tipo in tipos:
        print(f"- {tipo.nome}")
    
    # Verificar produtos
    print(f"\nTotal de produtos: {Produto.objects.count()}")
    print(f"Produtos ativos: {Produto.objects.filter(ativo=True).count()}")
    
    # Testar endpoint para cada tipo
    client = Client()
    
    # Fazer login
    User = get_user_model()
    user = User.objects.filter(email='admin@essere.com').first()
    if user:
        client.force_login(user)
        print(f"\nUsuário logado: {user.email}")
    else:
        print("\nERRO: Usuário admin não encontrado!")
        return
    
    # Testar tipos mapeados
    tipos_teste = ['sofa', 'banqueta', 'cadeira', 'poltrona', 'pufe', 'almofada', 'acessorio']
    
    for tipo in tipos_teste:
        print(f"\n--- Testando tipo: {tipo} ---")
        response = client.get(f'/orcamentos/produtos-por-tipo/?tipo={tipo}')
        
        if response.status_code == 200:
            data = response.json()
            produtos = data.get('produtos', [])
            print(f"Status: OK - {len(produtos)} produtos encontrados")
            
            # Mostrar primeiros 3 produtos
            for produto in produtos[:3]:
                print(f"  - {produto['nome_produto']} ({produto['ref_produto']})")
        else:
            print(f"Status: ERRO {response.status_code}")
            print(f"Resposta: {response.content.decode()}")

def test_orcamento_form():
    """Testa o acesso ao formulário de orçamento"""
    print("\n=== Testando formulário de orçamento ===")
    
    client = Client()
    User = get_user_model()
    user = User.objects.filter(email='admin@essere.com').first()
    
    if user:
        client.force_login(user)
        
        # Testar formulário novo
        response = client.get('/orcamentos/novo/')
        print(f"Novo orçamento - Status: {response.status_code}")
        
        if response.status_code == 200:
            # Verificar se o template contém elementos esperados
            content = response.content.decode()
            elementos = [
                'Itens do Pedido',
                'modalAdicionarItem',
                'produtos-por-tipo',
                'btnAdicionarItem'
            ]
            
            for elemento in elementos:
                if elemento in content:
                    print(f"✓ {elemento} encontrado no template")
                else:
                    print(f"✗ {elemento} NÃO encontrado no template")
        
        # Testar com orçamento existente
        orcamento = Orcamento.objects.first()
        if orcamento:
            response = client.get(f'/orcamentos/{orcamento.pk}/editar/')
            print(f"Editar orçamento - Status: {response.status_code}")
        else:
            print("Nenhum orçamento encontrado para testar edição")
    else:
        print("ERRO: Usuário admin não encontrado!")

def verificar_estrutura_db():
    """Verifica estrutura do banco de dados"""
    print("\n=== Verificando estrutura do banco ===")
    
    # Verificar modelos
    print(f"Tipos de produto: {TipoItem.objects.count()}")
    print(f"Produtos: {Produto.objects.count()}")
    print(f"Clientes: {Cliente.objects.count()}")
    print(f"Orçamentos: {Orcamento.objects.count()}")
    print(f"Itens de orçamento: {OrcamentoItem.objects.count()}")
    
    # Verificar usuários
    User = get_user_model()
    admin = User.objects.filter(email='admin@essere.com').first()
    print(f"Admin user: {'OK' if admin else 'NÃO ENCONTRADO'}")
    
    # Verificar se há produtos por tipo
    print("\nProdutos por tipo:")
    for tipo in TipoItem.objects.all():
        count = Produto.objects.filter(id_tipo_produto=tipo, ativo=True).count()
        print(f"  {tipo.nome}: {count} produtos")

if __name__ == "__main__":
    print("Testando funcionalidade Itens do Pedido...")
    
    verificar_estrutura_db()
    test_produtos_por_tipo()
    test_orcamento_form()
    
    print("\n=== Teste concluído ===")
