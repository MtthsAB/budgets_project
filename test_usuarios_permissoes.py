#!/usr/bin/env python
"""
Script de teste para verificar o sistema de usuários e permissões
"""
import os
import sys
import django
from pathlib import Path

# Setup Django
sys.path.append(str(Path(__file__).parent))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema_produtos.settings')
django.setup()

from authentication.models import CustomUser, TipoPermissao

def test_user_permissions():
    """Testa as permissões dos usuários"""
    print("=== TESTE DE PERMISSÕES ===")
    
    # Teste para cada tipo de usuário
    test_cases = [
        {
            'tipo': TipoPermissao.MASTER,
            'expected_permissions': {
                'can_access_home': True,
                'can_access_produtos': True,
                'can_access_clientes': True,
                'can_access_orcamentos': True,
                'can_manage_users': True,
            }
        },
        {
            'tipo': TipoPermissao.ADMIN,
            'expected_permissions': {
                'can_access_home': True,
                'can_access_produtos': True,
                'can_access_clientes': True,
                'can_access_orcamentos': True,
                'can_manage_users': False,
            }
        },
        {
            'tipo': TipoPermissao.VENDEDOR,
            'expected_permissions': {
                'can_access_home': False,
                'can_access_produtos': False,
                'can_access_clientes': False,
                'can_access_orcamentos': True,
                'can_manage_users': False,
            }
        },
        {
            'tipo': TipoPermissao.OPERADOR_PRODUTOS,
            'expected_permissions': {
                'can_access_home': False,
                'can_access_produtos': True,
                'can_access_clientes': False,
                'can_access_orcamentos': False,
                'can_manage_users': False,
            }
        },
    ]
    
    # Criar usuários de teste
    test_users = []
    for i, test_case in enumerate(test_cases):
        email = f"test_{test_case['tipo'].lower()}@test.com"
        
        # Remover usuário existente se houver
        CustomUser.objects.filter(email=email).delete()
        
        # Criar usuário
        user = CustomUser.objects.create_user(
            email=email,
            password='testpass123',
            first_name='Test',
            last_name=f'User {i+1}',
            tipo_permissao=test_case['tipo']
        )
        test_users.append(user)
    
    # Executar testes
    all_passed = True
    
    for user, test_case in zip(test_users, test_cases):
        print(f"\nTestando usuário: {user.email} ({user.get_tipo_permissao_display()})")
        
        for permission, expected in test_case['expected_permissions'].items():
            actual = getattr(user, permission)()
            status = "✓" if actual == expected else "✗"
            
            if actual != expected:
                all_passed = False
                
            print(f"  {status} {permission}: {actual} (esperado: {expected})")
    
    # Limpar usuários de teste
    for user in test_users:
        user.delete()
    
    print(f"\n=== RESULTADO FINAL ===")
    if all_passed:
        print("✓ Todos os testes passaram!")
    else:
        print("✗ Alguns testes falharam!")
    
    return all_passed

def test_user_creation():
    """Testa a criação de usuários"""
    print("\n=== TESTE DE CRIAÇÃO DE USUÁRIOS ===")
    
    # Teste criação de usuário Master
    email = "master@test.com"
    
    # Remover se existir
    CustomUser.objects.filter(email=email).delete()
    
    try:
        user = CustomUser.objects.create_user(
            email=email,
            password='masterpass123',
            first_name='Master',
            last_name='User',
            tipo_permissao=TipoPermissao.MASTER
        )
        
        # Verificar se foi criado corretamente
        assert user.email == email
        assert user.tipo_permissao == TipoPermissao.MASTER
        assert user.can_manage_users()
        
        print(f"✓ Usuário Master criado com sucesso: {user.email}")
        
        # Limpar
        user.delete()
        
        return True
        
    except Exception as e:
        print(f"✗ Erro ao criar usuário Master: {e}")
        return False

def main():
    """Executa todos os testes"""
    print("Iniciando testes do sistema de usuários e permissões...")
    
    test1_passed = test_user_permissions()
    test2_passed = test_user_creation()
    
    print("\n" + "="*50)
    if test1_passed and test2_passed:
        print("🎉 TODOS OS TESTES PASSARAM!")
        print("O sistema de usuários e permissões está funcionando corretamente.")
    else:
        print("❌ ALGUNS TESTES FALHARAM!")
        print("Verifique os logs acima para mais detalhes.")
    
    return test1_passed and test2_passed

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
