#!/usr/bin/env python
"""
Script para cadastrar banquetas completas conforme tabela anexada
"""
import os
import sys
import django
from decimal import Decimal

# Configurar Django
sys.path.append('/home/matas/projetos/Project')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema_produtos.settings')
django.setup()

from produtos.models import Banqueta

def cadastrar_banquetas():
    """
    Cadastra todas as banquetas conforme tabela anexada
    """
    
    # Dados das banquetas conforme tabela anexada
    banquetas_dados = [
        {
            'ref_banqueta': 'BQ13',
            'nome': 'CERES',
            'largura': Decimal('42'),
            'profundidade': Decimal('50'), 
            'altura': Decimal('39'),
            'tecido_metros': Decimal('0.80'),
            'volume_m3': Decimal('0.24'),
            'peso_kg': Decimal('8'),
            'preco': Decimal('658'),
            'imagem_nome': 'BQ13.png'
        },
        {
            'ref_banqueta': 'BQ249',
            'nome': 'GIO',
            'largura': Decimal('44'),
            'profundidade': Decimal('50'),
            'altura': Decimal('39'),
            'tecido_metros': Decimal('1.70'),
            'volume_m3': Decimal('0.30'),
            'peso_kg': Decimal('8'),
            'preco': Decimal('908'),
            'imagem_nome': 'BQ249.png'
        },
        {
            'ref_banqueta': 'BQ278',
            'nome': 'GIO GIRATÓRIA',
            'largura': Decimal('55'),
            'profundidade': Decimal('50'),
            'altura': Decimal('100'),
            'tecido_metros': Decimal('1.70'),
            'volume_m3': Decimal('0.30'),
            'peso_kg': Decimal('8'),
            'preco': Decimal('908'),
            'imagem_nome': 'BQ278.png'
        },
        {
            'ref_banqueta': 'BQ250',
            'nome': 'IAN',
            'largura': Decimal('58'),
            'profundidade': Decimal('58'),
            'altura': Decimal('112'),
            'tecido_metros': Decimal('2.30'),
            'volume_m3': Decimal('0.38'),
            'peso_kg': Decimal('9'),
            'preco': Decimal('1065'),
            'imagem_nome': 'BQ250.png'
        },
        {
            'ref_banqueta': 'BQ251',
            'nome': 'MET',
            'largura': Decimal('43'),
            'profundidade': Decimal('50'),
            'altura': Decimal('39'),
            'tecido_metros': Decimal('1.30'),
            'volume_m3': Decimal('0.22'),
            'peso_kg': Decimal('8'),
            'preco': Decimal('988'),
            'imagem_nome': 'BQ251.png'
        },
        {
            'ref_banqueta': 'BQ254',
            'nome': 'VIC',
            'largura': Decimal('55'),
            'profundidade': Decimal('55'),
            'altura': Decimal('110'),
            'tecido_metros': Decimal('1.70'),
            'volume_m3': Decimal('0.33'),
            'peso_kg': Decimal('8'),
            'preco': Decimal('1019'),
            'imagem_nome': 'BQ254.png'
        },
        {
            'ref_banqueta': 'BQ273',
            'nome': 'VIC GIRATÓRIA COM REGULAGEM',
            'largura': Decimal('54'),
            'profundidade': Decimal('55'),
            'altura': Decimal('113'),
            'tecido_metros': Decimal('1.70'),
            'volume_m3': Decimal('0.33'),
            'peso_kg': Decimal('8'),
            'preco': Decimal('1019'),
            'imagem_nome': 'BQ273.png'
        }
    ]
    
    print("🪑 Iniciando cadastro das banquetas...")
    print("=" * 50)
    
    for banqueta_data in banquetas_dados:
        ref_banqueta = banqueta_data['ref_banqueta']
        
        try:
            # Verificar se a banqueta já existe
            banqueta, created = Banqueta.objects.get_or_create(
                ref_banqueta=ref_banqueta,
                defaults={
                    'nome': banqueta_data['nome'],
                    'largura': banqueta_data['largura'],
                    'profundidade': banqueta_data['profundidade'],
                    'altura': banqueta_data['altura'],
                    'tecido_metros': banqueta_data['tecido_metros'],
                    'volume_m3': banqueta_data['volume_m3'],
                    'peso_kg': banqueta_data['peso_kg'],
                    'preco': banqueta_data['preco'],
                    'ativo': True,
                    'descricao': f"Banqueta {banqueta_data['nome']} - Ref: {ref_banqueta}"
                }
            )
            
            if created:
                print(f"✅ {ref_banqueta} - {banqueta_data['nome']}: CRIADA")
                print(f"   📐 Dimensões: {banqueta_data['largura']}x{banqueta_data['profundidade']}x{banqueta_data['altura']} cm")
                print(f"   💰 Preço: R$ {banqueta_data['preco']}")
                print(f"   📦 Volume: {banqueta_data['volume_m3']} m³")
                print(f"   ⚖️  Peso: {banqueta_data['peso_kg']} kg")
            else:
                print(f"ℹ️  {ref_banqueta} - {banqueta_data['nome']}: JÁ EXISTE")
                
                # Atualizar dados caso necessário
                banqueta.nome = banqueta_data['nome']
                banqueta.largura = banqueta_data['largura']
                banqueta.profundidade = banqueta_data['profundidade']
                banqueta.altura = banqueta_data['altura']
                banqueta.tecido_metros = banqueta_data['tecido_metros']
                banqueta.volume_m3 = banqueta_data['volume_m3']
                banqueta.peso_kg = banqueta_data['peso_kg']
                banqueta.preco = banqueta_data['preco']
                banqueta.ativo = True
                banqueta.save()
                print(f"   🔄 Dados atualizados")
            
            print("-" * 30)
            
        except Exception as e:
            print(f"❌ Erro ao cadastrar {ref_banqueta}: {e}")
            print("-" * 30)
    
    # Relatório final
    total_banquetas = Banqueta.objects.count()
    banquetas_ativas = Banqueta.objects.filter(ativo=True).count()
    
    print("=" * 50)
    print("📊 RELATÓRIO FINAL:")
    print(f"   🪑 Total de banquetas: {total_banquetas}")
    print(f"   ✅ Banquetas ativas: {banquetas_ativas}")
    print("=" * 50)
    
    # Listar todas as banquetas cadastradas
    print("\n📋 BANQUETAS CADASTRADAS:")
    for banqueta in Banqueta.objects.all().order_by('ref_banqueta'):
        status = "✅ ATIVA" if banqueta.ativo else "❌ INATIVA"
        print(f"   {banqueta.ref_banqueta} - {banqueta.nome} ({status}) - R$ {banqueta.preco}")
    
    print("\n🎉 Cadastro concluído!")

if __name__ == "__main__":
    cadastrar_banquetas()
