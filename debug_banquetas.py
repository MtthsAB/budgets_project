#!/usr/bin/env python3

import os
import sys
import django

# Configurar o path do Django
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(BASE_DIR)

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema_produtos.settings')
django.setup()

from produtos.models import Banqueta

try:
    banquetas = Banqueta.objects.all()
    print(f"Total de banquetas: {banquetas.count()}")
    
    for banqueta in banquetas[:3]:
        print(f"\n--- {banqueta.ref_banqueta} - {banqueta.nome} ---")
        print(f"ID: {banqueta.id}")
        print(f"Imagem Principal: '{banqueta.imagem_principal}'")
        print(f"Imagem Secundária: '{banqueta.imagem_secundaria}'")
        
        if banqueta.imagem_principal:
            print(f"URL Principal: {banqueta.imagem_principal.url}")
        if banqueta.imagem_secundaria:
            print(f"URL Secundária: {banqueta.imagem_secundaria.url}")
            
except Exception as e:
    print(f"Erro: {e}")
    import traceback
    traceback.print_exc()
