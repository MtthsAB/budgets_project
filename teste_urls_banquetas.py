#!/usr/bin/env python
import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema_produtos.settings')
sys.path.append('/home/matas/projetos/Project')
django.setup()

from django.test import Client
from django.contrib.auth import get_user_model
from produtos.models import Banqueta

def teste_urls_banquetas():
    print("=== TESTE DAS URLs DE BANQUETAS ===")
    
    # Criar cliente de teste
    client = Client()
    
    # Usar o modelo de usuário customizado
    User = get_user_model()
    
    # Criar usuário de teste se não existir
    try:
        user = User.objects.get(email='admin@test.com')
        print("✅ Usuário admin encontrado")
    except User.DoesNotExist:
        user = User.objects.create_superuser('admin@test.com', 'admin123', first_name='Admin', last_name='Test')
        print("✅ Usuário admin criado")
    
    # Fazer login
    client.login(email='admin@test.com', password='admin123')
    print("✅ Login realizado")
    
    # Testar URLs
    urls_teste = [
        ('/banquetas/', 'Lista de banquetas'),
        ('/banquetas/cadastro/', 'Cadastro de banqueta'),
    ]
    
    for url, descricao in urls_teste:
        try:
            response = client.get(url)
            if response.status_code == 200:
                print(f"✅ {descricao}: {url} - Status {response.status_code}")
            else:
                print(f"❌ {descricao}: {url} - Status {response.status_code}")
                print(f"   Erro: {response.content.decode()[:200]}...")
        except Exception as e:
            print(f"❌ Erro ao testar {url}: {e}")
    
    # Testar detalhes de banqueta específica
    banqueta = Banqueta.objects.first()
    if banqueta:
        url_detalhes = f'/banquetas/{banqueta.id}/'
        try:
            response = client.get(url_detalhes)
            if response.status_code == 200:
                print(f"✅ Detalhes de banqueta: {url_detalhes} - Status {response.status_code}")
            else:
                print(f"❌ Detalhes de banqueta: {url_detalhes} - Status {response.status_code}")
        except Exception as e:
            print(f"❌ Erro ao testar detalhes: {e}")

if __name__ == '__main__':
    teste_urls_banquetas()
