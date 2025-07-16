#!/usr/bin/env python3
"""
Script para verificar produtos de cada tipo no sistema
"""

import os
import sys
import django

# Configurar Django
sys.path.append('/home/matas/projetos/Project')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema_produtos.settings')
django.setup()

from produtos.models import (
    TipoItem, Produto, Acessorio, Banqueta, 
    Cadeira, Poltrona, Pufe, Almofada
)

def main():
    print("=== ANÁLISE DE PRODUTOS POR TIPO ===")
    
    # Verificar TipoItem cadastrados
    print("\n1. TIPOS DE ITEM CADASTRADOS:")
    tipos = TipoItem.objects.all()
    for tipo in tipos:
        produtos_count = Produto.objects.filter(id_tipo_produto=tipo, ativo=True).count()
        print(f"   {tipo.nome}: {produtos_count} produtos na tabela Produto")
    
    # Verificar produtos específicos
    print("\n2. PRODUTOS ESPECÍFICOS (tabelas próprias):")
    print(f"   Acessórios: {Acessorio.objects.filter(ativo=True).count()}")
    print(f"   Banquetas: {Banqueta.objects.filter(ativo=True).count()}")
    print(f"   Cadeiras: {Cadeira.objects.filter(ativo=True).count()}")
    print(f"   Poltronas: {Poltrona.objects.filter(ativo=True).count()}")
    print(f"   Pufes: {Pufe.objects.filter(ativo=True).count()}")
    print(f"   Almofadas: {Almofada.objects.filter(ativo=True).count()}")
    
    # Mostrar alguns exemplos
    print("\n3. EXEMPLOS DE CADA TIPO:")
    
    if Acessorio.objects.filter(ativo=True).exists():
        acessorio = Acessorio.objects.filter(ativo=True).first()
        print(f"   Acessório: {acessorio.nome} - {acessorio.ref_acessorio}")
    
    if Banqueta.objects.filter(ativo=True).exists():
        banqueta = Banqueta.objects.filter(ativo=True).first()
        print(f"   Banqueta: {banqueta.nome} - {banqueta.ref_banqueta}")
    
    if Cadeira.objects.filter(ativo=True).exists():
        cadeira = Cadeira.objects.filter(ativo=True).first()
        print(f"   Cadeira: {cadeira.nome} - {cadeira.ref_cadeira}")
    
    if Poltrona.objects.filter(ativo=True).exists():
        poltrona = Poltrona.objects.filter(ativo=True).first()
        print(f"   Poltrona: {poltrona.nome} - {poltrona.ref_poltrona}")
    
    if Pufe.objects.filter(ativo=True).exists():
        pufe = Pufe.objects.filter(ativo=True).first()
        print(f"   Pufe: {pufe.nome} - {pufe.ref_pufe}")
    
    if Almofada.objects.filter(ativo=True).exists():
        almofada = Almofada.objects.filter(ativo=True).first()
        print(f"   Almofada: {almofada.nome} - {almofada.ref_almofada}")

if __name__ == '__main__':
    main()
