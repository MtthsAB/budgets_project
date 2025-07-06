#!/usr/bin/env python
"""
Script de teste para verificar o funcionamento da integração de produtos e acessórios
"""

import os
import sys
import django

# Configurar Django
sys.path.append('/home/matas/projetos/Project')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema_produtos.settings')
django.setup()

from produtos.models import Item, TipoItem

def test_integration():
    """Teste básico da integração"""
    print("=== TESTE DE INTEGRAÇÃO ===")
    
    # Verificar tipos existentes
    tipos = TipoItem.objects.all()
    print(f"Tipos de produto disponíveis: {[t.nome for t in tipos]}")
    
    # Verificar produtos existentes
    produtos = Item.objects.all()
    print(f"Total de produtos cadastrados: {produtos.count()}")
    
    for produto in produtos:
        print(f"- {produto.ref_produto}: {produto.nome_produto} ({produto.id_tipo_produto.nome})")
        if produto.eh_acessorio():
            print(f"  -> Acessório - Preço: R$ {produto.preco_acessorio}")
            print(f"  -> Descrição: {produto.descricao_acessorio}")
            vinculados = produto.produtos_vinculados.all()
            if vinculados:
                print(f"  -> Produtos vinculados: {[v.ref_produto for v in vinculados]}")
        else:
            print(f"  -> Produto normal - Módulos: {produto.modulos.count()}")
    
    print("\n=== TESTE DE CRIAÇÃO DE ACESSÓRIO ===")
    
    # Verificar se existe tipo "Acessório"
    try:
        tipo_acessorio = TipoItem.objects.get(nome__iexact='acessório')
        print(f"Tipo acessório encontrado: {tipo_acessorio.nome}")
        
        # Criar um acessório de teste
        if not Item.objects.filter(ref_produto='ACC001').exists():
            acessorio_teste = Item.objects.create(
                ref_produto='ACC001',
                nome_produto='Acessório de Teste',
                id_tipo_produto=tipo_acessorio,
                ativo=True,
                preco_acessorio=150.00,
                descricao_acessorio='Acessório criado via script de teste',
                tem_cor_tecido=False,
                tem_difer_desenho_lado_dir_esq=False,
                tem_difer_desenho_tamanho=False
            )
            print(f"Acessório de teste criado: {acessorio_teste}")
        else:
            print("Acessório de teste já existe")
            
    except TipoItem.DoesNotExist:
        print("Tipo 'Acessório' não encontrado!")
    
    print("\n=== TESTE CONCLUÍDO ===")

if __name__ == '__main__':
    test_integration()
