#!/usr/bin/env python
"""
Teste do novo layout de imagens para banquetas.
Verifica se a seção de imagens está seguindo o padrão dos acessórios.
"""

import os
import sys
import django

# Configurar Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema_produtos.settings')
django.setup()

from django.test import Client
from django.contrib.auth import get_user_model
from produtos.models import Banqueta

def teste_template_banquetas():
    """Testa se o template de banquetas foi atualizado corretamente"""
    
    print("🔍 TESTANDO LAYOUT DE IMAGENS - BANQUETAS")
    print("=" * 50)
    
    # Verificar se existem banquetas cadastradas
    banquetas = Banqueta.objects.all()
    print(f"📊 Banquetas encontradas: {banquetas.count()}")
    
    if banquetas.count() == 0:
        print("❌ Nenhuma banqueta encontrada para teste")
        return
    
    # Pegar a primeira banqueta para teste
    banqueta = banquetas.first()
    print(f"🪑 Testando com: {banqueta.ref_banqueta} - {banqueta.nome}")
    
    # Verificar se o template foi modificado
    template_path = 'templates/produtos/banquetas/cadastro.html'
    if os.path.exists(template_path):
        with open(template_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        print("\n🎨 VERIFICAÇÕES DO TEMPLATE:")
        
        # Verificar título da seção
        if "Imagens do Produto" in content:
            print("✅ Título 'Imagens do Produto' encontrado")
        else:
            print("❌ Título 'Imagens do Produto' NÃO encontrado")
        
        # Verificar informações de formato
        if "JPG, PNG, GIF (máx. 5MB)" in content:
            print("✅ Informações de formato encontradas")
        else:
            print("❌ Informações de formato NÃO encontradas")
        
        # Verificar estrutura de campos
        if 'class="form-text"' in content:
            print("✅ Estrutura de ajuda dos campos encontrada")
        else:
            print("❌ Estrutura de ajuda dos campos NÃO encontrada")
        
        # Verificar ordem dos elementos
        if 'small class="text-muted">Imagem atual:</small>' in content:
            print("✅ Texto 'Imagem atual' formatado corretamente")
        else:
            print("❌ Texto 'Imagem atual' com formatação incorreta")
            
    else:
        print(f"❌ Template não encontrado: {template_path}")
    
    print("\n🔗 TESTANDO ACESSO VIA HTTP:")
    
    # Criar cliente de teste
    client = Client()
    
    # Tentar acessar página de edição
    try:
        # Como precisa de autenticação, vamos criar um usuário temporário
        User = get_user_model()
        
        # Tentar encontrar um usuário existente ou criar um temporário
        try:
            user = User.objects.get(username='admin')
        except User.DoesNotExist:
            user = User.objects.create_user(
                username='teste',
                password='teste123',
                is_staff=True,
                is_superuser=True
            )
        
        # Fazer login
        logged_in = client.login(username=user.username, password='teste123' if user.username == 'teste' else 'admin')
        
        if logged_in:
            print("✅ Login realizado com sucesso")
            
            # Acessar página de edição da banqueta
            url = f'/produtos/banquetas/{banqueta.id}/editar/'
            response = client.get(url)
            
            if response.status_code == 200:
                print(f"✅ Página de edição acessível: {url}")
                
                # Verificar se o conteúdo contém os elementos esperados
                content = response.content.decode('utf-8')
                
                if "Imagens do Produto" in content:
                    print("✅ Seção 'Imagens do Produto' renderizada")
                else:
                    print("❌ Seção 'Imagens do Produto' NÃO renderizada")
                
                if "JPG, PNG, GIF" in content:
                    print("✅ Informações de formato renderizadas")
                else:
                    print("❌ Informações de formato NÃO renderizadas")
                    
            else:
                print(f"❌ Erro ao acessar página: {response.status_code}")
                
        else:
            print("❌ Falha no login")
            
        # Limpar usuário temporário se foi criado
        if user.username == 'teste':
            user.delete()
            
    except Exception as e:
        print(f"❌ Erro durante teste HTTP: {e}")
    
    print("\n🎉 TESTE CONCLUÍDO!")
    print("\n💡 PRÓXIMOS PASSOS:")
    print("1. Acesse http://localhost:8000/produtos/")
    print("2. Clique em uma banqueta")
    print("3. Clique em 'Editar'")
    print("4. Verifique a seção 'Imagens do Produto'")
    print("5. Teste o upload de uma imagem")

if __name__ == '__main__':
    teste_template_banquetas()
