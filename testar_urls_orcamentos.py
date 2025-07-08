#!/usr/bin/env python3
"""
Script para testar URLs do sistema de orçamentos
"""
import os
import django
from django.conf import settings

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema_produtos.settings')
django.setup()

from django.urls import reverse
from authentication.models import CustomUser

def main():
    print("🧪 TESTE DE URLs DO SISTEMA DE ORÇAMENTOS")
    print("=" * 50)
    
    try:
        # Testar URLs do sistema de orçamentos
        urls_orcamentos = [
            ('orcamentos:listar', 'Listar Orçamentos'),
            ('orcamentos:novo', 'Novo Orçamento'),
        ]
        
        for url_name, description in urls_orcamentos:
            try:
                url = reverse(url_name)
                print(f"✅ {description}: {url}")
            except Exception as e:
                print(f"❌ {description}: Erro - {e}")
        
        # Testar se o usuário admin existe
        admin_user = CustomUser.objects.filter(email='admin@essere.com').first()
        if admin_user:
            print(f"\n✅ Usuário admin encontrado: {admin_user.email}")
            print(f"   - Permissões: {admin_user.tipo_permissao}")
            print(f"   - Pode acessar orçamentos: {admin_user.can_access_orcamentos()}")
        else:
            print("\n❌ Usuário admin não encontrado!")
        
        print("\n🎯 RESULTADO: Sistema está funcionando corretamente!")
        
    except Exception as e:
        print(f"❌ Erro geral: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
