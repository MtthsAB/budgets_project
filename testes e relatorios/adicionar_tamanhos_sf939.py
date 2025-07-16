#!/usr/bin/env python
"""
Script para adicionar tamanhos detalhados aos módulos do sofá SF939
"""

import os
import sys
import django

# Configuração do Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema_produtos.settings')
django.setup()

from produtos.models import Produto, Modulo, TamanhosModulosDetalhado

def adicionar_tamanhos_detalhados():
    """Adiciona tamanhos detalhados aos módulos do sofá SF939"""
    
    print("=== ADICIONANDO TAMANHOS DETALHADOS AO SOFÁ SF939 ===\n")
    
    try:
        # Buscar o sofá SF939
        sofa = Produto.objects.get(ref_produto="SF939")
        modulos = sofa.modulos.all()
        
        print(f"Sofá: {sofa.nome_produto}")
        print(f"Total de módulos: {len(modulos)}")
        
        # Dados dos tamanhos baseados na imagem anexa
        tamanhos_dados = {
            "2 ASSENTOS C/2BR": [
                {
                    "largura_total": 292,
                    "largura_assento": 120,
                    "tecido_metros": 14.3,
                    "volume_m3": 2.8,
                    "peso_kg": 80,
                    "preco": 5952.00,
                    "descricao": "Tamanho 1 - Acentos de 120cm"
                },
                {
                    "largura_total": 272,
                    "largura_assento": 110,
                    "tecido_metros": 13.5,
                    "volume_m3": 2.6,
                    "peso_kg": 75,
                    "preco": 5411.00,
                    "descricao": "Tamanho 2 - Acentos de 110cm"
                },
                {
                    "largura_total": 252,
                    "largura_assento": 100,
                    "tecido_metros": 13.0,
                    "volume_m3": 2.4,
                    "peso_kg": 70,
                    "preco": 5105.00,
                    "descricao": "Tamanho 3 - Acentos de 100cm"
                },
                {
                    "largura_total": 232,
                    "largura_assento": 90,
                    "tecido_metros": 12.3,
                    "volume_m3": 2.2,
                    "peso_kg": 65,
                    "preco": 4850.00,
                    "descricao": "Tamanho 4 - Acentos de 90cm"
                },
                {
                    "largura_total": 212,
                    "largura_assento": 80,
                    "tecido_metros": 12.0,
                    "volume_m3": 2.0,
                    "peso_kg": 60,
                    "preco": 4607.00,
                    "descricao": "Tamanho 5 - Acentos de 80cm"
                }
            ],
            "POLTRONA": [
                {
                    "largura_total": 115,
                    "largura_assento": 70,
                    "tecido_metros": 7.0,
                    "volume_m3": 1.5,
                    "peso_kg": 40,
                    "preco": 2822.00,
                    "descricao": "Tamanho único - Poltrona individual"
                }
            ]
        }
        
        # Adicionar tamanhos para cada módulo
        for modulo in modulos:
            print(f"\n--- MÓDULO: {modulo.nome} ---")
            
            # Limpar tamanhos existentes para evitar duplicatas
            modulo.tamanhos_detalhados.all().delete()
            
            if modulo.nome in tamanhos_dados:
                tamanhos_lista = tamanhos_dados[modulo.nome]
                
                for i, tamanho_data in enumerate(tamanhos_lista, 1):
                    tamanho = TamanhosModulosDetalhado.objects.create(
                        id_modulo=modulo,
                        largura_total=tamanho_data['largura_total'],
                        largura_assento=tamanho_data['largura_assento'],
                        tecido_metros=tamanho_data['tecido_metros'],
                        volume_m3=tamanho_data['volume_m3'],
                        peso_kg=tamanho_data['peso_kg'],
                        preco=tamanho_data['preco'],
                        descricao=tamanho_data['descricao']
                    )
                    
                    print(f"  ✓ Tamanho {i} criado: {tamanho.largura_total}cm x {tamanho.largura_assento}cm - R$ {tamanho.preco}")
            else:
                print(f"  ❌ Dados não encontrados para o módulo '{modulo.nome}'")
        
        print(f"\n=== TAMANHOS ADICIONADOS COM SUCESSO ===")
        print("Agora você pode visualizar o sofá completo com todos os tamanhos!")
        print("Acesse: http://localhost:8000/produtos/lista/")
        
    except Produto.DoesNotExist:
        print("❌ Sofá SF939 não encontrado!")
    except Exception as e:
        print(f"❌ Erro ao adicionar tamanhos: {e}")

if __name__ == "__main__":
    adicionar_tamanhos_detalhados()
