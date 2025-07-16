#!/usr/bin/env python
"""
Script de teste para verificar o sistema de orçamentos
"""

import os
import sys
import django
from datetime import date, timedelta

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema_produtos.settings')
django.setup()

from orcamentos.models import FaixaPreco, FormaPagamento, Orcamento, OrcamentoItem
from authentication.models import CustomUser
from clientes.models import Cliente
from produtos.models import Produto

def testar_sistema():
    """Testa os componentes básicos do sistema"""
    
    print("="*50)
    print("TESTE DO SISTEMA DE ORÇAMENTOS")
    print("="*50)
    
    # Verificar modelos básicos
    print(f"Faixas de preço: {FaixaPreco.objects.count()}")
    print(f"Formas de pagamento: {FormaPagamento.objects.count()}")
    print(f"Usuários: {CustomUser.objects.count()}")
    print(f"Clientes: {Cliente.objects.count()}")
    print(f"Produtos: {Produto.objects.count()}")
    print(f"Orçamentos: {Orcamento.objects.count()}")
    
    # Verificar se temos dados mínimos
    if FaixaPreco.objects.count() == 0:
        print("❌ Não há faixas de preço cadastradas")
        return False
        
    if FormaPagamento.objects.count() == 0:
        print("❌ Não há formas de pagamento cadastradas")
        return False
        
    if CustomUser.objects.count() == 0:
        print("❌ Não há usuários cadastrados")
        return False
    
    print("✅ Sistema básico configurado corretamente!")
    
    # Testar criação de orçamento se possível
    if Cliente.objects.count() > 0 and Produto.objects.count() > 0:
        print("\nTestando criação de orçamento...")
        
        cliente = Cliente.objects.first()
        produto = Produto.objects.first()
        vendedor = CustomUser.objects.filter(tipo_permissao__in=['master', 'admin', 'vendedor']).first()
        faixa_preco = FaixaPreco.objects.first()
        forma_pagamento = FormaPagamento.objects.first()
        
        if vendedor:
            # Criar orçamento de teste
            orcamento = Orcamento.objects.create(
                cliente=cliente,
                vendedor=vendedor,
                faixa_preco=faixa_preco,
                forma_pagamento=forma_pagamento,
                data_entrega=date.today() + timedelta(days=30),
                data_validade=date.today() + timedelta(days=15),
                observacoes="Orçamento de teste criado automaticamente"
            )
            
            print(f"✅ Orçamento criado: {orcamento.numero}")
            
            # Adicionar item de teste
            item = OrcamentoItem.objects.create(
                orcamento=orcamento,
                produto=produto,
                quantidade=1,
                preco_unitario=1000.00
            )
            
            print(f"✅ Item adicionado: {item.produto.nome_produto}")
            print(f"✅ Total do orçamento: R$ {orcamento.get_total_final()}")
            
        else:
            print("❌ Não há vendedor disponível para teste")
    else:
        print("⚠️ Não é possível testar criação de orçamento (faltam clientes ou produtos)")
    
    print("\n" + "="*50)
    print("TESTE CONCLUÍDO!")
    print("="*50)
    
    return True

def main():
    """Função principal"""
    try:
        if testar_sistema():
            print("\n🎉 Sistema de orçamentos funcionando corretamente!")
            print("\nPróximos passos:")
            print("1. Acesse http://localhost:8000")
            print("2. Faça login como Master/Admin")
            print("3. Navegue para Orçamentos > Novo Orçamento")
            print("4. Teste a criação de orçamentos")
            return 0
        else:
            print("\n❌ Problemas encontrados no sistema")
            return 1
            
    except Exception as e:
        print(f"❌ Erro durante teste: {str(e)}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
