#!/usr/bin/env python
"""
Script para migrar produtos do modelo genérico Produto para os modelos específicos

Uso:
    docker compose exec app python /app/migrar_produtos.py

Este script:
1. Pega todos os produtos da tabela Produto
2. Move cada um para sua tabela específica (Banqueta, Cadeira, Poltrona, Pufe, Almofada)
3. Mantém as imagens e dados
"""

import os
import sys
import django
from pathlib import Path

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema_produtos.settings')
django.setup()

from produtos.models import (
    Produto, TipoItem, 
    Banqueta, Cadeira, Poltrona, Pufe, Almofada
)

def migrar_produtos():
    """Migra todos os produtos para seus modelos específicos"""
    
    print('📊 MIGRAÇÃO DE PRODUTOS')
    print('═' * 60)
    
    # Mapeamento de tipos para modelos e campos
    mapeamento = {
        'Sofás': None,  # Sofás não têm modelo específico, vão ficar em Produto
        'Cadeiras': Cadeira,
        'Banquetas': Banqueta,
        'Poltronas': Poltrona,
        'Pufes': Pufe,
        'Almofadas': Almofada,
    }
    
    total_migrante = 0
    total_sucesso = 0
    total_erro = 0
    
    for tipo_nome, model_class in mapeamento.items():
        print(f'\n📂 {tipo_nome}')
        print(f'─' * 60)
        
        try:
            tipo = TipoItem.objects.get(nome=tipo_nome)
        except TipoItem.DoesNotExist:
            print(f'  ❌ Tipo não encontrado: {tipo_nome}')
            continue
        
        produtos = Produto.objects.filter(id_tipo_produto=tipo)
        
        if not produtos.exists():
            print(f'  ℹ️  Nenhum produto encontrado')
            continue
        
        for produto in produtos:
            total_migrante += 1
            
            if model_class is None:
                # Sofás ficam em Produto
                print(f'  ✓ {produto.ref_produto:15} -> Fica em Produto (ok)')
                total_sucesso += 1
                continue
            
            try:
                # Preparar dados
                dados = {
                    f'ref_{model_class.__name__.lower()}': produto.ref_produto,
                    'nome': produto.nome_produto,
                    'imagem_principal': produto.imagem_principal,
                    'imagem_secundaria': produto.imagem_secundaria,
                    'ativo': produto.ativo,
                }
                
                # Adicionar dimensões padrão e preço
                if model_class in [Banqueta, Cadeira, Poltrona, Pufe, Almofada]:
                    # Campos obrigatórios com valores padrão
                    dados['preco'] = 0  # Preço padrão
                    for campo in ['largura', 'profundidade', 'altura', 'tecido_metros', 'volume_m3', 'peso_kg']:
                        if hasattr(model_class, campo):
                            # Usar valores padrão
                            dados[campo] = 0
                
                # Criar nova instância no modelo específico
                nova_instancia = model_class.objects.create(**dados)
                
                # Deletar do modelo genérico
                produto.delete()
                
                print(f'  ✅ {nova_instancia.ref_cadeira if hasattr(nova_instancia, "ref_cadeira") else nova_instancia.ref_banqueta if hasattr(nova_instancia, "ref_banqueta") else produto.ref_produto:15} -> {model_class.__name__}')
                total_sucesso += 1
                
            except Exception as e:
                print(f'  ❌ {produto.ref_produto:15} -> ERRO: {str(e)[:40]}')
                total_erro += 1
    
    print(f'\n' + '═' * 60)
    print(f'✅ Migração concluída!')
    print(f'   Total processados: {total_migrante}')
    print(f'   Sucesso: {total_sucesso}')
    print(f'   Erros: {total_erro}')
    print(f'═' * 60)

if __name__ == '__main__':
    migrar_produtos()
