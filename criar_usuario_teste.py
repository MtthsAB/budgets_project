#!/usr/bin/env python3

import os
import sys
import django

# Configurar Django
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(BASE_DIR)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema_produtos.settings')
django.setup()

from django.contrib.auth.models import User

def criar_usuario_teste():
    """Criar um usuário de teste para visualizar as banquetas"""
    
    # Verificar se o usuário já existe
    if User.objects.filter(username='teste').exists():
        print("✅ Usuário 'teste' já existe")
        user = User.objects.get(username='teste')
    else:
        # Criar usuário de teste
        user = User.objects.create_user(
            username='teste',
            email='teste@teste.com',
            password='123456',
            first_name='Usuário',
            last_name='Teste'
        )
        print("✅ Usuário 'teste' criado com sucesso")
    
    print(f"📧 Username: teste")
    print(f"🔑 Password: 123456")
    print(f"👤 Nome: {user.get_full_name()}")
    print("\n🌐 Agora você pode fazer login em: http://localhost:8000/auth/login/")
    print("📦 E visualizar as banquetas em: http://localhost:8000/produtos/")

if __name__ == "__main__":
    criar_usuario_teste()
