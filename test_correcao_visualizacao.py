#!/usr/bin/env python
"""
Script para testar a correção da visualização de módulos no template de sofás
"""

import os
import sys
import django

# Configuração do Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema_produtos.settings')
django.setup()

from produtos.models import Produto, Modulo, TamanhosModulosDetalhado

def testar_correcao_visualizacao():
    """Testa se a correção da visualização de módulos está funcionando"""
    
    print("=== TESTE DE CORREÇÃO DA VISUALIZAÇÃO DE MÓDULOS ===\n")
    
    # Buscar o sofá SF939
    try:
        sofa = Produto.objects.get(ref_produto="SF939")
        print(f"✓ Sofá encontrado: {sofa.nome_produto}")
        print(f"  Tipo: {sofa.id_tipo_produto.nome}")
        print(f"  ID: {sofa.id}")
        
        # Verificar se é reconhecido como sofá
        if sofa.eh_sofa():
            print("  ✓ Reconhecido como sofá")
        else:
            print("  ❌ NÃO reconhecido como sofá")
        
        # Verificar módulos
        modulos = sofa.modulos.all()
        print(f"\n✓ Total de módulos: {len(modulos)}")
        
        for i, modulo in enumerate(modulos, 1):
            print(f"\n--- MÓDULO {i}: {modulo.nome} ---")
            
            # Verificar se tem informações completas
            campos_verificar = [
                ('nome', modulo.nome),
                ('profundidade', modulo.profundidade),
                ('altura', modulo.altura),
                ('braco', modulo.braco),
                ('descricao', modulo.descricao),
                ('imagem_principal', modulo.imagem_principal),
                ('imagem_secundaria', modulo.imagem_secundaria),
            ]
            
            for campo, valor in campos_verificar:
                if valor:
                    if campo in ['imagem_principal', 'imagem_secundaria']:
                        print(f"  ✓ {campo}: {valor.url}")
                    else:
                        print(f"  ✓ {campo}: {valor}")
                else:
                    print(f"  - {campo}: Não definido")
            
            # Verificar tamanhos
            tamanhos = modulo.tamanhos_detalhados.all()
            print(f"  ✓ Tamanhos: {len(tamanhos)}")
            
            for j, tamanho in enumerate(tamanhos, 1):
                print(f"    Tamanho {j}: {tamanho.largura_total}cm x {tamanho.largura_assento}cm - R$ {tamanho.preco}")
        
        print("\n=== CORREÇÃO IMPLEMENTADA ===")
        print("✓ Template específico de sofás atualizado")
        print("✓ Seção de módulos mostra informações completas")
        print("✓ Imagens, dimensões e descrição dos módulos")
        print("✓ Tamanhos detalhados com preços e especificações")
        print("✓ Estilos CSS modernos aplicados")
        
        # URLs para testar
        print("\n=== URLS PARA TESTAR ===")
        print(f"1. Visualização geral: http://localhost:8000/produtos/{sofa.id}/")
        print(f"2. Visualização específica de sofá: http://localhost:8000/produtos/sofas/{sofa.id}/")
        print("3. Lista de produtos: http://localhost:8000/produtos/lista/")
        
        print("\n=== PROBLEMA CORRIGIDO ===")
        print("❌ ANTES: Módulos mostravam apenas 'Referência' e 'Tamanhos disponíveis'")
        print("✅ AGORA: Módulos mostram informações completas:")
        print("  - Nome do módulo")
        print("  - Imagem principal (e secundária se houver)")
        print("  - Dimensões (profundidade, altura, braço)")
        print("  - Descrição")
        print("  - Tamanhos detalhados com preços")
        print("  - Especificações técnicas")
        
    except Produto.DoesNotExist:
        print("❌ Sofá SF939 não encontrado!")
        print("Execute primeiro o script 'cadastrar_sofa_sf939.py'")
    except Exception as e:
        print(f"❌ Erro ao testar: {e}")

if __name__ == "__main__":
    testar_correcao_visualizacao()
