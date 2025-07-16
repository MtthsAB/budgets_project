#!/usr/bin/env python
import os
import sys
import django

# Configurar Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema_produtos.settings')
django.setup()

from orcamentos.models import Orcamento
from produtos.models import Produto

def debug_tipo_produto():
    try:
        orcamento = Orcamento.objects.get(pk=52)
        item = orcamento.itens.select_related('produto').first()
        
        produto = item.produto
        print(f"Produto: {produto.nome_produto}")
        print(f"Tipo produto nome: '{produto.id_tipo_produto.nome}'")
        print(f"Tipo produto nome lower: '{produto.id_tipo_produto.nome.lower()}'")
        print(f"eh_sofa() resultado: {produto.eh_sofa()}")
        
        # Testar as condições
        nome_lower = produto.id_tipo_produto.nome.lower()
        print(f"\nTestes:")
        print(f"  nome_lower == 'sofá': {nome_lower == 'sofá'}")
        print(f"  nome_lower == 'sofas': {nome_lower == 'sofas'}")
        print(f"  nome_lower == 'sofa': {nome_lower == 'sofa'}")
        print(f"  nome_lower in ['sofá', 'sofas', 'sofa']: {nome_lower in ['sofá', 'sofas', 'sofa']}")
        
    except Exception as e:
        print(f"Erro: {e}")

if __name__ == "__main__":
    debug_tipo_produto()
