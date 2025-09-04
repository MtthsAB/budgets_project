#!/usr/bin/env python3
"""
Teste da nova edição de sofá com formsets.
"""

import os
import sys
import django

# Configurar Django
sys.path.append('/home/matas/projetos/Project')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema_produtos.settings')
django.setup()

from produtos.models import Produto, Modulo, TamanhosModulosDetalhado
from produtos.forms import SofaForm, ModuloFormSet, TamanhoFormSet

def teste_formsets_sofas():
    """Testar criação e validação de formsets para sofás"""
    
    print("🧪 Testando formsets para edição de sofás...")
    
    # Buscar um sofá existente
    sofa = Produto.objects.filter(id_tipo_produto__nome__icontains='sofá').first()
    
    if not sofa:
        print("❌ Nenhum sofá encontrado")
        return False
    
    print(f"🛋️ Testando com sofá: {sofa.ref_produto} - {sofa.nome_produto}")
    
    # 1. Testar formulário básico
    print("\n1️⃣ Testando SofaForm...")
    sofa_form = SofaForm(instance=sofa)
    print(f"   ✅ SofaForm criado com {len(sofa_form.fields)} campos")
    
    # 2. Testar formset de módulos
    print("\n2️⃣ Testando ModuloFormSet...")
    modulo_formset = ModuloFormSet(instance=sofa)
    print(f"   ✅ ModuloFormSet criado com {modulo_formset.total_form_count()} forms")
    print(f"   📊 Forms iniciais: {modulo_formset.initial_form_count()}")
    print(f"   📊 Forms extras: {modulo_formset.extra}")
    
    # 3. Testar formsets de tamanhos para cada módulo
    print("\n3️⃣ Testando TamanhoFormSets...")
    modulos = sofa.modulos.all()
    
    for i, modulo in enumerate(modulos):
        tamanho_formset = TamanhoFormSet(instance=modulo, prefix=f'modulo-{i}-tamanho')
        print(f"   ✅ TamanhoFormSet {i+1} criado para módulo '{modulo.nome}'")
        print(f"      📊 Forms: {tamanho_formset.total_form_count()} total, {tamanho_formset.initial_form_count()} iniciais")
    
    # 4. Testar estrutura de dados POST simulada
    print("\n4️⃣ Testando estrutura POST simulada...")
    
    # Simular dados de POST para edição
    post_data = {
        # Dados básicos do sofá
        'ref_produto': sofa.ref_produto,
        'nome_produto': f"{sofa.nome_produto} - EDITADO",
        'id_tipo_produto': str(sofa.id_tipo_produto.id),
        'ativo': 'on',
        
        # Management form do módulo
        'modulos-TOTAL_FORMS': '2',
        'modulos-INITIAL_FORMS': str(modulos.count()),
        'modulos-MIN_NUM_FORMS': '0',
        'modulos-MAX_NUM_FORMS': '1000',
        
        # Módulo 1 (existente)
        'modulos-0-id': str(modulos[0].id) if modulos.count() > 0 else '',
        'modulos-0-nome': 'Módulo 1 - Editado',
        'modulos-0-profundidade': '85.0',
        'modulos-0-altura': '90.0',
        'modulos-0-braco': '25.0',
        'modulos-0-descricao': 'Módulo editado via formset',
        
        # Módulo 2 (novo)
        'modulos-1-id': '',  # Vazio = novo módulo
        'modulos-1-nome': 'Módulo 2 - Novo',
        'modulos-1-profundidade': '80.0',
        'modulos-1-altura': '85.0',
        'modulos-1-braco': '20.0',
        'modulos-1-descricao': 'Módulo novo via formset',
    }
    
    # Testar validação
    print("\n5️⃣ Testando validação de formsets...")
    
    sofa_form_test = SofaForm(post_data, instance=sofa)
    modulo_formset_test = ModuloFormSet(post_data, instance=sofa)
    
    sofa_valid = sofa_form_test.is_valid()
    modulo_valid = modulo_formset_test.is_valid()
    
    print(f"   📋 SofaForm válido: {sofa_valid}")
    if not sofa_valid:
        print(f"      ❌ Erros: {sofa_form_test.errors}")
    
    print(f"   📋 ModuloFormSet válido: {modulo_valid}")
    if not modulo_valid:
        print(f"      ❌ Erros: {modulo_formset_test.errors}")
        print(f"      ❌ Erros não-form: {modulo_formset_test.non_form_errors()}")
    
    # 6. Verificar campos renderizados
    print("\n6️⃣ Verificando campos renderizados...")
    
    print("   🔍 Campos do SofaForm:")
    for field_name, field in sofa_form.fields.items():
        print(f"      - {field_name}: {field.__class__.__name__}")
    
    if modulo_formset.forms:
        print("   🔍 Campos do primeiro ModuloForm:")
        for field_name, field in modulo_formset.forms[0].fields.items():
            print(f"      - {field_name}: {field.__class__.__name__}")
    
    return sofa_valid and modulo_valid

if __name__ == "__main__":
    sucesso = teste_formsets_sofas()
    if sucesso:
        print("\n🎉 Todos os testes de formset passaram!")
    else:
        print("\n❌ Alguns testes falharam.")
