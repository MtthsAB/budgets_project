#!/usr/bin/env python3
"""
Script para adicionar itens de teste ao orçamento para validar a implementação
"""

import os
import sys
import django

# Configurar Django
sys.path.append('/home/matas/projetos/Project')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema_produtos.settings')
django.setup()

from orcamentos.models import Orcamento, OrcamentoItem
from produtos.models import Produto
from decimal import Decimal

def main():
    print("=== ADICIONANDO ITENS DE TESTE AO ORÇAMENTO ===")
    
    # Buscar orçamento 43
    try:
        orcamento = Orcamento.objects.get(pk=43)
        print(f"Orçamento encontrado: {orcamento.numero}")
    except Orcamento.DoesNotExist:
        print("Orçamento 43 não encontrado")
        return
    
    # Buscar produtos disponíveis
    produtos = Produto.objects.filter(ativo=True)[:3]
    print(f"Produtos disponíveis: {produtos.count()}")
    
    if produtos.count() == 0:
        print("Nenhum produto encontrado")
        return
    
    # Limpar itens existentes do orçamento para teste limpo
    OrcamentoItem.objects.filter(orcamento=orcamento).delete()
    print("Itens existentes removidos")
    
    # Adicionar itens de teste
    itens_criados = 0
    for i, produto in enumerate(produtos):
        # Usar preço base fixo para teste
        preco_base = Decimal('1000.00')  # R$ 1000,00 base
        preco_com_faixa = preco_base * orcamento.faixa_preco.multiplicador
        
        item = OrcamentoItem.objects.create(
            orcamento=orcamento,
            produto=produto,
            quantidade=i + 1,  # 1, 2, 3
            preco_unitario=preco_com_faixa,
            observacoes=f"Item de teste {i + 1}",
            dados_produto={
                'teste': True,
                'criado_por_script': True
            }
        )
        
        print(f"Item {i + 1}: {produto.nome_produto} - Qtd: {item.quantidade} - Preço: R$ {item.preco_unitario} - Total: R$ {item.get_total()}")
        itens_criados += 1
    
    print(f"\n✅ {itens_criados} itens criados com sucesso!")
    
    # Verificar totais do orçamento
    print(f"\n=== TOTAIS DO ORÇAMENTO ===")
    print(f"Subtotal: R$ {orcamento.get_subtotal()}")
    print(f"Desconto: R$ {orcamento.get_total_desconto()}")
    print(f"Acréscimo: R$ {orcamento.get_total_acrescimo()}")
    print(f"Total Final: R$ {orcamento.get_total_final()}")
    
    print(f"\n✅ Teste concluído! Agora acesse:")
    print(f"   - Edição: http://127.0.0.1:8000/orcamentos/43/editar/")
    print(f"   - Visualização: http://127.0.0.1:8000/orcamentos/43/")

if __name__ == '__main__':
    main()
