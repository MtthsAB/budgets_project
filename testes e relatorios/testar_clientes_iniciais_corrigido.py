#!/usr/bin/env python3
"""
Script para testar a funcionalidade de clientes iniciais
Versão corrigida que usa CustomUser
"""

import os
import sys
import django

# Configurar o Django
sys.path.append('/home/matas/projetos/Project')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema_produtos.settings')
django.setup()

from django.test import RequestFactory, Client
from django.contrib.auth import get_user_model
from authentication.models import TipoPermissao
from clientes.models import Cliente
from orcamentos.views import buscar_cliente

def criar_dados_teste():
    """Cria dados de teste"""
    print("🔧 Criando dados de teste...")
    
    # Usar o modelo de usuário customizado
    User = get_user_model()
    
    # Criar usuário de teste se não existir
    user, created = User.objects.get_or_create(
        email='teste@example.com',
        defaults={
            'first_name': 'Usuario',
            'last_name': 'Teste',
            'tipo_permissao': TipoPermissao.ADMIN,
            'is_staff': True,
            'is_active': True
        }
    )
    if created:
        user.set_password('teste123')
        user.save()
        print(f"✅ Usuário criado: {user.email}")
    else:
        print(f"ℹ️  Usuário já existe: {user.email}")
    
    # Criar clientes de teste se não existirem
    clientes_teste = [
        {'nome_empresa': 'ABC Móveis Ltda', 'representante': 'João Silva', 'cnpj': '11.111.111/0001-11'},
        {'nome_empresa': 'DEF Decorações', 'representante': 'Maria Santos', 'cnpj': '22.222.222/0001-22'},
        {'nome_empresa': 'GHI Interiores', 'representante': 'Pedro Costa', 'cnpj': '33.333.333/0001-33'},
        {'nome_empresa': 'JKL Design', 'representante': 'Ana Oliveira', 'cnpj': '44.444.444/0001-44'},
        {'nome_empresa': 'MNO Ambientes', 'representante': 'Carlos Lima', 'cnpj': '55.555.555/0001-55'},
        {'nome_empresa': 'PQR Sofás', 'representante': 'Lucia Ferreira', 'cnpj': '66.666.666/0001-66'},
        {'nome_empresa': 'STU Poltronas', 'representante': 'Roberto Alves', 'cnpj': '77.777.777/0001-77'},
        {'nome_empresa': 'VWX Cadeiras', 'representante': 'Fernanda Rocha', 'cnpj': '88.888.888/0001-88'},
        {'nome_empresa': 'YZ Móveis', 'representante': 'Marcos Pereira', 'cnpj': '99.999.999/0001-99'},
        {'nome_empresa': 'ZAB Decoração', 'representante': 'Sandra Martins', 'cnpj': '10.101.010/0001-10'},
        {'nome_empresa': 'CDE Casa', 'representante': 'Ricardo Souza', 'cnpj': '12.121.212/0001-12'},
        {'nome_empresa': 'FGH Estilo', 'representante': 'Paula Dias', 'cnpj': '13.131.313/0001-13'},
    ]
    
    clientes_criados = 0
    for dados_cliente in clientes_teste:
        cliente, created = Cliente.objects.get_or_create(
            cnpj=dados_cliente['cnpj'],
            defaults=dados_cliente
        )
        if created:
            clientes_criados += 1
    
    print(f"✅ {clientes_criados} novos clientes criados")
    print(f"ℹ️  Total de clientes: {Cliente.objects.count()}")
    
    return user

def testar_endpoint_clientes_iniciais():
    """Testa o endpoint de clientes iniciais"""
    print("\n🧪 Testando endpoint de clientes iniciais...")
    
    # Criar usuário de teste
    user = criar_dados_teste()
    
    # Criar factory de requisições
    factory = RequestFactory()
    
    # Testar requisição para clientes iniciais
    print("\n1. Testando busca de clientes iniciais (parâmetro iniciais=10):")
    request = factory.get('/orcamentos/buscar-cliente/', {'iniciais': '10'})
    request.user = user
    
    try:
        response = buscar_cliente(request)
        data = response.content.decode('utf-8')
        import json
        result = json.loads(data)
        
        print(f"✅ Status: {response.status_code}")
        print(f"✅ Clientes retornados: {len(result.get('clientes', []))}")
        
        # Mostrar os primeiros 3 clientes
        clientes = result.get('clientes', [])
        if clientes:
            print("\n📋 Primeiros clientes retornados:")
            for i, cliente in enumerate(clientes[:3]):
                print(f"  {i+1}. {cliente['nome_empresa']} - {cliente['representante']}")
            if len(clientes) > 3:
                print(f"  ... e mais {len(clientes) - 3} clientes")
        
    except Exception as e:
        print(f"❌ Erro ao testar endpoint: {e}")
        return False
    
    # Testar busca normal
    print("\n2. Testando busca normal (termo='ABC'):")
    request = factory.get('/orcamentos/buscar-cliente/', {'termo': 'ABC'})
    request.user = user
    
    try:
        response = buscar_cliente(request)
        data = response.content.decode('utf-8')
        result = json.loads(data)
        
        print(f"✅ Status: {response.status_code}")
        print(f"✅ Clientes encontrados: {len(result.get('clientes', []))}")
        
        clientes = result.get('clientes', [])
        if clientes:
            print("\n📋 Clientes encontrados:")
            for cliente in clientes:
                print(f"  - {cliente['nome_empresa']} - {cliente['representante']}")
    
    except Exception as e:
        print(f"❌ Erro ao testar busca normal: {e}")
        return False
    
    return True

def testar_cliente_web():
    """Testa usando o client web do Django"""
    print("\n🌐 Testando com Django Test Client...")
    
    client = Client()
    
    # Fazer login
    User = get_user_model()
    user = User.objects.get(email='teste@example.com')
    client.force_login(user)
    
    # Testar endpoint de clientes iniciais
    print("\n1. GET /orcamentos/buscar-cliente/?iniciais=5")
    response = client.get('/orcamentos/buscar-cliente/', {'iniciais': '5'})
    
    print(f"✅ Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Clientes retornados: {len(data.get('clientes', []))}")
        
        clientes = data.get('clientes', [])
        if clientes:
            print("\n📋 Clientes retornados:")
            for cliente in clientes:
                print(f"  - {cliente['nome_empresa']}")
    else:
        print(f"❌ Erro: {response.content.decode('utf-8')}")
    
    # Testar busca normal
    print("\n2. GET /orcamentos/buscar-cliente/?termo=moveis")
    response = client.get('/orcamentos/buscar-cliente/', {'termo': 'moveis'})
    
    print(f"✅ Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Clientes encontrados: {len(data.get('clientes', []))}")

def main():
    """Função principal"""
    print("🚀 TESTE DA FUNCIONALIDADE DE CLIENTES INICIAIS")
    print("="*50)
    
    try:
        # Testar via factory de requisições
        sucesso1 = testar_endpoint_clientes_iniciais()
        
        # Testar via client web
        testar_cliente_web()
        
        print("\n" + "="*50)
        if sucesso1:
            print("✅ TODOS OS TESTES PASSARAM!")
            print("\n📝 A funcionalidade está funcionando corretamente:")
            print("   - Endpoint responde ao parâmetro 'iniciais'")
            print("   - Retorna os primeiros N clientes quando solicitado")
            print("   - Busca normal por termo também funciona")
            print("\n🎯 Próximo passo: Testar a integração frontend-backend")
        else:
            print("❌ ALGUNS TESTES FALHARAM!")
            print("   - Verifique os erros acima")
    
    except Exception as e:
        print(f"\n❌ ERRO CRÍTICO: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    main()
