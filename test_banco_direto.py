#!/usr/bin/env python
"""
Script para testar edição de produto diretamente no banco
"""
import os
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema_produtos.settings')
django.setup()

from produtos.models import Item, TipoItem, Modulo

def test_edicao_direta():
    """Teste direto no banco para verificar criação de módulos"""
    print("=== TESTE EDIÇÃO DIRETA ===")
    
    # Buscar produto
    produto = Item.objects.first()
    if not produto:
        print("❌ Nenhum produto encontrado")
        return
    
    print(f"🔍 Produto: {produto.ref_produto}")
    print(f"📦 Módulos antes: {produto.modulos.count()}")
    
    # Remover módulos existentes
    produto.modulos.all().delete()
    
    # Criar novo módulo como seria feito na view
    modulo = Modulo.objects.create(
        item=produto,
        nome="Módulo de Teste Direto",
        profundidade=80.0,
        altura=85.0,
        braco=25.0,
        descricao="Teste de criação direta"
    )
    
    print(f"✅ Módulo criado: {modulo.nome}")
    print(f"📦 Módulos depois: {produto.modulos.count()}")
    
    # Verificar dados salvos
    modulo_verificacao = produto.modulos.first()
    if modulo_verificacao:
        print(f"   ✅ Nome: {modulo_verificacao.nome}")
        print(f"   ✅ Profundidade: {modulo_verificacao.profundidade}")
        print(f"   ✅ Altura: {modulo_verificacao.altura}")
        print(f"   ✅ Braço: {modulo_verificacao.braco}")
    
    print("\n=== SALVAMENTO NO BANCO: OK ===")
    return True

if __name__ == "__main__":
    test_edicao_direta()
