#!/usr/bin/env python3
"""
Script simples para verificar se há itens sendo adicionados
"""

import os
import sys
import django

# Configurar Django
sys.path.append('/home/matas/projetos/Project')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema_produtos.settings')
django.setup()

from orcamentos.models import Orcamento, OrcamentoItem

def main():
    print("=== VERIFICAÇÃO RÁPIDA DE ITENS ===")
    
    # Buscar último orçamento
    ultimo_orcamento = Orcamento.objects.order_by('-id').first()
    
    if ultimo_orcamento:
        print(f"📋 Último orçamento: {ultimo_orcamento.numero}")
        itens = ultimo_orcamento.itens.all()
        print(f"🔢 Quantidade de itens: {itens.count()}")
        
        for item in itens:
            print(f"   ✅ {item.produto.nome_produto} - Qtd: {item.quantidade} - R$ {item.preco_unitario}")
    else:
        print("❌ Nenhum orçamento encontrado")

if __name__ == '__main__':
    main()
