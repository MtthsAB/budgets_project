#!/usr/bin/env python
"""
Script para cadastrar uma banqueta de teste no banco de dados.
"""
import os
import sys
import django
from decimal import Decimal

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema_produtos.settings')
django.setup()

from produtos.models import Banqueta

def cadastrar_banqueta_teste():
    """Cadastra uma banqueta de teste no banco de dados"""
    print("🪑 Cadastrando banqueta de teste...")
    
    # Dados da banqueta de teste
    dados_banqueta = {
        'ref_banqueta': 'BQ001',
        'nome': 'BANQUETA TESTE',
        'largura': Decimal('45.00'),
        'profundidade': Decimal('35.00'),
        'altura': Decimal('45.00'),
        'tecido_metros': Decimal('0.80'),
        'volume_m3': Decimal('0.071'),
        'peso_kg': Decimal('5.50'),
        'preco': Decimal('450.00'),
        'ativo': True,
        'descricao': 'Banqueta de teste para validação da página de visualização. Design moderno e confortável.'
    }
    
    try:
        # Verificar se a banqueta já existe
        banqueta, criada = Banqueta.objects.get_or_create(
            ref_banqueta=dados_banqueta['ref_banqueta'],
            defaults=dados_banqueta
        )
        
        if criada:
            print(f"✅ Banqueta {dados_banqueta['ref_banqueta']} - {dados_banqueta['nome']} criada com sucesso!")
            print(f"   🆔 ID: {banqueta.id}")
            print(f"   📏 Dimensões: {banqueta.largura} x {banqueta.profundidade} x {banqueta.altura} cm")
            print(f"   💰 Preço: R$ {banqueta.preco}")
            print(f"   🔗 URL de visualização: http://127.0.0.1:8000/banquetas/{banqueta.id}/")
        else:
            print(f"⚠️ Banqueta {dados_banqueta['ref_banqueta']} já existia!")
            print(f"   🆔 ID: {banqueta.id}")
            print(f"   🔗 URL de visualização: http://127.0.0.1:8000/banquetas/{banqueta.id}/")
        
        return banqueta
        
    except Exception as e:
        print(f"❌ Erro ao cadastrar banqueta: {str(e)}")
        return None

def main():
    print("🚀 Iniciando cadastro de banqueta de teste...")
    print("=" * 50)
    
    banqueta = cadastrar_banqueta_teste()
    
    if banqueta:
        print("\n" + "=" * 50)
        print("✅ Cadastro concluído com sucesso!")
        print(f"🌐 Acesse: http://127.0.0.1:8000/banquetas/{banqueta.id}/")
        print(f"📋 Lista de produtos: http://127.0.0.1:8000/produtos/")
        print("=" * 50)
    else:
        print("\n❌ Falha no cadastro.")
        sys.exit(1)

if __name__ == '__main__':
    main()
