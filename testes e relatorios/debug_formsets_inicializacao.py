#!/usr/bin/env python
"""
Script para debugar os formsets e verificar se estão sendo inicializados corretamente.
"""

import os
import sys
import django
from django.conf import settings

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema_produtos.settings')
sys.path.append('/home/matas/projetos/Project')
django.setup()

from produtos.models import Produto
from produtos.forms import SofaForm, ModuloFormSet, TamanhoFormSet


def main():
    print("🔧 Debugando formsets e inicialização...")
    
    try:
        # 1. Buscar o sofá
        sofa = Produto.objects.filter(id_tipo_produto__nome__icontains='sofá').first()
        print(f"🛋️ Sofá: {sofa.ref_produto} - {sofa.nome_produto}")
        
        # 2. Verificar dados dos módulos no banco
        print("\n📦 Módulos no banco:")
        modulos = sofa.modulos.all()
        for i, modulo in enumerate(modulos):
            print(f"   Módulo {i}: {modulo.nome}")
            print(f"      ID: {modulo.id}")
            print(f"      Profundidade: {modulo.profundidade}")
            print(f"      Altura: {modulo.altura}")
            print(f"      Braço: {modulo.braco}")
            print(f"      Descrição: {modulo.descricao}")
        
        # 3. Criar SofaForm
        sofa_form = SofaForm(instance=sofa)
        print(f"\n📋 SofaForm criado: {len(sofa_form.fields)} campos")
        
        # 4. Criar ModuloFormSet
        modulo_formset = ModuloFormSet(instance=sofa)
        print(f"\n📦 ModuloFormSet:")
        print(f"   Total forms: {len(modulo_formset.forms)}")
        print(f"   Initial forms: {modulo_formset.initial_form_count()}")
        
        # 5. Verificar cada form do módulo
        for i, form in enumerate(modulo_formset.forms):
            print(f"\n   Form {i}:")
            print(f"      Instance: {form.instance}")
            print(f"      Instance ID: {form.instance.id if form.instance else 'None'}")
            
            if form.instance and form.instance.pk:
                print(f"      Dados da instance:")
                print(f"         Nome: {form.instance.nome}")
                print(f"         Profundidade: {form.instance.profundidade}")
                print(f"         Altura: {form.instance.altura}")
                print(f"         Braço: {form.instance.braco}")
                
                # Verificar valores nos campos do form
                print(f"      Valores nos campos do form:")
                print(f"         Nome field: {form['nome'].value()}")
                print(f"         Profundidade field: {form['profundidade'].value()}")
                print(f"         Altura field: {form['altura'].value()}")
                print(f"         Braço field: {form['braco'].value()}")
                print(f"         Descrição field: {form['descricao'].value()}")
            else:
                print(f"      Form sem instance (novo)")
        
        # 6. Testar criação de TamanhoFormSet para um módulo específico
        primeiro_modulo = modulos.first()
        print(f"\n📏 Testando TamanhoFormSet para: {primeiro_modulo.nome}")
        
        tamanho_formset = TamanhoFormSet(instance=primeiro_modulo, prefix='modulo-0-tamanho')
        print(f"   Total forms: {len(tamanho_formset.forms)}")
        print(f"   Initial forms: {tamanho_formset.initial_form_count()}")
        
        # Verificar cada form de tamanho
        for i, form in enumerate(tamanho_formset.forms):
            print(f"\n   Tamanho Form {i}:")
            print(f"      Instance: {form.instance}")
            if form.instance and form.instance.pk:
                print(f"      Dados da instance:")
                print(f"         Largura Total: {form.instance.largura_total}")
                print(f"         Largura Assento: {form.instance.largura_assento}")
                print(f"         Tecido: {form.instance.tecido_metros}")
                print(f"         Volume: {form.instance.volume_m3}")
                print(f"         Peso: {form.instance.peso_kg}")
                print(f"         Preço: {form.instance.preco}")
                print(f"         Descrição: {form.instance.descricao}")
                
                # Verificar valores nos campos do form
                print(f"      Valores nos campos do form:")
                print(f"         Largura Total field: {form['largura_total'].value()}")
                print(f"         Largura Assento field: {form['largura_assento'].value()}")
                print(f"         Tecido field: {form['tecido_metros'].value()}")
                print(f"         Volume field: {form['volume_m3'].value()}")
                print(f"         Peso field: {form['peso_kg'].value()}")
                print(f"         Preço field: {form['preco'].value()}")
                print(f"         Descrição field: {form['descricao'].value()}")
        
    except Exception as e:
        print(f"❌ Erro: {e}")
        import traceback
        traceback.print_exc()


if __name__ == '__main__':
    main()
