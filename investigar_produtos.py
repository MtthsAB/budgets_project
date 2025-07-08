#!/usr/bin/env python
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema_produtos.settings')
django.setup()

from produtos.models import Produto, TipoItem, Cadeira, Banqueta, Poltrona

print('=== INVESTIGANDO PRODUTOS ===')

print('Total na tabela Produto:', Produto.objects.count())
print('Total na tabela Cadeira:', Cadeira.objects.count())
print('Total na tabela Banqueta:', Banqueta.objects.count())
print('Total na tabela Poltrona:', Poltrona.objects.count())

print('\nCadeiras:')
for cadeira in Cadeira.objects.all()[:5]:
    print(f'  - {cadeira.nome} (Ref: {cadeira.ref_cadeira})')

print('\nBanquetas:')
for banqueta in Banqueta.objects.all()[:5]:
    print(f'  - {banqueta.nome} (Ref: {banqueta.ref_banqueta})')

print('\nPoltronas:')
for poltrona in Poltrona.objects.all()[:5]:
    print(f'  - {poltrona.nome} (Ref: {poltrona.ref_poltrona})')
