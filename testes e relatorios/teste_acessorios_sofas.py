#!/usr/bin/env python
"""
Script de teste para verificar a funcionalidade de acessórios em sofás
"""

import os
import sys
import django

# Configurar Django
sys.path.append('/home/matas/projetos/Project')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema_produtos.settings')
django.setup()

from produtos.models import Produto, TipoItem, Acessorio, SofaAcessorio

def testar_acessorios_sofa():
    """Teste da funcionalidade de acessórios em sofás"""
    
    print("=== TESTE: Funcionalidade de Acessórios em Sofás ===\n")
    
    # 1. Verificar se existe tipo sofá
    print("1. Verificando tipo de produto 'Sofá'...")
    tipo_sofa = TipoItem.objects.filter(nome__icontains='sofá').first()
    if tipo_sofa:
        print(f"   ✅ Encontrado: {tipo_sofa}")
    else:
        print("   ❌ Tipo 'Sofá' não encontrado!")
        return False
    
    # 2. Verificar acessórios disponíveis
    print("\n2. Verificando acessórios disponíveis...")
    acessorios = Acessorio.objects.filter(ativo=True)
    print(f"   ✅ Total de acessórios ativos: {acessorios.count()}")
    for acessorio in acessorios:
        print(f"      - {acessorio.ref_acessorio}: {acessorio.nome} (R$ {acessorio.preco or 'N/A'})")
    
    # 3. Verificar se existe algum sofá
    print("\n3. Verificando sofás existentes...")
    sofas = Produto.objects.filter(id_tipo_produto=tipo_sofa)
    print(f"   ✅ Total de sofás: {sofas.count()}")
    
    if sofas.exists():
        sofa_teste = sofas.first()
        print(f"   Sofá de teste: {sofa_teste.ref_produto} - {sofa_teste.nome_produto}")
        
        # 4. Testar vinculação de acessório
        print("\n4. Testando vinculação de acessório...")
        if acessorios.exists():
            acessorio_teste = acessorios.first()
            
            # Verificar se já existe vinculação
            vinculacao_existente = SofaAcessorio.objects.filter(
                sofa=sofa_teste, 
                acessorio=acessorio_teste
            ).first()
            
            if vinculacao_existente:
                print(f"   ✅ Vinculação já existe: {vinculacao_existente}")
            else:
                # Criar nova vinculação
                vinculacao = SofaAcessorio.objects.create(
                    sofa=sofa_teste,
                    acessorio=acessorio_teste,
                    quantidade=2,
                    observacoes="Teste de vinculação automática"
                )
                print(f"   ✅ Nova vinculação criada: {vinculacao}")
        
        # 5. Listar todas as vinculações do sofá
        print("\n5. Listando vinculações do sofá...")
        vinculacoes = SofaAcessorio.objects.filter(sofa=sofa_teste)
        if vinculacoes.exists():
            for vinc in vinculacoes:
                print(f"   - {vinc.acessorio.nome} (Qtd: {vinc.quantidade})")
                if vinc.observacoes:
                    print(f"     Obs: {vinc.observacoes}")
        else:
            print("   Nenhuma vinculação encontrada")
    
    # 6. Testar FormSet
    print("\n6. Testando FormSet...")
    try:
        from produtos.forms import SofaAcessorioFormSet
        
        # Criar formset vazio
        formset = SofaAcessorioFormSet()
        print(f"   ✅ FormSet criado com sucesso")
        print(f"   - Total de forms: {len(formset.forms)}")
        print(f"   - Management form válido: {formset.management_form.is_valid()}")
        
    except Exception as e:
        print(f"   ❌ Erro ao criar FormSet: {e}")
        return False
    
    print("\n=== TESTE CONCLUÍDO COM SUCESSO! ===")
    return True

if __name__ == "__main__":
    sucesso = testar_acessorios_sofa()
    sys.exit(0 if sucesso else 1)
