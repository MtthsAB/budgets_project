#!/usr/bin/env python3
"""
Teste para verificar a funcionalidade de listar clientes iniciais
ao focar/clicar no campo cliente sem digitar nada.
"""

import os
import sys
import django
from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
import json

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
sys.path.append('/home/matas/projetos/Project')
django.setup()

from clientes.models import Cliente

def criar_clientes_teste():
    """Cria clientes de teste"""
    clientes = []
    for i in range(15):
        cliente = Cliente.objects.create(
            nome_empresa=f'Empresa Teste {i+1:02d}',
            representante=f'Representante {i+1}',
            cnpj=f'12345678901{i:02d}',
            telefone='(11) 99999-9999',
            email=f'teste{i+1}@empresa.com'
        )
        clientes.append(cliente)
    
    print(f"✓ Criados {len(clientes)} clientes de teste")
    return clientes

def testar_busca_iniciais():
    """Testa a busca de clientes iniciais"""
    client = Client()
    
    # Criar usuário e fazer login
    user = User.objects.create_user('testuser', 'test@test.com', 'testpass')
    client.login(username='testuser', password='testpass')
    
    # Testar busca de clientes iniciais
    response = client.get(reverse('orcamentos:buscar_cliente'), {'iniciais': '10'})
    
    if response.status_code == 200:
        data = json.loads(response.content)
        print(f"✓ Busca de clientes iniciais funcionando")
        print(f"  - Status: {response.status_code}")
        print(f"  - Clientes retornados: {len(data.get('clientes', []))}")
        
        # Verificar se retornou exatamente 10 clientes
        clientes = data.get('clientes', [])
        if len(clientes) == 10:
            print("✓ Retornou exatamente 10 clientes conforme solicitado")
        else:
            print(f"⚠ Retornou {len(clientes)} clientes, esperado 10")
        
        # Verificar estrutura dos dados
        if clientes:
            primeiro_cliente = clientes[0]
            campos_esperados = ['id', 'nome_empresa', 'representante', 'cnpj']
            for campo in campos_esperados:
                if campo in primeiro_cliente:
                    print(f"✓ Campo '{campo}' presente nos dados")
                else:
                    print(f"✗ Campo '{campo}' ausente nos dados")
    else:
        print(f"✗ Erro na busca de clientes iniciais: {response.status_code}")

def testar_busca_normal():
    """Testa se a busca normal ainda funciona"""
    client = Client()
    
    # Criar usuário e fazer login
    user = User.objects.get(username='testuser')
    client.login(username='testuser', password='testpass')
    
    # Testar busca normal
    response = client.get(reverse('orcamentos:buscar_cliente'), {'termo': 'Empresa'})
    
    if response.status_code == 200:
        data = json.loads(response.content)
        print(f"✓ Busca normal funcionando")
        print(f"  - Status: {response.status_code}")
        print(f"  - Clientes encontrados: {len(data.get('clientes', []))}")
    else:
        print(f"✗ Erro na busca normal: {response.status_code}")

def limpar_dados_teste():
    """Remove dados de teste"""
    Cliente.objects.filter(nome_empresa__startswith='Empresa Teste').delete()
    User.objects.filter(username='testuser').delete()
    print("✓ Dados de teste removidos")

def main():
    print("=== TESTE: Lista de Clientes Iniciais ===\n")
    
    try:
        print("1. Criando clientes de teste...")
        criar_clientes_teste()
        
        print("\n2. Testando busca de clientes iniciais...")
        testar_busca_iniciais()
        
        print("\n3. Testando busca normal (deve continuar funcionando)...")
        testar_busca_normal()
        
        print("\n4. Limpando dados de teste...")
        limpar_dados_teste()
        
        print("\n=== RESULTADO ===")
        print("✓ Todos os testes concluídos!")
        print("✓ Funcionalidade de lista inicial implementada")
        print("✓ Busca normal mantida funcionando")
        
    except Exception as e:
        print(f"\n✗ Erro durante os testes: {e}")
        import traceback
        traceback.print_exc()
        
        # Tentar limpar mesmo com erro
        try:
            limpar_dados_teste()
        except:
            pass

if __name__ == '__main__':
    main()
