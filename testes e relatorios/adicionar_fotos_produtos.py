#!/usr/bin/env python
"""
Script para adicionar fotos dos produtos a partir da pasta dados_produtos

Uso:
    python adicionar_fotos_produtos.py

Este script:
1. Verifica a pasta dados_produtos
2. Para cada pasta de produto, procura por imagens (JPG/PNG)
3. Seleciona a maior imagem como principal e segunda maior como secundária
4. Adiciona as imagens aos produtos cadastrados no banco

Estrutura esperada:
    dados_produtos/fotos/
        ├── sofa/
        │   ├── sf939/          → Imagens do SF939
        │   └── bigboss/        → Imagens do LE_COULTRE
        ├── cadeiras/
        ├── banquetas/
        ├── poltronas/
        ├── PUFES/
        └── almofadas/
"""

import os
import sys
import django
from pathlib import Path
from django.core.files.base import ContentFile

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema_produtos.settings')
django.setup()

from produtos.models import Produto, TipoItem

# Mapeamento de pastas para referências
PRODUCT_FOLDER_MAP = {
    'sofa': {
        'sf939': 'SF939',
        'bigboss': 'LE_COULTRE',
    },
    'cadeiras': {
        # Adicionar quando houver produtos cadastrados
    },
    'banquetas': {
        # Adicionar quando houver produtos cadastrados
    },
    'poltronas': {
        # Adicionar quando houver produtos cadastrados
    },
    'PUFES': {
        # Adicionar quando houver produtos cadastrados
    },
    'almofadas': {
        # Adicionar quando houver produtos cadastrados
    }
}

def adicionar_fotos_produtos(pasta_base='/app/dados_produtos'):
    """
    Adiciona fotos dos produtos do banco de dados baseado na estrutura
    de pastas de dados_produtos
    
    Args:
        pasta_base: Caminho da pasta dados_produtos
    """
    pasta_fotos = Path(pasta_base) / 'fotos'
    
    if not pasta_fotos.exists():
        print(f'❌ Pasta não encontrada: {pasta_fotos}')
        return
    
    print(f'📁 Analisando: {pasta_fotos}')
    print(f'═' * 50)
    
    total_produtos = 0
    total_imagens = 0
    
    # Percorrer tipos de produto
    for tipo_pasta, produtos_map in PRODUCT_FOLDER_MAP.items():
        tipo_path = pasta_fotos / tipo_pasta
        
        if not tipo_path.exists():
            continue
        
        print(f'\n📂 {tipo_pasta.upper()}')
        print(f'─' * 50)
        
        # Percorrer cada pasta de produto
        for pasta_produto, ref_produto in produtos_map.items():
            produto_path = tipo_path / pasta_produto
            
            if not produto_path.is_dir():
                print(f'  ⚠️  {ref_produto:15} - Pasta não encontrada: {pasta_produto}')
                continue
            
            try:
                produto = Produto.objects.get(ref_produto=ref_produto)
            except Produto.DoesNotExist:
                print(f'  ❌ {ref_produto:15} - Produto não cadastrado no BD')
                continue
            except Exception as e:
                print(f'  ❌ {ref_produto:15} - Erro ao procurar: {str(e)}')
                continue
            
            # Procurar imagens
            jpg_files = sorted(
                list(produto_path.glob('*.jpg')),
                key=lambda x: x.stat().st_size,
                reverse=True
            )
            png_files = sorted(
                list(produto_path.glob('*.png')),
                key=lambda x: x.stat().st_size,
                reverse=True
            )
            
            all_images = jpg_files + png_files
            
            if not all_images:
                print(f'  ⚠️  {ref_produto:15} - Nenhuma imagem encontrada')
                continue
            
            try:
                # Adicionar imagem principal (maior)
                with open(all_images[0], 'rb') as f:
                    filename = f'{ref_produto}_principal{all_images[0].suffix}'
                    produto.imagem_principal.save(filename, ContentFile(f.read()), save=True)
                
                # Adicionar imagem secundária (segunda maior) se existir
                if len(all_images) > 1:
                    with open(all_images[1], 'rb') as f:
                        filename = f'{ref_produto}_secundaria{all_images[1].suffix}'
                        produto.imagem_secundaria.save(filename, ContentFile(f.read()), save=True)
                
                total_imagens += len(all_images)
                total_produtos += 1
                print(f'  ✅ {ref_produto:15} - {len(all_images)} imagem(ns)')
                
            except Exception as e:
                print(f'  ❌ {ref_produto:15} - Erro ao salvar: {str(e)}')
    
    # Resumo final
    print(f'\n' + '═' * 50)
    print(f'✅ Resumo: {total_produtos} produtos | {total_imagens} imagens adicionadas')
    print(f'═' * 50)

if __name__ == '__main__':
    # Detectar caminho automaticamente
    pasta_base = '/app/dados_produtos'
    
    # Se não estiver em container, usar caminho local
    if not Path(pasta_base).exists():
        pasta_base = str(Path(__file__).parent.parent / 'dados_produtos')
    
    adicionar_fotos_produtos(pasta_base)
