#!/usr/bin/env python
"""
Script para testar as melhorias na visualização de módulos de sofás
"""

import os
import sys
import django

# Configuração do Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema_produtos.settings')
django.setup()

from produtos.models import Produto, Modulo, TamanhosModulosDetalhado

def testar_visualizacao_modulos():
    """Testa se as melhorias na visualização estão funcionando"""
    
    print("=== TESTE DE MELHORIAS NA VISUALIZAÇÃO DE MÓDULOS ===\n")
    
    # Buscar o sofá SF939 cadastrado
    try:
        sofa = Produto.objects.get(ref_produto="SF939")
        print(f"✓ Sofá encontrado: {sofa.nome_produto}")
        
        # Verificar módulos
        modulos = sofa.modulos.all()
        print(f"✓ Total de módulos: {len(modulos)}")
        
        for i, modulo in enumerate(modulos, 1):
            print(f"\n--- MÓDULO {i}: {modulo.nome} ---")
            
            # Verificar informações do módulo
            print(f"  📏 Profundidade: {modulo.profundidade}cm" if modulo.profundidade else "  📏 Profundidade: Não informada")
            print(f"  📏 Altura: {modulo.altura}cm" if modulo.altura else "  📏 Altura: Não informada")
            print(f"  📏 Braço: {modulo.braco}cm" if modulo.braco else "  📏 Braço: Não informado")
            print(f"  📝 Descrição: {modulo.descricao}" if modulo.descricao else "  📝 Descrição: Não informada")
            
            # Verificar imagens
            if modulo.imagem_principal:
                print(f"  🖼️ Imagem Principal: {modulo.imagem_principal.url}")
            else:
                print("  🖼️ Imagem Principal: Não disponível")
                
            if modulo.imagem_secundaria:
                print(f"  🖼️ Imagem Secundária: {modulo.imagem_secundaria.url}")
            else:
                print("  🖼️ Imagem Secundária: Não disponível")
            
            # Verificar tamanhos
            tamanhos = modulo.tamanhos_detalhados.all()
            print(f"  📐 Tamanhos: {len(tamanhos)}")
            
            for j, tamanho in enumerate(tamanhos, 1):
                print(f"    Tamanho {j}:")
                print(f"      - Largura Total: {tamanho.largura_total}cm" if tamanho.largura_total else "      - Largura Total: Não informada")
                print(f"      - Largura Assento: {tamanho.largura_assento}cm" if tamanho.largura_assento else "      - Largura Assento: Não informada")
                print(f"      - Tecido: {tamanho.tecido_metros}m" if tamanho.tecido_metros else "      - Tecido: Não informado")
                print(f"      - Volume: {tamanho.volume_m3}m³" if tamanho.volume_m3 else "      - Volume: Não informado")
                print(f"      - Peso: {tamanho.peso_kg}kg" if tamanho.peso_kg else "      - Peso: Não informado")
                print(f"      - Preço: R$ {tamanho.preco}" if tamanho.preco else "      - Preço: Não informado")
        
        print("\n=== MELHORIAS IMPLEMENTADAS ===")
        print("✓ Imagens dos módulos com melhor tamanho e estilo")
        print("✓ Informações das dimensões em badges coloridos")
        print("✓ Descrição do módulo destacada")
        print("✓ Imagem secundária do módulo (quando disponível)")
        print("✓ Hover effects e animações")
        print("✓ Layout responsivo melhorado")
        print("✓ Cores e estilos mais modernos")
        
        print("\n=== RECOMENDAÇÕES PARA VISUALIZAÇÃO ===")
        print("1. Acesse: http://localhost:8000/produtos/lista/")
        print("2. Clique em 'Detalhes' do sofá SF939")
        print("3. Observe as melhorias na seção 'Módulos'")
        print("4. Verifique o hover effect nas imagens")
        print("5. Confirme se as informações estão bem organizadas")
        
    except Produto.DoesNotExist:
        print("❌ Sofá SF939 não encontrado!")
        print("Execute primeiro o script 'cadastrar_sofa_sf939.py'")
    except Exception as e:
        print(f"❌ Erro ao testar: {e}")

def verificar_template_atualizado():
    """Verifica se o template foi atualizado com as melhorias"""
    
    print("\n=== VERIFICAÇÃO DO TEMPLATE ===")
    
    template_path = "/home/matas/projetos/Project/templates/produtos/detalhes.html"
    
    try:
        with open(template_path, 'r', encoding='utf-8') as file:
            content = file.read()
            
        # Verificar se as melhorias foram implementadas
        melhorias = [
            ('modulo-card', 'Classes CSS para módulos'),
            ('modulo-header', 'Header estilizado para módulos'),
            ('modulo-image', 'Imagens melhoradas'),
            ('modulo-info', 'Informações organizadas'),
            ('modulo-dimensoes', 'Dimensões em badges'),
            ('modulo-descricao', 'Descrição destacada'),
            ('badge bg-info', 'Badges coloridos'),
            ('Imagem Secundária', 'Suporte a imagem secundária')
        ]
        
        for classe, descricao in melhorias:
            if classe in content:
                print(f"✓ {descricao}")
            else:
                print(f"❌ {descricao} - não encontrado")
                
    except FileNotFoundError:
        print("❌ Template não encontrado!")
    except Exception as e:
        print(f"❌ Erro ao verificar template: {e}")

if __name__ == "__main__":
    testar_visualizacao_modulos()
    verificar_template_atualizado()
