#!/usr/bin/env python
"""
Teste completo de sofás com módulos e cálculos
"""
import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema_produtos.settings')
django.setup()

from produtos.models import TipoItem, Produto, Modulo, TamanhosModulos
from orcamentos.models import FaixaPreco

def testar_sofas_completo():
    """Teste completo de sofás e seus módulos"""
    print("🛋️  TESTE COMPLETO DE SOFÁS")
    print("=" * 50)
    
    # 1. Buscar sofás disponíveis
    tipo_sofa = TipoItem.objects.filter(nome__icontains='Sofás').first()
    if not tipo_sofa:
        print("❌ Tipo 'Sofás' não encontrado")
        return
    
    sofas = Produto.objects.filter(id_tipo_produto=tipo_sofa, ativo=True)
    print(f"📊 Sofás disponíveis: {sofas.count()}")
    
    for sofa in sofas:
        print(f"\n🛋️  {sofa.nome_produto} (ID: {sofa.id})")
        print(f"   - Referência: {sofa.ref_produto}")
        # Produtos não têm preço direto, vem dos módulos
        
        # Buscar módulos
        modulos = sofa.modulos.all()
        print(f"   - Módulos: {modulos.count()}")
        
        for modulo in modulos:
            print(f"      • {modulo.nome}")
            print(f"        - Descrição: {modulo.descricao}")
            # Preço está nos tamanhos, não no módulo
            
            # Buscar tamanhos do módulo
            tamanhos = modulo.tamanhos_detalhados.all()
            print(f"        - Tamanhos: {tamanhos.count()}")
            
            for tamanho in tamanhos:
                print(f"          · {tamanho.largura_total}cm - R$ {tamanho.preco:.2f}")
    
    return sofas

def testar_calculo_sofa_com_faixa():
    """Testa cálculo de sofá aplicando faixa de preço"""
    print("\n💰 TESTE DE CÁLCULO COM FAIXA DE PREÇO")
    print("=" * 50)
    
    # Buscar primeiro sofá com módulos
    tipo_sofa = TipoItem.objects.filter(nome__icontains='Sofás').first()
    sofa = Produto.objects.filter(id_tipo_produto=tipo_sofa, ativo=True).first()
    
    if not sofa:
        print("❌ Nenhum sofá encontrado")
        return
    
    print(f"Sofá: {sofa.nome_produto}")
    
    # Buscar módulos e tamanhos
    modulo = sofa.modulos.first()
    if not modulo:
        print("❌ Nenhum módulo encontrado")
        return
    
    print(f"Módulo: {modulo.nome}")
    
    tamanho = modulo.tamanhos_detalhados.first()
    if not tamanho:
        print("❌ Nenhum tamanho encontrado")
        return
    
    print(f"Tamanho: {tamanho.largura_total}cm - R$ {tamanho.preco:.2f}")
    
    # Testar com diferentes faixas de preço
    faixas = FaixaPreco.objects.filter(ativo=True)
    print(f"\n🎯 Testando com {faixas.count()} faixas de preço:")
    
    quantidade = 2
    print(f"Quantidade: {quantidade}")
    
    for faixa in faixas:
        preco_base = tamanho.preco
        preco_com_faixa = preco_base * faixa.multiplicador
        subtotal = preco_com_faixa * quantidade
        
        print(f"  • {faixa.nome} ({faixa.multiplicador}x):")
        print(f"    - Preço base: R$ {preco_base:.2f}")
        print(f"    - Preço c/ faixa: R$ {preco_com_faixa:.2f}")
        print(f"    - Subtotal: R$ {subtotal:.2f}")

def simular_selecao_frontend():
    """Simula a seleção que seria feita no frontend"""
    print("\n🖥️  SIMULAÇÃO DE SELEÇÃO FRONTEND")
    print("=" * 50)
    
    # Buscar dados como o frontend faria
    tipo_sofa = TipoItem.objects.filter(nome__icontains='Sofás').first()
    sofa = Produto.objects.filter(id_tipo_produto=tipo_sofa, ativo=True).first()
    
    if not sofa:
        print("❌ Nenhum sofá encontrado")
        return
    
    print(f"Sofá selecionado: {sofa.nome_produto}")
    
    # Simular dados que seriam enviados pelo frontend
    modulos_selecionados = []
    
    # Pegar primeiro módulo com primeiro tamanho
    modulo = sofa.modulos.first()
    tamanho = modulo.tamanhos_detalhados.first() if modulo else None
    
    if modulo and tamanho:
        # Aplicar faixa de preço "Varejo" (1.0x)
        faixa_varejo = FaixaPreco.objects.filter(nome__icontains='Varejo').first()
        multiplicador = faixa_varejo.multiplicador if faixa_varejo else 1.0
        
        quantidade = 1
        preco_base = tamanho.preco
        preco_com_faixa = preco_base * multiplicador
        subtotal = preco_com_faixa * quantidade
        
        modulo_data = {
            'modulo_id': modulo.id,
            'tamanho_id': tamanho.id,
            'quantidade': quantidade,
            'preco_base': preco_base,
            'preco_com_faixa': preco_com_faixa,
            'subtotal': subtotal,
            'nome': modulo.nome
        }
        
        modulos_selecionados.append(modulo_data)
        
        print(f"Módulo: {modulo.nome}")
        print(f"Tamanho: {tamanho.largura_total}cm")
        print(f"Quantidade: {quantidade}")
        print(f"Preço base: R$ {preco_base:.2f}")
        print(f"Multiplicador faixa: {multiplicador}")
        print(f"Preço com faixa: R$ {preco_com_faixa:.2f}")
        print(f"Subtotal: R$ {subtotal:.2f}")
    
    # Calcular total geral
    total_sofa = sum(m['subtotal'] for m in modulos_selecionados)
    print(f"\n💰 Total do sofá: R$ {total_sofa:.2f}")
    
    return {
        'produto_id': f'produto_{sofa.id}',
        'tipo': 'sofa',
        'preco_unitario': total_sofa,
        'dados_especificos': {
            'modulos': modulos_selecionados,
            'acessorios': []
        }
    }

if __name__ == '__main__':
    try:
        sofas = testar_sofas_completo()
        if sofas and sofas.count() > 0:
            testar_calculo_sofa_com_faixa()
            dados_simulacao = simular_selecao_frontend()
            print(f"\n📋 Dados para envio: {dados_simulacao}")
        else:
            print("❌ Não há sofás suficientes para teste")
            
    except Exception as e:
        print(f"❌ Erro durante teste: {e}")
        import traceback
        traceback.print_exc()
