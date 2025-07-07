#!/usr/bin/env python
"""
Script de teste para verificar os templates de edição de produtos
"""

import os
import sys
import django

# Configurar Django
sys.path.append('/home/matas/projetos/Project')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema_produtos.settings')
django.setup()

from produtos.models import Item, Banqueta, Cadeira, Poltrona, Pufe, Almofada
from django.urls import reverse, NoReverseMatch
from django.template.loader import get_template
from django.template import TemplateDoesNotExist

def testar_templates_edicao():
    """Testa se todos os templates de edição existem e estão corretos"""
    print("🔍 TESTANDO TEMPLATES DE EDIÇÃO")
    print("=" * 50)
    
    templates_para_testar = [
        ('produtos/banquetas/editar.html', 'Banquetas'),
        ('produtos/cadeiras/editar.html', 'Cadeiras'),
        ('produtos/poltronas/editar.html', 'Poltronas'),
        ('produtos/pufes/editar.html', 'Pufes'),
        ('produtos/almofadas/editar.html', 'Almofadas'),
        ('produtos/acessorios/editar.html', 'Acessórios'),
        ('produtos/sofas/editar.html', 'Sofás'),
        ('produtos/includes/editar_base.html', 'Template Base'),
    ]
    
    for template_path, tipo_nome in templates_para_testar:
        try:
            template = get_template(template_path)
            print(f"✅ {tipo_nome}: {template_path}")
        except TemplateDoesNotExist:
            print(f"❌ {tipo_nome}: {template_path} - TEMPLATE NÃO ENCONTRADO")
    
    print("\n📋 RESUMO DOS PRODUTOS E SUAS URLS DE EDIÇÃO:")
    print("-" * 50)
    
    # Testar banquetas
    banquetas = Banqueta.objects.all()[:2]
    for banqueta in banquetas:
        try:
            url = reverse('banqueta_editar', args=[banqueta.id])
            print(f"🔧 Banqueta {banqueta.ref_banqueta}: {url}")
        except Exception as e:
            print(f"❌ Banqueta {banqueta.ref_banqueta}: ERRO - {e}")
    
    # Testar cadeiras
    cadeiras = Cadeira.objects.all()[:2]
    for cadeira in cadeiras:
        try:
            url = reverse('cadeira_editar', args=[cadeira.id])
            print(f"🔧 Cadeira {cadeira.ref_cadeira}: {url}")
        except Exception as e:
            print(f"❌ Cadeira {cadeira.ref_cadeira}: ERRO - {e}")
    
    # Testar poltronas
    poltronas = Poltrona.objects.all()[:2]
    for poltrona in poltronas:
        try:
            url = reverse('poltrona_editar', args=[poltrona.id])
            print(f"🔧 Poltrona {poltrona.ref_poltrona}: {url}")
        except Exception as e:
            print(f"❌ Poltrona {poltrona.ref_poltrona}: ERRO - {e}")
    
    # Testar sofás
    sofas = Item.objects.filter(id_tipo_produto__nome__icontains='sofá')[:2]
    for sofa in sofas:
        try:
            url = reverse('sofa_editar', args=[sofa.id])
            print(f"🔧 Sofá {sofa.ref_produto}: {url}")
        except Exception as e:
            print(f"❌ Sofá {sofa.ref_produto}: ERRO - {e}")

def verificar_estrutura_templates():
    """Verifica se a estrutura de templates está correta"""
    print("\n🏗️ VERIFICANDO ESTRUTURA DE TEMPLATES")
    print("=" * 50)
    
    import os
    
    base_path = '/home/matas/projetos/Project/templates/produtos'
    
    diretorios_esperados = [
        'banquetas',
        'cadeiras', 
        'poltronas',
        'pufes',
        'almofadas',
        'acessorios',
        'sofas',
        'includes'
    ]
    
    for diretorio in diretorios_esperados:
        dir_path = os.path.join(base_path, diretorio)
        if os.path.exists(dir_path):
            print(f"✅ Diretório {diretorio}/ existe")
            
            # Verificar se tem template de edição
            editar_path = os.path.join(dir_path, 'editar.html')
            if os.path.exists(editar_path):
                print(f"   ✅ Template de edição: {diretorio}/editar.html")
            else:
                print(f"   ❌ Template de edição: {diretorio}/editar.html NÃO ENCONTRADO")
        else:
            print(f"❌ Diretório {diretorio}/ NÃO EXISTE")

if __name__ == '__main__':
    testar_templates_edicao()
    verificar_estrutura_templates()
    print("\n✅ TESTE DE TEMPLATES CONCLUÍDO!")
