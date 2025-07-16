#!/usr/bin/env python3

import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema_produtos.settings')
django.setup()

from produtos.models import Acessorio, Produto

print("=== INVESTIGAÇÃO ACESSÓRIOS DELETADOS ===")

print("\n1. Acessórios na tabela Acessorio:")
acessorios = Acessorio.objects.all()
print(f"Total: {acessorios.count()}")
for acessorio in acessorios:
    print(f"   - ID {acessorio.id}: {acessorio.ref_acessorio} - {acessorio.nome}")

print("\n2. Produtos do tipo 'Acessórios' na tabela Produto:")
produtos_acessorio = Produto.objects.filter(id_tipo_produto__nome__icontains='acessório')
print(f"Total: {produtos_acessorio.count()}")
for produto in produtos_acessorio:
    print(f"   - ID {produto.id}: {produto.ref_produto} - {produto.nome_produto}")
    
    # Verificar se tem acessório correspondente
    try:
        acessorio_corresp = Acessorio.objects.get(ref_acessorio=produto.ref_produto)
        print(f"     ✓ Tem acessório ID {acessorio_corresp.id}")
    except Acessorio.DoesNotExist:
        print(f"     ✗ SEM acessório correspondente na tabela Acessorio")

print("\n3. Verificando inconsistências:")
print("   3.1 Acessórios sem produto correspondente:")
for acessorio in acessorios:
    try:
        produto_corresp = Produto.objects.get(ref_produto=acessorio.ref_acessorio)
        print(f"       Acessório {acessorio.ref_acessorio} ✓ tem produto ID {produto_corresp.id}")
    except Produto.DoesNotExist:
        print(f"       Acessório {acessorio.ref_acessorio} ✗ SEM produto correspondente")

print("\n   3.2 Produtos sem acessório correspondente:")
for produto in produtos_acessorio:
    try:
        acessorio_corresp = Acessorio.objects.get(ref_acessorio=produto.ref_produto)
        # OK, tem correspondência
        pass
    except Acessorio.DoesNotExist:
        print(f"       Produto {produto.ref_produto} (ID {produto.id}) ✗ SEM acessório correspondente")

print("\n4. Verificando se há registros com soft delete ou flags especiais:")
# Verificar se algum acessório tem campo 'ativo' = False ou similar
acessorios_inativos = acessorios.filter(ativo=False)
print(f"   Acessórios inativos: {acessorios_inativos.count()}")
for acessorio in acessorios_inativos:
    print(f"   - ID {acessorio.id}: {acessorio.ref_acessorio} (INATIVO)")

produtos_inativos = produtos_acessorio.filter(ativo=False)
print(f"   Produtos acessórios inativos: {produtos_inativos.count()}")
for produto in produtos_inativos:
    print(f"   - ID {produto.id}: {produto.ref_produto} (INATIVO)")

print("\n=== FIM INVESTIGAÇÃO ===")
