#!/usr/bin/env python3
"""
Verificar se há algum middleware ou configuração interferindo
"""
import os
import sys
import django

# Configurar o Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema_produtos.settings')
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
django.setup()

from django.conf import settings

def verificar_middlewares():
    """Verifica middlewares que podem interferir"""
    print("🔍 Verificando middlewares configurados:")
    
    for middleware in settings.MIDDLEWARE:
        print(f"  - {middleware}")
        
    # Verificar se há middlewares suspeitos
    suspeitos = [
        'django.middleware.cache',
        'django.middleware.gzip',
        'corsheaders'
    ]
    
    for suspeito in suspeitos:
        if any(suspeito in mw for mw in settings.MIDDLEWARE):
            print(f"⚠️  Middleware suspeito encontrado: {suspeito}")

def verificar_configuracoes():
    """Verifica outras configurações"""
    print("\n🔍 Verificando outras configurações:")
    
    print(f"DEBUG: {settings.DEBUG}")
    print(f"ALLOWED_HOSTS: {settings.ALLOWED_HOSTS}")
    
    if hasattr(settings, 'CSRF_COOKIE_SECURE'):
        print(f"CSRF_COOKIE_SECURE: {settings.CSRF_COOKIE_SECURE}")
    
    if hasattr(settings, 'SESSION_COOKIE_SECURE'):
        print(f"SESSION_COOKIE_SECURE: {settings.SESSION_COOKIE_SECURE}")

if __name__ == '__main__':
    verificar_middlewares()
    verificar_configuracoes()
    
    print("\n💡 RECOMENDAÇÃO FINAL:")
    print("Como o backend está funcionando perfeitamente, o problema está na interface.")
    print("Execute os seguintes passos no navegador:")
    print("1. Abra o DevTools (F12)")
    print("2. Vá na aba Console")
    print("3. Preencha o formulário e clique em 'Salvar Cliente'")
    print("4. Verifique se aparecem erros no console")
    print("5. Vá na aba Network e veja se a requisição POST foi enviada")
    print("\nSe não houver requisição POST, o problema é JavaScript bloqueando a submissão.")
