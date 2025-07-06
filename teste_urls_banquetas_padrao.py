#!/usr/bin/env python
"""
Script para testar se a implementação da URL padrão para banquetas está funcionando
"""
import os
import sys
import django

# Adicionar o diretório do projeto ao path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema_produtos.settings')
django.setup()

from django.test import Client
from django.contrib.auth import get_user_model
from produtos.models import Banqueta, Item

User = get_user_model()

def teste_url_banquetas():
    """Testa se as banquetas podem ser acessadas via URL padrão /produtos/ID/"""
    
    print("=== TESTANDO URLS PADRÃO PARA BANQUETAS ===\n")
    
    # Verificar se há banquetas no banco
    banquetas = Banqueta.objects.all()[:3]  # Pegar até 3 banquetas para teste
    
    if not banquetas:
        print("❌ Nenhuma banqueta encontrada no banco de dados")
        return
    
    print(f"✅ Encontradas {len(banquetas)} banquetas para teste")
    
    # Criar cliente de teste
    client = Client()
    
    # Tentar fazer login (criar um usuário de teste se necessário)
    try:
        user = User.objects.first()  # Pegar qualquer usuário
        if not user:
            print("❌ Nenhum usuário encontrado no banco")
            return
    except Exception as e:
        print(f"❌ Erro ao buscar usuário: {e}")
        return
    
    # Fazer login
    client.force_login(user)
    
    # Testar cada banqueta
    for banqueta in banquetas:
        print(f"\n--- Testando Banqueta ID: {banqueta.id} ({banqueta.ref_banqueta} - {banqueta.nome}) ---")
        
        # Testar a nova URL padrão
        url_nova = f'/produtos/{banqueta.id}/'
        response = client.get(url_nova)
        
        if response.status_code == 200:
            print(f"✅ URL padrão funcionando: {url_nova}")
            print(f"   Status: {response.status_code}")
            
            # Verificar se o template correto está sendo usado
            template_names = [t.name for t in response.templates]
            if 'produtos/banquetas/detalhes.html' in template_names:
                print(f"✅ Template correto sendo usado: produtos/banquetas/detalhes.html")
            else:
                print(f"⚠️  Template usado: {template_names}")
                
            # Verificar se o contexto tem a banqueta
            if 'banqueta' in response.context:
                print(f"✅ Contexto tem banqueta: {response.context['banqueta'].ref_banqueta}")
            else:
                print(f"❌ Contexto não tem banqueta. Contexto: {list(response.context.keys())}")
                
        else:
            print(f"❌ URL padrão falhou: {url_nova}")
            print(f"   Status: {response.status_code}")
            if response.status_code == 404:
                print("   Erro 404: Banqueta não encontrada")
        
        # Testar se a URL antiga ainda funciona (deve funcionar)
        url_antiga = f'/banquetas/{banqueta.id}/'
        response_antiga = client.get(url_antiga)
        
        if response_antiga.status_code == 200:
            print(f"✅ URL antiga ainda funciona: {url_antiga}")
        else:
            print(f"⚠️  URL antiga não funciona: {url_antiga} (Status: {response_antiga.status_code})")
    
    print("\n=== TESTANDO LISTAGEM DE PRODUTOS ===")
    
    # Testar se a listagem de produtos tem links corretos
    response_lista = client.get('/produtos/')
    if response_lista.status_code == 200:
        print("✅ Listagem de produtos carregando")
        
        # Verificar se tem banquetas no contexto
        if 'banquetas' in response_lista.context:
            banquetas_lista = response_lista.context['banquetas']
            print(f"✅ {len(banquetas_lista)} banquetas na listagem")
        else:
            print("❌ Banquetas não encontradas na listagem")
    else:
        print(f"❌ Listagem de produtos falhou: Status {response_lista.status_code}")
    
    print("\n=== TESTE CONCLUÍDO ===")

if __name__ == '__main__':
    teste_url_banquetas()
