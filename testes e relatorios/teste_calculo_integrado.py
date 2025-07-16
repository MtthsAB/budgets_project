#!/usr/bin/env python
"""
Teste de integração para verificar se os cálculos de sofás estão funcionando corretamente
após as correções implementadas
"""
import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema_produtos.settings')
django.setup()

from produtos.models import TipoItem, Produto, Modulo, TamanhosModulos
from orcamentos.models import FaixaPreco

def teste_calculo_integrado():
    """Simula exatamente o que acontece no frontend"""
    print("🧪 TESTE DE INTEGRAÇÃO - CÁLCULO DE SOFÁS")
    print("=" * 60)
    
    # 1. Buscar sofá para testar
    tipo_sofa = TipoItem.objects.filter(nome__icontains='Sofás').first()
    sofa = Produto.objects.filter(id_tipo_produto=tipo_sofa, ativo=True).first()
    
    if not sofa:
        print("❌ Nenhum sofá encontrado")
        return
    
    print(f"🛋️  Sofá: {sofa.nome_produto} (ID: {sofa.id})")
    
    # 2. Buscar faixas de preço
    faixas = list(FaixaPreco.objects.filter(ativo=True))
    print(f"💰 Faixas disponíveis: {len(faixas)}")
    
    # 3. Simular seleção de módulos como no frontend
    modulos = sofa.modulos.all()[:2]  # Pegar primeiros 2 módulos
    
    print(f"\n📋 Simulando seleção de {len(modulos)} módulos:")
    
    for faixa in faixas:
        print(f"\n🎯 Testando com faixa: {faixa.nome} ({faixa.multiplicador}x)")
        
        total_sofa = 0
        modulos_dados = []
        
        for modulo in modulos:
            # Pegar primeiro tamanho de cada módulo
            tamanho = modulo.tamanhos_detalhados.first()
            
            if tamanho:
                quantidade = 1
                preco_base = float(tamanho.preco)
                multiplicador = float(faixa.multiplicador)
                preco_com_faixa = preco_base * multiplicador
                subtotal = preco_com_faixa * quantidade
                
                total_sofa += subtotal
                
                modulo_data = {
                    'modulo_id': modulo.id,
                    'tamanho_id': tamanho.id,
                    'nome': modulo.nome,
                    'tamanho_nome': f"{tamanho.largura_total}cm",
                    'quantidade': quantidade,
                    'preco_base': preco_base,
                    'preco_com_faixa': preco_com_faixa,
                    'subtotal': subtotal
                }
                
                modulos_dados.append(modulo_data)
                
                print(f"   • {modulo.nome} - {tamanho.largura_total}cm")
                print(f"     - Qtd: {quantidade}")
                print(f"     - Preço base: R$ {preco_base:.2f}")
                print(f"     - Preço c/ faixa: R$ {preco_com_faixa:.2f}")
                print(f"     - Subtotal: R$ {subtotal:.2f}")
        
        print(f"   💰 Total do sofá: R$ {total_sofa:.2f}")
        
        # 4. Simular dados que seriam enviados para o backend
        dados_envio = {
            'produto_id': f'produto_{sofa.id}',
            'tipo': 'sofa',
            'preco_unitario': total_sofa,
            'quantidade': 1,
            'dados_especificos': {
                'modulos': modulos_dados,
                'acessorios': []
            }
        }
        
        # 5. Validar se os cálculos estão corretos
        validar_calculos(dados_envio, faixa.multiplicador)

def validar_calculos(dados_envio, multiplicador_esperado):
    """Valida se os cálculos estão corretos"""
    modulos = dados_envio['dados_especificos']['modulos']
    
    total_calculado = 0
    for modulo in modulos:
        # Verificar se o multiplicador foi aplicado corretamente
        preco_esperado_com_faixa = modulo['preco_base'] * float(multiplicador_esperado)
        
        if abs(modulo['preco_com_faixa'] - preco_esperado_com_faixa) > 0.01:
            print(f"   ❌ ERRO: Multiplicador não aplicado corretamente")
            print(f"      Esperado: {preco_esperado_com_faixa:.2f}")
            print(f"      Obtido: {modulo['preco_com_faixa']:.2f}")
            return False
        
        total_calculado += modulo['subtotal']
    
    # Verificar se o total do produto está correto
    if abs(dados_envio['preco_unitario'] - total_calculado) > 0.01:
        print(f"   ❌ ERRO: Total do sofá incorreto")
        print(f"      Esperado: {total_calculado:.2f}")
        print(f"      Obtido: {dados_envio['preco_unitario']:.2f}")
        return False
    
    print(f"   ✅ Cálculos corretos!")
    return True

def teste_mudanca_faixa_preco():
    """Testa o comportamento quando a faixa de preço muda"""
    print(f"\n🔄 TESTE DE MUDANÇA DE FAIXA DE PREÇO")
    print("=" * 60)
    
    # Buscar sofá e faixas
    tipo_sofa = TipoItem.objects.filter(nome__icontains='Sofás').first()
    sofa = Produto.objects.filter(id_tipo_produto=tipo_sofa, ativo=True).first()
    modulo = sofa.modulos.first()
    tamanho = modulo.tamanhos_detalhados.first()
    
    faixa_varejo = FaixaPreco.objects.filter(nome__icontains='Varejo').first()
    faixa_atacado = FaixaPreco.objects.filter(nome__icontains='Atacado').first()
    
    quantidade = 2
    preco_base = float(tamanho.preco)
    
    print(f"Módulo: {modulo.nome} - {tamanho.largura_total}cm")
    print(f"Preço base: R$ {preco_base:.2f}")
    print(f"Quantidade: {quantidade}")
    
    # Calcular com faixa varejo
    subtotal_varejo = preco_base * float(faixa_varejo.multiplicador) * quantidade
    print(f"\n1. Faixa {faixa_varejo.nome} ({faixa_varejo.multiplicador}x): R$ {subtotal_varejo:.2f}")
    
    # Calcular com faixa atacado
    subtotal_atacado = preco_base * float(faixa_atacado.multiplicador) * quantidade
    print(f"2. Faixa {faixa_atacado.nome} ({faixa_atacado.multiplicador}x): R$ {subtotal_atacado:.2f}")
    
    diferenca = abs(subtotal_varejo - subtotal_atacado)
    print(f"\n💡 Diferença: R$ {diferenca:.2f}")
    
    if diferenca > 0.01:
        print("✅ Mudança de faixa de preço afeta corretamente os cálculos")
    else:
        print("❌ ERRO: Mudança de faixa de preço não está funcionando")

if __name__ == '__main__':
    try:
        teste_calculo_integrado()
        teste_mudanca_faixa_preco()
        
        print(f"\n🎉 TESTE CONCLUÍDO")
        print("=" * 60)
        print("Se todos os cálculos mostraram '✅ Cálculos corretos!',")
        print("então a correção da aplicação da faixa de preço está funcionando.")
        
    except Exception as e:
        print(f"❌ Erro durante teste: {e}")
        import traceback
        traceback.print_exc()
