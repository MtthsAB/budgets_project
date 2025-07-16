#!/usr/bin/env python
import os
import sys
import django
from datetime import timedelta
from django.utils import timezone

# Configurar Django
sys.path.append('/home/matas/projetos/Project')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema_produtos.settings')
django.setup()

from orcamentos.forms import OrcamentoForm
from django.forms.widgets import DateInput

def debug_formulario_completo():
    """Debug completo do formulário para entender o problema"""
    
    print("=== DEBUG COMPLETO DO FORMULÁRIO ===\n")
    
    # 1. Testar exatamente como a view faz
    hoje = timezone.now().date()
    data_entrega = hoje + timedelta(days=30)
    data_validade = hoje + timedelta(days=15)
    
    print(f"1. DADOS CALCULADOS:")
    print(f"   - Hoje: {hoje}")
    print(f"   - Data entrega: {data_entrega}")
    print(f"   - Data validade: {data_validade}")
    
    # 2. Criar initial data como na view
    inicial_data = {
        'data_entrega': data_entrega,
        'data_validade': data_validade,
        'status': 'rascunho'
    }
    
    print(f"\n2. INITIAL DATA:")
    for key, value in inicial_data.items():
        print(f"   - {key}: {value}")
    
    # 3. Criar formulário como na view
    form = OrcamentoForm(initial=inicial_data)
    
    print(f"\n3. CAMPOS DO FORMULÁRIO:")
    print(f"   - data_validade.initial: {form.fields['data_validade'].initial}")
    print(f"   - data_entrega.initial: {form.fields['data_entrega'].initial}")
    
    # 4. Verificar widgets
    print(f"\n4. WIDGETS:")
    print(f"   - data_validade widget: {form.fields['data_validade'].widget}")
    print(f"   - data_entrega widget: {form.fields['data_entrega'].widget}")
    
    # 5. Renderizar campos para ver o HTML
    print(f"\n5. HTML RENDERIZADO:")
    print(f"   - data_validade HTML:")
    print(f"     {form['data_validade']}")
    print(f"   - data_entrega HTML:")
    print(f"     {form['data_entrega']}")
    
    # 6. Verificar valor atual dos campos
    print(f"\n6. VALORES ATUAIS:")
    print(f"   - data_validade.value(): {form['data_validade'].value()}")
    print(f"   - data_entrega.value(): {form['data_entrega'].value()}")
    
    # 7. Testar formulário sem initial (comportamento padrão)
    print(f"\n7. FORMULÁRIO SEM INITIAL (comportamento padrão):")
    form_padrao = OrcamentoForm()
    print(f"   - data_validade.initial: {form_padrao.fields['data_validade'].initial}")
    print(f"   - data_entrega.initial: {form_padrao.fields['data_entrega'].initial}")
    print(f"   - data_validade.value(): {form_padrao['data_validade'].value()}")
    print(f"   - data_entrega.value(): {form_padrao['data_entrega'].value()}")
    
    # 8. Verificar se o problema está no __init__ do form
    print(f"\n8. ANÁLISE DO PROBLEMA:")
    
    # Quando passamos initial data, o __init__ não deve sobrescrever
    # Mas quando há initial data, o form.initial.get() retorna valor
    # e a condição "not self.initial.get('data_validade')" falha
    
    print(f"   - form.initial: {form.initial}")
    print(f"   - form.initial.get('data_validade'): {form.initial.get('data_validade')}")
    print(f"   - form.initial.get('data_entrega'): {form.initial.get('data_entrega')}")
    
    # O problema pode estar aqui: quando há initial data, 
    # o campo não recebe o initial porque a condição falha
    
    print(f"\n9. DIAGNÓSTICO:")
    if form['data_validade'].value() and form['data_entrega'].value():
        print("   ✅ SUCESSO: Campos têm valores!")
    else:
        print("   ❌ PROBLEMA: Campos estão vazios!")
        print("   📋 POSSÍVEL CAUSA: initial data da view está interferindo com __init__ do form")

if __name__ == '__main__':
    debug_formulario_completo()
