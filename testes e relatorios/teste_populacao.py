#!/usr/bin/env python
"""
Script para testar a população de dados e gerar dados de exemplo

Uso:
    python teste_populacao.py --gerar-exemplo /caminho/saida
    python teste_populacao.py --validar /caminho/dados_produtos
"""

import json
import sys
from pathlib import Path
import argparse
from decimal import Decimal


def gerar_dados_exemplo(pasta_saida):
    """Gera estrutura completa de exemplo para teste"""
    pasta = Path(pasta_saida)
    
    print(f"🏗️  Criando estrutura de exemplo em {pasta}...")
    
    # Criar pastas
    pastas = [
        'infos/sofas',
        'infos/cadeiras',
        'infos/banquetas',
        'infos/poltronas',
        'infos/PUFES',
        'infos/almofadas',
        'fotos/sofa',
        'fotos/cadeiras',
        'fotos/banquetas',
        'fotos/poltronas',
        'fotos/PUFES',
        'fotos/almofadas',
    ]
    
    for pasta_nome in pastas:
        (pasta / pasta_nome).mkdir(parents=True, exist_ok=True)
        print(f"  ✓ {pasta_nome}/")
    
    # Criar arquivos JSON de exemplo
    exemplos = {
        'infos/cadeiras/CD001.json': {
            'ref_cadeira': 'CD001',
            'nome': 'EVA',
            'largura': 52.5,
            'profundidade': 45.0,
            'altura': 85.0,
            'tecido_metros': 1.5,
            'volume_m3': 0.2,
            'peso_kg': 8.5,
            'preco': 450.00,
            'ativo': True,
            'tem_cor_tecido': False,
            'descricao': 'Cadeira moderna com design contemporâneo'
        },
        'infos/cadeiras/CD24.json': {
            'ref_cadeira': 'CD24',
            'nome': 'EVA BR',
            'largura': 52.5,
            'profundidade': 45.0,
            'altura': 85.0,
            'tecido_metros': 1.6,
            'volume_m3': 0.21,
            'peso_kg': 8.8,
            'preco': 475.00,
            'ativo': True,
            'tem_cor_tecido': True,
            'descricao': 'Cadeira com braços'
        },
        'infos/banquetas/BQ13.json': {
            'ref_banqueta': 'BQ13',
            'nome': 'CERES',
            'largura': 60.0,
            'profundidade': 60.0,
            'altura': 45.0,
            'tecido_metros': 1.2,
            'volume_m3': 0.16,
            'peso_kg': 12.0,
            'preco': 350.00,
            'ativo': True,
            'descricao': 'Banqueta quadrada'
        },
        'infos/banquetas/BQ249.json': {
            'ref_banqueta': 'BQ249',
            'nome': 'GIO',
            'largura': 50.0,
            'profundidade': 50.0,
            'altura': 40.0,
            'tecido_metros': 1.0,
            'volume_m3': 0.12,
            'peso_kg': 10.0,
            'preco': 300.00,
            'ativo': True,
            'descricao': 'Banqueta compacta'
        },
        'infos/almofadas/AL001.json': {
            'ref_almofada': 'AL001',
            'nome': 'DECORATIVA 40x40',
            'largura': 40.0,
            'altura': 40.0,
            'tecido_metros': 0.3,
            'volume_m3': 0.02,
            'peso_kg': 0.8,
            'preco': 89.90,
            'ativo': True,
            'descricao': 'Almofada decorativa quadrada'
        },
        'infos/almofadas/AL002.json': {
            'ref_almofada': 'AL002',
            'nome': 'CERVICAL 50x30',
            'largura': 50.0,
            'altura': 30.0,
            'tecido_metros': 0.25,
            'volume_m3': 0.015,
            'peso_kg': 0.6,
            'preco': 79.90,
            'ativo': True,
            'descricao': 'Almofada cervical'
        },
        'infos/sofas/SF939.json': {
            'ref_produto': 'SF939',
            'nome': 'SOFÁ SF939',
            'tem_cor_tecido': True,
            'tem_difer_desenho_lado_dir_esq': True,
            'tem_difer_desenho_tamanho': False,
            'ativo': True,
            'modulos': [
                {
                    'nome': 'Assento',
                    'profundidade': 90.0,
                    'altura': 75.0,
                    'braco': 25.0,
                    'descricao': 'Assento principal',
                    'tamanhos': [
                        {
                            'largura_total': 180.0,
                            'largura_assento': 150.0,
                            'tecido_metros': 8.5,
                            'volume_m3': 0.85,
                            'peso_kg': 45.0,
                            'preco': 2500.00
                        },
                        {
                            'largura_total': 200.0,
                            'largura_assento': 170.0,
                            'tecido_metros': 9.5,
                            'volume_m3': 0.95,
                            'peso_kg': 50.0,
                            'preco': 2800.00
                        }
                    ]
                },
                {
                    'nome': 'Braço Esquerdo',
                    'profundidade': 90.0,
                    'altura': 75.0,
                    'braco': 25.0,
                    'descricao': 'Braço lado esquerdo',
                    'tamanhos': [
                        {
                            'largura_total': 25.0,
                            'largura_assento': 25.0,
                            'tecido_metros': 2.0,
                            'volume_m3': 0.15,
                            'peso_kg': 8.0,
                            'preco': 400.00
                        }
                    ]
                }
            ]
        },
        'infos/sofas/LE_COULTRE.json': {
            'ref_produto': 'LE_COULTRE',
            'nome': 'SOFÁ LE COULTRE',
            'tem_cor_tecido': True,
            'tem_difer_desenho_lado_dir_esq': False,
            'tem_difer_desenho_tamanho': True,
            'ativo': True,
            'modulos': [
                {
                    'nome': 'Assento Único',
                    'profundidade': 85.0,
                    'altura': 70.0,
                    'braco': 20.0,
                    'descricao': 'Assento único do sofá',
                    'tamanhos': [
                        {
                            'largura_total': 200.0,
                            'largura_assento': 170.0,
                            'tecido_metros': 9.0,
                            'volume_m3': 0.9,
                            'peso_kg': 48.0,
                            'preco': 2300.00
                        }
                    ]
                }
            ]
        },
        'infos/poltronas/PL243.json': {
            'ref_poltrona': 'PL243',
            'nome': 'ARIA',
            'largura': 80.0,
            'profundidade': 85.0,
            'altura': 90.0,
            'tecido_metros': 2.5,
            'volume_m3': 0.6,
            'peso_kg': 25.0,
            'preco': 850.00,
            'ativo': True,
            'tem_cor_tecido': True,
            'descricao': 'Poltrona estilo moderno'
        },
        'infos/PUFES/PF13.json': {
            'ref_pufe': 'PF13',
            'nome': 'ROUND',
            'largura': 50.0,
            'profundidade': 50.0,
            'altura': 35.0,
            'tecido_metros': 1.0,
            'volume_m3': 0.088,
            'peso_kg': 9.0,
            'preco': 250.00,
            'ativo': True,
            'descricao': 'Pufe redondo'
        }
    }
    
    for caminho, conteudo in exemplos.items():
        arquivo = pasta / caminho
        with open(arquivo, 'w', encoding='utf-8') as f:
            json.dump(conteudo, f, ensure_ascii=False, indent=2)
        print(f"  ✓ {caminho}")
    
    print(f"\n✅ Estrutura de exemplo criada com sucesso!")
    print(f"📍 Localização: {pasta}")
    print(f"\n💡 Próximo passo:")
    print(f"   python manage.py popular_dados_produtos --pasta {pasta}")


def validar_estrutura(pasta_dados):
    """Valida estrutura de pastas e arquivos JSON"""
    pasta = Path(pasta_dados)
    
    if not pasta.exists():
        print(f"❌ Pasta não encontrada: {pasta}")
        return False
    
    print(f"🔍 Validando estrutura em {pasta}...")
    
    # Verificar pastas obrigatórias
    pastas_obrigatorias = ['infos', 'fotos']
    for pasta_obr in pastas_obrigatorias:
        if not (pasta / pasta_obr).exists():
            print(f"❌ Falta pasta: {pasta_obr}/")
            return False
        print(f"  ✓ {pasta_obr}/")
    
    # Verificar subpastas
    tipos_esperados = ['sofas', 'cadeiras', 'banquetas', 'poltronas', 'PUFES', 'almofadas']
    
    for tipo in tipos_esperados:
        infos_path = pasta / 'infos' / tipo
        fotos_path = pasta / 'fotos' / tipo
        
        if infos_path.exists():
            jsons = list(infos_path.glob('*.json'))
            print(f"  ✓ infos/{tipo}/ ({len(jsons)} arquivos JSON)")
        
        if fotos_path.exists():
            imagens = list(fotos_path.rglob('*.[jJ][pP][gG]')) + \
                      list(fotos_path.rglob('*.[jJ][pP][eE][gG]')) + \
                      list(fotos_path.rglob('*.[pP][nN][gG]'))
            print(f"  ✓ fotos/{tipo}/ ({len(imagens)} imagens)")
    
    # Validar JSONs
    print("\n📋 Validando JSONs...")
    total_jsons = 0
    erros = []
    
    for tipo in tipos_esperados:
        infos_path = pasta / 'infos' / tipo
        if not infos_path.exists():
            continue
        
        for json_file in infos_path.glob('*.json'):
            total_jsons += 1
            try:
                with open(json_file, 'r', encoding='utf-8') as f:
                    json.load(f)
            except json.JSONDecodeError as e:
                erros.append(f"  ❌ {json_file.name}: {str(e)}")
            except Exception as e:
                erros.append(f"  ❌ {json_file.name}: {str(e)}")
    
    if erros:
        print(f"❌ Erros encontrados:")
        for erro in erros:
            print(erro)
        return False
    
    print(f"  ✓ {total_jsons} arquivos JSON válidos")
    print(f"\n✅ Estrutura validada com sucesso!")
    return True


def main():
    parser = argparse.ArgumentParser(
        description='Ferramenta de teste para população de dados'
    )
    parser.add_argument(
        '--gerar-exemplo',
        metavar='PASTA',
        help='Gerar estrutura de exemplo em PASTA'
    )
    parser.add_argument(
        '--validar',
        metavar='PASTA',
        help='Validar estrutura em PASTA'
    )
    
    args = parser.parse_args()
    
    if args.gerar_exemplo:
        try:
            gerar_dados_exemplo(args.gerar_exemplo)
        except Exception as e:
            print(f"❌ Erro ao gerar exemplo: {str(e)}")
            sys.exit(1)
    
    elif args.validar:
        if not validar_estrutura(args.validar):
            sys.exit(1)
    
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
