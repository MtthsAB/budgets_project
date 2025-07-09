#!/usr/bin/env python3

import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema_produtos.settings')
django.setup()

from produtos.models import Acessorio, Produto

print("=== INVESTIGAÇÃO PRODUTOS VINCULADOS ===")

print("\n1. Verificando vinculações para cada acessório:")
for acessorio in Acessorio.objects.all():
    produtos_vinculados = acessorio.produtos_vinculados.all()
    print(f"\nAcessório ID {acessorio.id}: {acessorio.ref_acessorio} - {acessorio.nome}")
    print(f"   Produtos vinculados: {produtos_vinculados.count()}")
    
    if produtos_vinculados:
        for produto in produtos_vinculados:
            print(f"   - Produto ID {produto.id}: {produto.ref_produto} - {produto.nome_produto}")
    else:
        print("   - Nenhum produto vinculado")

print("\n2. Verificando sofás disponíveis para vinculação:")
sofas = Produto.objects.filter(id_tipo_produto__nome__icontains='sofá')
print(f"Total de sofás no sistema: {sofas.count()}")
for sofa in sofas[:5]:  # Mostrar apenas os primeiros 5
    print(f"   - Produto ID {sofa.id}: {sofa.ref_produto} - {sofa.nome_produto}")

print("\n3. Verificando relação inversa (quais acessórios cada sofá tem):")
for sofa in sofas[:3]:  # Verificar primeiros 3 sofás
    acessorios_vinculados = sofa.acessorio_set.all()
    print(f"\nSofá ID {sofa.id}: {sofa.ref_produto}")
    print(f"   Acessórios vinculados: {acessorios_vinculados.count()}")
    if acessorios_vinculados:
        for acessorio in acessorios_vinculados:
            print(f"   - Acessório ID {acessorio.id}: {acessorio.nome}")

print("\n4. Verificando modelo de relação:")
# Verificar a estrutura do campo produtos_vinculados
acessorio_exemplo = Acessorio.objects.first()
if acessorio_exemplo:
    print(f"\nExemplo com acessório ID {acessorio_exemplo.id}:")
    print(f"   Tipo do campo produtos_vinculados: {type(acessorio_exemplo.produtos_vinculados)}")
    print(f"   Manager: {acessorio_exemplo.produtos_vinculados}")
    
    # Tentar query direta
    try:
        todos_produtos = acessorio_exemplo.produtos_vinculados.all()
        print(f"   Query .all() resultado: {todos_produtos.count()} produtos")
        
        # Verificar se há produtos ativos
        produtos_ativos = acessorio_exemplo.produtos_vinculados.filter(ativo=True)
        print(f"   Produtos ativos vinculados: {produtos_ativos.count()}")
        
    except Exception as e:
        print(f"   Erro na query: {e}")

print("\n=== FIM INVESTIGAÇÃO ===")
