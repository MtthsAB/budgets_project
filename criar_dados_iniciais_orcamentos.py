#!/usr/bin/env python
"""
Script para criar dados iniciais para o sistema de orçamentos
"""

import os
import sys
import django
from datetime import date, timedelta

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema_produtos.settings')
django.setup()

from orcamentos.models import FaixaPreco, FormaPagamento
from decimal import Decimal

def criar_faixas_preco():
    """Cria faixas de preço padrão"""
    
    faixas = [
        {
            'nome': 'Varejo',
            'descricao': 'Preço para venda ao consumidor final',
            'multiplicador': Decimal('1.00'),
            'ativo': True
        },
        {
            'nome': 'Atacado',
            'descricao': 'Preço para venda em grandes quantidades',
            'multiplicador': Decimal('0.85'),
            'ativo': True
        },
        {
            'nome': 'Promocional',
            'descricao': 'Preço promocional com desconto especial',
            'multiplicador': Decimal('0.75'),
            'ativo': True
        },
        {
            'nome': 'Distribuidor',
            'descricao': 'Preço para revendedores autorizados',
            'multiplicador': Decimal('0.70'),
            'ativo': True
        },
        {
            'nome': 'Especial',
            'descricao': 'Preço especial para clientes VIP',
            'multiplicador': Decimal('0.65'),
            'ativo': True
        }
    ]
    
    print("Criando faixas de preço...")
    for faixa_data in faixas:
        faixa, created = FaixaPreco.objects.get_or_create(
            nome=faixa_data['nome'],
            defaults=faixa_data
        )
        status = "criada" if created else "já existe"
        print(f"  - {faixa.nome}: {status}")
    
    print(f"Total de faixas de preço: {FaixaPreco.objects.count()}")

def criar_formas_pagamento():
    """Cria formas de pagamento padrão"""
    
    formas = [
        {
            'nome': 'À Vista',
            'descricao': 'Pagamento à vista com desconto',
            'prazo_dias': 0,
            'desconto_maximo': Decimal('5.00'),
            'ativo': True
        },
        {
            'nome': '30 DDL',
            'descricao': 'Pagamento em 30 dias da data de entrega',
            'prazo_dias': 30,
            'desconto_maximo': Decimal('2.00'),
            'ativo': True
        },
        {
            'nome': '60 DDL',
            'descricao': 'Pagamento em 60 dias da data de entrega',
            'prazo_dias': 60,
            'desconto_maximo': Decimal('0.00'),
            'ativo': True
        },
        {
            'nome': '90 DDL',
            'descricao': 'Pagamento em 90 dias da data de entrega',
            'prazo_dias': 90,
            'desconto_maximo': Decimal('0.00'),
            'ativo': True
        },
        {
            'nome': '2x sem juros',
            'descricao': 'Pagamento em 2 parcelas sem juros',
            'prazo_dias': 30,
            'desconto_maximo': Decimal('0.00'),
            'ativo': True
        },
        {
            'nome': '3x sem juros',
            'descricao': 'Pagamento em 3 parcelas sem juros',
            'prazo_dias': 60,
            'desconto_maximo': Decimal('0.00'),
            'ativo': True
        },
        {
            'nome': 'Boleto 15 dias',
            'descricao': 'Pagamento via boleto em 15 dias',
            'prazo_dias': 15,
            'desconto_maximo': Decimal('3.00'),
            'ativo': True
        },
        {
            'nome': 'PIX',
            'descricao': 'Pagamento via PIX com desconto',
            'prazo_dias': 0,
            'desconto_maximo': Decimal('7.00'),
            'ativo': True
        }
    ]
    
    print("Criando formas de pagamento...")
    for forma_data in formas:
        forma, created = FormaPagamento.objects.get_or_create(
            nome=forma_data['nome'],
            defaults=forma_data
        )
        status = "criada" if created else "já existe"
        print(f"  - {forma.nome}: {status}")
    
    print(f"Total de formas de pagamento: {FormaPagamento.objects.count()}")

def main():
    """Função principal"""
    print("="*50)
    print("SCRIPT DE DADOS INICIAIS - SISTEMA DE ORÇAMENTOS")
    print("="*50)
    
    try:
        criar_faixas_preco()
        print()
        criar_formas_pagamento()
        
        print()
        print("="*50)
        print("DADOS INICIAIS CRIADOS COM SUCESSO!")
        print("="*50)
        print()
        print("Próximos passos:")
        print("1. Acesse o sistema como Master/Admin")
        print("2. Vá para o menu 'Orçamentos' > 'Novo Orçamento'")
        print("3. Teste a criação de orçamentos")
        print("4. Verifique se os clientes estão cadastrados")
        print("5. Verifique se os produtos têm preços definidos")
        print()
        
    except Exception as e:
        print(f"Erro ao criar dados iniciais: {str(e)}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
