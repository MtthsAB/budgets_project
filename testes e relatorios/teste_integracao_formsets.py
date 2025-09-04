#!/usr/bin/env python
"""
Teste de integração para verificar se a nova view de edição
de sofás com formsets está funcionando corretamente.
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
from django.conf import settings
if 'testserver' not in settings.ALLOWED_HOSTS:
    settings.ALLOWED_HOSTS.append('testserver')

from django.test import Client
from django.contrib.auth.models import User
from produtos.models import Produto, TipoItem, Modulo
from authentication.models import CustomUser


def main():
    print("🧪 Teste de integração: Edição de sofás com formsets")
    
    try:
        # 1. Buscar um sofá existente
        sofa = Produto.objects.filter(id_tipo_produto__nome__icontains='sofá').first()
        
        if not sofa:
            print("❌ Nenhum sofá encontrado no banco")
            return
        
        print(f"🛋️ Sofá selecionado: {sofa.ref_produto} - {sofa.nome_produto}")
        
        # 2. Verificar módulos existentes
        modulos = sofa.modulos.all()
        print(f"📦 Módulos existentes: {modulos.count()}")
        for modulo in modulos:
            print(f"   - {modulo.nome} (ID: {modulo.id})")
        
        # 3. Criar cliente de teste
        client = Client()
        
        # 4. Buscar ou criar usuário admin
        user, created = CustomUser.objects.get_or_create(
            email='admin@test.com',
            defaults={
                'first_name': 'Admin',
                'last_name': 'Test',
                'is_staff': True,
                'is_superuser': True,
                'tipo_permissao': 'admin'
            }
        )
        
        if created:
            user.set_password('admin123')
            user.save()
        
        # 5. Fazer login
        client.force_login(user)
        
        # 6. Fazer GET na view de edição
        url = f'/produtos/sofas/{sofa.id}/editar-formsets/'
        print(f"🔗 Acessando: {url}")
        
        response = client.get(url)
        print(f"📊 Status da resposta: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ View carregada com sucesso!")
            
            # Verificar se tem formsets no contexto
            if 'modulo_formset' in response.context:
                formset = response.context['modulo_formset']
                print(f"📋 ModuloFormSet encontrado com {len(formset.forms)} forms")
                
                # Verificar management form
                management_form = formset.management_form
                print(f"📊 TOTAL_FORMS: {management_form['TOTAL_FORMS'].value()}")
                print(f"📊 INITIAL_FORMS: {management_form['INITIAL_FORMS'].value()}")
                
            else:
                print("❌ ModuloFormSet não encontrado no contexto")
                
        elif response.status_code == 404:
            print("❌ Página não encontrada - verifique se a URL está configurada")
        elif response.status_code == 403:
            print("❌ Acesso negado - problema de permissão")
        else:
            print(f"❌ Erro: {response.status_code}")
            if hasattr(response, 'content'):
                print(f"Conteúdo: {response.content[:500]}...")
        
    except Exception as e:
        print(f"❌ Erro durante o teste: {e}")
        import traceback
        traceback.print_exc()


if __name__ == '__main__':
    main()
