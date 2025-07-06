#!/usr/bin/env python
"""
Script para testar a listagem de acessórios através da interface
"""

import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema_produtos.settings')
django.setup()

from produtos.models import Item, Acessorio

def test_listagem_acessorios():
    """Testa a listagem de acessórios como seria vista na interface"""
    
    print("🖥️  TESTE DE LISTAGEM DE ACESSÓRIOS")
    print("=" * 50)
    
    # Simular listagem completa de acessórios
    print("\n1. LISTAGEM COMPLETA DE ACESSÓRIOS:")
    print("-" * 50)
    
    todos_acessorios = Acessorio.objects.all().order_by('ref_acessorio')
    
    for acessorio in todos_acessorios:
        produtos_vinc = acessorio.produtos_vinculados.all()
        produtos_nomes = [p.nome_produto for p in produtos_vinc]
        
        print(f"🔧 {acessorio.ref_acessorio} - {acessorio.nome}")
        print(f"   💰 Preço: R$ {acessorio.preco}")
        print(f"   🔗 Vinculado a: {', '.join(produtos_nomes) if produtos_nomes else 'Nenhum produto'}")
        print(f"   📊 Status: {'Ativo' if acessorio.ativo else 'Inativo'}")
        print()
    
    # Simular listagem filtrada por produto
    print("\n2. ACESSÓRIOS DISPONÍVEIS PARA BIG BOSS:")
    print("-" * 50)
    
    try:
        big_boss = Item.objects.get(nome_produto__icontains='BIG BOSS')
        acessorios_big_boss = Acessorio.objects.filter(
            produtos_vinculados=big_boss,
            ativo=True
        ).order_by('preco')
        
        print(f"📦 Produto: {big_boss.nome_produto}")
        print(f"🔧 Acessórios disponíveis: {acessorios_big_boss.count()}")
        print()
        
        total_valor = 0
        for acessorio in acessorios_big_boss:
            print(f"   • {acessorio.ref_acessorio} - {acessorio.nome}")
            print(f"     💰 R$ {acessorio.preco:,.2f}")
            total_valor += acessorio.preco
            print()
        
        print(f"💎 VALOR TOTAL DOS ACESSÓRIOS: R$ {total_valor:,.2f}")
        
    except Item.DoesNotExist:
        print("❌ Produto BIG BOSS não encontrado!")
    
    # Estatísticas gerais
    print("\n3. ESTATÍSTICAS GERAIS:")
    print("-" * 50)
    
    total_acessorios = Acessorio.objects.count()
    acessorios_ativos = Acessorio.objects.filter(ativo=True).count()
    acessorios_com_preco = Acessorio.objects.filter(preco__isnull=False).count()
    
    # Acessórios mais caros e mais baratos
    acessorio_mais_caro = Acessorio.objects.filter(preco__isnull=False).order_by('-preco').first()
    acessorio_mais_barato = Acessorio.objects.filter(preco__isnull=False).order_by('preco').first()
    
    print(f"📊 Total de acessórios: {total_acessorios}")
    print(f"✅ Acessórios ativos: {acessorios_ativos}")
    print(f"💰 Acessórios com preço: {acessorios_com_preco}")
    
    if acessorio_mais_caro:
        print(f"🔝 Mais caro: {acessorio_mais_caro.ref_acessorio} - {acessorio_mais_caro.nome} (R$ {acessorio_mais_caro.preco:,.2f})")
    
    if acessorio_mais_barato:
        print(f"💸 Mais barato: {acessorio_mais_barato.ref_acessorio} - {acessorio_mais_barato.nome} (R$ {acessorio_mais_barato.preco:,.2f})")
    
    # Produtos com mais acessórios
    print(f"\n4. PRODUTOS COM ACESSÓRIOS:")
    print("-" * 50)
    
    produtos_com_acessorios = Item.objects.filter(acessorio__isnull=False).distinct()
    
    for produto in produtos_com_acessorios:
        qtd_acessorios = produto.acessorio_set.count()
        print(f"📦 {produto.nome_produto}: {qtd_acessorios} acessórios")

if __name__ == "__main__":
    test_listagem_acessorios()
