#!/usr/bin/env python3
"""
Script para criar usuário de teste e testar login
"""

import os
import django
import sys
import requests

# Configurar Django
sys.path.append('/home/matas/projetos/Project')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema_produtos.settings')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

def create_test_user():
    """Cria um usuário de teste"""
    try:
        user = User.objects.get(email='test@example.com')
        print("✅ Usuário 'test@example.com' já existe")
        return user
    except User.DoesNotExist:
        user = User.objects.create_user(
            email='test@example.com',
            first_name='Test',
            last_name='User',
            password='testpass123'
        )
        print("✅ Usuário 'test@example.com' criado com sucesso")
        return user

def test_with_login():
    """Testa a página com login"""
    # Criar sessão
    session = requests.Session()
    
    # Pegar CSRF token da página de login
    login_page = session.get('http://localhost:8000/auth/login/')
    csrf_token = None
    
    for line in login_page.text.split('\n'):
        if 'csrfmiddlewaretoken' in line and 'value=' in line:
            start = line.find('value="') + 7
            end = line.find('"', start)
            csrf_token = line[start:end]
            break
    
    if not csrf_token:
        print("❌ Não foi possível encontrar o CSRF token")
        return False
    
    # Fazer login
    login_data = {
        'username': 'test@example.com',  # O campo se chama username no form mas usa email
        'password': 'testpass123',
        'csrfmiddlewaretoken': csrf_token
    }
    
    login_response = session.post('http://localhost:8000/auth/login/', data=login_data)
    
    if login_response.status_code == 200 and 'Usuário ou senha incorretos' not in login_response.text:
        print("✅ Login realizado com sucesso")
        
        # Agora testar a página de cadastro
        cadastro_response = session.get('http://localhost:8000/produtos/cadastro/')
        
        if cadastro_response.status_code == 200:
            content = cadastro_response.text
            
            # Verificar elementos essenciais
            checks = {
                'Seção de imagens presente': 'id="secao-imagens"' in content,
                'Include funcionando': 'Imagens do Produto' in content,
                'Função toggleCamposPorTipo': 'function toggleCamposPorTipo()' in content,
                'Select de tipo': 'id="tipo_produto"' in content,
                'Campo imagem principal': 'name="imagem_principal"' in content,
                'JavaScript para exibir seção': 'secaoImagens.style.display = \'block\'' in content,
            }
            
            print("\n=== VERIFICAÇÃO DOS ELEMENTOS (COM LOGIN) ===")
            all_ok = True
            for check_name, result in checks.items():
                status = "✅" if result else "❌"
                print(f"{status} {check_name}: {'OK' if result else 'FALTANDO'}")
                if not result:
                    all_ok = False
            
            return all_ok
        else:
            print(f"❌ Erro ao acessar página de cadastro: {cadastro_response.status_code}")
            return False
    else:
        print("❌ Falha no login")
        return False

if __name__ == '__main__':
    print("🔧 Criando usuário de teste...")
    create_test_user()
    
    print("\n🔍 Testando com login...")
    result = test_with_login()
    
    if result:
        print("\n✅ TESTE PASSOU: Todos os elementos estão presentes!")
    else:
        print("\n❌ TESTE FALHOU: Alguns elementos estão faltando!")
