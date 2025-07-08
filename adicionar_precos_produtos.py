#!/usr/bin/env python
"""
Script para adicionar preços básicos aos produtos para teste do sistema de orçamentos
"""

import os
import sys
import django
from decimal import Decimal
import random

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema_produtos.settings')
django.setup()

from produtos.models import Produto, Banqueta, Cadeira
from orcamentos.models import FaixaPreco

def adicionar_precos_produtos():
    """Adiciona preços básicos aos produtos para teste"""
    
    print("Adicionando preços aos produtos...")
    
    # Preços base por tipo de produto
    precos_base = {
        'sofá': {'min': 800, 'max': 5000},
        'sofas': {'min': 800, 'max': 5000},
        'acessório': {'min': 50, 'max': 300},
        'acessórios': {'min': 50, 'max': 300},
        'banqueta': {'min': 200, 'max': 800},
        'banquetas': {'min': 200, 'max': 800},
        'cadeira': {'min': 300, 'max': 1200},
        'cadeiras': {'min': 300, 'max': 1200},
        'poltrona': {'min': 600, 'max': 2000},
        'poltronas': {'min': 600, 'max': 2000},
        'pufe': {'min': 150, 'max': 500},
        'pufes': {'min': 150, 'max': 500},
        'almofada': {'min': 30, 'max': 150},
        'almofadas': {'min': 30, 'max': 150},
    }
    
    # Atualizar banquetas
    banquetas = Banqueta.objects.all()
    for banqueta in banquetas:
        if not banqueta.preco or banqueta.preco == 0:
            preco_range = precos_base.get('banqueta', {'min': 200, 'max': 800})
            preco = Decimal(str(random.randint(preco_range['min'], preco_range['max'])))
            banqueta.preco = preco
            banqueta.save()
            print(f"  - Banqueta {banqueta.nome}: R$ {preco}")
    
    # Atualizar cadeiras
    cadeiras = Cadeira.objects.all()
    for cadeira in cadeiras:
        if not cadeira.preco or cadeira.preco == 0:
            preco_range = precos_base.get('cadeira', {'min': 300, 'max': 1200})
            preco = Decimal(str(random.randint(preco_range['min'], preco_range['max'])))
            cadeira.preco = preco
            cadeira.save()
            print(f"  - Cadeira {cadeira.nome}: R$ {preco}")
    
    print(f"Preços adicionados com sucesso!")

def criar_produto_exemplo():
    """Cria um produto de exemplo para teste"""
    
    from produtos.models import TipoItem
    
    # Buscar ou criar tipo "Exemplo"
    tipo_exemplo, created = TipoItem.objects.get_or_create(
        nome='Exemplo',
        defaults={'nome': 'Exemplo'}
    )
    
    # Criar produto de exemplo
    produto_exemplo, created = Produto.objects.get_or_create(
        ref_produto='EX001',
        defaults={
            'nome_produto': 'Produto de Exemplo para Orçamentos',
            'id_tipo_produto': tipo_exemplo,
            'ativo': True
        }
    )
    
    if created:
        print(f"Produto de exemplo criado: {produto_exemplo.nome_produto}")
    else:
        print(f"Produto de exemplo já existe: {produto_exemplo.nome_produto}")

def main():
    """Função principal"""
    print("="*60)
    print("SCRIPT PARA ADICIONAR PREÇOS AOS PRODUTOS")
    print("="*60)
    
    try:
        adicionar_precos_produtos()
        print()
        criar_produto_exemplo()
        
        print()
        print("="*60)
        print("PREÇOS ADICIONADOS COM SUCESSO!")
        print("="*60)
        print()
        print("Agora você pode:")
        print("1. Criar orçamentos com produtos que têm preços")
        print("2. Testar a funcionalidade completa do sistema")
        print("3. Os preços podem ser editados na tela de orçamento")
        print()
        
    except Exception as e:
        print(f"Erro ao adicionar preços: {str(e)}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
