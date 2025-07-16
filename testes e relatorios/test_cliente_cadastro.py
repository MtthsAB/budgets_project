#!/usr/bin/env python3
"""
Teste de cadastro de clientes para diagnosticar problemas
"""
import os
import sys
import django

# Configurar o Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema_produtos.settings')
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
django.setup()

from django.test import TestCase, Client
from django.urls import reverse
from clientes.forms import ClienteForm
from clientes.models import Cliente
from django.contrib.auth import get_user_model

User = get_user_model()

def test_cliente_form_valido():
    """Testa se o formulário de cliente aceita dados válidos"""
    print("🔍 Testando formulário de cliente...")
    
    dados_validos = {
        'nome_empresa': f'Nova Empresa Teste {Cliente.objects.count() + 1} Ltda',
        'representante': 'João Silva',
        'cnpj': f'{20 + Cliente.objects.count()}.222.333/0001-44',
        'logradouro': 'Rua das Flores',
        'numero': '123',
        'bairro': 'Centro',
        'cidade': 'São Paulo',
        'estado': 'SP',
        'cep': '01234-567',
        'telefone': '(11) 99999-9999',
        'email': f'teste{Cliente.objects.count() + 1}@empresa.com'
    }
    
    form = ClienteForm(data=dados_validos)
    
    if form.is_valid():
        print("✅ Formulário está válido!")
        try:
            cliente = form.save()
            print(f"✅ Cliente salvo com sucesso: {cliente.nome_empresa}")
            return True
        except Exception as e:
            print(f"❌ Erro ao salvar cliente: {str(e)}")
            return False
    else:
        print("❌ Formulário inválido!")
        print("Erros encontrados:")
        for field, errors in form.errors.items():
            print(f"  - {field}: {errors}")
        return False

def test_view_cadastro():
    """Testa a view de cadastro diretamente"""
    print("\n🔍 Testando view de cadastro...")
    
    # Criar usuário de teste
    try:
        user = User.objects.filter(is_superuser=True).first()
        if not user:
            print("❌ Nenhum superusuário encontrado. Criando usuário de teste...")
            user = User.objects.create_user(
                email='test@test.com',
                password='test_pass',
                is_staff=True,
                is_superuser=True
            )
            print("✅ Usuário de teste criado")
        else:
            print(f"✅ Usuário {user.email} encontrado")
    except Exception as e:
        print(f"❌ Erro ao verificar usuário: {str(e)}")
        return False
    
    # Criar cliente de teste
    client = Client()
    
    # Fazer login
    login_success = False
    
    # Tentar várias combinações de login
    login_attempts = [
        (user.email, 'test_pass'),
        ('admin@essere.com', 'admin123'),
        ('admin@admin.com', 'admin'),
        ('master@master.com', 'master'),
    ]
    
    for email, password in login_attempts:
        login_success = client.login(username=email, password=password)  # Django usa 'username' mesmo com email
        if login_success:
            print(f"✅ Login realizado com sucesso usando {email}")
            break
    
    if not login_success:
        print("❌ Falha no login com todas as tentativas")
        return False
    
    dados_post = {
        'nome_empresa': f'Empresa Teste View {Cliente.objects.count() + 1}',
        'representante': 'Maria Santos',
        'cnpj': f'{30 + Cliente.objects.count()}.765.432/0001-10',
        'logradouro': 'Av. Principal',
        'numero': '456',
        'bairro': 'Jardim',
        'cidade': 'Rio de Janeiro',
        'estado': 'RJ',
        'cep': '20000-000',
        'telefone': '(21) 88888-8888',
        'email': f'testeview{Cliente.objects.count() + 1}@empresa.com'
    }
    
    try:
        response = client.post(reverse('cliente_cadastro'), data=dados_post)
        
        if response.status_code == 302:  # Redirect após sucesso
            print("✅ Cadastro realizado com sucesso (redirect detectado)")
            return True
        elif response.status_code == 200:
            # Verificar se há erros no contexto
            if hasattr(response, 'context') and response.context:
                form = response.context.get('form')
                if form and form.errors:
                    print("❌ Erros no formulário:")
                    for field, errors in form.errors.items():
                        print(f"  - {field}: {errors}")
                else:
                    print("⚠️  Formulário retornado mas sem erros visíveis")
            else:
                print("⚠️  Resposta 200 mas sem contexto disponível")
            return False
        else:
            print(f"❌ Código de status inesperado: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Erro ao testar view: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def verificar_tabela_clientes():
    """Verifica se a tabela de clientes existe e está acessível"""
    print("\n🔍 Verificando tabela de clientes...")
    
    try:
        # Verificar se conseguimos contar clientes
        count = Cliente.objects.count()
        print(f"✅ Tabela acessível. Total de clientes: {count}")
        
        # Listar alguns clientes se existirem
        if count > 0:
            print("Clientes existentes:")
            for cliente in Cliente.objects.all()[:3]:
                print(f"  - {cliente.nome_empresa} ({cliente.cnpj})")
        
        return True
    except Exception as e:
        print(f"❌ Erro ao acessar tabela: {str(e)}")
        return False

def main():
    print("🚀 Iniciando diagnóstico do sistema de cadastro de clientes...\n")
    
    # Verificar tabela
    table_ok = verificar_tabela_clientes()
    
    # Testar formulário
    form_ok = test_cliente_form_valido()
    
    # Testar view
    view_ok = test_view_cadastro()
    
    print("\n📊 RESUMO DOS TESTES:")
    print(f"  Tabela de clientes: {'✅' if table_ok else '❌'}")
    print(f"  Formulário de cliente: {'✅' if form_ok else '❌'}")
    print(f"  View de cadastro: {'✅' if view_ok else '❌'}")
    
    if all([table_ok, form_ok, view_ok]):
        print("\n🎉 Todos os testes passaram! O sistema parece estar funcionando.")
    else:
        print("\n⚠️  Alguns testes falharam. Verifique os detalhes acima.")

if __name__ == '__main__':
    main()
