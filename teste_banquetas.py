#!/usr/bin/env python
import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema_produtos.settings')
sys.path.append('/home/matas/projetos/Project')
django.setup()

from produtos.models import Banqueta

def teste_banquetas():
    print("=== TESTE DE BANQUETAS ===")
    
    # Verificar se o modelo existe e funciona
    print(f"Total de banquetas: {Banqueta.objects.count()}")
    
    # Criar banquetas de teste baseadas na imagem anexada
    banquetas_teste = [
        {
            'ref_banqueta': 'BQ13',
            'nome': 'CERES',
            'largura': 42.50,
            'profundidade': 50.99,
            'altura': 99.00,
            'tecido_metros': 0.90,
            'volume_m3': 0.24,
            'peso_kg': 8.0,
            'preco': 658.00,
            'descricao': 'Banqueta CERES - BQ13'
        },
        {
            'ref_banqueta': 'BQ249',
            'nome': 'GIO',
            'largura': 44.50,
            'profundidade': 50.99,
            'altura': 99.00,
            'tecido_metros': 1.70,
            'volume_m3': 0.30,
            'peso_kg': 8.0,
            'preco': 908.00,
            'descricao': 'Banqueta GIO - BQ249'
        },
        {
            'ref_banqueta': 'BQ278',
            'nome': 'GIRATÓRIA',
            'largura': 55.50,
            'profundidade': 50.00,
            'altura': 100.00,
            'tecido_metros': 1.70,
            'volume_m3': 0.30,
            'peso_kg': 8.0,
            'preco': 908.00,
            'descricao': 'Banqueta GIRATÓRIA - BQ278'
        }
    ]
    
    print("\nCriando banquetas de teste...")
    for dados in banquetas_teste:
        try:
            # Verificar se já existe
            if not Banqueta.objects.filter(ref_banqueta=dados['ref_banqueta']).exists():
                banqueta = Banqueta.objects.create(**dados)
                print(f"✅ Criada: {banqueta}")
            else:
                print(f"⚠️  Já existe: {dados['ref_banqueta']}")
        except Exception as e:
            print(f"❌ Erro ao criar {dados['ref_banqueta']}: {e}")
    
    print(f"\nTotal de banquetas após criação: {Banqueta.objects.count()}")
    
    # Listar todas as banquetas
    print("\n=== BANQUETAS CADASTRADAS ===")
    for banqueta in Banqueta.objects.all():
        print(f"- {banqueta.ref_banqueta}: {banqueta.nome}")
        print(f"  Dimensões: {banqueta.get_dimensoes_formatadas()} cm")
        print(f"  Preço: R$ {banqueta.preco}")
        print(f"  Status: {'Ativo' if banqueta.ativo else 'Inativo'}")
        print()

if __name__ == '__main__':
    teste_banquetas()
