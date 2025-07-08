#!/usr/bin/env python3
"""
Script para verificar URLs do sistema
"""
import os
import django
from django.conf import settings

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema_produtos.settings')
django.setup()

from django.urls import reverse
from django.urls.exceptions import NoReverseMatch

def main():
    print("🔍 VERIFICAÇÃO DE URLs DO SISTEMA")
    print("=" * 50)
    
    # URLs importantes do sistema
    urls_sistema = [
        # Clientes
        ('cliente_lista', 'Listar Clientes'),
        ('cliente_cadastro', 'Novo Cliente'),
        
        # Orçamentos
        ('orcamentos:listar', 'Listar Orçamentos'),
        ('orcamentos:novo', 'Novo Orçamento'),
        
        # Produtos
        ('produtos_lista', 'Listar Produtos'),
        ('produto_cadastro', 'Novo Produto'),
        
        # Autenticação
        ('login', 'Login'),
        ('logout', 'Logout'),
        ('home', 'Home'),
        
        # Usuários
        ('usuarios_lista', 'Listar Usuários'),
        ('usuario_novo', 'Novo Usuário'),
    ]
    
    print("📋 URLs Verificadas:")
    for url_name, description in urls_sistema:
        try:
            url = reverse(url_name)
            print(f"✅ {description}: {url}")
        except NoReverseMatch as e:
            print(f"❌ {description}: ERRO - {e}")
        except Exception as e:
            print(f"⚠️  {description}: ERRO DESCONHECIDO - {e}")
    
    print("\n🎯 Verificação concluída!")

if __name__ == "__main__":
    main()
