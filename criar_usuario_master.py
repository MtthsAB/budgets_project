#!/usr/bin/env python
"""
Script para recriar o usuário master admin@essere.com
"""

import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema_produtos.settings')
django.setup()

from authentication.models import CustomUser, TipoPermissao

def recriar_usuario_master():
    """Recria o usuário master"""
    
    email = 'admin@essere.com'
    senha = 'admin123'
    
    print("="*50)
    print("RECRIANDO USUÁRIO MASTER")
    print("="*50)
    
    # Verificar se o usuário já existe
    try:
        usuario_existente = CustomUser.objects.get(email=email)
        print(f"Usuário {email} já existe. Removendo...")
        usuario_existente.delete()
        print("Usuário removido com sucesso.")
    except CustomUser.DoesNotExist:
        print(f"Usuário {email} não existe.")
    
    # Criar novo usuário master
    try:
        usuario = CustomUser.objects.create_user(
            email=email,
            password=senha,
            first_name='Admin',
            last_name='Sistema',
            tipo_permissao=TipoPermissao.MASTER,
            is_staff=True,
            is_superuser=True,
            is_active=True
        )
        
        print(f"✅ Usuário master criado com sucesso!")
        print(f"   Email: {email}")
        print(f"   Senha: {senha}")
        print(f"   Tipo: {usuario.get_tipo_permissao_display()}")
        print(f"   Staff: {usuario.is_staff}")
        print(f"   Superuser: {usuario.is_superuser}")
        print(f"   Ativo: {usuario.is_active}")
        
        # Verificar permissões
        print("\nVerificando permissões:")
        print(f"   - Pode acessar home: {usuario.can_access_home()}")
        print(f"   - Pode acessar produtos: {usuario.can_access_produtos()}")
        print(f"   - Pode acessar clientes: {usuario.can_access_clientes()}")
        print(f"   - Pode acessar orçamentos: {usuario.can_access_orcamentos()}")
        print(f"   - Pode gerenciar usuários: {usuario.can_manage_users()}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro ao criar usuário: {str(e)}")
        return False

def main():
    """Função principal"""
    try:
        if recriar_usuario_master():
            print("\n" + "="*50)
            print("USUÁRIO MASTER RECRIADO COM SUCESSO!")
            print("="*50)
            print("\nVocê pode agora:")
            print("1. Acessar http://localhost:8000")
            print("2. Fazer login com admin@essere.com / admin123")
            print("3. Acessar todos os módulos do sistema")
            print("4. Continuar testando o sistema de orçamentos")
            return 0
        else:
            print("\n❌ Falha ao recriar usuário master")
            return 1
            
    except Exception as e:
        print(f"❌ Erro geral: {str(e)}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
