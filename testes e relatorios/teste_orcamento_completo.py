#!/usr/bin/env python
"""
Script para testar a criação de orçamento com produtos não-sofás
"""
import os
import sys
import django
from decimal import Decimal

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema_produtos.settings')
django.setup()

from orcamentos.models import Orcamento, OrcamentoItem
from clientes.models import Cliente
from produtos.models import Produto
from authentication.models import CustomUser

def criar_orcamento_teste():
    """Cria um orçamento de teste com produtos de diferentes tipos"""
    
    print("🧪 Criando orçamento de teste com produtos diversos...")
    print("=" * 60)
    
    # Buscar dados necessários
    try:
        cliente = Cliente.objects.first()
        if not cliente:
            print("❌ Nenhum cliente encontrado!")
            return
        print(f"✓ Cliente: {cliente.nome_empresa}")
        
        usuario = CustomUser.objects.filter(tipo_permissao='master').first()
        if not usuario:
            print("❌ Nenhum usuário master encontrado!")
            return
        print(f"✓ Usuário: {usuario.email}")
        
        # Buscar produtos de diferentes tipos
        print("\n📦 Produtos disponíveis por tipo:")
        produtos_por_tipo = {}
        
        produtos = Produto.objects.all().order_by('id_tipo_produto__nome', 'nome_produto')
        for produto in produtos:
            tipo = produto.id_tipo_produto.nome
            if tipo not in produtos_por_tipo:
                produtos_por_tipo[tipo] = []
            produtos_por_tipo[tipo].append(produto)
            
        for tipo, lista in produtos_por_tipo.items():
            print(f"   • {tipo}: {len(lista)} produtos")
            for p in lista[:2]:  # Mostrar apenas os 2 primeiros
                print(f"     - {p.ref_produto}: {p.nome_produto}")
        
        # Criar orçamento
        from orcamentos.models import FaixaPreco, FormaPagamento
        from django.utils import timezone
        from datetime import timedelta
        
        faixa_preco = FaixaPreco.objects.first()
        forma_pagamento = FormaPagamento.objects.first()
        
        if not faixa_preco or not forma_pagamento:
            print("❌ Faixa de preço ou forma de pagamento não encontradas!")
            return
            
        orcamento = Orcamento.objects.create(
            cliente=cliente,
            vendedor=usuario,
            faixa_preco=faixa_preco,
            forma_pagamento=forma_pagamento,
            data_entrega=timezone.now().date() + timedelta(days=30),
            data_validade=timezone.now().date() + timedelta(days=15),
            desconto_valor=Decimal('50.00'),
            acrescimo_percentual=Decimal('5.00'),
            observacoes="Orçamento de teste criado automaticamente com produtos diversos"
        )
        
        print(f"\n✓ Orçamento criado: {orcamento.numero}")
        
        # Adicionar produtos de diferentes tipos
        print("\n📋 Adicionando itens ao orçamento:")
        
        produtos_teste = []
        for tipo, lista in produtos_por_tipo.items():
            if lista:  # Se tem produtos deste tipo
                produto = lista[0]  # Pegar o primeiro
                produtos_teste.append(produto)
                
        for i, produto in enumerate(produtos_teste[:6]):  # Máximo 6 produtos
            # Buscar preço do produto específico
            preco = Decimal('100.00')  # Preço padrão
            
            # Tentar encontrar preço real baseado no tipo
            if produto.id_tipo_produto.nome == 'Cadeiras':
                from produtos.models import Cadeira
                try:
                    cadeira = Cadeira.objects.get(ref_cadeira=produto.ref_produto)
                    preco = cadeira.preco
                except Cadeira.DoesNotExist:
                    pass
            elif produto.id_tipo_produto.nome == 'Banquetas':
                from produtos.models import Banqueta
                try:
                    banqueta = Banqueta.objects.get(ref_banqueta=produto.ref_produto)
                    preco = banqueta.preco
                except Banqueta.DoesNotExist:
                    pass
            elif produto.id_tipo_produto.nome == 'Poltronas':
                from produtos.models import Poltrona
                try:
                    poltrona = Poltrona.objects.get(ref_poltrona=produto.ref_produto)
                    preco = poltrona.preco
                except Poltrona.DoesNotExist:
                    pass
                    
            item = OrcamentoItem.objects.create(
                orcamento=orcamento,
                produto=produto,
                quantidade=i + 1,  # Quantidade variável
                preco_unitario=preco,
                observacoes=f"Item de teste - {produto.id_tipo_produto.nome}"
            )
            
            print(f"   ✓ {produto.id_tipo_produto.nome}: {produto.ref_produto} - {produto.nome_produto}")
            print(f"     Qtd: {item.quantidade}, Preço: R$ {item.preco_unitario}, Total: R$ {item.get_total()}")
        
        print(f"\n✅ Orçamento teste criado com sucesso!")
        print(f"   • ID: {orcamento.id}")
        print(f"   • Número: {orcamento.numero}")
        print(f"   • Total de itens: {orcamento.itens.count()}")
        print(f"   • Subtotal: R$ {orcamento.get_subtotal()}")
        print(f"   • Total final: R$ {orcamento.get_total_final()}")
        
        # URLs para testar
        print(f"\n🌐 URLs para testar:")
        print(f"   • Visualizar: http://127.0.0.1:8001/orcamentos/{orcamento.id}/")
        print(f"   • Editar: http://127.0.0.1:8001/orcamentos/{orcamento.id}/editar/")
        
        return orcamento
        
    except Exception as e:
        print(f"❌ Erro: {e}")
        import traceback
        traceback.print_exc()
        
if __name__ == '__main__':
    try:
        criar_orcamento_teste()
    except Exception as e:
        print(f"\n❌ Erro geral: {e}")
        sys.exit(1)
