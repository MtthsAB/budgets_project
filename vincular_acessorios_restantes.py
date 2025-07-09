#!/usr/bin/env python3

import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema_produtos.settings')
django.setup()

from produtos.models import Acessorio, Produto

print("=== VINCULANDO ACESSÓRIOS RESTANTES ===")

# Buscar sofás disponíveis
sofas = Produto.objects.filter(id_tipo_produto__nome__icontains='sofá')
print(f"Sofás disponíveis: {sofas.count()}")

# Buscar acessórios sem vinculações
acessorios_sem_vinculacao = []
for acessorio in Acessorio.objects.all():
    if acessorio.produtos_vinculados.count() == 0:
        acessorios_sem_vinculacao.append(acessorio)

print(f"Acessórios sem vinculação: {len(acessorios_sem_vinculacao)}")

for acessorio in acessorios_sem_vinculacao:
    print(f"\nVinculando {acessorio.ref_acessorio} - {acessorio.nome}")
    
    # Vincular a todos os sofás
    for sofa in sofas:
        acessorio.produtos_vinculados.add(sofa)
        print(f"   ✓ Vinculado ao sofá {sofa.ref_produto}")
    
    print(f"   Total produtos vinculados: {acessorio.produtos_vinculados.count()}")

print("\n=== VERIFICAÇÃO FINAL ===")
for acessorio in Acessorio.objects.all():
    count = acessorio.produtos_vinculados.count()
    print(f"Acessório {acessorio.ref_acessorio}: {count} produtos vinculados")

print("\n=== CONCLUÍDO ===")
