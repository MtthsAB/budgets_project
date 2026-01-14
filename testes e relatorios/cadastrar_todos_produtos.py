#!/usr/bin/env python
"""
Script para cadastrar TODOS os produtos automaticamente a partir das imagens em dados_produtos

Uso:
    docker compose exec app python /app/cadastrar_todos_produtos.py

Este script:
1. Verifica todas as imagens na pasta dados_produtos/fotos
2. Cria um produto para cada imagem encontrada
3. Adiciona a imagem ao produto
4. Suporta todos os 6 tipos de produtos

Estrutura esperada:
    dados_produtos/fotos/
        ├── sofa/
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
import re

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema_produtos.settings')
django.setup()

from produtos.models import Produto, TipoItem

def limpar_ref_produto(filename: str) -> str:
    """
    Converte nome de arquivo em referência de produto válida
    
    Exemplos:
        'pf240.png' -> 'PF240'
        'cd01.png' -> 'CD01'
        'le coultre.jpg' -> 'LE_COULTRE'
    """
    # Remover extensão
    nome = Path(filename).stem
    
    # Limpar espaços e caracteres especiais
    nome = nome.strip()
    nome = re.sub(r'\s+', '_', nome)  # Substituir espaços por underscore
    nome = re.sub(r'[^a-zA-Z0-9_]', '', nome)  # Remover caracteres especiais
    
    # Converter para maiúsculas
    nome = nome.upper()
    
    return nome

def get_tipo_item(tipo_pasta: str) -> TipoItem:
    """Obter ou criar o tipo de item"""
    tipo_map = {
        'sofa': 'Sofás',
        'cadeiras': 'Cadeiras',
        'banquetas': 'Banquetas',
        'poltronas': 'Poltronas',
        'PUFES': 'Pufes',
        'almofadas': 'Almofadas',
    }
    
    tipo_nome = tipo_map.get(tipo_pasta, tipo_pasta)
    tipo, created = TipoItem.objects.get_or_create(nome=tipo_nome)
    return tipo

def cadastrar_todos_produtos(pasta_base='/app/dados_produtos'):
    """
    Cadastra todos os produtos baseado nas imagens encontradas
    
    Args:
        pasta_base: Caminho da pasta dados_produtos
    """
    pasta_fotos = Path(pasta_base) / 'fotos'
    
    if not pasta_fotos.exists():
        print(f'❌ Pasta não encontrada: {pasta_fotos}')
        return
    
    print(f'📁 Analisando: {pasta_fotos}')
    print(f'═' * 60)
    
    total_cadastrados = 0
    total_imagens = 0
    
    tipos_produto = ['sofa', 'cadeiras', 'banquetas', 'poltronas', 'PUFES', 'almofadas']
    
    # Percorrer cada tipo de produto
    for tipo_pasta in tipos_produto:
        tipo_path = pasta_fotos / tipo_pasta
        
        if not tipo_path.exists():
            continue
        
        print(f'\n📂 {tipo_pasta.upper()}')
        print(f'─' * 60)
        
        tipo_item = get_tipo_item(tipo_pasta)
        
        # Para sofás, há subpastas
        if tipo_pasta == 'sofa':
            # Processar subpastas como produtos
            for subdir in tipo_path.iterdir():
                if subdir.is_dir() and subdir.name not in ['sf939', 'bigboss']:
                    continue
                if subdir.is_dir():
                    processar_pasta_produto(
                        subdir,
                        limpar_ref_produto(subdir.name),
                        tipo_item,
                        tipo_pasta
                    )
        else:
            # Para outros tipos, cada imagem é um produto
            imagens = sorted(list(tipo_path.glob('*.jpg')) + list(tipo_path.glob('*.png')))
            for imagem_path in imagens:
                ref_produto = limpar_ref_produto(imagem_path.name)
                
                try:
                    # Verificar se produto já existe
                    produto, created = Produto.objects.get_or_create(
                        ref_produto=ref_produto,
                        defaults={
                            'nome_produto': imagem_path.stem.replace('_', ' ').title(),
                            'id_tipo_produto': tipo_item,
                            'ativo': True,
                        }
                    )
                    
                    # Adicionar imagem
                    if not produto.imagem_principal:
                        with open(imagem_path, 'rb') as f:
                            filename = f'{ref_produto}_principal{imagem_path.suffix}'
                            produto.imagem_principal.save(filename, ContentFile(f.read()), save=True)
                        
                        status = '✅ NOVO' if created else '🔄 ATUALIZADO'
                        print(f'  {status:15} {ref_produto:20} - {imagem_path.name}')
                        total_cadastrados += 1
                        total_imagens += 1
                    else:
                        print(f'  ⏭️  EXISTENTE      {ref_produto:20} - Imagem já existe')
                        
                except Exception as e:
                    print(f'  ❌ ERRO            {ref_produto:20} - {str(e)[:40]}')

def processar_pasta_produto(pasta_produto: Path, ref_produto: str, tipo_item: TipoItem, tipo_pasta: str):
    """Processa uma pasta de produto específico"""
    try:
        # Verificar se produto já existe
        produto, created = Produto.objects.get_or_create(
            ref_produto=ref_produto,
            defaults={
                'nome_produto': ref_produto.replace('_', ' ').title(),
                'id_tipo_produto': tipo_item,
                'ativo': True,
            }
        )
        
        # Procurar imagens
        jpg_files = sorted(
            list(pasta_produto.glob('*.jpg')),
            key=lambda x: x.stat().st_size,
            reverse=True
        )
        png_files = sorted(
            list(pasta_produto.glob('*.png')),
            key=lambda x: x.stat().st_size,
            reverse=True
        )
        
        all_images = jpg_files + png_files
        
        if not all_images:
            print(f'  ⚠️  SEM IMAGENS    {ref_produto:20}')
            return
        
        # Adicionar imagem principal
        if not produto.imagem_principal:
            with open(all_images[0], 'rb') as f:
                filename = f'{ref_produto}_principal{all_images[0].suffix}'
                produto.imagem_principal.save(filename, ContentFile(f.read()), save=True)
        
        # Adicionar imagem secundária
        if len(all_images) > 1 and not produto.imagem_secundaria:
            with open(all_images[1], 'rb') as f:
                filename = f'{ref_produto}_secundaria{all_images[1].suffix}'
                produto.imagem_secundaria.save(filename, ContentFile(f.read()), save=True)
        
        status = '✅ NOVO' if created else '🔄 ATUALIZADO'
        print(f'  {status:15} {ref_produto:20} - {len(all_images)} imagem(ns)')
        
        return True
        
    except Exception as e:
        print(f'  ❌ ERRO            {ref_produto:20} - {str(e)[:40]}')
        return False

if __name__ == '__main__':
    pasta_base = '/app/dados_produtos'
    
    if not Path(pasta_base).exists():
        pasta_base = str(Path(__file__).parent.parent / 'dados_produtos')
    
    cadastrar_todos_produtos(pasta_base)
    
    # Resumo final
    print(f'\n' + '═' * 60)
    print(f'✅ Cadastro completo!')
    print(f'═' * 60)
    
    # Estatísticas finais
    from produtos.models import Produto, TipoItem
    
    total_produtos = Produto.objects.count()
    com_imagem = Produto.objects.exclude(imagem_principal='').count()
    
    print(f'\n📊 ESTATÍSTICAS FINAIS:')
    print(f'   Total de produtos: {total_produtos}')
    print(f'   Com imagem principal: {com_imagem}')
    
    # Por tipo
    print(f'\n   Por tipo:')
    for tipo in TipoItem.objects.all():
        count = Produto.objects.filter(id_tipo_produto=tipo).count()
        print(f'     • {tipo.nome:20} {count:3} produto(s)')
