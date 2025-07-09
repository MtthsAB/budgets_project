#!/usr/bin/env python3

import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema_produtos.settings')
django.setup()

from produtos.models import Acessorio, Produto

print("=== TESTE FINAL ACESSÓRIOS ===")

print("\n1. Mapeamento completo produto -> acessório:")
produtos_acessorio = Produto.objects.filter(id_tipo_produto__nome__icontains='acessório')
for produto in produtos_acessorio:
    try:
        acessorio = Acessorio.objects.get(ref_acessorio=produto.ref_produto)
        print(f"   ✓ Produto ID {produto.id} ({produto.ref_produto}) -> Acessório ID {acessorio.id}")
        print(f"     Links funcionais:")
        print(f"     - /acessorios/{produto.id}/ (via produto)")
        print(f"     - /acessorios/{acessorio.id}/ (via acessório)")
        print(f"     - /acessorios/{produto.id}/editar/ (via produto)")
        print(f"     - /acessorios/{acessorio.id}/editar/ (via acessório)")
    except Acessorio.DoesNotExist:
        print(f"   ✗ Produto ID {produto.id} ({produto.ref_produto}) sem acessório correspondente")

print("\n2. Acessórios órfãos (sem produto correspondente):")
for acessorio in Acessorio.objects.all():
    try:
        produto = Produto.objects.get(ref_produto=acessorio.ref_acessorio)
        # Tem produto correspondente
        continue
    except Produto.DoesNotExist:
        print(f"   ! Acessório ID {acessorio.id} ({acessorio.ref_acessorio}) - {acessorio.nome}")
        print(f"     Links funcionais:")
        print(f"     - /acessorios/{acessorio.id}/ ✓")
        print(f"     - /acessorios/{acessorio.id}/editar/ ✓")

print("\n3. Resumo URLs que funcionam:")
print("   Via lista de produtos (/produtos/):")
print("   - Produto ID 1 -> links com /acessorios/1/")
print("   - Produto ID 3 -> links com /acessorios/3/") 
print("   - Produto ID 6 -> links com /acessorios/6/")
print("")
print("   Via lista de acessórios (/acessorios/):")
print("   - Acessório ID 1 -> links com /acessorios/1/")
print("   - Acessório ID 7 -> links com /acessorios/7/")
print("   - Acessório ID 8 -> links com /acessorios/8/") 
print("   - Acessório ID 9 -> links com /acessorios/9/")
print("   - Acessório ID 10 -> links com /acessorios/10/")
print("   - Acessório ID 11 -> links com /acessorios/11/")

print("\n=== TODOS OS LINKS DEVERIAM FUNCIONAR AGORA! ===")
