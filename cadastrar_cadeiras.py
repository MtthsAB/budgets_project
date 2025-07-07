#!/usr/bin/env python
"""
Script para cadastrar cadeiras no banco de dados baseado na tabela fornecida.
"""
import os
import sys
import django
from decimal import Decimal

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema_produtos.settings')
django.setup()

from produtos.models import Cadeira

def cadastrar_cadeiras():
    """Cadastra todas as cadeiras da tabela no banco de dados"""
    
    # Dados extraídos da tabela na imagem
    cadeiras_dados = [
        {
            'ref_cadeira': 'CD001',
            'nome': 'EVA',
            'largura': Decimal('48'),
            'profundidade': Decimal('65'),
            'altura': Decimal('97'),
            'tecido_metros': Decimal('1.30'),
            'volume_m3': Decimal('0.40'),
            'peso_kg': Decimal('8'),
            'preco': Decimal('857'),
        },
        {
            'ref_cadeira': 'CD24',
            'nome': 'EVA BR',
            'largura': Decimal('73'),
            'profundidade': Decimal('65'),
            'altura': Decimal('97'),
            'tecido_metros': Decimal('2.30'),
            'volume_m3': Decimal('0.48'),
            'peso_kg': Decimal('11'),
            'preco': Decimal('1033'),
        },
        {
            'ref_cadeira': 'CD267',
            'nome': 'FIT',
            'largura': Decimal('47'),
            'profundidade': Decimal('58'),
            'altura': Decimal('89'),
            'tecido_metros': Decimal('1.30'),
            'volume_m3': Decimal('0.33'),
            'peso_kg': Decimal('7'),
            'preco': Decimal('520'),
        },
        {
            'ref_cadeira': 'CD74AC15',
            'nome': 'FIT GIRATÓRIA',
            'largura': Decimal('47'),
            'profundidade': Decimal('58'),
            'altura': Decimal('89'),
            'tecido_metros': Decimal('1.30'),
            'volume_m3': Decimal('0.33'),
            'peso_kg': Decimal('7'),
            'preco': Decimal('543'),
        },
        {
            'ref_cadeira': 'CD210',
            'nome': 'KIA',
            'largura': Decimal('44'),
            'profundidade': Decimal('61'),
            'altura': Decimal('98'),
            'tecido_metros': Decimal('1.20'),
            'volume_m3': Decimal('0.32'),
            'peso_kg': Decimal('6'),
            'preco': Decimal('357'),
        },
        {
            'ref_cadeira': 'CD120',
            'nome': 'MIA',
            'largura': Decimal('55'),
            'profundidade': Decimal('65'),
            'altura': Decimal('98'),
            'tecido_metros': Decimal('1.50'),
            'volume_m3': Decimal('0.50'),
            'peso_kg': Decimal('8'),
            'preco': Decimal('713'),
        },
        {
            'ref_cadeira': 'CD120BR',
            'nome': 'MIA BR',
            'largura': Decimal('55'),
            'profundidade': Decimal('65'),
            'altura': Decimal('98'),
            'tecido_metros': Decimal('2.20'),
            'volume_m3': Decimal('0.37'),
            'peso_kg': Decimal('9'),
            'preco': Decimal('698'),
        },
        {
            'ref_cadeira': 'CD236',
            'nome': 'NEO',
            'largura': Decimal('52'),
            'profundidade': Decimal('60'),
            'altura': Decimal('86'),
            'tecido_metros': Decimal('1.50'),
            'volume_m3': Decimal('0.43'),
            'peso_kg': Decimal('7'),
            'preco': Decimal('577'),
        },
        {
            'ref_cadeira': 'CD236BR',
            'nome': 'NEO BR',
            'largura': Decimal('55'),
            'profundidade': Decimal('65'),
            'altura': Decimal('88'),
            'tecido_metros': Decimal('1.80'),
            'volume_m3': Decimal('0.33'),
            'peso_kg': Decimal('8'),
            'preco': Decimal('594'),
        },
        {
            'ref_cadeira': 'CD80',
            'nome': 'NET',
            'largura': Decimal('48'),
            'profundidade': Decimal('67'),
            'altura': Decimal('92'),
            'tecido_metros': Decimal('1.50'),
            'volume_m3': Decimal('0.44'),
            'peso_kg': Decimal('7'),
            'preco': Decimal('758'),
        },
        {
            'ref_cadeira': 'CD80BR',
            'nome': 'NET BR',
            'largura': Decimal('60'),
            'profundidade': Decimal('67'),
            'altura': Decimal('92'),
            'tecido_metros': Decimal('2.50'),
            'volume_m3': Decimal('0.33'),
            'peso_kg': Decimal('8'),
            'preco': Decimal('871'),
        },
    ]
    
    cadeiras_criadas = 0
    cadeiras_atualizadas = 0
    
    for dados in cadeiras_dados:
        ref_cadeira = dados['ref_cadeira']
        
        # Verificar se a cadeira já existe
        cadeira, criada = Cadeira.objects.get_or_create(
            ref_cadeira=ref_cadeira,
            defaults=dados
        )
        
        if criada:
            cadeiras_criadas += 1
            print(f"✓ Cadeira {ref_cadeira} - {dados['nome']} criada com sucesso!")
        else:
            # Atualizar os dados se a cadeira já existir
            for campo, valor in dados.items():
                if campo != 'ref_cadeira':  # Não atualizar a referência
                    setattr(cadeira, campo, valor)
            cadeira.save()
            cadeiras_atualizadas += 1
            print(f"⚠ Cadeira {ref_cadeira} - {dados['nome']} já existia e foi atualizada!")
    
    print(f"\n📊 Resumo:")
    print(f"   • Cadeiras criadas: {cadeiras_criadas}")
    print(f"   • Cadeiras atualizadas: {cadeiras_atualizadas}")
    print(f"   • Total de cadeiras processadas: {len(cadeiras_dados)}")
    
    return cadeiras_criadas, cadeiras_atualizadas

def associar_imagens():
    """Associa as imagens das cadeiras baseado na referência"""
    
    cadeiras_com_imagem = 0
    cadeiras_sem_imagem = 0
    
    # Mapear as imagens existentes com as referências
    imagens_map = {
        'CD001': 'cd01.png',
        'CD24': 'cd24.png', 
        'CD267': 'cd267.png',
        'CD74AC15': 'cd74-ac15.png',
        'CD210': 'cd210.png',
        'CD120': 'cd120.png',
        'CD120BR': 'cd120-br.png',
        'CD236': 'cd236.png',
        'CD236BR': 'cd236 br.png',
        'CD80': 'cd80.png',
        'CD80BR': 'cd80 br.png',
    }
    
    for cadeira in Cadeira.objects.all():
        ref = cadeira.ref_cadeira
        
        if ref in imagens_map:
            nome_imagem = imagens_map[ref]
            caminho_imagem = f'produtos/cadeiras/{nome_imagem}'
            
            # Verificar se o arquivo existe no sistema de arquivos
            caminho_completo = f'media/{caminho_imagem}'
            if os.path.exists(caminho_completo):
                cadeira.imagem_principal = caminho_imagem
                cadeira.save()
                cadeiras_com_imagem += 1
                print(f"✓ Imagem associada para {ref}: {nome_imagem}")
            else:
                cadeiras_sem_imagem += 1
                print(f"⚠ Imagem não encontrada para {ref}: {nome_imagem}")
        else:
            cadeiras_sem_imagem += 1
            print(f"❌ Nenhuma imagem mapeada para {ref}")
    
    print(f"\n🖼️  Resumo das imagens:")
    print(f"   • Cadeiras com imagem: {cadeiras_com_imagem}")
    print(f"   • Cadeiras sem imagem: {cadeiras_sem_imagem}")
    
    return cadeiras_com_imagem, cadeiras_sem_imagem

if __name__ == '__main__':
    print("🪑 Iniciando cadastro das cadeiras...")
    print("=" * 50)
    
    try:
        # Cadastrar as cadeiras
        criadas, atualizadas = cadastrar_cadeiras()
        
        print("\n" + "=" * 50)
        print("🖼️ Associando imagens...")
        
        # Associar as imagens
        com_imagem, sem_imagem = associar_imagens()
        
        print("\n" + "=" * 50)
        print("✅ Processo concluído com sucesso!")
        
        if sem_imagem > 0:
            print(f"\n⚠️  Atenção: {sem_imagem} cadeiras ficaram sem imagem.")
            print("   Verifique se os arquivos existem na pasta media/produtos/cadeiras/")
        
    except Exception as e:
        print(f"\n❌ Erro durante o processo: {e}")
        sys.exit(1)
