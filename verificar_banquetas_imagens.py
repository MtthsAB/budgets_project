#!/usr/bin/env python3
"""
Script para verificar banquetas e suas imagens
"""

import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema_produtos.settings')
django.setup()

from produtos.models import Banqueta

def main():
    print("=== VERIFICAÇÃO DE BANQUETAS E IMAGENS ===\n")
    
    banquetas = Banqueta.objects.all()
    print(f"Total de banquetas: {banquetas.count()}\n")
    
    if banquetas.count() == 0:
        print("❌ Nenhuma banqueta encontrada no banco de dados!")
        return
    
    for i, banqueta in enumerate(banquetas[:5], 1):
        print(f"--- Banqueta {i} ---")
        print(f"ID: {banqueta.id}")
        print(f"Referência: {banqueta.ref_banqueta}")
        print(f"Nome: {banqueta.nome}")
        print(f"Ativo: {banqueta.ativo}")
        
        # Verificar imagem principal
        if banqueta.imagem_principal:
            print(f"✅ Imagem Principal: {banqueta.imagem_principal}")
            print(f"   URL: {banqueta.imagem_principal.url}")
            print(f"   Path: {banqueta.imagem_principal.path}")
            print(f"   Existe: {os.path.exists(banqueta.imagem_principal.path)}")
        else:
            print("❌ Imagem Principal: Não definida")
        
        # Verificar imagem secundária
        if banqueta.imagem_secundaria:
            print(f"✅ Imagem Secundária: {banqueta.imagem_secundaria}")
            print(f"   URL: {banqueta.imagem_secundaria.url}")
            print(f"   Path: {banqueta.imagem_secundaria.path}")
            print(f"   Existe: {os.path.exists(banqueta.imagem_secundaria.path)}")
        else:
            print("❌ Imagem Secundária: Não definida")
        
        print()
    
    # Verificar configurações de media
    from django.conf import settings
    print("=== CONFIGURAÇÕES DE MEDIA ===")
    print(f"MEDIA_URL: {settings.MEDIA_URL}")
    print(f"MEDIA_ROOT: {settings.MEDIA_ROOT}")
    print(f"MEDIA_ROOT existe: {os.path.exists(settings.MEDIA_ROOT)}")
    
    # Verificar diretório de banquetas
    banquetas_dir = os.path.join(settings.MEDIA_ROOT, 'produtos', 'banquetas')
    print(f"Diretório banquetas: {banquetas_dir}")
    print(f"Diretório banquetas existe: {os.path.exists(banquetas_dir)}")
    
    if os.path.exists(banquetas_dir):
        arquivos = os.listdir(banquetas_dir)
        print(f"Arquivos no diretório: {len(arquivos)}")
        for arquivo in arquivos[:5]:
            print(f"  - {arquivo}")

if __name__ == "__main__":
    main()
