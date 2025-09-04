#!/usr/bin/env python
"""
Teste de POST na view de edição com formsets para verificar validação.
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
from authentication.models import CustomUser, TipoPermissao


def main():
    print("🧪 Teste de POST: Edição de sofás com formsets")
    
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
        
        # 3. Criar cliente de teste
        client = Client()
        
        # 4. Criar usuário admin
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
        
        if created:
            user.set_password('admin123')
            user.save()
        else:
            # Atualizar usuário existente
            user.tipo_permissao = TipoPermissao.ADMIN
            user.is_staff = True
            user.is_superuser = True
            user.save()
        
        # 5. Fazer login real
        login_success = client.login(email='admin@test.com', password='admin123')
        print(f"🔑 Login realizado: {login_success}")
        
        # Verificar permissões do usuário
        if login_success:
            print(f"👤 Usuário: {user.email}")
            print(f"🔐 Tipo permissão: {user.tipo_permissao}")
            print(f"📦 Pode acessar produtos: {user.can_access_produtos()}")
            print(f"🏠 Pode acessar home: {user.can_access_home()}")
            print(f"👨‍💼 É staff: {user.is_staff}")
            print(f"🔱 É superuser: {user.is_superuser}")
        
        # 6. Primeiro, fazer GET para obter os dados dos formsets
        url = f'/sofas/{sofa.id}/editar-formsets/'
        print(f"🔗 Fazendo GET em: {url}")
        
        get_response = client.get(url)
        print(f"📊 Status GET: {get_response.status_code}")
        
        if get_response.status_code == 302:
            print(f"🔀 Redirecionamento para: {get_response.url}")
            return
        
        if get_response.status_code != 200:
            print(f"❌ Erro no GET: {get_response.content[:500]}")
            return
        
        # Verificar se o template foi renderizado
        if not hasattr(get_response, 'context') or get_response.context is None:
            print("❌ Sem contexto na resposta - possível erro de template")
            print(f"Content: {get_response.content[:1000]}")
            return
        
        # 7. Extrair dados dos formsets do contexto
        context = get_response.context
        sofa_form = context['sofa_form']
        modulo_formset = context['modulo_formset']
        
        print(f"📋 Dados obtidos:")
        print(f"   SofaForm: {len(sofa_form.fields)} campos")
        print(f"   ModuloFormset: {len(modulo_formset.forms)} forms")
        
        # 8. Montar dados de POST válidos
        post_data = {}
        
        # Dados do sofá (manter os valores atuais)
        for field_name, field in sofa_form.fields.items():
            if hasattr(sofa, field_name):
                value = getattr(sofa, field_name)
                if value is not None:
                    if field_name == 'id_tipo_produto':
                        post_data[field_name] = value.id
                    elif isinstance(value, bool):
                        post_data[field_name] = value
                    else:
                        post_data[field_name] = str(value)
        
        # Management form do módulo formset
        mgmt = modulo_formset.management_form
        for field in mgmt:
            post_data[field.html_name] = field.value() or 0
        
        # Dados dos módulos existentes
        for i, form in enumerate(modulo_formset.forms):
            prefix = f'modulos-{i}'
            
            # Dados do módulo
            if form.instance and form.instance.pk:
                modulo = form.instance
                post_data[f'{prefix}-id'] = modulo.id
                post_data[f'{prefix}-nome'] = modulo.nome
                post_data[f'{prefix}-profundidade'] = str(modulo.profundidade)
                post_data[f'{prefix}-altura'] = str(modulo.altura)
                post_data[f'{prefix}-braco'] = str(modulo.braco or 0)
                post_data[f'{prefix}-descricao'] = modulo.descricao or ''
                post_data[f'{prefix}-DELETE'] = ''  # Não deletar
                post_data[f'{prefix}-produto'] = sofa.id
        
        print(f"📝 Dados de POST preparados: {len(post_data)} campos")
        for key, value in list(post_data.items())[:10]:  # Mostrar apenas os primeiros 10
            print(f"   {key}: {value}")
        
        # 9. Fazer POST
        print(f"📤 Fazendo POST em: {url}")
        post_response = client.post(url, data=post_data)
        print(f"📊 Status POST: {post_response.status_code}")
        
        if post_response.status_code == 302:
            print(f"✅ Redirecionamento para: {post_response.url}")
        elif post_response.status_code == 200:
            print("📋 Formulário retornado com possíveis erros")
            # Verificar se há erros no contexto
            if 'sofa_form' in post_response.context:
                sofa_form = post_response.context['sofa_form']
                if sofa_form.errors:
                    print(f"❌ Erros no SofaForm: {sofa_form.errors}")
                
            if 'modulo_formset' in post_response.context:
                modulo_formset = post_response.context['modulo_formset']
                if modulo_formset.errors:
                    print(f"❌ Erros no ModuloFormset: {modulo_formset.errors}")
                if modulo_formset.non_form_errors():
                    print(f"❌ Erros não-form: {modulo_formset.non_form_errors()}")
        else:
            print(f"❌ Erro POST: {post_response.content[:500]}")
        
    except Exception as e:
        print(f"❌ Erro durante o teste: {e}")
        import traceback
        traceback.print_exc()


if __name__ == '__main__':
    main()
