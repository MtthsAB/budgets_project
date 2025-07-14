#!/usr/bin/env python3
"""
Script para configurar permissões do usuário admin
"""
import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema_produtos.settings')
sys.path.append('/home/matas/projetos/Project')
django.setup()

from authentication.models import CustomUser, TipoPermissao

def main():
    try:
        user = CustomUser.objects.get(email='admin@test.com')
        print(f"Usuario encontrado: {user.email}")
        print(f"Tipo permissao atual: {user.tipo_permissao}")
        
        # Atualizar para MASTER
        user.tipo_permissao = TipoPermissao.MASTER
        user.save()
        
        print(f"Novo tipo permissao: {user.tipo_permissao}")
        print(f"Pode acessar orcamentos: {user.can_access_orcamentos()}")
        print("✅ Permissões atualizadas com sucesso!")
        
    except CustomUser.DoesNotExist:
        print("❌ Usuário admin@test.com não encontrado!")
    except Exception as e:
        print(f"❌ Erro: {e}")

if __name__ == "__main__":
    main()
