#!/usr/bin/env python
import os
import sys
import django

# Configurar Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema_produtos.settings')
django.setup()

from orcamentos.models import Orcamento, OrcamentoItem

def debug_orcamento_52():
    try:
        orcamento = Orcamento.objects.get(pk=52)
        print(f"Orçamento {orcamento.numero} encontrado")
        
        itens = orcamento.itens.select_related('produto').all()
        print(f"Total de itens: {itens.count()}")
        
        for item in itens:
            print(f"\n--- Item {item.id} ---")
            print(f"Produto: {item.produto.nome_produto}")
            print(f"Tipo: {item.produto.id_tipo_produto.nome}")
            print(f"É sofá? {item.produto.eh_sofa()}")
            print(f"Dados produto: {item.dados_produto}")
            print(f"Tipo dados_produto: {type(item.dados_produto)}")
            
            if item.dados_produto:
                print("Chaves em dados_produto:")
                for key, value in item.dados_produto.items():
                    print(f"  - {key}: {type(value)} = {value}")
            
    except Orcamento.DoesNotExist:
        print("Orçamento 52 não encontrado")
    except Exception as e:
        print(f"Erro: {e}")

if __name__ == "__main__":
    debug_orcamento_52()
