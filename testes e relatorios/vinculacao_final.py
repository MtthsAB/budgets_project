#!/usr/bin/env python3

import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema_produtos.settings')
django.setup()

from produtos.models import Acessorio, Produto

print("=== VINCULAÇÃO FINAL ===")

# Vincular o último acessório aos sofás
acessorio_alexa = Acessorio.objects.get(ref_acessorio='AC 601')
sofas = Produto.objects.filter(id_tipo_produto__nome__icontains='sofá', ativo=True)

print(f"Vinculando {acessorio_alexa.ref_acessorio} aos sofás...")
print(f"Antes: {acessorio_alexa.produtos_vinculados.count()} produtos vinculados")

for sofa in sofas:
    acessorio_alexa.produtos_vinculados.add(sofa)
    print(f"  + Vinculado ao {sofa.ref_produto}")

acessorio_alexa.save()
print(f"Depois: {acessorio_alexa.produtos_vinculados.count()} produtos vinculados")

print(f"\n=== RESULTADO FINAL ===")
print("Todos os acessórios agora têm produtos vinculados:")
for acessorio in Acessorio.objects.all():
    count = acessorio.produtos_vinculados.count()
    print(f"  - {acessorio.ref_acessorio}: {count} produtos vinculados")

print("\n✅ Problema resolvido!")
print("Agora todos os acessórios devem mostrar os sofás vinculados na página de detalhes.")
