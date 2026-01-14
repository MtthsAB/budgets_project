#!/usr/bin/env python
"""
Utilitário para converter dados de produtos de CSV para JSON
Útil se você já tem os dados em formato tabular

Uso:
    python converter_csv_json.py --entrada dados.csv --saida produtos_json --tipo cadeiras
"""

import csv
import json
import sys
from pathlib import Path
import argparse


def converter_csv_cadeiras(csv_file):
    """Converte CSV para JSON de cadeiras"""
    produtos = []
    
    with open(csv_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Mapear colunas do CSV para campos do modelo
            produto = {
                'ref_cadeira': row.get('ref_cadeira', row.get('referencia', '')).strip(),
                'nome': row.get('nome', '').strip(),
                'largura': float(row.get('largura', 0) or 0),
                'profundidade': float(row.get('profundidade', 0) or 0),
                'altura': float(row.get('altura', 0) or 0),
                'tecido_metros': float(row.get('tecido_metros', 0) or 0),
                'volume_m3': float(row.get('volume_m3', 0) or 0),
                'peso_kg': float(row.get('peso_kg', 0) or 0),
                'preco': float(row.get('preco', 0) or 0),
                'ativo': row.get('ativo', 'true').lower() in ['true', '1', 'sim', 'yes'],
                'tem_cor_tecido': row.get('tem_cor_tecido', 'false').lower() in ['true', '1', 'sim', 'yes'],
                'descricao': row.get('descricao', '').strip(),
            }
            produtos.append(produto)
    
    return produtos


def converter_csv_banquetas(csv_file):
    """Converte CSV para JSON de banquetas"""
    produtos = []
    
    with open(csv_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            produto = {
                'ref_banqueta': row.get('ref_banqueta', row.get('referencia', '')).strip(),
                'nome': row.get('nome', '').strip(),
                'largura': float(row.get('largura', 0) or 0),
                'profundidade': float(row.get('profundidade', 0) or 0),
                'altura': float(row.get('altura', 0) or 0),
                'tecido_metros': float(row.get('tecido_metros', 0) or 0),
                'volume_m3': float(row.get('volume_m3', 0) or 0),
                'peso_kg': float(row.get('peso_kg', 0) or 0),
                'preco': float(row.get('preco', 0) or 0),
                'ativo': row.get('ativo', 'true').lower() in ['true', '1', 'sim', 'yes'],
                'descricao': row.get('descricao', '').strip(),
            }
            produtos.append(produto)
    
    return produtos


def converter_csv_almofadas(csv_file):
    """Converte CSV para JSON de almofadas"""
    produtos = []
    
    with open(csv_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            produto = {
                'ref_almofada': row.get('ref_almofada', row.get('referencia', '')).strip(),
                'nome': row.get('nome', '').strip(),
                'largura': float(row.get('largura', 0) or 0),
                'altura': float(row.get('altura', 0) or 0),
                'tecido_metros': float(row.get('tecido_metros', 0) or 0),
                'volume_m3': float(row.get('volume_m3', 0) or 0),
                'peso_kg': float(row.get('peso_kg', 0) or 0),
                'preco': float(row.get('preco', 0) or 0),
                'ativo': row.get('ativo', 'true').lower() in ['true', '1', 'sim', 'yes'],
                'descricao': row.get('descricao', '').strip(),
            }
            produtos.append(produto)
    
    return produtos


def converter_csv_sofas(csv_file):
    """Converte CSV para JSON de sofás (estrutura simplificada)"""
    produtos = []
    
    with open(csv_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            produto = {
                'ref_produto': row.get('ref_produto', row.get('referencia', '')).strip(),
                'nome': row.get('nome', '').strip(),
                'tem_cor_tecido': row.get('tem_cor_tecido', 'false').lower() in ['true', '1', 'sim', 'yes'],
                'tem_difer_desenho_lado_dir_esq': row.get('tem_difer_desenho_lado_dir_esq', 'false').lower() in ['true', '1', 'sim', 'yes'],
                'tem_difer_desenho_tamanho': row.get('tem_difer_desenho_tamanho', 'false').lower() in ['true', '1', 'sim', 'yes'],
                'ativo': row.get('ativo', 'true').lower() in ['true', '1', 'sim', 'yes'],
                'modulos': [],  # Será preciso adicionar manualmente ou fazer script separado
            }
            produtos.append(produto)
    
    return produtos


def salvar_jsons(produtos, pasta_saida, tipo):
    """Salva lista de produtos como arquivos JSON individuais"""
    pasta = Path(pasta_saida)
    pasta.mkdir(parents=True, exist_ok=True)
    
    count = 0
    for produto in produtos:
        # Determinar campo de referência
        if tipo == 'cadeiras':
            ref = produto['ref_cadeira']
        elif tipo == 'banquetas':
            ref = produto['ref_banqueta']
        elif tipo == 'almofadas':
            ref = produto['ref_almofada']
        elif tipo == 'sofas':
            ref = produto['ref_produto']
        else:
            ref = produto.get('ref_produto', 'produto')
        
        # Salvar como arquivo JSON
        nome_arquivo = f"{ref}.json"
        caminho = pasta / nome_arquivo
        
        with open(caminho, 'w', encoding='utf-8') as f:
            json.dump(produto, f, ensure_ascii=False, indent=2)
        
        print(f"✓ {nome_arquivo}")
        count += 1
    
    print(f"\n✅ {count} arquivos JSON criados em {pasta}")
    return count


def main():
    parser = argparse.ArgumentParser(
        description='Converter dados de produtos de CSV para JSON'
    )
    parser.add_argument(
        '--entrada',
        required=True,
        help='Arquivo CSV de entrada'
    )
    parser.add_argument(
        '--saida',
        required=True,
        help='Pasta de saída para arquivos JSON'
    )
    parser.add_argument(
        '--tipo',
        required=True,
        choices=['cadeiras', 'banquetas', 'almofadas', 'sofas', 'poltronas', 'pufes'],
        help='Tipo de produto'
    )
    
    args = parser.parse_args()
    
    # Verificar arquivo
    if not Path(args.entrada).exists():
        print(f"❌ Arquivo não encontrado: {args.entrada}")
        sys.exit(1)
    
    print(f"📖 Lendo {args.entrada}...")
    
    # Converter baseado no tipo
    conversores = {
        'cadeiras': converter_csv_cadeiras,
        'banquetas': converter_csv_banquetas,
        'almofadas': converter_csv_almofadas,
        'sofas': converter_csv_sofas,
        'poltronas': converter_csv_cadeiras,  # Mesma estrutura
        'pufes': converter_csv_banquetas,     # Mesma estrutura
    }
    
    try:
        produtos = conversores[args.tipo](args.entrada)
        print(f"✓ {len(produtos)} produtos lidos")
        
        # Salvar JSONs
        salvar_jsons(produtos, args.saida, args.tipo)
        
    except Exception as e:
        print(f"❌ Erro: {str(e)}")
        sys.exit(1)


if __name__ == '__main__':
    main()
