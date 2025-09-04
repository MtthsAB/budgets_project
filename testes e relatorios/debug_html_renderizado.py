#!/usr/bin/env python
"""
Script para verificar exatamente o HTML renderizado dos campos.
"""

import os
import sys
import django
from django.conf import settings

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema_produtos.settings')
sys.path.append('/home/matas/projetos/Project')
django.setup()

# Adicionar testserver ao ALLOWED_HOSTS
if 'testserver' not in settings.ALLOWED_HOSTS:
    settings.ALLOWED_HOSTS.append('testserver')

from bs4 import BeautifulSoup
from django.test import Client
from authentication.models import CustomUser, TipoPermissao


def main():
    print("🔍 Analisando HTML renderizado dos campos...")
    
    try:
        # Configurar cliente
        client = Client()
        
        # Criar/atualizar usuário admin
        user, created = CustomUser.objects.get_or_create(
            email='admin@test.com',
            defaults={
                'first_name': 'Admin',
                'last_name': 'Test',
                'is_staff': True,
                'is_superuser': True,
                'tipo_permissao': TipoPermissao.ADMIN
            }
        )
        
        if not created:
            user.tipo_permissao = TipoPermissao.ADMIN
            user.is_staff = True
            user.is_superuser = True
            user.save()
        
        # Fazer login
        client.force_login(user)
        
        # Acessar a página
        response = client.get('/sofas/6/editar-formsets/')
        
        if response.status_code != 200:
            print(f"❌ Erro: {response.status_code}")
            return
        
        # Analisar HTML
        soup = BeautifulSoup(response.content, 'html.parser')
        
        print("🔍 Verificando campos dos módulos...")
        
        # Verificar módulos
        for i in range(2):
            print(f"\n📦 Módulo {i}:")
            
            # Nome
            nome_input = soup.find('input', {'name': f'modulos-{i}-nome'})
            if nome_input:
                print(f"   ✅ Nome: value='{nome_input.get('value', 'VAZIO')}' type='{nome_input.get('type')}' class='{nome_input.get('class')}'")
                print(f"      HTML: {str(nome_input)[:100]}...")
            else:
                print(f"   ❌ Nome: CAMPO NÃO ENCONTRADO")
            
            # Profundidade
            prof_input = soup.find('input', {'name': f'modulos-{i}-profundidade'})
            if prof_input:
                print(f"   ✅ Profundidade: value='{prof_input.get('value', 'VAZIO')}' type='{prof_input.get('type')}' class='{prof_input.get('class')}'")
                print(f"      HTML: {str(prof_input)[:100]}...")
            else:
                print(f"   ❌ Profundidade: CAMPO NÃO ENCONTRADO")
                
            # Altura
            altura_input = soup.find('input', {'name': f'modulos-{i}-altura'})
            if altura_input:
                print(f"   ✅ Altura: value='{altura_input.get('value', 'VAZIO')}' type='{altura_input.get('type')}' class='{altura_input.get('class')}'")
                print(f"      HTML: {str(altura_input)[:100]}...")
            else:
                print(f"   ❌ Altura: CAMPO NÃO ENCONTRADO")
                
            # Braço
            braco_input = soup.find('input', {'name': f'modulos-{i}-braco'})
            if braco_input:
                print(f"   ✅ Braço: value='{braco_input.get('value', 'VAZIO')}' type='{braco_input.get('type')}' class='{braco_input.get('class')}'")
                print(f"      HTML: {str(braco_input)[:100]}...")
            else:
                print(f"   ❌ Braço: CAMPO NÃO ENCONTRADO")
        
        print("\n🔍 Verificando campos dos tamanhos...")
        
        # Verificar tamanhos (apenas primeiros 2)
        for i in range(2):
            prefix = f'modulo-0-tamanho-{i}'
            print(f"\n📏 Tamanho {i} (prefix: {prefix}):")
            
            # Largura Total
            largura_input = soup.find('input', {'name': f'{prefix}-largura_total'})
            if largura_input:
                print(f"   ✅ Largura Total: value='{largura_input.get('value', 'VAZIO')}' type='{largura_input.get('type')}' class='{largura_input.get('class')}'")
                print(f"      HTML: {str(largura_input)[:100]}...")
            else:
                print(f"   ❌ Largura Total: CAMPO NÃO ENCONTRADO")
                
            # Largura Assento
            assento_input = soup.find('input', {'name': f'{prefix}-largura_assento'})
            if assento_input:
                print(f"   ✅ Largura Assento: value='{assento_input.get('value', 'VAZIO')}' type='{assento_input.get('type')}' class='{assento_input.get('class')}'")
                print(f"      HTML: {str(assento_input)[:100]}...")
            else:
                print(f"   ❌ Largura Assento: CAMPO NÃO ENCONTRADO")
                
            # Preço
            preco_input = soup.find('input', {'name': f'{prefix}-preco'})
            if preco_input:
                print(f"   ✅ Preço: value='{preco_input.get('value', 'VAZIO')}' type='{preco_input.get('type')}' class='{preco_input.get('class')}'")
                print(f"      HTML: {str(preco_input)[:100]}...")
            else:
                print(f"   ❌ Preço: CAMPO NÃO ENCONTRADO")
        
        # Verificar se há algum erro de JavaScript ou CSS que pode estar escondendo valores
        print(f"\n🔍 Verificando possíveis problemas...")
        
        # Verificar se os valores estão sendo definidos via JavaScript
        scripts = soup.find_all('script')
        for script in scripts:
            if script.string and ('value' in script.string or 'setValue' in script.string):
                print(f"   ⚠️ JavaScript modificando valores encontrado")
                print(f"      Snippet: {script.string[:200]}...")
        
        # Verificar atributos de formulário que podem estar interferindo
        forms = soup.find_all('form')
        for form in forms:
            if form.get('autocomplete'):
                print(f"   ⚠️ Form autocomplete: {form.get('autocomplete')}")
        
    except Exception as e:
        print(f"❌ Erro: {e}")
        import traceback
        traceback.print_exc()


if __name__ == '__main__':
    main()
