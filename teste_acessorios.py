#!/usr/bin/env python
"""
Script de teste específico para verificar a edição de acessórios
"""

import os
import sys
import django

# Configurar Django
sys.path.append('/home/matas/projetos/Project')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema_produtos.settings')
django.setup()

from produtos.models import Acessorio, Item
from django.urls import reverse, NoReverseMatch

def testar_acessorios():
    """Testa especificamente os acessórios"""
    print("🔍 TESTANDO EDIÇÃO DE ACESSÓRIOS")
    print("=" * 50)
    
    # Verificar se existem acessórios
    acessorios = Acessorio.objects.all()[:5]
    print(f"📦 Total de acessórios encontrados: {Acessorio.objects.count()}")
    
    if not acessorios:
        print("⚠️  Nenhum acessório encontrado no banco de dados!")
        return
    
    print("\n📋 TESTANDO URLs DE ACESSÓRIOS:")
    for acessorio in acessorios:
        try:
            url_detalhes = reverse('acessorio_detalhes', args=[acessorio.id])
            url_editar = reverse('acessorio_editar', args=[acessorio.id])
            print(f"✅ {acessorio.ref_acessorio} - Detalhes: {url_detalhes}, Editar: {url_editar}")
            
            # Verificar dados do acessório
            print(f"   📝 Nome: {acessorio.nome}")
            print(f"   💰 Preço: R$ {acessorio.preco or 'Não definido'}")
            print(f"   🔗 Produtos vinculados: {acessorio.produtos_vinculados.count()}")
            print(f"   🖼️  Imagem principal: {'Sim' if acessorio.imagem_principal else 'Não'}")
            print(f"   ✅ Ativo: {'Sim' if acessorio.ativo else 'Não'}")
            
        except NoReverseMatch as e:
            print(f"❌ {acessorio.ref_acessorio} - ERRO: {e}")
        except Exception as e:
            print(f"❌ {acessorio.ref_acessorio} - ERRO INESPERADO: {e}")
        
        print("")

def verificar_formulario_acessorio():
    """Verifica se o formulário de acessório está funcionando"""
    print("🔍 TESTANDO FORMULÁRIO DE ACESSÓRIOS")
    print("=" * 50)
    
    try:
        from produtos.forms import AcessorioForm
        
        # Testar formulário vazio
        form = AcessorioForm()
        print("✅ Formulário de acessório criado com sucesso")
        print(f"📝 Campos disponíveis: {list(form.fields.keys())}")
        
        # Verificar se há produtos disponíveis para vinculação
        produtos_disponiveis = form.fields['produtos_vinculados'].queryset.count()
        print(f"🔗 Produtos disponíveis para vinculação: {produtos_disponiveis}")
        
        # Testar com um acessório existente
        if Acessorio.objects.exists():
            acessorio = Acessorio.objects.first()
            form_with_instance = AcessorioForm(instance=acessorio)
            print(f"✅ Formulário carregado com dados do acessório: {acessorio.ref_acessorio}")
        
    except Exception as e:
        print(f"❌ ERRO no formulário: {e}")

if __name__ == '__main__':
    testar_acessorios()
    print("\n")
    verificar_formulario_acessorio()
    print("\n✅ TESTE DE ACESSÓRIOS CONCLUÍDO!")
