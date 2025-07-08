#!/usr/bin/env python3
"""
Script para testar o fluxo completo de CRUD do sofá LE COULTRE - SF939
Testa: visualização, edição, criação de módulos adicionais e exclusão
"""

import os
import sys
import django
from decimal import Decimal

# Configurar Django
sys.path.append('/home/matas/projetos/Project')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema_produtos.settings')
django.setup()

from produtos.models import Produto, Modulo, TamanhosModulosDetalhado

def testar_visualizacao_produto():
    """Testa se o produto pode ser visualizado corretamente"""
    print("📋 Testando visualização do produto...")
    
    try:
        produto = Produto.objects.get(ref_produto='SF939')
        print(f"✅ Produto encontrado: {produto.nome_produto}")
        print(f"   - Referência: {produto.ref_produto}")
        print(f"   - Tipo: {produto.id_tipo_produto.nome}")
        print(f"   - Status: {'Ativo' if produto.ativo else 'Inativo'}")
        print(f"   - Imagem principal: {produto.imagem_principal}")
        
        # Verificar módulos
        modulos = produto.modulos.all()
        print(f"   - Módulos: {modulos.count()}")
        
        for modulo in modulos:
            tamanhos = modulo.tamanhos_detalhados.all()
            print(f"     * {modulo.nome}: {tamanhos.count()} tamanhos")
            
            for tamanho in tamanhos:
                print(f"       - {tamanho.largura_total}cm: R$ {tamanho.preco}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro na visualização: {str(e)}")
        return False

def testar_edicao_produto():
    """Testa se o produto pode ser editado"""
    print("\n🔧 Testando edição do produto...")
    
    try:
        produto = Produto.objects.get(ref_produto='SF939')
        
        # Testar edição de campo simples
        descricao_original = produto.descricao
        produto.descricao = "Sofá modular Le Coultre modelo SF939 com 2 módulos - ATUALIZADO"
        produto.save()
        
        # Verificar se foi salvo
        produto.refresh_from_db()
        if "ATUALIZADO" in produto.descricao:
            print("✅ Edição de descrição funcionando")
        else:
            print("❌ Erro na edição de descrição")
            return False
        
        # Restaurar descrição original
        produto.descricao = descricao_original
        produto.save()
        
        return True
        
    except Exception as e:
        print(f"❌ Erro na edição: {str(e)}")
        return False

def testar_adicao_modulo():
    """Testa se é possível adicionar um novo módulo"""
    print("\n➕ Testando adição de novo módulo...")
    
    try:
        produto = Produto.objects.get(ref_produto='SF939')
        
        # Contar módulos antes
        count_antes = produto.modulos.count()
        
        # Criar módulo temporário para teste
        modulo_teste = Modulo(
            produto=produto,
            nome='MÓDULO TESTE',
            profundidade=Decimal('90'),
            altura=Decimal('85'),
            descricao='Módulo criado para teste'
        )
        modulo_teste.save()
        
        # Verificar se foi criado
        count_depois = produto.modulos.count()
        if count_depois == count_antes + 1:
            print("✅ Adição de módulo funcionando")
        else:
            print("❌ Erro na adição de módulo")
            return False
        
        # Remover módulo de teste
        modulo_teste.delete()
        
        return True
        
    except Exception as e:
        print(f"❌ Erro na adição de módulo: {str(e)}")
        return False

def testar_adicao_tamanho():
    """Testa se é possível adicionar um novo tamanho a um módulo"""
    print("\n📏 Testando adição de novo tamanho...")
    
    try:
        produto = Produto.objects.get(ref_produto='SF939')
        modulo = produto.modulos.first()
        
        # Contar tamanhos antes
        count_antes = modulo.tamanhos_detalhados.count()
        
        # Criar tamanho temporário para teste
        tamanho_teste = TamanhosModulosDetalhado(
            id_modulo=modulo,
            largura_total=Decimal('200'),
            largura_assento=Decimal('80'),
            tecido_metros=Decimal('10.0'),
            volume_m3=Decimal('2.0'),
            peso_kg=Decimal('50'),
            preco=Decimal('4000.00'),
            descricao='Tamanho criado para teste'
        )
        tamanho_teste.save()
        
        # Verificar se foi criado
        count_depois = modulo.tamanhos_detalhados.count()
        if count_depois == count_antes + 1:
            print("✅ Adição de tamanho funcionando")
        else:
            print("❌ Erro na adição de tamanho")
            return False
        
        # Remover tamanho de teste
        tamanho_teste.delete()
        
        return True
        
    except Exception as e:
        print(f"❌ Erro na adição de tamanho: {str(e)}")
        return False

def testar_integridade_relacoes():
    """Testa se as relações entre produto, módulos e tamanhos estão corretas"""
    print("\n🔗 Testando integridade das relações...")
    
    try:
        produto = Produto.objects.get(ref_produto='SF939')
        
        # Verificar relacionamentos
        modulos = produto.modulos.all()
        print(f"   - Produto tem {modulos.count()} módulos")
        
        total_tamanhos = 0
        for modulo in modulos:
            tamanhos = modulo.tamanhos_detalhados.all()
            total_tamanhos += tamanhos.count()
            print(f"   - Módulo '{modulo.nome}' tem {tamanhos.count()} tamanhos")
            
            # Verificar se cada tamanho tem referência correta ao módulo
            for tamanho in tamanhos:
                if tamanho.id_modulo != modulo:
                    print(f"❌ Erro: Tamanho {tamanho.id} tem referência incorreta")
                    return False
        
        print(f"   - Total de tamanhos: {total_tamanhos}")
        
        # Verificar se todos os módulos têm referência correta ao produto
        for modulo in modulos:
            if modulo.produto != produto:
                print(f"❌ Erro: Módulo {modulo.id} tem referência incorreta")
                return False
        
        print("✅ Integridade das relações verificada")
        return True
        
    except Exception as e:
        print(f"❌ Erro na verificação de integridade: {str(e)}")
        return False

def testar_valores_calculos():
    """Testa se os valores e cálculos estão corretos"""
    print("\n🧮 Testando valores e cálculos...")
    
    try:
        produto = Produto.objects.get(ref_produto='SF939')
        
        # Verificar se todos os tamanhos têm preços
        for modulo in produto.modulos.all():
            for tamanho in modulo.tamanhos_detalhados.all():
                if not tamanho.preco:
                    print(f"❌ Erro: Tamanho {tamanho.id} sem preço")
                    return False
                
                if tamanho.preco <= 0:
                    print(f"❌ Erro: Tamanho {tamanho.id} com preço inválido")
                    return False
        
        # Verificar se as dimensões fazem sentido
        for modulo in produto.modulos.all():
            for tamanho in modulo.tamanhos_detalhados.all():
                if tamanho.largura_total <= 0:
                    print(f"❌ Erro: Tamanho {tamanho.id} com largura inválida")
                    return False
                
                if tamanho.largura_assento and tamanho.largura_assento >= tamanho.largura_total:
                    print(f"❌ Erro: Largura do assento maior que largura total")
                    return False
        
        print("✅ Valores e cálculos verificados")
        return True
        
    except Exception as e:
        print(f"❌ Erro na verificação de valores: {str(e)}")
        return False

def executar_todos_testes():
    """Executa todos os testes do fluxo CRUD"""
    print("🧪 INICIANDO BATERIA DE TESTES COMPLETA")
    print("="*60)
    
    testes = [
        ('Visualização', testar_visualizacao_produto),
        ('Edição', testar_edicao_produto),
        ('Adição de Módulo', testar_adicao_modulo),
        ('Adição de Tamanho', testar_adicao_tamanho),
        ('Integridade das Relações', testar_integridade_relacoes),
        ('Valores e Cálculos', testar_valores_calculos),
    ]
    
    resultados = []
    
    for nome, funcao in testes:
        try:
            resultado = funcao()
            resultados.append((nome, resultado))
        except Exception as e:
            print(f"❌ Erro crítico em {nome}: {str(e)}")
            resultados.append((nome, False))
    
    # Resumo dos resultados
    print("\n" + "="*60)
    print("📊 RESUMO DOS TESTES")
    print("="*60)
    
    sucessos = 0
    falhas = 0
    
    for nome, resultado in resultados:
        status = "✅ PASSOU" if resultado else "❌ FALHOU"
        print(f"{status} - {nome}")
        
        if resultado:
            sucessos += 1
        else:
            falhas += 1
    
    print(f"\n📈 ESTATÍSTICAS:")
    print(f"   - Testes executados: {len(resultados)}")
    print(f"   - Sucessos: {sucessos}")
    print(f"   - Falhas: {falhas}")
    print(f"   - Taxa de sucesso: {(sucessos/len(resultados)*100):.1f}%")
    
    if falhas == 0:
        print("\n🎉 TODOS OS TESTES PASSARAM!")
        print("✅ O sofá LE COULTRE - SF939 está funcionando perfeitamente!")
    else:
        print(f"\n⚠️  {falhas} TESTE(S) FALHARAM!")
        print("🔧 Revise os logs acima para identificar os problemas.")
    
    return falhas == 0

if __name__ == '__main__':
    print("🧪 Sistema de Testes - Sofá LE COULTRE SF939")
    print("📋 Testando fluxo completo de CRUD")
    print("-" * 60)
    
    sucesso_geral = executar_todos_testes()
    
    if sucesso_geral:
        print("\n🎯 TODOS OS TESTES FORAM CONCLUÍDOS COM SUCESSO!")
        sys.exit(0)
    else:
        print("\n❌ ALGUNS TESTES FALHARAM!")
        sys.exit(1)
