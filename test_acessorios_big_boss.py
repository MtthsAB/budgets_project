#!/usr/bin/env python
"""
Script de teste para validar os acessórios cadastrados do BIG BOSS
"""

import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema_produtos.settings')
django.setup()

from produtos.models import Item, Acessorio

def test_acessorios_big_boss():
    """Testa se os acessórios foram cadastrados e vinculados corretamente"""
    
    print("🧪 TESTE DE VALIDAÇÃO DOS ACESSÓRIOS BIG BOSS")
    print("=" * 60)
    
    # 1. Verificar se o BIG BOSS existe
    try:
        big_boss = Item.objects.get(nome_produto__icontains='BIG BOSS')
        print(f"✅ 1. Produto BIG BOSS encontrado: {big_boss.nome_produto} (ID: {big_boss.id})")
    except Item.DoesNotExist:
        print("❌ 1. Produto BIG BOSS não encontrado!")
        return False
    
    # 2. Verificar se todos os acessórios esperados existem
    acessorios_esperados = [
        "AC 45", "AC 48", "AC 56", "AC 600", "AC 601"
    ]
    
    print(f"\n✅ 2. Verificando acessórios cadastrados:")
    acessorios_encontrados = []
    
    for ref in acessorios_esperados:
        try:
            acessorio = Acessorio.objects.get(ref_acessorio=ref)
            print(f"   ✓ {ref}: {acessorio.nome} - R$ {acessorio.preco}")
            acessorios_encontrados.append(acessorio)
        except Acessorio.DoesNotExist:
            print(f"   ❌ {ref}: NÃO ENCONTRADO!")
    
    print(f"   Total encontrados: {len(acessorios_encontrados)}/{len(acessorios_esperados)}")
    
    # 3. Verificar vinculação com o BIG BOSS
    print(f"\n✅ 3. Verificando vinculação com BIG BOSS:")
    acessorios_vinculados = Acessorio.objects.filter(produtos_vinculados=big_boss)
    
    for acessorio in acessorios_vinculados:
        print(f"   ✓ {acessorio.ref_acessorio}: {acessorio.nome} (ID: {acessorio.id})")
    
    print(f"   Total vinculados: {acessorios_vinculados.count()}")
    
    # 4. Teste de consulta reversa (acessórios do produto)
    print(f"\n✅ 4. Teste de consulta reversa (via produto):")
    acessorios_do_produto = big_boss.acessorio_set.all()
    print(f"   Acessórios via produto.acessorio_set: {acessorios_do_produto.count()}")
    
    # 5. Verificar campos obrigatórios
    print(f"\n✅ 5. Verificando integridade dos dados:")
    todos_ok = True
    
    for acessorio in acessorios_vinculados:
        problemas = []
        
        if not acessorio.ref_acessorio:
            problemas.append("referência vazia")
        if not acessorio.nome:
            problemas.append("nome vazio")
        if acessorio.preco is None:
            problemas.append("preço nulo")
        
        if problemas:
            print(f"   ❌ {acessorio.ref_acessorio}: {', '.join(problemas)}")
            todos_ok = False
        else:
            print(f"   ✓ {acessorio.ref_acessorio}: todos os campos OK")
    
    # 6. Teste de unicidade das referências
    print(f"\n✅ 6. Teste de unicidade das referências:")
    referencias = list(Acessorio.objects.values_list('ref_acessorio', flat=True))
    referencias_unicas = set(referencias)
    
    if len(referencias) == len(referencias_unicas):
        print(f"   ✓ Todas as {len(referencias)} referências são únicas")
    else:
        print(f"   ❌ Referências duplicadas encontradas!")
        print(f"      Total: {len(referencias)}, Únicas: {len(referencias_unicas)}")
    
    # Relatório final
    print(f"\n📊 RELATÓRIO DO TESTE:")
    print("=" * 60)
    print(f"✅ Produto BIG BOSS: {'OK' if big_boss else 'FALHOU'}")
    print(f"✅ Acessórios cadastrados: {len(acessorios_encontrados)}/{len(acessorios_esperados)}")
    print(f"✅ Acessórios vinculados: {acessorios_vinculados.count()}")
    print(f"✅ Integridade dos dados: {'OK' if todos_ok else 'PROBLEMAS ENCONTRADOS'}")
    print(f"✅ Unicidade das referências: {'OK' if len(referencias) == len(referencias_unicas) else 'DUPLICADAS'}")
    
    sucesso = (
        big_boss and 
        len(acessorios_encontrados) == len(acessorios_esperados) and
        acessorios_vinculados.count() == len(acessorios_esperados) and
        todos_ok and
        len(referencias) == len(referencias_unicas)
    )
    
    print(f"\n{'✅ TESTE PASSOU!' if sucesso else '❌ TESTE FALHOU!'}")
    return sucesso

if __name__ == "__main__":
    test_acessorios_big_boss()
