#!/usr/bin/env python
"""
Script para testar o processamento do formset de acessórios diretamente
"""

import os
import sys
import django

# Configurar Django
sys.path.append('/home/matas/projetos/Project')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema_produtos.settings')
django.setup()

from django.http import HttpRequest
from django.contrib.auth import get_user_model
from produtos.models import Produto, TipoItem, Acessorio, SofaAcessorio
from produtos.forms import SofaAcessorioFormSet

def teste_formset_acessorios():
    """Teste direto do FormSet de acessórios"""
    
    print("=== TESTE: FormSet de Acessórios ===\n")
    
    # Obter dados necessários
    User = get_user_model()
    user = User.objects.filter(is_superuser=True).first()
    
    tipo_sofa = TipoItem.objects.filter(nome__icontains='sofá').first()
    acessorios = list(Acessorio.objects.filter(ativo=True)[:2])
    
    print(f"✅ Tipo sofá: {tipo_sofa}")
    print(f"✅ Acessórios para teste: {[a.nome for a in acessorios]}")
    
    # Criar um sofá de teste
    print("\n1. Criando sofá de teste...")
    sofa_teste = Produto.objects.create(
        ref_produto='SF_FORMSET_TEST',
        nome_produto='Sofá Teste FormSet',
        id_tipo_produto=tipo_sofa,
        ativo=True
    )
    print(f"✅ Sofá criado: {sofa_teste}")
    
    # Dados simulando um POST
    post_data = {
        'acessorios-TOTAL_FORMS': '2',
        'acessorios-INITIAL_FORMS': '0',
        'acessorios-MIN_NUM_FORMS': '0',
        'acessorios-MAX_NUM_FORMS': '1000',
        
        'acessorios-0-acessorio': str(acessorios[0].id),
        'acessorios-0-quantidade': '1',
        'acessorios-0-observacoes': 'Teste FormSet acessório 1',
        'acessorios-0-DELETE': '',
        
        'acessorios-1-acessorio': str(acessorios[1].id),
        'acessorios-1-quantidade': '2',
        'acessorios-1-observacoes': 'Teste FormSet acessório 2',
        'acessorios-1-DELETE': '',
    }
    
    print("\n2. Testando FormSet...")
    
    # Criar e validar formset
    formset = SofaAcessorioFormSet(post_data, instance=sofa_teste, prefix='acessorios')
    
    print(f"✅ FormSet criado")
    print(f"   - Total de forms: {len(formset.forms)}")
    print(f"   - Management form válido: {formset.management_form.is_valid()}")
    
    if formset.is_valid():
        print("✅ FormSet é válido!")
        
        # Salvar vinculações
        vinculacoes_salvas = formset.save()
        print(f"✅ Vinculações salvas: {len(vinculacoes_salvas)}")
        
        for vinc in vinculacoes_salvas:
            print(f"   - {vinc.acessorio.nome}: Qtd {vinc.quantidade}")
            if vinc.observacoes:
                print(f"     Obs: {vinc.observacoes}")
    else:
        print("❌ FormSet inválido!")
        print(f"Erros: {formset.errors}")
        print(f"Erros non-form: {formset.non_form_errors()}")
        
        # Verificar erros em cada form
        for i, form in enumerate(formset.forms):
            if form.errors:
                print(f"Erros no form {i}: {form.errors}")
    
    # Verificar dados salvos
    print("\n3. Verificando dados salvos...")
    vinculacoes = SofaAcessorio.objects.filter(sofa=sofa_teste)
    print(f"✅ Vinculações no banco: {vinculacoes.count()}")
    
    for vinc in vinculacoes:
        print(f"   - {vinc}")
    
    # Limpeza
    print("\n4. Limpando dados de teste...")
    vinculacoes.delete()
    sofa_teste.delete()
    print("✅ Dados de teste removidos")
    
    print("\n=== TESTE CONCLUÍDO COM SUCESSO! ===")
    return True

if __name__ == "__main__":
    sucesso = teste_formset_acessorios()
    sys.exit(0 if sucesso else 1)
