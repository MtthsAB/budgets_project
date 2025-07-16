#!/usr/bin/env python3
"""
Script para verificar e criar o usuário admin
"""
import os
import django
from django.conf import settings

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema_produtos.settings')
django.setup()

from authentication.models import CustomUser

def main():
    print("Verificando usuário admin...")
    
    # Verificar se o usuário admin existe
    admin_user = CustomUser.objects.filter(email='admin@essere.com').first()
    
    if admin_user:
        print(f"✓ Usuário admin encontrado: {admin_user.email}")
        print(f"  - Ativo: {admin_user.is_active}")
        print(f"  - Staff: {admin_user.is_staff}")
        print(f"  - Superuser: {admin_user.is_superuser}")
        print(f"  - Tipo permissão: {admin_user.tipo_permissao}")
    else:
        print("✗ Usuário admin não encontrado. Criando...")
        
        # Criar usuário admin
        admin_user = CustomUser.objects.create_user(
            email='admin@essere.com',
            password='admin123',
            first_name='Admin',
            last_name='Sistema',
            is_active=True,
            is_staff=True,
            is_superuser=True,
            tipo_permissao='admin'
        )
        
        print(f"✓ Usuário admin criado: {admin_user.email}")
        print(f"  - Email: admin@essere.com")
        print(f"  - Senha: admin123")
        print(f"  - Tipo permissão: admin")
    
    # Verificar total de usuários
    total_users = CustomUser.objects.count()
    print(f"\nTotal de usuários no sistema: {total_users}")

if __name__ == "__main__":
    main()
