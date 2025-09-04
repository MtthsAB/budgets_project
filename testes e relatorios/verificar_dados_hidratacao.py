#!/usr/bin/env python
"""
Script para verificar e criar dados de tamanhos para teste da hidratação.
"""

import os
import sys
import django
from django.conf import settings

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema_produtos.settings')
sys.path.append('/home/matas/projetos/Project')
django.setup()

from produtos.models import Produto, Modulo, TamanhosModulosDetalhado
from decimal import Decimal


def main():
    print("🔍 Verificando dados existentes para hidratação...")
    
    try:
        # 1. Buscar o sofá de teste
        sofa = Produto.objects.filter(id_tipo_produto__nome__icontains='sofá').first()
        
        if not sofa:
            print("❌ Nenhum sofá encontrado")
            return
        
        print(f"🛋️ Sofá: {sofa.ref_produto} - {sofa.nome_produto}")
        
        # 2. Verificar módulos e seus tamanhos
        modulos = sofa.modulos.all()
        print(f"📦 Módulos: {modulos.count()}")
        
        for modulo in modulos:
            tamanhos = modulo.tamanhos_detalhados.all()
            print(f"   - {modulo.nome} (ID: {modulo.id})")
            print(f"     📏 Tamanhos: {tamanhos.count()}")
            
            if tamanhos.count() == 0:
                print(f"     ➕ Criando tamanhos de exemplo para '{modulo.nome}'...")
                
                # Criar tamanhos de exemplo
                if "2 ASSENTOS" in modulo.nome.upper():
                    tamanhos_exemplo = [
                        {
                            'largura_total': Decimal('140.00'),
                            'largura_assento': Decimal('120.00'),
                            'tecido_metros': Decimal('3.50'),
                            'volume_m3': Decimal('0.850'),
                            'peso_kg': Decimal('45.00'),
                            'preco': Decimal('1200.00'),
                            'descricao': 'Tamanho padrão 2 lugares'
                        },
                        {
                            'largura_total': Decimal('160.00'),
                            'largura_assento': Decimal('140.00'),
                            'tecido_metros': Decimal('4.00'),
                            'volume_m3': Decimal('0.950'),
                            'peso_kg': Decimal('52.00'),
                            'preco': Decimal('1350.00'),
                            'descricao': 'Tamanho grande 2 lugares'
                        }
                    ]
                elif "POLTRONA" in modulo.nome.upper():
                    tamanhos_exemplo = [
                        {
                            'largura_total': Decimal('80.00'),
                            'largura_assento': Decimal('60.00'),
                            'tecido_metros': Decimal('2.20'),
                            'volume_m3': Decimal('0.450'),
                            'peso_kg': Decimal('28.00'),
                            'preco': Decimal('850.00'),
                            'descricao': 'Poltrona padrão'
                        }
                    ]
                else:
                    # Tamanho genérico
                    tamanhos_exemplo = [
                        {
                            'largura_total': Decimal('100.00'),
                            'largura_assento': Decimal('80.00'),
                            'tecido_metros': Decimal('2.50'),
                            'volume_m3': Decimal('0.600'),
                            'peso_kg': Decimal('35.00'),
                            'preco': Decimal('950.00'),
                            'descricao': 'Tamanho padrão'
                        }
                    ]
                
                # Criar os tamanhos
                for i, dados_tamanho in enumerate(tamanhos_exemplo):
                    tamanho = TamanhosModulosDetalhado.objects.create(
                        id_modulo=modulo,
                        **dados_tamanho
                    )
                    print(f"       ✅ Criado: {dados_tamanho['descricao']} (ID: {tamanho.id})")
            else:
                for tamanho in tamanhos:
                    print(f"       📏 {tamanho.descricao or 'Sem descrição'} - {tamanho.largura_total}cm - R$ {tamanho.preco or 0}")
        
        print("\n📊 Resumo final:")
        print(f"   🛋️ Sofá: {sofa.ref_produto}")
        print(f"   📦 Módulos: {modulos.count()}")
        
        total_tamanhos = 0
        for modulo in modulos:
            count = modulo.tamanhos_detalhados.count()
            total_tamanhos += count
            print(f"   📏 Tamanhos em '{modulo.nome}': {count}")
        
        print(f"   📏 Total de tamanhos: {total_tamanhos}")
        
        if total_tamanhos > 0:
            print("✅ Dados prontos para teste de hidratação!")
        else:
            print("❌ Nenhum tamanho encontrado - hidratação pode não funcionar")
        
    except Exception as e:
        print(f"❌ Erro: {e}")
        import traceback
        traceback.print_exc()


if __name__ == '__main__':
    main()
