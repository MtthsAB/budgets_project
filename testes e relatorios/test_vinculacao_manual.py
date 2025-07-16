#!/usr/bin/env python3

import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema_produtos.settings')
django.setup()

from produtos.models import Acessorio, Produto

print("=== TESTE VINCULAÇÃO MANUAL ===")

# Pegar o primeiro acessório
acessorio = Acessorio.objects.first()
print(f"\nTrabalhando com acessório: {acessorio.ref_acessorio} - {acessorio.nome}")

# Pegar os sofás disponíveis
sofas = Produto.objects.filter(id_tipo_produto__nome__icontains='sofá', ativo=True)
print(f"Sofás disponíveis: {sofas.count()}")

if sofas.exists():
    print("\nSofás no sistema:")
    for sofa in sofas:
        print(f"  - ID {sofa.id}: {sofa.ref_produto} - {sofa.nome_produto}")
    
    # Testar vinculação manual
    primeiro_sofa = sofas.first()
    print(f"\n1. Antes da vinculação:")
    print(f"   Acessório tem {acessorio.produtos_vinculados.count()} produtos vinculados")
    
    # Adicionar vinculação
    print(f"\n2. Vinculando acessório ao sofá {primeiro_sofa.ref_produto}...")
    acessorio.produtos_vinculados.add(primeiro_sofa)
    acessorio.save()
    
    print(f"\n3. Após vinculação:")
    print(f"   Acessório tem {acessorio.produtos_vinculados.count()} produtos vinculados")
    
    produtos_vinculados = acessorio.produtos_vinculados.all()
    for produto in produtos_vinculados:
        print(f"   - {produto.ref_produto} - {produto.nome_produto}")
    
    # Testar vinculação de mais produtos
    if sofas.count() > 1:
        segundo_sofa = sofas[1]
        print(f"\n4. Vinculando também ao sofá {segundo_sofa.ref_produto}...")
        acessorio.produtos_vinculados.add(segundo_sofa)
        acessorio.save()
        
        print(f"\n5. Após segunda vinculação:")
        print(f"   Acessório tem {acessorio.produtos_vinculados.count()} produtos vinculados")
        
        produtos_vinculados = acessorio.produtos_vinculados.all()
        for produto in produtos_vinculados:
            print(f"   - {produto.ref_produto} - {produto.nome_produto}")
else:
    print("   Nenhum sofá encontrado!")

print(f"\n6. Vinculando outros acessórios também...")
# Vincular todos os acessórios aos sofás disponíveis
for acess in Acessorio.objects.all()[:3]:  # Apenas os primeiros 3
    print(f"\nVinculando {acess.ref_acessorio}...")
    for sofa in sofas:
        acess.produtos_vinculados.add(sofa)
    acess.save()
    print(f"   Agora tem {acess.produtos_vinculados.count()} produtos vinculados")

print("\n=== FIM TESTE ===")
