#!/usr/bin/env python3
"""
Script para testar o formulário de orçamentos
"""
import os
import django
from django.conf import settings

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema_produtos.settings')
django.setup()

from orcamentos.forms import OrcamentoForm
from clientes.models import Cliente
from orcamentos.models import FaixaPreco, FormaPagamento
from produtos.models import Produto

def main():
    print("🧪 TESTE DO FORMULÁRIO DE ORÇAMENTOS")
    print("=" * 50)
    
    try:
        # Testar se o formulário pode ser criado
        form = OrcamentoForm()
        print("✅ Formulário criado com sucesso!")
        
        # Verificar dados disponíveis
        clientes = Cliente.objects.all().count()
        faixas = FaixaPreco.objects.filter(ativo=True).count()
        formas = FormaPagamento.objects.filter(ativo=True).count()
        produtos = Produto.objects.filter(ativo=True).count()
        
        print(f"📊 Dados disponíveis:")
        print(f"   - Clientes: {clientes}")
        print(f"   - Faixas de preço ativas: {faixas}")
        print(f"   - Formas de pagamento ativas: {formas}")
        print(f"   - Produtos ativos: {produtos}")
        
        # Testar queryset do formulário
        cliente_choices = form.fields['cliente'].queryset.count()
        faixa_choices = form.fields['faixa_preco'].queryset.count()
        forma_choices = form.fields['forma_pagamento'].queryset.count()
        
        print(f"\n🎯 Opções no formulário:")
        print(f"   - Clientes disponíveis: {cliente_choices}")
        print(f"   - Faixas de preço disponíveis: {faixa_choices}")
        print(f"   - Formas de pagamento disponíveis: {forma_choices}")
        
        if cliente_choices > 0 and faixa_choices > 0 and forma_choices > 0:
            print("\n✅ SUCESSO: Formulário está funcionando corretamente!")
            print("🎉 Você pode criar orçamentos agora!")
        else:
            print("\n⚠️  AVISO: Algum campo não tem opções disponíveis")
            if cliente_choices == 0:
                print("   - Nenhum cliente encontrado")
            if faixa_choices == 0:
                print("   - Nenhuma faixa de preço ativa")
            if forma_choices == 0:
                print("   - Nenhuma forma de pagamento ativa")
        
    except Exception as e:
        print(f"❌ Erro: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
