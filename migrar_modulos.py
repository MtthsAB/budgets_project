#!/usr/bin/env python
"""
Script para migrar módulos de Item para Produto
Execute: python migrar_modulos.py
"""

import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema_produtos.settings')
django.setup()

from produtos.models import Modulo, Item, Produto

def migrar_modulos():
    """Migra os módulos que referenciam Item para referenciar Produto"""
    
    print("=== INICIANDO MIGRAÇÃO DE MÓDULOS ===")
    
    modulos_problematicos = []
    modulos_migrados = 0
    
    for modulo in Modulo.objects.all():
        try:
            # Encontrar o Item original
            item = Item.objects.get(id=modulo.item_id)
            
            # Encontrar o Produto correspondente pela ref_produto
            try:
                produto = Produto.objects.get(ref_produto=item.ref_produto)
                
                # Atualizar o módulo para referenciar o Produto correto
                modulo.item_id = produto.id
                modulo.save()
                modulos_migrados += 1
                print(f"✓ Módulo {modulo.id} migrado: Item {item.id}({item.ref_produto}) -> Produto {produto.id}({produto.ref_produto})")
                
            except Produto.DoesNotExist:
                modulos_problematicos.append(f"Módulo {modulo.id}: Produto não encontrado para {item.ref_produto}")
                
        except Item.DoesNotExist:
            modulos_problematicos.append(f"Módulo {modulo.id}: Item {modulo.item_id} não existe")
    
    print(f"\n=== MIGRAÇÃO CONCLUÍDA ===")
    print(f"✓ Módulos migrados: {modulos_migrados}")
    
    if modulos_problematicos:
        print(f"❌ Problemas encontrados:")
        for problema in modulos_problematicos:
            print(f"  - {problema}")
        return False
    
    return True

if __name__ == '__main__':
    try:
        print("Verificando dados antes da migração...")
        print(f"Total de registros em Item: {Item.objects.count()}")
        print(f"Total de registros em Produto: {Produto.objects.count()}")
        print(f"Total de registros em Modulo: {Modulo.objects.count()}")
        
        if migrar_modulos():
            print("\n🎉 Migração concluída com sucesso!")
        else:
            print("\n⚠️ Migração concluída com problemas!")
            
    except Exception as e:
        print(f"❌ Erro durante a migração: {e}")
        sys.exit(1)
