#!/usr/bin/env python3
"""
Teste direto da funcionalidade de cadastro de clientes
"""
import os
import sys
import django

# Configurar o Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema_produtos.settings')
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
django.setup()

from django.contrib.auth import get_user_model
from clientes.forms import ClienteForm
from clientes.models import Cliente
from clientes.views import cliente_cadastro
from django.http import HttpRequest
from django.contrib.auth.models import AnonymousUser
from unittest.mock import Mock

User = get_user_model()

def test_cadastro_direto():
    """Testa o cadastro de cliente diretamente"""
    print("🔍 Testando cadastro direto de cliente...")
    
    # Obter usuário admin
    try:
        admin = User.objects.get(email='admin@essere.com')
        print(f"✅ Usuário admin encontrado: {admin.email}")
        print(f"   Tipo de permissão: {admin.tipo_permissao}")
        print(f"   Pode acessar clientes: {admin.can_access_clientes()}")
    except User.DoesNotExist:
        print("❌ Usuário admin não encontrado")
        return False
    
    # Simular uma requisição POST
    request = HttpRequest()
    request.method = 'POST'
    request.user = admin
    
    # Dados do cliente
    request.POST = {
        'nome_empresa': 'Empresa Teste Direto Ltda',
        'representante': 'Carlos Silva',
        'cnpj': '45.678.901/0001-23',
        'logradouro': 'Rua do Teste',
        'numero': '789',
        'bairro': 'Bairro Teste',
        'cidade': 'Cidade Teste',
        'estado': 'SP',
        'cep': '12345-678',
        'telefone': '(11) 91234-5678',
        'email': 'teste_direto@empresa.com'
    }
    
    # Mock para messages
    request._messages = Mock()
    
    try:
        # Testar formulário primeiro
        form = ClienteForm(data=request.POST)
        if form.is_valid():
            print("✅ Formulário válido")
            
            # Testar salvamento
            cliente = form.save(commit=False)
            cliente.save()
            print(f"✅ Cliente salvo: {cliente.nome_empresa}")
            
            # Verificar se foi salvo no banco
            cliente_db = Cliente.objects.get(cnpj='45.678.901/0001-23')
            print(f"✅ Cliente encontrado no banco: {cliente_db.nome_empresa}")
            
            return True
        else:
            print("❌ Formulário inválido:")
            for field, errors in form.errors.items():
                print(f"  - {field}: {errors}")
            return False
            
    except Exception as e:
        print(f"❌ Erro durante o teste: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def test_validacao_cnpj():
    """Testa a validação de CNPJ"""
    print("\n🔍 Testando validação de CNPJ...")
    
    # Teste com CNPJ inválido
    dados_invalidos = {
        'nome_empresa': 'Empresa Teste CNPJ',
        'representante': 'João Silva',
        'cnpj': '12.345.678/0001-00',  # CNPJ inválido
        'logradouro': 'Rua das Flores',
        'numero': '123',
        'bairro': 'Centro',
        'cidade': 'São Paulo',
        'estado': 'SP',
        'cep': '01234-567',
        'telefone': '(11) 99999-9999',
        'email': 'teste_cnpj@empresa.com'
    }
    
    form = ClienteForm(data=dados_invalidos)
    if not form.is_valid():
        print("✅ Validação de CNPJ funcionando corretamente")
        print("Erros esperados:")
        for field, errors in form.errors.items():
            print(f"  - {field}: {errors}")
        return True
    else:
        print("❌ Validação de CNPJ não está funcionando")
        return False

def main():
    print("🚀 Teste direto da funcionalidade de cadastro de clientes\n")
    
    # Testar cadastro direto
    cadastro_ok = test_cadastro_direto()
    
    # Testar validação
    validacao_ok = test_validacao_cnpj()
    
    print("\n📊 RESUMO DOS TESTES:")
    print(f"  Cadastro direto: {'✅' if cadastro_ok else '❌'}")
    print(f"  Validação CNPJ: {'✅' if validacao_ok else '❌'}")
    
    if cadastro_ok and validacao_ok:
        print("\n🎉 Sistema de cadastro funcionando corretamente!")
        print("\n💡 Se o botão 'Salvar Cliente' não está funcionando na interface,")
        print("   o problema pode estar no JavaScript ou na submissão do formulário.")
    else:
        print("\n⚠️  Foram encontrados problemas no sistema de cadastro.")

if __name__ == '__main__':
    main()
