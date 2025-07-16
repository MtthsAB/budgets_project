#!/usr/bin/env python3
"""
Script para verificar orçamentos existentes
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
    print("=== ORÇAMENTOS EXISTENTES ===")
    
    orcamentos = Orcamento.objects.all()
    print(f"Total de orçamentos: {orcamentos.count()}")
    
    for orc in orcamentos:
        itens_count = orc.itens.count()
        print(f"ID: {orc.id} | Número: {orc.numero} | Cliente: {orc.cliente.nome_empresa} | Itens: {itens_count}")
    
    if orcamentos.exists():
        primeiro = orcamentos.first()
        print(f"\n✅ Use o orçamento ID {primeiro.id} para teste")

if __name__ == '__main__':
    main()
