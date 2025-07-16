#!/usr/bin/env python3

import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema_produtos.settings')
django.setup()

from produtos.models import Acessorio, Produto

print("=== TESTE FUNCIONALIDADE MELHORADA DE EXCLUSÃO ===")

# Criar um acessório de teste
print("\n1. Criando acessório de teste...")
acessorio_teste = Acessorio.objects.create(
    ref_acessorio="AC TEST",
    nome="Acessório de Teste",
    ativo=True,
    preco=150.00,
    descricao="Acessório criado para testar a exclusão"
)
print(f"   ✓ Acessório criado: ID {acessorio_teste.id} - {acessorio_teste.ref_acessorio}")

# Vincular aos sofás existentes
print("\n2. Vinculando aos sofás...")
sofas = Produto.objects.filter(id_tipo_produto__nome__icontains='sofá')
for sofa in sofas:
    acessorio_teste.produtos_vinculados.add(sofa)
    print(f"   ✓ Vinculado ao sofá: {sofa.ref_produto}")

acessorio_teste.save()
print(f"   Total de produtos vinculados: {acessorio_teste.produtos_vinculados.count()}")

# Verificar vinculações
print("\n3. Produtos vinculados:")
for produto in acessorio_teste.produtos_vinculados.all():
    print(f"   - {produto.ref_produto} - {produto.nome_produto}")

print(f"\n4. Acessório de teste criado com sucesso!")
print(f"   ID para testar: {acessorio_teste.id}")
print(f"   URL para testar: http://localhost:8000/acessorios/{acessorio_teste.id}/")
print(f"   Agora você pode testar a exclusão pela interface!")

print("\n=== FIM TESTE ===")
