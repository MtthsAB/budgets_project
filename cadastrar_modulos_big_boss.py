#!/usr/bin/env python3
"""
Script para cadastrar os módulos do BIG BOSS conforme a tabela da imagem anexa.

Módulos a cadastrar:
- MOD 07 CANTO (110x110cm, 8.5m tecido, 1.4m³, 50kg, R$ 2.249)
- MOD 08 PUFE TERMINAL (60x110cm, 2.6m tecido, 0.4m³, 28kg, R$ 968)
"""

import os
import django
import sys
from decimal import Decimal

# Configurar Django
sys.path.append('/home/matas/projetos/Project')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema_produtos.settings')
django.setup()

from produtos.models import Item, Modulo, TamanhosModulosDetalhado

def cadastrar_modulos_big_boss():
    """Cadastra os módulos MOD 07 e MOD 08 para o produto BIG BOSS"""
    
    print("🔍 CADASTRANDO MÓDULOS DO BIG BOSS")
    print("=" * 60)
    
    # Buscar o produto BIG BOSS
    try:
        produto = Item.objects.get(ref_produto='SF982', nome_produto='Big Boss')
        print(f"✅ Produto encontrado: {produto.nome_produto} (ID: {produto.id})")
    except Item.DoesNotExist:
        print("❌ Produto BIG BOSS (SF982) não encontrado!")
        return
    
    # Dados dos módulos conforme a imagem
    modulos_dados = [
        {
            'nome': 'MOD 07 CANTO',
            'profundidade': 110.0,
            'altura': 37.0,
            'braco': None,  # Não especificado na imagem
            'descricao': 'Módulo de canto para composição',
            'tamanhos': [
                {
                    'largura_total': 110.0,
                    'largura_assento': 110.0,
                    'tecido_metros': 8.5,
                    'volume_m3': 1.4,
                    'peso_kg': 50.0,
                    'preco': 2249.0,
                    'descricao': 'Tamanho único para módulo de canto'
                }
            ]
        },
        {
            'nome': 'MOD 08 PUFE TERMINAL',
            'profundidade': 110.0,
            'altura': 45.0,
            'braco': None,  # Não especificado na imagem
            'descricao': 'Pufe terminal para finalização da composição',
            'tamanhos': [
                {
                    'largura_total': 60.0,
                    'largura_assento': 110.0,
                    'tecido_metros': 2.6,
                    'volume_m3': 0.4,
                    'peso_kg': 28.0,
                    'preco': 968.0,
                    'descricao': 'Tamanho único para pufe terminal'
                }
            ]
        }
    ]
    
    # Verificar se os módulos já existem
    modulos_existentes = produto.modulos.filter(
        nome__in=['MOD 07 CANTO', 'MOD 08 PUFE TERMINAL']
    )
    
    if modulos_existentes.exists():
        print("⚠️  Alguns módulos já existem:")
        for mod in modulos_existentes:
            print(f"   - {mod.nome}")
        
        resposta = input("Deseja sobrescrever? (s/N): ").lower()
        if resposta == 's':
            modulos_existentes.delete()
            print("🗑️  Módulos existentes removidos")
        else:
            print("❌ Operação cancelada")
            return
    
    # Cadastrar os novos módulos
    print("\n📦 Cadastrando módulos...")
    
    for modulo_data in modulos_dados:
        print(f"\n🔧 Criando módulo: {modulo_data['nome']}")
        
        # Criar o módulo
        modulo = Modulo.objects.create(
            item=produto,
            nome=modulo_data['nome'],
            profundidade=modulo_data['profundidade'],
            altura=modulo_data['altura'],
            braco=modulo_data['braco'],
            descricao=modulo_data['descricao']
        )
        
        print(f"   ✅ Módulo criado: ID {modulo.id}")
        
        # Cadastrar os tamanhos
        for tamanho_data in modulo_data['tamanhos']:
            tamanho = TamanhosModulosDetalhado.objects.create(
                id_modulo=modulo,
                largura_total=Decimal(str(tamanho_data['largura_total'])),
                largura_assento=Decimal(str(tamanho_data['largura_assento'])),
                tecido_metros=Decimal(str(tamanho_data['tecido_metros'])),
                volume_m3=Decimal(str(tamanho_data['volume_m3'])),
                peso_kg=Decimal(str(tamanho_data['peso_kg'])),
                preco=Decimal(str(tamanho_data['preco'])),
                descricao=tamanho_data['descricao']
            )
            
            print(f"   📏 Tamanho criado: {tamanho_data['largura_total']}x{tamanho_data['largura_assento']}cm - R$ {tamanho_data['preco']}")
    
    print("\n🎉 CADASTRO CONCLUÍDO!")
    print(f"📊 Total de módulos cadastrados: {len(modulos_dados)}")
    
    # Validar cadastro
    print("\n🔍 VALIDAÇÃO:")
    modulos_cadastrados = produto.modulos.filter(
        nome__in=['MOD 07 CANTO', 'MOD 08 PUFE TERMINAL']
    )
    
    for modulo in modulos_cadastrados:
        print(f"✅ {modulo.nome}")
        print(f"   📐 Dimensões: {modulo.profundidade}x{modulo.altura}cm")
        print(f"   📝 Descrição: {modulo.descricao}")
        
        tamanhos = modulo.tamanhos_detalhados.all()
        print(f"   📏 Tamanhos: {tamanhos.count()}")
        
        for tamanho in tamanhos:
            print(f"      • {tamanho.largura_total}x{tamanho.largura_assento}cm - {tamanho.tecido_metros}m tecido - R$ {tamanho.preco}")
    
    print(f"\n🌐 Acesse: http://localhost:8000/produtos/{produto.id}/editar/")
    print("Para visualizar os módulos cadastrados na interface de edição.")

if __name__ == "__main__":
    cadastrar_modulos_big_boss()
