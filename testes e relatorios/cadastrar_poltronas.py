#!/usr/bin/env python3
"""
Script para cadastrar poltronas no sistema de produto        {
            'ref_poltrona': 'PL32',
            'nome': 'COMPATIO',
            'largura': Decimal('61'),
            'profundidade': Decimal('65'),
            'altura': Decimal('73'),
            'tecido_metros': Decimal('2.40'),
            'volume_m3': Decimal('0.32'),
            'peso_kg': Decimal('15'),
            'preco': Decimal    # Mapeamento das referências para os nomes dos arquivos de imagem
    imagens_map = {
        'PL243': 'pl243.png',
        'PL246': 'pl246.png', 
        'PL105': 'pl105.png',
        'PL869': 'pl869.png',
        'PL97': 'pl97.png',
        'PL32': 'pl92.png',  # Referência PL32 usa imagem pl92.png
        'PL214': 'pl214.png',
        },nos dados das imagens fornecidas na tabela de especificações.

Execução: python cadastrar_poltronas.py
"""

import os
import sys
import django
from decimal import Decimal

# Configurar Django
sys.path.append('/home/matas/projetos/Project')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema_produtos.settings')
django.setup()

from produtos.models import Poltrona

def cadastrar_poltronas():
    """Cadastrar todas as poltronas baseadas na tabela fornecida."""
    
    # Dados extraídos das imagens da tabela
    poltronas_dados = [
        {
            'ref_poltrona': 'PL243',
            'nome': 'ARIA',
            'largura': Decimal('82'),
            'profundidade': Decimal('81'),
            'altura': Decimal('84'),
            'tecido_metros': Decimal('4.60'),
            'volume_m3': Decimal('0.60'),
            'peso_kg': Decimal('25'),
            'preco': Decimal('1301'),
        },
        {
            'ref_poltrona': 'PL246',
            'nome': 'ARISTOCRATA',
            'largura': Decimal('78'),
            'profundidade': Decimal('81'),
            'altura': Decimal('83'),
            'tecido_metros': Decimal('3.80'),
            'volume_m3': Decimal('0.60'),
            'peso_kg': Decimal('25'),
            'preco': Decimal('1168'),
        },
        {
            'ref_poltrona': 'PL105',
            'nome': 'CERNE',
            'largura': Decimal('63'),
            'profundidade': Decimal('78'),
            'altura': Decimal('86'),
            'tecido_metros': Decimal('2.60'),
            'volume_m3': Decimal('0.50'),
            'peso_kg': Decimal('15'),
            'preco': Decimal('1673'),
        },
        {
            'ref_poltrona': 'PL869',
            'nome': 'CHANEL',
            'largura': Decimal('104'),
            'profundidade': Decimal('80'),
            'altura': Decimal('73'),
            'tecido_metros': Decimal('6.40'),
            'volume_m3': Decimal('0.65'),
            'peso_kg': Decimal('20'),
            'preco': Decimal('1712'),
        },
        {
            'ref_poltrona': 'PL97',
            'nome': 'CLARA',
            'largura': Decimal('67'),
            'profundidade': Decimal('74'),
            'altura': Decimal('86'),
            'tecido_metros': Decimal('3.50'),
            'volume_m3': Decimal('0.46'),
            'peso_kg': Decimal('15'),
            'preco': Decimal('1027'),
        },
        {
            'ref_poltrona': 'PL32',
            'nome': 'COMPATTO',
            'largura': Decimal('61'),
            'profundidade': Decimal('66'),
            'altura': Decimal('73'),
            'tecido_metros': Decimal('2.40'),
            'volume_m3': Decimal('0.32'),
            'peso_kg': Decimal('15'),
            'preco': Decimal('1334'),
        },
        {
            'ref_poltrona': 'PL214',
            'nome': 'CORDONE',
            'largura': Decimal('70'),
            'profundidade': Decimal('80'),
            'altura': Decimal('80'),
            'tecido_metros': Decimal('3.30'),
            'volume_m3': Decimal('0.52'),
            'peso_kg': Decimal('15'),
            'preco': Decimal('1854'),
        },
        {
            'ref_poltrona': 'PL53',
            'nome': 'DEMETER',
            'largura': Decimal('78'),
            'profundidade': Decimal('85'),
            'altura': Decimal('105'),
            'tecido_metros': Decimal('3.40'),
            'volume_m3': Decimal('0.74'),
            'peso_kg': Decimal('20'),
            'preco': Decimal('3854'),
        },
        {
            'ref_poltrona': 'PL134',
            'nome': 'DIPLOMATA',
            'largura': Decimal('67'),
            'profundidade': Decimal('75'),
            'altura': Decimal('76'),
            'tecido_metros': Decimal('3.70'),
            'volume_m3': Decimal('0.41'),
            'peso_kg': Decimal('25'),
            'preco': Decimal('1550'),
        },
        {
            'ref_poltrona': 'PL988',
            'nome': 'FLOW',
            'largura': Decimal('80'),
            'profundidade': Decimal('68'),
            'altura': Decimal('76'),
            'tecido_metros': Decimal('3.80'),
            'volume_m3': Decimal('0.60'),
            'peso_kg': Decimal('26'),
            'preco': Decimal('1254'),
        },
        {
            'ref_poltrona': 'PL273',
            'nome': 'BOLL',
            'largura': Decimal('72'),
            'profundidade': Decimal('60'),
            'altura': Decimal('63'),
            'tecido_metros': Decimal('2.30'),
            'volume_m3': Decimal('0.33'),
            'peso_kg': Decimal('25'),
            'preco': Decimal('1613'),
        },
        {
            'ref_poltrona': 'PL287',
            'nome': 'GUCCI',
            'largura': Decimal('61'),
            'profundidade': Decimal('74'),
            'altura': Decimal('78'),
            'tecido_metros': Decimal('3.00'),
            'volume_m3': Decimal('0.40'),
            'peso_kg': Decimal('22'),
            'preco': Decimal('1538'),
        },
        {
            'ref_poltrona': 'PL232/2B',
            'nome': 'HALL 2B',
            'largura': Decimal('72'),
            'profundidade': Decimal('67'),
            'altura': Decimal('71'),
            'tecido_metros': Decimal('3.30'),
            'volume_m3': Decimal('0.40'),
            'peso_kg': Decimal('20'),
            'preco': Decimal('1232'),
        },
        {
            'ref_poltrona': 'PL232/1B',
            'nome': 'HALL 1B',
            'largura': Decimal('67'),
            'profundidade': Decimal('67'),
            'altura': Decimal('71'),
            'tecido_metros': Decimal('3.00'),
            'volume_m3': Decimal('0.38'),
            'peso_kg': Decimal('18'),
            'preco': Decimal('1109'),
        },
        {
            'ref_poltrona': 'PL232/SB',
            'nome': 'HALL SB',
            'largura': Decimal('67'),
            'profundidade': Decimal('67'),
            'altura': Decimal('71'),
            'tecido_metros': Decimal('2.50'),
            'volume_m3': Decimal('0.38'),
            'peso_kg': Decimal('16'),
            'preco': Decimal('1000'),
        },
        {
            'ref_poltrona': 'PL232',
            'nome': 'HALL',
            'largura': Decimal('67'),
            'profundidade': Decimal('67'),
            'altura': Decimal('45'),
            'tecido_metros': Decimal('2.50'),
            'volume_m3': Decimal('0.25'),
            'peso_kg': Decimal('10'),
            'preco': Decimal('901'),
        },
        {
            'ref_poltrona': 'ME232',
            'nome': 'HALL MESA',
            'largura': Decimal('67'),
            'profundidade': Decimal('67'),
            'altura': Decimal('21'),
            'tecido_metros': Decimal('0.10'),
            'volume_m3': Decimal('0.10'),
            'peso_kg': Decimal('5'),
            'preco': Decimal('835'),
        },
        {
            'ref_poltrona': 'PL25',
            'nome': 'ISIS',
            'largura': Decimal('72'),
            'profundidade': Decimal('65'),
            'altura': Decimal('85'),
            'tecido_metros': Decimal('2.80'),
            'volume_m3': Decimal('0.44'),
            'peso_kg': Decimal('8'),
            'preco': Decimal('1178'),
        },
        {
            'ref_poltrona': 'PL915',
            'nome': 'JARRAR',
            'largura': Decimal('125'),
            'profundidade': Decimal('100'),
            'altura': Decimal('37'),
            'tecido_metros': Decimal('8.10'),
            'volume_m3': Decimal('1.30'),
            'peso_kg': Decimal('30'),
            'preco': Decimal('3683'),
        },
        {
            'ref_poltrona': 'LE COULTHE',
            'nome': 'LE COULTHE',
            'largura': Decimal('115'),
            'profundidade': Decimal('100'),
            'altura': Decimal('30'),
            'tecido_metros': Decimal('6.45'),
            'volume_m3': Decimal('1.07'),
            'peso_kg': Decimal('30'),
            'preco': Decimal('2822'),
        },
        {
            'ref_poltrona': 'LUXOR',
            'nome': 'LUXOR',
            'largura': Decimal('84'),
            'profundidade': Decimal('87'),
            'altura': Decimal('30'),
            'tecido_metros': Decimal('6.70'),
            'volume_m3': Decimal('0.70'),
            'peso_kg': Decimal('23'),
            'preco': Decimal('1330'),
        },
        {
            'ref_poltrona': 'MALIBU',
            'nome': 'MALIBU',
            'largura': Decimal('90'),
            'profundidade': Decimal('80'),
            'altura': Decimal('80'),
            'tecido_metros': Decimal('3.30'),
            'volume_m3': Decimal('0.70'),
            'peso_kg': Decimal('22'),
            'preco': Decimal('981'),
        },
        {
            'ref_poltrona': 'PL244',
            'nome': 'MIS',
            'largura': Decimal('52'),
            'profundidade': Decimal('61'),
            'altura': Decimal('80'),
            'tecido_metros': Decimal('1.30'),
            'volume_m3': Decimal('0.23'),
            'peso_kg': Decimal('7'),
            'preco': Decimal('882'),
        },
        {
            'ref_poltrona': 'PL239',
            'nome': 'ORBI',
            'largura': Decimal('120'),
            'profundidade': Decimal('90'),
            'altura': Decimal('76'),
            'tecido_metros': Decimal('6.30'),
            'volume_m3': Decimal('0.83'),
            'peso_kg': Decimal('30'),
            'preco': Decimal('2386'),
        },
        {
            'ref_poltrona': 'PL22',
            'nome': 'PIRRA',
            'largura': Decimal('61'),
            'profundidade': Decimal('63'),
            'altura': Decimal('83'),
            'tecido_metros': Decimal('1.50'),
            'volume_m3': Decimal('0.36'),
            'peso_kg': Decimal('8'),
            'preco': Decimal('702'),
        },
        {
            'ref_poltrona': 'RIALTO',
            'nome': 'RIALTO',
            'largura': Decimal('100'),
            'profundidade': Decimal('90'),
            'altura': Decimal('85'),
            'tecido_metros': Decimal('4.90'),
            'volume_m3': Decimal('0.90'),
            'peso_kg': Decimal('18'),
            'preco': Decimal('1388'),
        },
        {
            'ref_poltrona': 'TIFFANY',
            'nome': 'TIFFANY',
            'largura': Decimal('107'),
            'profundidade': Decimal('107'),
            'altura': Decimal('72'),
            'tecido_metros': Decimal('5.80'),
            'volume_m3': Decimal('0.90'),
            'peso_kg': Decimal('32'),
            'preco': Decimal('2379'),
        },
        {
            'ref_poltrona': 'VERSACE',
            'nome': 'VERSACE',
            'largura': Decimal('118'),
            'profundidade': Decimal('109'),
            'altura': Decimal('83'),
            'tecido_metros': Decimal('6.50'),
            'volume_m3': Decimal('1.08'),
            'peso_kg': Decimal('35'),
            'preco': Decimal('6096'),
        },
        {
            'ref_poltrona': 'PL225',
            'nome': 'XANGAI',
            'largura': Decimal('77'),
            'profundidade': Decimal('97'),
            'altura': Decimal('86'),
            'tecido_metros': Decimal('3.30'),
            'volume_m3': Decimal('0.70'),
            'peso_kg': Decimal('20'),
            'preco': Decimal('2007'),
        },
        {
            'ref_poltrona': 'PL238',
            'nome': 'ZARA',
            'largura': Decimal('76'),
            'profundidade': Decimal('63'),
            'altura': Decimal('88'),
            'tecido_metros': Decimal('4.40'),
            'volume_m3': Decimal('0.61'),
            'peso_kg': Decimal('25'),
            'preco': Decimal('1180'),
        },
        {
            'ref_poltrona': 'PL262',
            'nome': 'RETRO',
            'largura': Decimal('78'),
            'profundidade': Decimal('74'),
            'altura': Decimal('85'),
            'tecido_metros': Decimal('3.30'),
            'volume_m3': Decimal('0.53'),
            'peso_kg': Decimal('14'),
            'preco': Decimal('845'),
        },
        {
            'ref_poltrona': 'PL274',
            'nome': 'KOLEOS',
            'largura': Decimal('63'),
            'profundidade': Decimal('80'),
            'altura': Decimal('82'),
            'tecido_metros': Decimal('2.45'),
            'volume_m3': Decimal('0.43'),
            'peso_kg': Decimal('15'),
            'preco': Decimal('1458'),
        },
    ]
    
    total_cadastradas = 0
    total_atualizadas = 0
    total_erros = 0
    
    print("🚀 Iniciando cadastro de poltronas...")
    print(f"📊 Total de poltronas para processar: {len(poltronas_dados)}")
    print("-" * 60)
    
    for dados in poltronas_dados:
        try:
            poltrona, criada = Poltrona.objects.get_or_create(
                ref_poltrona=dados['ref_poltrona'],
                defaults=dados
            )
            
            if criada:
                print(f"✅ Poltrona cadastrada: {dados['ref_poltrona']} - {dados['nome']}")
                total_cadastradas += 1
            else:
                # Atualizar dados existentes
                for campo, valor in dados.items():
                    if campo != 'ref_poltrona':  # Não atualizar a referência
                        setattr(poltrona, campo, valor)
                poltrona.save()
                print(f"🔄 Poltrona atualizada: {dados['ref_poltrona']} - {dados['nome']}")
                total_atualizadas += 1
                
        except Exception as e:
            print(f"❌ Erro ao cadastrar {dados['ref_poltrona']}: {str(e)}")
            total_erros += 1
    
    print("-" * 60)
    print("📈 RESUMO DO CADASTRO:")
    print(f"✅ Poltronas cadastradas: {total_cadastradas}")
    print(f"🔄 Poltronas atualizadas: {total_atualizadas}")
    print(f"❌ Erros: {total_erros}")
    print(f"📊 Total processadas: {total_cadastradas + total_atualizadas + total_erros}")
    print("-" * 60)

def associar_imagens():
    """Associar imagens às poltronas cadastradas."""
    
    # Mapeamento de referências para arquivos de imagem
    imagens_map = {
        'PL243': 'pl243.png',
        'PL246': 'pl246.png', 
        'PL105': 'pl105.png',
        'PL869': 'pl869.png',
        'PL97': 'pl97.png',
        'PL32': 'pl92.png',  # Referência PL32 usa imagem pl92.png
        'PL214': 'pl214.png',
        'PL53': 'pl53.png',
        'PL134': 'pl134.png',
        'PL988': 'pl988.jpg',
        'PL273': 'pl273.png',
        'PL287': 'pl287.png',
        'PL232/2B': 'pl232 2b.png',
        'PL232/1B': 'pl232 1b.png',
        'PL232/SB': 'pl232 sb.png',
        'PL232': 'pl232.png',
        'ME232': 'me232.jpg',
        'PL25': 'pl25.png',
        'PL915': 'pl915.png',
        'LE COULTHE': 'le coultre.jpg',
        'LUXOR': 'luxor.jpg',
        'MALIBU': 'malibu.jpg',
        'PL244': 'pl244.png',
        'PL239': 'pl239.png',
        'PL22': 'pl22.png',
        'RIALTO': 'rialto.jpg',
        'TIFFANY': 'tiffany.jpg',
        'VERSACE': 'versace.jpg',
        'PL225': 'pl225.png',
        'PL238': 'pl238.png',
        'PL262': 'pl262.png',
        'PL274': 'pl274.png',
    }
    
    total_associadas = 0
    total_nao_encontradas = 0
    
    print("\n🖼️  Iniciando associação de imagens...")
    print(f"📊 Total de mapeamentos de imagem: {len(imagens_map)}")
    print("-" * 60)
    
    for poltrona in Poltrona.objects.all():
        if poltrona.ref_poltrona in imagens_map:
            nome_imagem = imagens_map[poltrona.ref_poltrona]
            caminho_imagem = f'produtos/poltronas/{nome_imagem}'
            
            # Verificar se o arquivo existe
            caminho_completo = f'/home/matas/projetos/Project/media/{caminho_imagem}'
            if os.path.exists(caminho_completo):
                poltrona.imagem_principal = caminho_imagem
                poltrona.save()
                print(f"🖼️  Imagem associada: {poltrona.ref_poltrona} -> {nome_imagem}")
                total_associadas += 1
            else:
                print(f"⚠️  Arquivo não encontrado: {caminho_completo}")
                total_nao_encontradas += 1
        else:
            print(f"❓ Sem mapeamento de imagem para: {poltrona.ref_poltrona}")
            total_nao_encontradas += 1
    
    print("-" * 60)
    print("📈 RESUMO DA ASSOCIAÇÃO DE IMAGENS:")
    print(f"🖼️  Imagens associadas: {total_associadas}")
    print(f"❓ Imagens não encontradas: {total_nao_encontradas}")
    print("-" * 60)

def main():
    """Função principal do script."""
    print("=" * 60)
    print("🪑 SCRIPT DE CADASTRO DE POLTRONAS")
    print("📅 Sistema de Produtos - Julho 2025")
    print("=" * 60)
    
    try:
        # Etapa 1: Cadastrar poltronas
        cadastrar_poltronas()
        
        # Etapa 2: Associar imagens
        associar_imagens()
        
        print("\n🎉 PROCESSO FINALIZADO COM SUCESSO!")
        print("✅ Todas as poltronas foram processadas.")
        print("🔗 Verifique a listagem em: /produtos/ ou /poltronas/")
        
    except Exception as e:
        print(f"\n💥 ERRO CRÍTICO: {str(e)}")
        print("❌ O processo foi interrompido.")
        return 1
    
    return 0

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
