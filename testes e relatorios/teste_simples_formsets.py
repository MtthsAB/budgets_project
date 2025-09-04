#!/usr/bin/env python
"""
Teste simples para verificar apenas a criação e estrutura dos formsets
sem simulação de POST data complexa.
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
    print("🧪 Teste simples: Criação de formsets para edição")
    
    try:
        # 1. Buscar um sofá existente
        sofa = Produto.objects.filter(id_tipo_produto__nome__icontains='sofá').first()
        
        if not sofa:
            print("❌ Nenhum sofá encontrado no banco")
            return
        
        print(f"🛋️ Sofá: {sofa.ref_produto} - {sofa.nome_produto}")
        
        # 2. Verificar módulos existentes
        modulos = sofa.modulos.all()
        print(f"📦 Módulos existentes: {modulos.count()}")
        for modulo in modulos:
            tamanhos = modulo.tamanhos_detalhados.all()
            print(f"   - {modulo.nome} (ID: {modulo.id}) - {tamanhos.count()} tamanhos")
        
        # 3. Criar SofaForm
        sofa_form = SofaForm(instance=sofa)
        print(f"✅ SofaForm criado com {len(sofa_form.fields)} campos")
        
        # 4. Criar ModuloFormSet
        modulo_formset = ModuloFormSet(instance=sofa)
        print(f"✅ ModuloFormSet criado")
        print(f"   📊 Total forms: {len(modulo_formset.forms)}")
        print(f"   📊 Initial forms: {modulo_formset.initial_form_count()}")
        print(f"   📊 Extra forms: {modulo_formset.extra}")
        print(f"   📊 Can delete: {modulo_formset.can_delete}")
        
        # 5. Verificar Management Form
        management_form = modulo_formset.management_form
        print(f"📋 Management Form válido: {management_form.is_valid()}")
        if management_form.is_valid():
            print(f"   📊 TOTAL_FORMS: {management_form.cleaned_data['TOTAL_FORMS']}")
            print(f"   📊 INITIAL_FORMS: {management_form.cleaned_data['INITIAL_FORMS']}")
            print(f"   📊 MIN_NUM_FORMS: {management_form.cleaned_data['MIN_NUM_FORMS']}")
            print(f"   📊 MAX_NUM_FORMS: {management_form.cleaned_data['MAX_NUM_FORMS']}")
        
        # 6. Verificar cada form de módulo
        print("🔍 Análise dos forms de módulos:")
        for i, form in enumerate(modulo_formset.forms):
            if form.instance and form.instance.pk:
                print(f"   Form {i}: {form.instance.nome} (Existente)")
            else:
                print(f"   Form {i}: Novo módulo")
            
            print(f"      Campos: {list(form.fields.keys())}")
            
        # 7. Criar TamanhoFormSets para módulos existentes
        print("📏 Criando TamanhoFormSets:")
        for modulo in modulos:
            tamanho_formset = TamanhoFormSet(instance=modulo)
            print(f"   ✅ TamanhoFormSet para '{modulo.nome}':")
            print(f"      📊 Total forms: {len(tamanho_formset.forms)}")
            print(f"      📊 Initial forms: {tamanho_formset.initial_form_count()}")
            
            # Verificar Management Form do tamanho
            tmgmt = tamanho_formset.management_form
            if tmgmt.is_valid():
                print(f"      📊 TOTAL_FORMS: {tmgmt.cleaned_data['TOTAL_FORMS']}")
        
        print("✅ Todos os formsets foram criados com sucesso!")
        
    except Exception as e:
        print(f"❌ Erro durante o teste: {e}")
        import traceback
        traceback.print_exc()


if __name__ == '__main__':
    main()
