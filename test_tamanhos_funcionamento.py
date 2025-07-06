#!/usr/bin/env python
"""
Script para testar a funcionalidade de tamanhos em módulos
"""
import os
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema_produtos.settings')
django.setup()

from produtos.models import Item, TipoItem, Modulo, TamanhosModulosDetalhado

def test_tamanhos():
    """Teste de tamanhos em módulos"""
    print("=== TESTE DE TAMANHOS ===")
    
    # Buscar produto com módulos
    produto = Item.objects.prefetch_related('modulos__tamanhos_detalhados').first()
    if not produto:
        print("❌ Nenhum produto encontrado")
        return
    
    print(f"🔍 Produto: {produto.ref_produto}")
    print(f"📦 Módulos: {produto.modulos.count()}")
    
    for i, modulo in enumerate(produto.modulos.all(), 1):
        print(f"\n   📋 Módulo {i}: {modulo.nome}")
        tamanhos = modulo.tamanhos_detalhados.all()
        print(f"       📏 Tamanhos: {tamanhos.count()}")
        
        for j, tamanho in enumerate(tamanhos, 1):
            print(f"          {j}. Largura Total: {tamanho.largura_total}")
            print(f"             Largura Assento: {tamanho.largura_assento}")
            print(f"             Tecido: {tamanho.tecido_metros}m")
            print(f"             Volume: {tamanho.volume_m3}m³")
            print(f"             Peso: {tamanho.peso_kg}kg")
            print(f"             Preço: R$ {tamanho.preco}")
    
    print(f"\n🔗 URL de edição: http://localhost:8000/produtos/{produto.id}/editar/")
    print("\n=== TESTE CONCLUÍDO ===")
    
    return produto

def criar_tamanho_teste():
    """Criar tamanho de teste se não existir"""
    print("\n=== CRIANDO TAMANHO DE TESTE ===")
    
    # Buscar primeiro módulo
    modulo = Modulo.objects.first()
    if not modulo:
        print("❌ Nenhum módulo encontrado")
        return
    
    # Criar tamanho de teste
    tamanho = TamanhosModulosDetalhado.objects.create(
        id_modulo=modulo,
        largura_total=120.0,
        largura_assento=80.0,
        tecido_metros=2.5,
        volume_m3=0.85,
        peso_kg=35.0,
        preco=1500.00,
        descricao="Tamanho de teste criado automaticamente"
    )
    
    print(f"✅ Tamanho criado para módulo: {modulo.nome}")
    print(f"   - Largura Total: {tamanho.largura_total}")
    print(f"   - Preço: R$ {tamanho.preco}")
    
    return tamanho

if __name__ == "__main__":
    produto = test_tamanhos()
    
    # Se não há tamanhos, criar um de teste
    if produto and not any(modulo.tamanhos_detalhados.exists() for modulo in produto.modulos.all()):
        criar_tamanho_teste()
        print("\n" + "="*50)
        test_tamanhos()  # Testar novamente
