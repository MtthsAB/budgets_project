#!/usr/bin/env python
"""
Script para adicionar imagens às banquetas baseado nas imagens anexas
"""
import os
import sys
import django
from pathlib import Path
import shutil

# Adicionar o diretório do projeto ao path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema_produtos.settings')
django.setup()

from produtos.models import Banqueta

def adicionar_imagens_banquetas():
    """Adiciona imagens às banquetas baseado nas referências"""
    
    print("=== ADICIONANDO IMAGENS ÀS BANQUETAS ===\n")
    
    # Diretório de destino para as imagens
    media_dir = Path("/home/matas/projetos/Project/media/produtos/banquetas")
    media_dir.mkdir(parents=True, exist_ok=True)
    
    # Mapear imagens baseado nas referências das banquetas
    banquetas = Banqueta.objects.all()
    
    print(f"Encontradas {len(banquetas)} banquetas:")
    
    for banqueta in banquetas:
        print(f"- {banqueta.ref_banqueta} - {banqueta.nome}")
        
        # Simular a adição de imagem baseada na referência
        # Como as imagens estão anexas, vou criar referências de exemplo
        imagem_nome = f"{banqueta.ref_banqueta.lower()}.jpg"
        
        # Caminho relativo para o Django
        caminho_relativo = f"produtos/banquetas/{imagem_nome}"
        
        print(f"  Imagem esperada: {caminho_relativo}")
        
        # Atualizar o modelo (apenas simulando, pois as imagens reais precisam ser carregadas)
        # banqueta.imagem_principal = caminho_relativo
        # banqueta.save()
    
    print(f"\n=== INSTRUÇÕES PARA ADICIONAR IMAGENS ===")
    print(f"1. Salve as imagens anexas na pasta:")
    print(f"   {media_dir}")
    print(f"2. Nomeie as imagens conforme as referências:")
    
    for banqueta in banquetas:
        print(f"   - {banqueta.ref_banqueta.lower()}.jpg para {banqueta.ref_banqueta} - {banqueta.nome}")
    
    print(f"\n3. Ou use o admin do Django para fazer upload das imagens")
    print(f"4. As imagens aparecerão automaticamente na tela de detalhes")

if __name__ == '__main__':
    adicionar_imagens_banquetas()
