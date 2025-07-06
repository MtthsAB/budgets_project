#!/usr/bin/env python
"""
Teste de integração final - simula um fluxo completo de cadastro
"""

import os
import sys
import django
from decimal import Decimal

# Configurar Django
sys.path.append('/home/matas/projetos/Project')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema_produtos.settings')
django.setup()

from produtos.models import Item, TipoItem, Modulo, TamanhosModulosDetalhado
from produtos.forms import TamanhosModulosDetalhadoForm, ModuloForm, ItemForm
from django.db import transaction

def teste_integracao_completa():
    """Teste completo do fluxo de cadastro"""
    print("=== TESTE DE INTEGRAÇÃO COMPLETA ===\n")
    
    with transaction.atomic():
        # 1. Criar tipo de item
        tipo_item = TipoItem.objects.create(nome="Sofá Integração")
        print(f"✓ Tipo criado: {tipo_item}")
        
        # 2. Criar item usando formulário
        item_data = {
            'ref_produto': 'SOF-INT-001',
            'nome_produto': 'Sofá Teste Integração',
            'id_tipo_produto': tipo_item.id,
            'ativo': True,
            'tem_cor_tecido': True,
            'tem_difer_desenho_lado_dir_esq': False,
            'tem_difer_desenho_tamanho': True
        }
        
        item_form = ItemForm(data=item_data)
        if item_form.is_valid():
            item = item_form.save()
            print(f"✓ Item criado via formulário: {item}")
        else:
            print(f"❌ Erro no formulário de item: {item_form.errors}")
            return False
        
        # 3. Criar módulo usando formulário
        modulo_data = {
            'item': item.id,
            'nome': 'Módulo Central Integração',
            'profundidade': Decimal('88.00'),
            'altura': Decimal('82.00'),
            'braco': Decimal('28.00'),
            'descricao': 'Módulo para teste de integração completa'
        }
        
        modulo_form = ModuloForm(data=modulo_data)
        if modulo_form.is_valid():
            modulo = modulo_form.save()
            print(f"✓ Módulo criado via formulário: {modulo}")
        else:
            print(f"❌ Erro no formulário de módulo: {modulo_form.errors}")
            return False
        
        # 4. Criar tamanhos usando formulário
        tamanhos_data = [
            {
                'id_modulo': modulo.id,
                'nome_tamanho': '1 Lugar',
                'largura_total': Decimal('95.00'),
                'largura_assento': Decimal('65.00'),
                'tecido_metros': Decimal('2.5'),
                'volume_m3': Decimal('0.85'),
                'peso_kg': Decimal('45.0'),
                'preco': Decimal('1500.00'),
                'descricao': 'Sofá individual'
            },
            {
                'id_modulo': modulo.id,
                'nome_tamanho': '2 Lugares',
                'largura_total': Decimal('145.00'),
                'largura_assento': Decimal('115.00'),
                'tecido_metros': Decimal('3.5'),
                'volume_m3': Decimal('1.25'),
                'peso_kg': Decimal('65.0'),
                'preco': Decimal('2200.00'),
                'descricao': 'Sofá para duas pessoas'
            },
            {
                'id_modulo': modulo.id,
                'nome_tamanho': '3 Lugares',
                'largura_total': Decimal('195.00'),
                'largura_assento': Decimal('165.00'),
                'tecido_metros': Decimal('4.5'),
                'volume_m3': Decimal('1.65'),
                'peso_kg': Decimal('85.0'),
                'preco': Decimal('2900.00'),
                'descricao': 'Sofá para três pessoas'
            }
        ]
        
        tamanhos_criados = []
        for i, tamanho_data in enumerate(tamanhos_data, 1):
            tamanho_form = TamanhosModulosDetalhadoForm(data=tamanho_data)
            if tamanho_form.is_valid():
                tamanho = tamanho_form.save()
                tamanhos_criados.append(tamanho)
                print(f"✓ Tamanho {i} criado via formulário: {tamanho}")
            else:
                print(f"❌ Erro no formulário de tamanho {i}: {tamanho_form.errors}")
                return False
        
        # 5. Validar herança
        print(f"\n=== VALIDAÇÃO DA HERANÇA ===")
        for tamanho in tamanhos_criados:
            print(f"\nTamanho: {tamanho.nome_tamanho}")
            print(f"  Módulo - Altura: {tamanho.id_modulo.altura} | Profundidade: {tamanho.id_modulo.profundidade}")
            print(f"  Herdado - Altura: {tamanho.altura_cm} | Profundidade: {tamanho.profundidade_cm}")
            
            # Verificar se a herança está correta
            altura_ok = tamanho.altura_cm == tamanho.id_modulo.altura
            profundidade_ok = tamanho.profundidade_cm == tamanho.id_modulo.profundidade
            
            status = "✓" if (altura_ok and profundidade_ok) else "❌"
            print(f"  Status: {status} {'Herança correta' if (altura_ok and profundidade_ok) else 'Herança incorreta'}")
            
            if not (altura_ok and profundidade_ok):
                return False
        
        # 6. Testar alteração no módulo
        print(f"\n=== TESTE DE ALTERAÇÃO DO MÓDULO ===")
        modulo.altura = Decimal('85.00')
        modulo.profundidade = Decimal('90.00')
        modulo.save()
        print(f"✓ Módulo atualizado: altura={modulo.altura}, profundidade={modulo.profundidade}")
        
        # Verificar se a herança reflete as mudanças
        for tamanho in tamanhos_criados:
            # Recarregar do banco
            tamanho.refresh_from_db()
            print(f"  {tamanho.nome_tamanho}: altura={tamanho.altura_cm}, profundidade={tamanho.profundidade_cm}")
            
            if tamanho.altura_cm != modulo.altura or tamanho.profundidade_cm != modulo.profundidade:
                print("❌ Herança não atualizou após mudança no módulo")
                return False
        
        print("✓ Herança atualizada corretamente após mudança no módulo")
        
        # 7. Testar string representation
        print(f"\n=== TESTE DE REPRESENTAÇÃO STRING ===")
        for tamanho in tamanhos_criados:
            print(f"  {tamanho}")
        
        print(f"\n🎉 TESTE DE INTEGRAÇÃO COMPLETO PASSOU!")
        print(f"✅ Produto criado com {len(tamanhos_criados)} tamanhos")
        print(f"✅ Herança funcionando corretamente")
        print(f"✅ Formulários customizados validados")
        
        return True

if __name__ == "__main__":
    sucesso = teste_integracao_completa()
    
    print("\n" + "="*60)
    if sucesso:
        print("🎉 TESTE DE INTEGRAÇÃO: SUCESSO!")
        print("✅ Sistema está funcionando perfeitamente!")
    else:
        print("❌ TESTE DE INTEGRAÇÃO: FALHOU!")
        print("⚠️ Há problemas a serem corrigidos!")
    print("="*60)
