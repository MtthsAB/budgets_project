#!/usr/bin/env python
"""
Script de teste para verificar o funcionamento das URLs de edição de produtos
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

def testar_urls():
    """Testa se todas as URLs estão funcionando corretamente"""
    print("🔍 TESTANDO URLS DE EDIÇÃO DE PRODUTOS")
    print("=" * 50)
    
    # Testar sofás
    print("\n📋 SOFÁS:")
    sofas = Item.objects.filter(id_tipo_produto__nome__icontains='sofá')[:3]
    for sofa in sofas:
        try:
            url_detalhes = reverse('sofa_detalhes', args=[sofa.id])
            url_editar = reverse('sofa_editar', args=[sofa.id])
            print(f"✅ {sofa.ref_produto} - Detalhes: {url_detalhes}, Editar: {url_editar}")
        except NoReverseMatch as e:
            print(f"❌ {sofa.ref_produto} - ERRO: {e}")
    
    # Testar acessórios
    print("\n📋 ACESSÓRIOS:")
    acessorios = Item.objects.filter(id_tipo_produto__nome__icontains='acessório')[:3]
    for acessorio in acessorios:
        try:
            url_detalhes = reverse('acessorio_detalhes', args=[acessorio.id])
            url_editar = reverse('acessorio_editar', args=[acessorio.id])
            print(f"✅ {acessorio.ref_produto} - Detalhes: {url_detalhes}, Editar: {url_editar}")
        except NoReverseMatch as e:
            print(f"❌ {acessorio.ref_produto} - ERRO: {e}")
    
    # Testar banquetas
    print("\n📋 BANQUETAS:")
    banquetas = Banqueta.objects.all()[:3]
    for banqueta in banquetas:
        try:
            url_detalhes = reverse('banqueta_detalhes', args=[banqueta.id])
            url_editar = reverse('banqueta_editar', args=[banqueta.id])
            print(f"✅ {banqueta.ref_banqueta} - Detalhes: {url_detalhes}, Editar: {url_editar}")
        except NoReverseMatch as e:
            print(f"❌ {banqueta.ref_banqueta} - ERRO: {e}")
    
    # Testar cadeiras
    print("\n📋 CADEIRAS:")
    cadeiras = Cadeira.objects.all()[:3]
    for cadeira in cadeiras:
        try:
            url_detalhes = reverse('cadeira_detalhes', args=[cadeira.id])
            url_editar = reverse('cadeira_editar', args=[cadeira.id])
            print(f"✅ {cadeira.ref_cadeira} - Detalhes: {url_detalhes}, Editar: {url_editar}")
        except NoReverseMatch as e:
            print(f"❌ {cadeira.ref_cadeira} - ERRO: {e}")
    
    # Testar poltronas
    print("\n📋 POLTRONAS:")
    poltronas = Poltrona.objects.all()[:3]
    for poltrona in poltronas:
        try:
            url_detalhes = reverse('poltrona_detalhes', args=[poltrona.id])
            url_editar = reverse('poltrona_editar', args=[poltrona.id])
            print(f"✅ {poltrona.ref_poltrona} - Detalhes: {url_detalhes}, Editar: {url_editar}")
        except NoReverseMatch as e:
            print(f"❌ {poltrona.ref_poltrona} - ERRO: {e}")
    
    # Testar pufes
    print("\n📋 PUFES:")
    pufes = Pufe.objects.all()[:3]
    for pufe in pufes:
        try:
            url_detalhes = reverse('pufe_detalhes', args=[pufe.id])
            url_editar = reverse('pufe_editar', args=[pufe.id])
            print(f"✅ {pufe.ref_pufe} - Detalhes: {url_detalhes}, Editar: {url_editar}")
        except NoReverseMatch as e:
            print(f"❌ {pufe.ref_pufe} - ERRO: {e}")
    
    # Testar almofadas
    print("\n📋 ALMOFADAS:")
    almofadas = Almofada.objects.all()[:3]
    for almofada in almofadas:
        try:
            url_detalhes = reverse('almofada_detalhes', args=[almofada.id])
            url_editar = reverse('almofada_editar', args=[almofada.id])
            print(f"✅ {almofada.ref_almofada} - Detalhes: {url_detalhes}, Editar: {url_editar}")
        except NoReverseMatch as e:
            print(f"❌ {almofada.ref_almofada} - ERRO: {e}")

def resumo_produtos():
    """Mostra um resumo dos produtos cadastrados"""
    print("\n📊 RESUMO DOS PRODUTOS")
    print("=" * 50)
    
    sofas_count = Item.objects.filter(id_tipo_produto__nome__icontains='sofá').count()
    acessorios_count = Item.objects.filter(id_tipo_produto__nome__icontains='acessório').count()
    banquetas_count = Banqueta.objects.count()
    cadeiras_count = Cadeira.objects.count()
    poltronas_count = Poltrona.objects.count()
    pufes_count = Pufe.objects.count()
    almofadas_count = Almofada.objects.count()
    
    print(f"🛋️  Sofás: {sofas_count}")
    print(f"🔧 Acessórios: {acessorios_count}")
    print(f"💺 Banquetas: {banquetas_count}")
    print(f"🪑 Cadeiras: {cadeiras_count}")
    print(f"🛋️  Poltronas: {poltronas_count}")
    print(f"🟠 Pufes: {pufes_count}")
    print(f"🟣 Almofadas: {almofadas_count}")
    print(f"📦 Total: {sofas_count + acessorios_count + banquetas_count + cadeiras_count + poltronas_count + pufes_count + almofadas_count}")

if __name__ == '__main__':
    resumo_produtos()
    testar_urls()
    print("\n✅ TESTE CONCLUÍDO!")
