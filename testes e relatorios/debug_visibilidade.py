#!/usr/bin/env python
"""
Script para verificar se os elementos estão visíveis ou ocultos por CSS.
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
    print("👁️ Verificando visibilidade dos elementos...")
    
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
        
        print("👁️ Verificando visibilidade dos containers...")
        
        # Verificar containers dos módulos
        modulo_containers = soup.find_all('div', class_='modulo-formset-content')
        print(f"\n📦 Containers de módulos encontrados: {len(modulo_containers)}")
        
        for i, container in enumerate(modulo_containers):
            style = container.get('style', '')
            print(f"   Módulo {i}: style='{style}'")
            
            if 'display: none' in style:
                print(f"      ⚠️ MÓDULO {i} ESTÁ OCULTO!")
            elif 'display: block' in style:
                print(f"      ✅ Módulo {i} está visível")
            else:
                print(f"      ❓ Módulo {i} sem estilo de display definido")
        
        # Verificar containers dos tamanhos
        tamanho_containers = soup.find_all('div', class_='tamanho-formset-content')
        print(f"\n📏 Containers de tamanhos encontrados: {len(tamanho_containers)}")
        
        for i, container in enumerate(tamanho_containers):
            style = container.get('style', '')
            print(f"   Tamanho {i}: style='{style}'")
            
            if 'display: none' in style:
                print(f"      ⚠️ TAMANHO {i} ESTÁ OCULTO!")
            elif 'display: block' in style:
                print(f"      ✅ Tamanho {i} está visível")
            else:
                print(f"      ❓ Tamanho {i} sem estilo de display definido")
        
        # Verificar se há ícones de expansão/colapso
        chevron_icons = soup.find_all('i', class_='toggle-icon')
        print(f"\n🔽 Ícones de toggle encontrados: {len(chevron_icons)}")
        
        for i, icon in enumerate(chevron_icons):
            classes = icon.get('class', [])
            if 'bi-chevron-up' in classes:
                print(f"   Ícone {i}: ⬆️ Expandido (chevron-up)")
            elif 'bi-chevron-down' in classes:
                print(f"   Ícone {i}: ⬇️ Colapsado (chevron-down)")
            else:
                print(f"   Ícone {i}: ❓ Estado indefinido")
        
        # Resumo
        print(f"\n📊 Resumo da Visibilidade:")
        visivel_modulos = sum(1 for c in modulo_containers if 'display: block' in c.get('style', ''))
        oculto_modulos = sum(1 for c in modulo_containers if 'display: none' in c.get('style', ''))
        
        visivel_tamanhos = sum(1 for c in tamanho_containers if 'display: block' in c.get('style', ''))
        oculto_tamanhos = sum(1 for c in tamanho_containers if 'display: none' in c.get('style', ''))
        
        print(f"   📦 Módulos visíveis: {visivel_modulos}/{len(modulo_containers)}")
        print(f"   📦 Módulos ocultos: {oculto_modulos}/{len(modulo_containers)}")
        print(f"   📏 Tamanhos visíveis: {visivel_tamanhos}/{len(tamanho_containers)}")
        print(f"   📏 Tamanhos ocultos: {oculto_tamanhos}/{len(tamanho_containers)}")
        
        if oculto_modulos > 0 or oculto_tamanhos > 0:
            print(f"\n⚠️ PROBLEMA ENCONTRADO: Alguns elementos estão ocultos!")
            print(f"   💡 Solução: Clicar nos ícones de expansão (⬇️) para ver os campos")
        else:
            print(f"\n✅ Todos os elementos estão visíveis!")
        
    except Exception as e:
        print(f"❌ Erro: {e}")
        import traceback
        traceback.print_exc()


if __name__ == '__main__':
    main()
