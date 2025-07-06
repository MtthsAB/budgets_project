#!/usr/bin/env python3
"""
Script de validação para verificar se os módulos do BIG BOSS foram cadastrados corretamente
conforme a tabela da imagem fornecida.
"""

import os
import django
import sys

# Configurar Django
sys.path.append('/home/matas/projetos/Project')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema_produtos.settings')
django.setup()

from produtos.models import Item, Modulo, TamanhosModulosDetalhado

def validar_modulos_big_boss():
    """Valida se os módulos foram cadastrados conforme a imagem"""
    
    print("🔍 VALIDAÇÃO COMPLETA DOS MÓDULOS BIG BOSS")
    print("=" * 60)
    
    # Buscar o produto
    try:
        produto = Item.objects.get(ref_produto='SF982', nome_produto='Big Boss')
        print(f"✅ Produto: {produto.nome_produto} (ID: {produto.id})")
    except Item.DoesNotExist:
        print("❌ Produto BIG BOSS não encontrado!")
        return
    
    # Dados esperados conforme a imagem
    modulos_esperados = {
        'MOD 07 CANTO': {
            'profundidade': 110.0,
            'altura': 37.0,
            'tamanhos': [
                {'largura_total': 110.0, 'largura_assento': 110.0, 'tecido': 8.5, 'volume': 1.4, 'peso': 50.0, 'preco': 2249.0}
            ]
        },
        'MOD 08 PUFE TERMINAL': {
            'profundidade': 110.0,
            'altura': 45.0,
            'tamanhos': [
                {'largura_total': 60.0, 'largura_assento': 110.0, 'tecido': 2.6, 'volume': 0.4, 'peso': 28.0, 'preco': 968.0}
            ]
        }
    }
    
    print(f"\n📦 TODOS OS MÓDULOS DO PRODUTO ({produto.modulos.count()} total):")
    print("-" * 60)
    
    modulos_produto = produto.modulos.all().order_by('id')
    
    for i, modulo in enumerate(modulos_produto, 1):
        print(f"\n{i}. 📋 {modulo.nome}")
        print(f"   🆔 ID: {modulo.id}")
        print(f"   📐 Profundidade: {modulo.profundidade}cm")
        print(f"   📏 Altura: {modulo.altura}cm")
        print(f"   🔧 Braço: {modulo.braco if modulo.braco else 'N/A'}cm")
        print(f"   📝 Descrição: {modulo.descricao or 'N/A'}")
        
        # Verificar se é um dos módulos da imagem
        if modulo.nome in modulos_esperados:
            esperado = modulos_esperados[modulo.nome]
            
            # Validar dimensões
            prof_ok = float(modulo.profundidade) == esperado['profundidade']
            alt_ok = float(modulo.altura) == esperado['altura']
            
            print(f"   ✅ Profundidade: {'✓' if prof_ok else '✗'} ({modulo.profundidade} = {esperado['profundidade']})")
            print(f"   ✅ Altura: {'✓' if alt_ok else '✗'} ({modulo.altura} = {esperado['altura']})")
        
        # Listar tamanhos
        tamanhos = modulo.tamanhos_detalhados.all()
        print(f"   📏 Tamanhos cadastrados: {tamanhos.count()}")
        
        for j, tamanho in enumerate(tamanhos, 1):
            print(f"      {j}. {tamanho.largura_total}x{tamanho.largura_assento}cm")
            print(f"         💰 R$ {tamanho.preco}")
            print(f"         🧵 {tamanho.tecido_metros}m tecido")
            print(f"         📦 {tamanho.volume_m3}m³")
            print(f"         ⚖️  {tamanho.peso_kg}kg")
            
            # Validar valores se for dos módulos da imagem
            if modulo.nome in modulos_esperados and j <= len(esperado['tamanhos']):
                esperado_tamanho = esperado['tamanhos'][j-1]
                
                validacoes = [
                    ('Largura Total', float(tamanho.largura_total), esperado_tamanho['largura_total']),
                    ('Largura Assento', float(tamanho.largura_assento), esperado_tamanho['largura_assento']),
                    ('Tecido', float(tamanho.tecido_metros), esperado_tamanho['tecido']),
                    ('Volume', float(tamanho.volume_m3), esperado_tamanho['volume']),
                    ('Peso', float(tamanho.peso_kg), esperado_tamanho['peso']),
                    ('Preço', float(tamanho.preco), esperado_tamanho['preco'])
                ]
                
                todas_ok = True
                for nome, valor, esperado_val in validacoes:
                    ok = valor == esperado_val
                    if not ok:
                        todas_ok = False
                        print(f"         ❌ {nome}: {valor} ≠ {esperado_val}")
                
                if todas_ok:
                    print(f"         ✅ Todos os valores conferem com a imagem!")
    
    print("\n" + "=" * 60)
    print("🎯 RESUMO DA VALIDAÇÃO:")
    
    # Verificar se os módulos da imagem estão presentes
    modulos_cadastrados = set(modulo.nome for modulo in modulos_produto)
    modulos_imagem = set(modulos_esperados.keys())
    
    print(f"📋 Módulos esperados da imagem: {len(modulos_imagem)}")
    print(f"📦 Módulos cadastrados no total: {len(modulos_cadastrados)}")
    
    modulos_faltando = modulos_imagem - modulos_cadastrados
    modulos_extras = modulos_cadastrados - modulos_imagem
    
    if modulos_faltando:
        print(f"❌ Módulos faltando: {', '.join(modulos_faltando)}")
    
    if modulos_extras:
        print(f"ℹ️  Módulos extras (não na imagem): {', '.join(modulos_extras)}")
    
    if not modulos_faltando:
        print("✅ Todos os módulos da imagem foram cadastrados!")
    
    print(f"\n🌐 Interface: http://localhost:8000/produtos/{produto.id}/editar/")
    print(f"🔍 Detalhes: http://localhost:8000/produtos/{produto.id}/")

if __name__ == "__main__":
    validar_modulos_big_boss()
