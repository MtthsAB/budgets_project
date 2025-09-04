#!/usr/bin/env python
"""
Script para popular os módulos com dados de dimensões.
"""

import os
import sys
import django
from django.conf import settings

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema_produtos.settings')
sys.path.append('/home/matas/projetos/Project')
django.setup()

from produtos.models import Produto, Modulo
from decimal import Decimal


def main():
    print("🔧 Atualizando dados dos módulos...")
    
    try:
        # Buscar o sofá
        sofa = Produto.objects.filter(id_tipo_produto__nome__icontains='sofá').first()
        
        if not sofa:
            print("❌ Sofá não encontrado")
            return
        
        print(f"🛋️ Sofá: {sofa.ref_produto} - {sofa.nome_produto}")
        
        # Atualizar cada módulo
        modulos = sofa.modulos.all()
        
        for modulo in modulos:
            print(f"\n📦 Atualizando módulo: {modulo.nome}")
            
            if "2 ASSENTOS" in modulo.nome.upper():
                # Dados para módulo de 2 assentos
                modulo.profundidade = Decimal('85.00')
                modulo.altura = Decimal('90.00') 
                modulo.braco = Decimal('25.00')
                modulo.descricao = 'Módulo para 2 pessoas com braços laterais. Estrutura em madeira maciça com espuma de alta densidade.'
                
            elif "POLTRONA" in modulo.nome.upper():
                # Dados para poltrona
                modulo.profundidade = Decimal('90.00')
                modulo.altura = Decimal('95.00')
                modulo.braco = Decimal('20.00')
                modulo.descricao = 'Poltrona individual com braços. Design ergonômico para conforto máximo.'
                
            else:
                # Dados genéricos
                modulo.profundidade = Decimal('80.00')
                modulo.altura = Decimal('85.00')
                modulo.braco = Decimal('22.00')
                modulo.descricao = 'Módulo padrão com acabamento premium.'
            
            modulo.save()
            print(f"   ✅ Profundidade: {modulo.profundidade} cm")
            print(f"   ✅ Altura: {modulo.altura} cm")
            print(f"   ✅ Braço: {modulo.braco} cm")
            print(f"   ✅ Descrição: {modulo.descricao}")
        
        print("\n✅ Todos os módulos foram atualizados!")
        
    except Exception as e:
        print(f"❌ Erro: {e}")
        import traceback
        traceback.print_exc()


if __name__ == '__main__':
    main()
