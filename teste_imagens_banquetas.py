#!/usr/bin/env python
"""
Script para testar e corrigir imagens das banquetas
"""
import os
import sys
import django
from pathlib import Path

# Adicionar o diretório do projeto ao path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema_produtos.settings')
django.setup()

from produtos.models import Banqueta
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage

def teste_imagens_banquetas():
    """Testa o sistema de imagens das banquetas"""
    
    print("=== TESTE DO SISTEMA DE IMAGENS ===\n")
    
    # Verificar configurações
    print("📁 Diretório de mídia:", default_storage.location)
    
    # Verificar banquetas
    banquetas = Banqueta.objects.all()[:3]  # Primeiras 3 para teste
    
    for banqueta in banquetas:
        print(f"\n--- {banqueta.ref_banqueta} - {banqueta.nome} ---")
        
        if banqueta.imagem_principal:
            print(f"✅ Imagem principal: {banqueta.imagem_principal.name}")
            # Verificar se o arquivo existe
            if banqueta.imagem_principal and default_storage.exists(banqueta.imagem_principal.name):
                print(f"   ✅ Arquivo existe no sistema")
                print(f"   🌐 URL: {banqueta.imagem_principal.url}")
            else:
                print(f"   ❌ Arquivo não encontrado no sistema")
        else:
            print(f"❌ Sem imagem principal")
            
        if banqueta.imagem_secundaria:
            print(f"✅ Imagem secundária: {banqueta.imagem_secundaria.name}")
            # Verificar se o arquivo existe
            if banqueta.imagem_secundaria and default_storage.exists(banqueta.imagem_secundaria.name):
                print(f"   ✅ Arquivo existe no sistema")
                print(f"   🌐 URL: {banqueta.imagem_secundaria.url}")
            else:
                print(f"   ❌ Arquivo não encontrado no sistema")
        else:
            print(f"❌ Sem imagem secundária")
    
    print(f"\n=== COMO ADICIONAR IMAGENS ===")
    print(f"1. Via Admin Django:")
    print(f"   - Acesse /admin/produtos/banqueta/")
    print(f"   - Edite a banqueta desejada")
    print(f"   - Faça upload das imagens")
    
    print(f"\n2. Via Shell Django:")
    print(f"   - python manage.py shell")
    print(f"   - from produtos.models import Banqueta")
    print(f"   - banqueta = Banqueta.objects.get(ref_banqueta='BQ249')")
    print(f"   - banqueta.imagem_principal = 'caminho/para/imagem.jpg'")
    print(f"   - banqueta.save()")
    
    print(f"\n3. Baseado nas imagens anexas:")
    referencias_imagens = {
        'BQ13': 'CERES - banqueta estofada',
        'BQ249': 'GIO - banqueta estofada',
        'BQ250': 'IAN - banqueta alta giratória',
        'BQ251': 'MET - banqueta estrutura metálica',
        'BQ254': 'VIC - banqueta estofada',
        'BQ273': 'VIC GIRATÓRIA - com regulagem',
        'BQ278': 'GIO GIRATÓRIA - modelo giratório'
    }
    
    print(f"\n📸 Imagens que você anexou correspondem a:")
    for ref, desc in referencias_imagens.items():
        print(f"   - {ref}: {desc}")
    
    print(f"\n=== SOLUÇÃO PARA CORRIGIR IMAGENS ===")
    print(f"✅ Template corrigido para tratar imagens ausentes")
    print(f"✅ Placeholder exibido quando não há imagem")
    print(f"✅ Tratamento de erro para imagens quebradas")
    print(f"✅ Layout responsivo mantido")
    
    print(f"\n🎯 Próximo passo: Fazer upload das imagens via admin")

if __name__ == '__main__':
    teste_imagens_banquetas()
