#!/usr/bin/env python
"""
Script para testar a herança de altura e profundidade dos módulos para os tamanhos.
"""

import os
import sys
import django

# Configurar Django
sys.path.append('/home/matas/projetos/Project')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema_produtos.settings')
django.setup()

from produtos.models import Item, TipoItem, Modulo, TamanhosModulosDetalhado
from django.db import transaction

def criar_dados_teste():
    """Cria dados de teste para validar a herança"""
    with transaction.atomic():
        # Criar tipo de item
        tipo_item, created = TipoItem.objects.get_or_create(
            nome="Sofá de Teste",
            defaults={'nome': "Sofá de Teste"}
        )
        
        # Criar item
        item, created = Item.objects.get_or_create(
            ref_produto="SOF001-TEST",
            defaults={
                'nome_produto': "Sofá Teste Herança",
                'id_tipo_produto': tipo_item,
                'ativo': True
            }
        )
        
        # Criar módulo com dimensões específicas
        modulo, created = Modulo.objects.get_or_create(
            item=item,
            nome="Módulo Central Test",
            defaults={
                'profundidade': 85.50,
                'altura': 78.20,
                'braco': 25.00,
                'descricao': "Módulo para teste de herança"
            }
        )
        
        # Criar tamanho detalhado
        tamanho, created = TamanhosModulosDetalhado.objects.get_or_create(
            id_modulo=modulo,
            nome_tamanho="1 Lugar Test",
            defaults={
                'largura_total': 95.00,
                'largura_assento': 65.00,
                'tecido_metros': 2.5,
                'volume_m3': 0.85,
                'peso_kg': 45.0,
                'preco': 1500.00,
                'descricao': "Tamanho teste para validação de herança"
            }
        )
        
        return item, modulo, tamanho

def testar_heranca():
    """Testa se a herança está funcionando corretamente"""
    print("=== TESTE DE HERANÇA DE ALTURA E PROFUNDIDADE ===\n")
    
    try:
        # Criar dados de teste
        item, modulo, tamanho = criar_dados_teste()
        
        print(f"✓ Dados de teste criados com sucesso")
        print(f"  Item: {item.ref_produto} - {item.nome_produto}")
        print(f"  Módulo: {modulo.nome}")
        print(f"  Tamanho: {tamanho.nome_tamanho}")
        print()
        
        # Testar valores do módulo
        print("=== DADOS DO MÓDULO ===")
        print(f"Altura do módulo: {modulo.altura} cm")
        print(f"Profundidade do módulo: {modulo.profundidade} cm")
        print()
        
        # Testar herança no tamanho
        print("=== DADOS HERDADOS NO TAMANHO ===")
        print(f"Altura herdada: {tamanho.altura_cm} cm")
        print(f"Profundidade herdada: {tamanho.profundidade_cm} cm")
        print()
        
        # Validar se os valores são iguais
        print("=== VALIDAÇÃO DA HERANÇA ===")
        altura_ok = tamanho.altura_cm == modulo.altura
        profundidade_ok = tamanho.profundidade_cm == modulo.profundidade
        
        print(f"Altura correta: {'✓' if altura_ok else '✗'} ({tamanho.altura_cm} == {modulo.altura})")
        print(f"Profundidade correta: {'✓' if profundidade_ok else '✗'} ({tamanho.profundidade_cm} == {modulo.profundidade})")
        print()
        
        # Testar string representation
        print("=== REPRESENTAÇÃO STRING ===")
        print(f"String do tamanho: {tamanho}")
        print()
        
        # Testar outras propriedades do tamanho
        print("=== OUTRAS PROPRIEDADES DO TAMANHO ===")
        print(f"Largura total: {tamanho.largura_total} cm")
        print(f"Largura do assento: {tamanho.largura_assento} cm")
        print(f"Tecido necessário: {tamanho.tecido_metros} metros")
        print(f"Volume: {tamanho.volume_m3} m³")
        print(f"Peso: {tamanho.peso_kg} kg")
        print(f"Preço: R$ {tamanho.preco}")
        print()
        
        if altura_ok and profundidade_ok:
            print("🎉 TESTE PASSOU! A herança está funcionando corretamente.")
            return True
        else:
            print("❌ TESTE FALHOU! A herança não está funcionando corretamente.")
            return False
            
    except Exception as e:
        print(f"❌ ERRO durante o teste: {e}")
        return False

def testar_todos_tamanhos_existentes():
    """Testa todos os tamanhos existentes no sistema"""
    print("\n=== TESTE DOS TAMANHOS EXISTENTES ===\n")
    
    tamanhos = TamanhosModulosDetalhado.objects.select_related('id_modulo').all()
    
    if not tamanhos.exists():
        print("⚠️  Nenhum tamanho encontrado no sistema.")
        return
    
    print(f"Encontrados {tamanhos.count()} tamanhos no sistema:\n")
    
    problemas = []
    
    for i, tamanho in enumerate(tamanhos, 1):
        print(f"{i}. {tamanho.nome_tamanho} ({tamanho.id_modulo.nome})")
        print(f"   Módulo - Altura: {tamanho.id_modulo.altura}, Profundidade: {tamanho.id_modulo.profundidade}")
        print(f"   Herdado - Altura: {tamanho.altura_cm}, Profundidade: {tamanho.profundidade_cm}")
        
        # Verificar se a herança está funcionando
        if tamanho.altura_cm != tamanho.id_modulo.altura:
            problemas.append(f"Tamanho {tamanho.id}: altura não herda corretamente")
        
        if tamanho.profundidade_cm != tamanho.id_modulo.profundidade:
            problemas.append(f"Tamanho {tamanho.id}: profundidade não herda corretamente")
        
        print(f"   Status: {'✓' if not problemas else '⚠️'}")
        print()
    
    if problemas:
        print("❌ Problemas encontrados:")
        for problema in problemas:
            print(f"  - {problema}")
    else:
        print("✅ Todos os tamanhos estão herdando corretamente!")

if __name__ == "__main__":
    print("Iniciando testes de herança de dados...\n")
    
    # Teste com dados novos
    sucesso = testar_heranca()
    
    # Teste com dados existentes
    testar_todos_tamanhos_existentes()
    
    print("\n" + "="*50)
    if sucesso:
        print("CONCLUSÃO: ✅ Sistema funcionando corretamente!")
    else:
        print("CONCLUSÃO: ❌ Sistema precisa de ajustes!")
    print("="*50)
