#!/usr/bin/env python
"""
Script para promover um usuário existente a administrador
"""

import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema_produtos.settings')
django.setup()

from authentication.models import CustomUser, TipoPermissao

def promover_usuario_admin():
    """Promove um usuário existente a admin"""
    
    print("="*60)
    print("PROMOVER USUÁRIO PARA ADMINISTRADOR")
    print("="*60)
    print()
    
    # Listar usuários existentes
    usuarios = CustomUser.objects.all()
    if not usuarios.exists():
        print("❌ Nenhum usuário encontrado no sistema!")
        return False
    
    print("Usuários existentes:")
    for i, user in enumerate(usuarios, 1):
        print(f"{i}. {user.email} - Tipo: {user.get_tipo_permissao_display()}")
    
    print()
    email = input("Digite o email do usuário que deseja promover a admin: ").strip()
    
    try:
        usuario = CustomUser.objects.get(email=email)
        
        print()
        print(f"Usuário encontrado: {usuario.email}")
        print(f"Nome: {usuario.get_full_name()}")
        print(f"Tipo atual: {usuario.get_tipo_permissao_display()}")
        print(f"É staff: {usuario.is_staff}")
        print(f"É superuser: {usuario.is_superuser}")
        
        print()
        confirmacao = input(f"Deseja promover {email} a ADMIN? (s/n): ").strip().lower()
        
        if confirmacao == 's':
            # Atualizar permissões
            usuario.tipo_permissao = TipoPermissao.ADMIN
            usuario.is_staff = True
            usuario.is_superuser = True
            usuario.save()
            
            print()
            print("✅ USUÁRIO PROMOVIDO COM SUCESSO!")
            print(f"   Email: {usuario.email}")
            print(f"   Tipo: {usuario.get_tipo_permissao_display()}")
            print(f"   Staff: {usuario.is_staff}")
            print(f"   Superuser: {usuario.is_superuser}")
            print()
            print("O usuário agora tem acesso a:")
            print("   ✓ Home")
            print("   ✓ Produtos")
            print("   ✓ Clientes")
            print("   ✓ Orçamentos")
            print("   ✓ Admin panel")
            
            return True
        else:
            print("❌ Operação cancelada.")
            return False
            
    except CustomUser.DoesNotExist:
        print(f"❌ Usuário com email '{email}' não encontrado!")
        return False
    except Exception as e:
        print(f"❌ Erro ao promover usuário: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Função principal"""
    try:
        if promover_usuario_admin():
            print("\n" + "="*60)
            print("PROMOÇÃO CONCLUÍDA COM SUCESSO!")
            print("="*60)
            return 0
        else:
            return 1
            
    except Exception as e:
        print(f"❌ Erro geral: {str(e)}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
