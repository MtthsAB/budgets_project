#!/usr/bin/env python3

import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema_produtos.settings')
django.setup()

from produtos.models import Acessorio, Produto

print("=== LIMPEZA ACESSÓRIOS ÓRFÃOS ===")

# Acessórios que você disse que deletou mas ainda aparecem
acessorios_para_deletar = ['AC 45', 'AC 56', 'AC 600']

print(f"\n1. Deletando acessórios órfãos: {acessorios_para_deletar}")

for ref_acessorio in acessorios_para_deletar:
    try:
        acessorio = Acessorio.objects.get(ref_acessorio=ref_acessorio)
        nome_completo = f"{acessorio.ref_acessorio} - {acessorio.nome}"
        print(f"\n   Deletando: {nome_completo}")
        
        # Verificar se tem produto correspondente
        try:
            produto = Produto.objects.get(ref_produto=acessorio.ref_acessorio)
            print(f"     ⚠️  Também há produto correspondente (ID {produto.id})")
            print(f"     ⚠️  Mantendo produto, deletando apenas acessório")
        except Produto.DoesNotExist:
            print(f"     ✓ Sem produto correspondente, pode deletar safely")
        
        # Deletar o acessório
        acessorio.delete()
        print(f"     ✅ Acessório deletado com sucesso!")
        
    except Acessorio.DoesNotExist:
        print(f"   ✗ Acessório {ref_acessorio} não encontrado")

print(f"\n2. Estado após limpeza:")
acessorios_restantes = Acessorio.objects.all()
print(f"   Total de acessórios: {acessorios_restantes.count()}")
for acessorio in acessorios_restantes:
    produtos_vinculados = acessorio.produtos_vinculados.count()
    print(f"   - ID {acessorio.id}: {acessorio.ref_acessorio} - {acessorio.nome} ({produtos_vinculados} produtos)")

print("\n=== LIMPEZA CONCLUÍDA ===")
