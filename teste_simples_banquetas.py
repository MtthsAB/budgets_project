#!/usr/bin/env python
"""
Script simples para testar se a view de produtos está reconhecendo banquetas
"""
import os
import sys
import django

# Adicionar o diretório do projeto ao path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema_produtos.settings')
django.setup()

from produtos.models import Banqueta, Item

def teste_simples():
    """Teste simples para verificar a lógica"""
    
    print("=== TESTE SIMPLES ===\n")
    
    # Verificar banquetas
    banquetas = Banqueta.objects.all()
    print(f"✅ Banquetas no banco: {len(banquetas)}")
    
    if banquetas:
        for b in banquetas[:3]:
            print(f"   - ID: {b.id}, Ref: {b.ref_banqueta}, Nome: {b.nome}")
    
    # Verificar produtos Item
    produtos = Item.objects.all()
    print(f"✅ Produtos Item no banco: {len(produtos)}")
    
    if produtos:
        for p in produtos[:3]:
            print(f"   - ID: {p.id}, Ref: {p.ref_produto}, Nome: {p.nome_produto}")
    
    # Verificar se há conflito de IDs
    banqueta_ids = set(Banqueta.objects.values_list('id', flat=True))
    item_ids = set(Item.objects.values_list('id', flat=True))
    
    conflitos = banqueta_ids & item_ids
    if conflitos:
        print(f"⚠️  CONFLITO DE IDs: {conflitos}")
        print("   Estes IDs existem tanto em Banqueta quanto em Item")
    else:
        print("✅ Não há conflito de IDs entre Banqueta e Item")
    
    print("\n=== TESTE DA LÓGICA DA VIEW ===")
    
    # Simular a lógica da view produto_detalhes_view
    test_ids = [1, 3, 8, 999]  # IDs para testar
    
    for test_id in test_ids:
        print(f"\n--- Testando ID: {test_id} ---")
        
        # Primeiro, tentar buscar na tabela Item
        try:
            produto = Item.objects.get(id=test_id)
            print(f"✅ Encontrado em Item: {produto.ref_produto} - {produto.nome_produto}")
            
        except Item.DoesNotExist:
            print(f"❌ Não encontrado em Item")
            
            # Se não encontrou na tabela Item, tentar buscar na tabela Banqueta
            try:
                banqueta = Banqueta.objects.get(id=test_id)
                print(f"✅ Encontrado em Banqueta: {banqueta.ref_banqueta} - {banqueta.nome}")
                
            except Banqueta.DoesNotExist:
                print(f"❌ Não encontrado em Banqueta - Retornaria 404")
    
    print("\n=== TESTE CONCLUÍDO ===")

if __name__ == '__main__':
    teste_simples()
