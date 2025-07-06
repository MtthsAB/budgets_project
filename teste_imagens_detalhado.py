#!/usr/bin/env python3

import os
import sys
import django

# Configurar Django
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(BASE_DIR)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema_produtos.settings')
django.setup()

from produtos.models import Banqueta
from django.conf import settings

def teste_imagens():
    print("=== TESTE DE IMAGENS DAS BANQUETAS ===\n")
    
    banquetas = Banqueta.objects.filter(imagem_principal__isnull=False)
    print(f"Banquetas com imagem principal: {banquetas.count()}\n")
    
    for banqueta in banquetas[:3]:
        print(f"--- {banqueta.ref_banqueta} - {banqueta.nome} ---")
        print(f"ID: {banqueta.id}")
        
        if banqueta.imagem_principal:
            print(f"Campo imagem_principal: '{banqueta.imagem_principal}'")
            print(f"URL da imagem: '{banqueta.imagem_principal.url}'")
            print(f"Path da imagem: '{banqueta.imagem_principal.path}'")
            print(f"Arquivo existe: {os.path.exists(banqueta.imagem_principal.path)}")
            
            # Construir URL completa
            url_completa = f"http://localhost:8000{banqueta.imagem_principal.url}"
            print(f"URL completa: {url_completa}")
            
            # Testar se consegue abrir o arquivo
            try:
                with open(banqueta.imagem_principal.path, 'rb') as f:
                    size = len(f.read())
                    print(f"Tamanho do arquivo: {size} bytes")
            except Exception as e:
                print(f"Erro ao abrir arquivo: {e}")
        
        print()

if __name__ == "__main__":
    teste_imagens()
