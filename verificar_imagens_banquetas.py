#!/usr/bin/env python
"""
Script para verificar imagens das banquetas
"""
import os
import sys
import django

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema_produtos.settings')
django.setup()

from produtos.models import Banqueta

print('=== VERIFICAÇÃO DE IMAGENS DAS BANQUETAS ===')
banquetas = Banqueta.objects.all()

for b in banquetas:
    print(f'Banqueta {b.ref_banqueta} - {b.nome}:')
    if b.imagem_principal:
        print(f'  ✅ Imagem Principal: {b.imagem_principal}')
        print(f'      URL: {b.imagem_principal.url}')
    else:
        print(f'  ❌ Imagem Principal: Não tem')
        
    if b.imagem_secundaria:
        print(f'  ✅ Imagem Secundária: {b.imagem_secundaria}')  
        print(f'      URL: {b.imagem_secundaria.url}')
    else:
        print(f'  ❌ Imagem Secundária: Não tem')
    print()
