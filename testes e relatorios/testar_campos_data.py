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

def testar_campos_data():
    """Testa se os campos de data estão sendo preenchidos automaticamente"""
    
    print("=== TESTE DOS CAMPOS DE DATA ===\n")
    
    # Testar formulário vazio (novo orçamento)
    print("1. Testando formulário vazio (novo orçamento):")
    form_novo = OrcamentoForm()
    
    data_validade_field = form_novo.fields['data_validade']
    data_entrega_field = form_novo.fields['data_entrega']
    
    print(f"   - Data de validade inicial: {data_validade_field.initial}")
    print(f"   - Data de entrega inicial: {data_entrega_field.initial}")
    
    # Verificar valores esperados
    hoje = timezone.now().date()
    data_validade_esperada = hoje + timedelta(days=15)
    data_entrega_esperada = hoje + timedelta(days=30)
    
    print(f"\n2. Valores esperados:")
    print(f"   - Data de hoje: {hoje}")
    print(f"   - Data de validade esperada (hoje + 15): {data_validade_esperada}")
    print(f"   - Data de entrega esperada (hoje + 30): {data_entrega_esperada}")
    
    # Verificar se os valores estão corretos
    print(f"\n3. Verificação:")
    validade_ok = data_validade_field.initial == data_validade_esperada
    entrega_ok = data_entrega_field.initial == data_entrega_esperada
    
    print(f"   - Data de validade OK: {validade_ok}")
    print(f"   - Data de entrega OK: {entrega_ok}")
    
    if validade_ok and entrega_ok:
        print("\n✅ SUCESSO: Ambos os campos estão sendo preenchidos corretamente!")
    else:
        print("\n❌ ERRO: Um ou ambos os campos não estão sendo preenchidos corretamente.")
        if not validade_ok:
            print(f"     - Data de validade: esperado {data_validade_esperada}, obtido {data_validade_field.initial}")
        if not entrega_ok:
            print(f"     - Data de entrega: esperado {data_entrega_esperada}, obtido {data_entrega_field.initial}")
    
    # Testar com initial data explícito
    print(f"\n4. Testando com initial data explícito:")
    initial_data = {
        'data_validade': data_validade_esperada,
        'data_entrega': data_entrega_esperada,
        'status': 'rascunho'
    }
    
    form_initial = OrcamentoForm(initial=initial_data)
    print(f"   - Data de validade com initial: {form_initial.fields['data_validade'].initial}")
    print(f"   - Data de entrega com initial: {form_initial.fields['data_entrega'].initial}")
    
    return validade_ok and entrega_ok

if __name__ == '__main__':
    try:
        sucesso = testar_campos_data()
        print(f"\n{'='*50}")
        if sucesso:
            print("RESULTADO: As datas estão sendo preenchidas automaticamente! ✅")
        else:
            print("RESULTADO: Precisa implementar ou corrigir o preenchimento automático das datas. ❌")
        print(f"{'='*50}")
    except Exception as e:
        print(f"Erro durante o teste: {e}")
        import traceback
        traceback.print_exc()
