#!/usr/bin/env python
import os
import sys
import django

# Configurar Django
sys.path.append('/home/matas/projetos/Project')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema_produtos.settings')
django.setup()

from produtos.models import TipoItem, Item, Banqueta

print('=== TIPOS DE ITEM ===')
for tipo in TipoItem.objects.all():
    print(f'- {tipo.id}: {tipo.nome}')

print(f'\n=== PRODUTOS (ITEM) ===')
print(f'Total de produtos: {Item.objects.count()}')
for item in Item.objects.all()[:3]:
    print(f'- {item.ref_produto}: {item.nome_produto} (Tipo: {item.id_tipo_produto.nome})')

print(f'\n=== BANQUETAS ===')
print(f'Total de banquetas: {Banqueta.objects.count()}')
for banqueta in Banqueta.objects.all()[:3]:
    print(f'- {banqueta.ref_banqueta}: {banqueta.nome} (R$ {banqueta.preco})')
