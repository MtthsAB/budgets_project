#!/usr/bin/env python
"""
Script para verificar se a hidratação está funcionando corretamente
fazendo uma requisição real e analisando o HTML retornado.
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
    print("🔍 Testando hidratação da tela de edição...")
    
    try:
        # Configurar cliente de teste
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
        print("✅ Login realizado com sucesso")
        
        # Agora acessar a página de edição
        url = '/sofas/6/editar-formsets/'
        response = client.get(url)
        
        print(f"📊 Status da página: {response.status_code}")
        
        if response.status_code != 200:
            print(f"❌ Erro ao acessar página: {response.status_code}")
            return
        
        # Analisar o HTML
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Verificar dados básicos do sofá
        ref_produto = soup.find('input', {'name': 'ref_produto'})
        nome_produto = soup.find('input', {'name': 'nome_produto'})
        
        print("\n📋 Dados Básicos Hidratados:")
        if ref_produto and ref_produto.get('value'):
            print(f"   ✅ Ref. Produto: {ref_produto.get('value')}")
        else:
            print("   ❌ Ref. Produto não encontrada")
            
        if nome_produto and nome_produto.get('value'):
            print(f"   ✅ Nome Produto: {nome_produto.get('value')}")
        else:
            print("   ❌ Nome Produto não encontrado")
        
        # Verificar módulos
        modulo_forms = soup.find_all('div', class_='modulo-formset-item')
        print(f"\n📦 Módulos Encontrados: {len(modulo_forms)}")
        
        for i, modulo_form in enumerate(modulo_forms):
            modulo_nome = modulo_form.find('input', {'name': f'modulos-{i}-nome'})
            modulo_id = modulo_form.find('input', {'name': f'modulos-{i}-id'})
            
            if modulo_nome and modulo_nome.get('value'):
                print(f"   📦 Módulo {i+1}: {modulo_nome.get('value')}")
                if modulo_id and modulo_id.get('value'):
                    print(f"      ID: {modulo_id.get('value')} (existente)")
                else:
                    print(f"      ID: vazio (novo)")
            else:
                print(f"   ❌ Módulo {i+1}: dados não encontrados")
        
        # Verificar tamanhos
        tamanho_forms = soup.find_all('div', class_='tamanho-formset-item')
        print(f"\n📏 Tamanhos Encontrados: {len(tamanho_forms)}")
        
        for i, tamanho_form in enumerate(tamanho_forms):
            largura_input = tamanho_form.find('input', attrs={'name': lambda x: x and 'largura_total' in x})
            preco_input = tamanho_form.find('input', attrs={'name': lambda x: x and 'preco' in x})
            
            if largura_input and largura_input.get('value'):
                largura = largura_input.get('value')
                preco = preco_input.get('value') if preco_input else 'N/A'
                print(f"   📏 Tamanho {i+1}: {largura}cm - R$ {preco}")
            else:
                print(f"   ❌ Tamanho {i+1}: dados não encontrados")
        
        # Verificar management forms
        modulo_total = soup.find('input', {'name': 'modulos-TOTAL_FORMS'})
        modulo_initial = soup.find('input', {'name': 'modulos-INITIAL_FORMS'})
        
        print(f"\n📊 Management Forms:")
        if modulo_total:
            print(f"   📦 Módulos TOTAL_FORMS: {modulo_total.get('value')}")
        if modulo_initial:
            print(f"   📦 Módulos INITIAL_FORMS: {modulo_initial.get('value')}")
        
        # Verificar se módulos estão expandidos
        modulos_expandidos = soup.find_all('div', class_='modulo-formset-content', style=lambda x: x and 'display: block' in x)
        print(f"   👁️ Módulos expandidos por padrão: {len(modulos_expandidos)}")
        
        # Verificar JavaScript
        scripts = soup.find_all('script')
        has_formset_js = any('toggleModuloFormset' in script.get_text() for script in scripts if script.string)
        print(f"   🟢 JavaScript de formsets carregado: {'✅' if has_formset_js else '❌'}")
        
        print("\n🎯 Resumo da Hidratação:")
        print(f"   📋 Dados básicos: {'✅' if ref_produto and nome_produto else '❌'}")
        print(f"   📦 Módulos: {'✅' if len(modulo_forms) > 0 else '❌'}")
        print(f"   📏 Tamanhos: {'✅' if len(tamanho_forms) > 0 else '❌'}")
        print(f"   🔧 Controles: {'✅' if has_formset_js else '❌'}")
        
        if len(modulo_forms) > 0 and len(tamanho_forms) > 0:
            print("\n✅ HIDRATAÇÃO COMPLETA E FUNCIONAL!")
        else:
            print("\n⚠️ Hidratação parcial - alguns dados podem estar faltando")
        
    except Exception as e:
        print(f"❌ Erro durante o teste: {e}")
        import traceback
        traceback.print_exc()


if __name__ == '__main__':
    main()
