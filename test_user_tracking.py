#!/usr/bin/env python
"""
Script de teste para validar o rastreamento de usuários
"""

import os
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema_produtos.settings')
django.setup()

from django.contrib.auth import get_user_model
from produtos.models import TipoItem, Item
from clientes.models import Cliente
from sistema_produtos.mixins import track_user_changes

User = get_user_model()

def test_user_tracking():
    """Teste básico do rastreamento de usuários"""
    
    print("🧪 Iniciando testes de rastreamento de usuários...")
    
    # Obter ou criar um usuário de teste
    test_user, created = User.objects.get_or_create(
        email='test@test.com',
        defaults={
            'first_name': 'Test',
            'last_name': 'User',
            'is_active': True
        }
    )
    
    if created:
        test_user.set_password('testpassword')
        test_user.save()
        print(f"✅ Usuário de teste criado: {test_user.email}")
    else:
        print(f"✅ Usuário de teste encontrado: {test_user.email}")
    
    # Teste 1: Criar TipoItem
    print("\n📋 Teste 1: Criando TipoItem...")
    tipo_test = TipoItem(nome='Teste Tipo')
    track_user_changes(tipo_test, test_user)
    tipo_test.save()
    
    # Verificar se os campos foram definidos
    tipo_test.refresh_from_db()
    assert tipo_test.created_by == test_user, "created_by não foi definido corretamente"
    assert tipo_test.updated_by == test_user, "updated_by não foi definido corretamente"
    print(f"✅ TipoItem criado por: {tipo_test.created_by.get_full_name()}")
    
    # Teste 2: Editar TipoItem com outro usuário
    print("\n📝 Teste 2: Editando TipoItem...")
    admin_user = User.objects.filter(is_superuser=True).first()
    if admin_user:
        tipo_test.nome = 'Teste Tipo Editado'
        track_user_changes(tipo_test, admin_user)
        tipo_test.save()
        
        tipo_test.refresh_from_db()
        assert tipo_test.created_by == test_user, "created_by não deveria ter mudado"
        assert tipo_test.updated_by == admin_user, "updated_by não foi atualizado"
        print(f"✅ TipoItem editado por: {tipo_test.updated_by.get_full_name()}")
    
    # Teste 3: Criar Item
    print("\n📦 Teste 3: Criando Item...")
    item_test = Item(
        ref_produto='TEST001',
        nome_produto='Produto Teste',
        id_tipo_produto=tipo_test,
        ativo=True
    )
    track_user_changes(item_test, test_user)
    item_test.save()
    
    item_test.refresh_from_db()
    assert item_test.created_by == test_user, "Item: created_by não foi definido"
    assert item_test.updated_by == test_user, "Item: updated_by não foi definido"
    print(f"✅ Item criado por: {item_test.created_by.get_full_name()}")
    
    # Teste 4: Criar Cliente
    print("\n👤 Teste 4: Criando Cliente...")
    cliente_test = Cliente(
        nome_empresa='Empresa Teste',
        representante='João Teste',
        cnpj='12.345.678/0001-90',
        logradouro='Rua Teste',
        numero='123',
        bairro='Bairro Teste',
        cidade='Cidade Teste',
        estado='SP',
        cep='12345-678',
        telefone='(11) 99999-9999',
        email='empresa@teste.com'
    )
    track_user_changes(cliente_test, test_user)
    cliente_test.save()
    
    cliente_test.refresh_from_db()
    assert cliente_test.created_by == test_user, "Cliente: created_by não foi definido"
    assert cliente_test.updated_by == test_user, "Cliente: updated_by não foi definido"
    print(f"✅ Cliente criado por: {cliente_test.created_by.get_full_name()}")
    
    # Limpar dados de teste
    print("\n🧹 Limpando dados de teste...")
    item_test.delete()
    tipo_test.delete()
    cliente_test.delete()
    if created:
        test_user.delete()
    
    print("\n🎉 Todos os testes passaram! O sistema de rastreamento está funcionando corretamente.")

if __name__ == '__main__':
    test_user_tracking()
