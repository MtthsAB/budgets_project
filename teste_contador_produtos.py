#!/usr/bin/env python
"""
Script para testar se o contador de produtos está funcionando corretamente
"""
import os
import sys
import django

# Configurar Django
sys.path.append('/home/matas/projetos/Project')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema_produtos.settings')
django.setup()

from produtos.models import TipoItem, Item, Banqueta

def testar_contador():
    """Testa se o contador está funcionando corretamente"""
    print("🔢 TESTE DO CONTADOR DE PRODUTOS NA LISTAGEM")
    print("=" * 50)
    
    # Simular diferentes cenários
    cenarios = [
        {"nome": "SEM FILTROS", "tipo_filtro": None},
        {"nome": "FILTRO: BANQUETAS", "tipo_filtro": "4"},
        {"nome": "FILTRO: SOFÁS", "tipo_filtro": "1"},
        {"nome": "FILTRO: ACESSÓRIOS", "tipo_filtro": "2"},
    ]
    
    for cenario in cenarios:
        print(f"\n📊 CENÁRIO: {cenario['nome']}")
        print("-" * 30)
        
        # Simular lógica da view
        produtos = Item.objects.select_related('id_tipo_produto').prefetch_related('modulos').all()
        banquetas = Banqueta.objects.filter(ativo=True).all()
        
        tipo_filtro = cenario['tipo_filtro']
        
        if tipo_filtro:
            produtos = produtos.filter(id_tipo_produto__id=tipo_filtro)
            
            if tipo_filtro == '4':  # Banquetas
                produtos = Item.objects.none()  # Não mostrar produtos da tabela Item
            else:
                banquetas = Banqueta.objects.none()  # Não mostrar banquetas se filtro não for banquetas
        
        # Calcular totais
        produtos_count = produtos.count()
        banquetas_count = banquetas.count()
        total = produtos_count + banquetas_count
        
        print(f"   • Produtos: {produtos_count}")
        print(f"   • Banquetas: {banquetas_count}")
        print(f"   • TOTAL: {total}")
        
        # Verificar o que apareceria no contador
        print(f"   • Contador deve mostrar: Lista de Produtos ({total})")
        
        if cenario['nome'] == "SEM FILTROS":
            esperado = 14  # 7 produtos + 7 banquetas
            if total == esperado:
                print(f"   ✅ CORRETO: {total} == {esperado}")
            else:
                print(f"   ❌ ERRO: {total} != {esperado}")
        elif cenario['nome'] == "FILTRO: BANQUETAS":
            esperado = 7  # Só banquetas
            if total == esperado:
                print(f"   ✅ CORRETO: {total} == {esperado}")
            else:
                print(f"   ❌ ERRO: {total} != {esperado}")
    
    print(f"\n🎯 RESUMO FINAL:")
    print(f"   • SEM FILTROS: deve mostrar 'Lista de Produtos (14)'")
    print(f"   • FILTRO BANQUETAS: deve mostrar 'Lista de Produtos (7)'")
    print(f"   • FILTRO SOFÁS: deve mostrar 'Lista de Produtos (1)'")
    print(f"   • FILTRO ACESSÓRIOS: deve mostrar 'Lista de Produtos (6)'")

if __name__ == "__main__":
    testar_contador()
