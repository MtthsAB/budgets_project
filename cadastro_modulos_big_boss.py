#!/usr/bin/env python
"""
Script para cadastrar os módulos do sofá BIG BOSS (SF982) no banco de dados
Baseado na tabela fornecida na imagem
"""

import os
import sys
import django
from decimal import Decimal

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema_produtos.settings')
django.setup()

from produtos.models import Item, Modulo, TamanhosModulosDetalhado

def cadastrar_modulos_big_boss():
    """Cadastra todos os módulos do BIG BOSS conforme a tabela da imagem"""
    
    # Buscar o produto BIG BOSS
    try:
        big_boss = Item.objects.get(ref_produto='SF982')
        print(f"✓ Produto encontrado: {big_boss.nome_produto} (ID: {big_boss.id})")
    except Item.DoesNotExist:
        print("❌ Produto BIG BOSS (SF982) não encontrado!")
        return False
    
    # Dados dos módulos conforme a imagem
    modulos_data = [
        {
            'nome': 'MOD 02 1LUGAR S/BR',
            'profundidade': Decimal('110.00'),
            'altura': Decimal('37.00'),
            'braco': Decimal('25.00'),
            'descricao': 'Com opção de automação\nProfundidade: 125 cm (aberto)',
            'tamanhos': [
                {
                    'largura_total': Decimal('120.00'),
                    'largura_assento': Decimal('120.00'),
                    'tecido_metros': Decimal('7.2'),
                    'volume_m3': Decimal('1.4'),
                    'peso_kg': Decimal('45.00'),
                    'preco': Decimal('2659.00')
                },
                {
                    'largura_total': Decimal('110.00'),
                    'largura_assento': Decimal('110.00'),
                    'tecido_metros': Decimal('6.8'),
                    'volume_m3': Decimal('1.3'),
                    'peso_kg': Decimal('43.00'),
                    'preco': Decimal('2501.00')
                },
                {
                    'largura_total': Decimal('100.00'),
                    'largura_assento': Decimal('100.00'),
                    'tecido_metros': Decimal('5.8'),
                    'volume_m3': Decimal('1.2'),
                    'peso_kg': Decimal('41.00'),
                    'preco': Decimal('2353.00')
                },
                {
                    'largura_total': Decimal('90.00'),
                    'largura_assento': Decimal('90.00'),
                    'tecido_metros': Decimal('5.4'),
                    'volume_m3': Decimal('1.1'),
                    'peso_kg': Decimal('39.00'),
                    'preco': Decimal('2212.00')
                }
            ]
        },
        {
            'nome': 'MOD 03 CHAISE',
            'profundidade': Decimal('157.00'),
            'altura': Decimal('37.00'),
            'braco': Decimal('25.00'),
            'descricao': 'Com opção de automação\nProfundidade: 172 cm (aberto)',
            'tamanhos': [
                {
                    'largura_total': Decimal('145.00'),
                    'largura_assento': Decimal('120.00'),
                    'tecido_metros': Decimal('9.0'),
                    'volume_m3': Decimal('2.3'),
                    'peso_kg': Decimal('70.00'),
                    'preco': Decimal('3575.00')
                },
                {
                    'largura_total': Decimal('135.00'),
                    'largura_assento': Decimal('110.00'),
                    'tecido_metros': Decimal('8.6'),
                    'volume_m3': Decimal('2.2'),
                    'peso_kg': Decimal('68.00'),
                    'preco': Decimal('3363.00')
                },
                {
                    'largura_total': Decimal('125.00'),
                    'largura_assento': Decimal('100.00'),
                    'tecido_metros': Decimal('8.4'),
                    'volume_m3': Decimal('2.1'),
                    'peso_kg': Decimal('65.00'),
                    'preco': Decimal('3163.00')
                },
                {
                    'largura_total': Decimal('115.00'),
                    'largura_assento': Decimal('90.00'),
                    'tecido_metros': Decimal('7.7'),
                    'volume_m3': Decimal('2.0'),
                    'peso_kg': Decimal('60.00'),
                    'preco': Decimal('2974.00')
                }
            ]
        },
        {
            'nome': 'MOD 05 AUXILIAR',
            'profundidade': Decimal('107.00'),
            'altura': Decimal('45.00'),
            'braco': None,
            'descricao': 'Acessórios Opcionais:\nTorre Usb\nLuminária\nCarregador Indução',
            'tamanhos': [
                {
                    'largura_total': Decimal('44.00'),
                    'largura_assento': Decimal('107.00'),
                    'tecido_metros': Decimal('2.3'),
                    'volume_m3': Decimal('0.6'),
                    'peso_kg': Decimal('30.00'),
                    'preco': Decimal('1169.00')
                }
            ]
        },
        {
            'nome': 'MOD 06 PUFE',
            'profundidade': Decimal('63.00'),
            'altura': Decimal('45.00'),
            'braco': None,
            'descricao': '',
            'tamanhos': [
                {
                    'largura_total': Decimal('120.00'),
                    'largura_assento': Decimal('63.00'),
                    'tecido_metros': Decimal('3.0'),
                    'volume_m3': Decimal('0.6'),
                    'peso_kg': Decimal('35.00'),
                    'preco': Decimal('1164.00')
                },
                {
                    'largura_total': Decimal('110.00'),
                    'largura_assento': Decimal('63.00'),
                    'tecido_metros': Decimal('2.8'),
                    'volume_m3': Decimal('0.5'),
                    'peso_kg': Decimal('33.00'),
                    'preco': Decimal('1095.00')
                },
                {
                    'largura_total': Decimal('100.00'),
                    'largura_assento': Decimal('63.00'),
                    'tecido_metros': Decimal('2.5'),
                    'volume_m3': Decimal('0.4'),
                    'peso_kg': Decimal('30.00'),
                    'preco': Decimal('1029.00')
                },
                {
                    'largura_total': Decimal('90.00'),
                    'largura_assento': Decimal('63.00'),
                    'tecido_metros': Decimal('2.3'),
                    'volume_m3': Decimal('0.3'),
                    'peso_kg': Decimal('28.00'),
                    'preco': Decimal('968.00')
                }
            ]
        }
    ]
    
    print(f"\n🚀 Iniciando cadastro de {len(modulos_data)} módulos...")
    
    total_modulos = 0
    total_tamanhos = 0
    
    for modulo_data in modulos_data:
        print(f"\n📦 Cadastrando módulo: {modulo_data['nome']}")
        
        # Verificar se o módulo já existe
        modulo_existente = Modulo.objects.filter(
            item=big_boss,
            nome=modulo_data['nome']
        ).first()
        
        if modulo_existente:
            print(f"   ⚠️  Módulo já existe (ID: {modulo_existente.id}). Atualizando...")
            modulo = modulo_existente
        else:
            # Criar novo módulo
            modulo = Modulo()
            print(f"   ✨ Criando novo módulo...")
        
        # Configurar dados do módulo
        modulo.item = big_boss
        modulo.nome = modulo_data['nome']
        modulo.profundidade = modulo_data['profundidade']
        modulo.altura = modulo_data['altura']
        modulo.braco = modulo_data['braco']
        modulo.descricao = modulo_data['descricao']
        modulo.save()
        
        total_modulos += 1
        print(f"   ✓ Módulo salvo (ID: {modulo.id})")
        
        # Cadastrar tamanhos detalhados
        print(f"   📏 Cadastrando {len(modulo_data['tamanhos'])} variações de tamanho...")
        
        for i, tamanho_data in enumerate(modulo_data['tamanhos'], 1):
            # Verificar se já existe um tamanho similar
            tamanho_existente = TamanhosModulosDetalhado.objects.filter(
                id_modulo=modulo,
                largura_total=tamanho_data['largura_total'],
                largura_assento=tamanho_data['largura_assento']
            ).first()
            
            if tamanho_existente:
                print(f"      ⚠️  Tamanho {i} já existe. Atualizando...")
                tamanho = tamanho_existente
            else:
                print(f"      ✨ Criando tamanho {i}...")
                tamanho = TamanhosModulosDetalhado()
            
            # Configurar dados do tamanho
            tamanho.id_modulo = modulo
            tamanho.largura_total = tamanho_data['largura_total']
            tamanho.largura_assento = tamanho_data['largura_assento']
            tamanho.tecido_metros = tamanho_data['tecido_metros']
            tamanho.volume_m3 = tamanho_data['volume_m3']
            tamanho.peso_kg = tamanho_data['peso_kg']
            tamanho.preco = tamanho_data['preco']
            tamanho.save()
            
            total_tamanhos += 1
            print(f"         ✓ Tamanho salvo: {tamanho_data['largura_total']}x{tamanho_data['largura_assento']}cm - R${tamanho_data['preco']}")
    
    print(f"\n🎉 Cadastro concluído com sucesso!")
    print(f"   📦 Total de módulos processados: {total_modulos}")
    print(f"   📏 Total de variações de tamanho: {total_tamanhos}")
    
    # Validação final
    print(f"\n🔍 Validação final:")
    modulos_cadastrados = Modulo.objects.filter(item=big_boss)
    print(f"   • Módulos no banco para BIG BOSS: {modulos_cadastrados.count()}")
    
    for modulo in modulos_cadastrados:
        tamanhos_count = TamanhosModulosDetalhado.objects.filter(id_modulo=modulo).count()
        print(f"     - {modulo.nome}: {tamanhos_count} variações")
    
    return True

if __name__ == '__main__':
    print("=" * 60)
    print("CADASTRO DE MÓDULOS - SOFÁ BIG BOSS (SF982)")
    print("=" * 60)
    
    success = cadastrar_modulos_big_boss()
    
    if success:
        print(f"\n✅ Processo finalizado com sucesso!")
    else:
        print(f"\n❌ Processo finalizado com erros!")
        sys.exit(1)
