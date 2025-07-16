#!/usr/bin/env python3
"""
Script para testar se os acessórios estão corretamente vinculados aos sofás
e verificar a estrutura de dados retornada pela API
"""

import os
import sys
import django

# Configuração do Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema_produtos.settings')
django.setup()

from produtos.models import Produto, Acessorio, Modulo

def verificar_acessorios_vinculados():
    """Verifica quais acessórios estão vinculados aos sofás"""
    
    print("=== VERIFICAÇÃO DE ACESSÓRIOS VINCULADOS AOS SOFÁS ===\n")
    
    # Buscar todos os sofás
    sofas = Produto.objects.filter(id_tipo_produto__nome__icontains='sofá', ativo=True)
    print(f"📊 Total de sofás ativos: {sofas.count()}")
    
    if not sofas.exists():
        print("❌ Nenhum sofá encontrado!")
        return
    
    # Verificar cada sofá
    for sofa in sofas:
        print(f"\n🛋️  Sofá: {sofa.ref_produto} - {sofa.nome_produto}")
        print(f"    ID: {sofa.id}")
        
        # Buscar módulos
        modulos = sofa.modulos.all()
        print(f"    📦 Módulos: {modulos.count()}")
        for modulo in modulos:
            tamanhos = modulo.tamanhos_detalhados.all()
            print(f"        - {modulo.nome} ({tamanhos.count()} tamanhos)")
        
        # Buscar acessórios vinculados
        acessorios_vinculados = Acessorio.objects.filter(produtos_vinculados=sofa, ativo=True)
        print(f"    🎨 Acessórios vinculados: {acessorios_vinculados.count()}")
        
        if acessorios_vinculados.exists():
            for acessorio in acessorios_vinculados:
                preco_str = f"R$ {acessorio.preco:.2f}" if acessorio.preco else "Sem preço"
                print(f"        - {acessorio.ref_acessorio}: {acessorio.nome} ({preco_str})")
        else:
            print(f"        ⚠️  Nenhum acessório vinculado")
    
    print(f"\n=== VERIFICAÇÃO DE ACESSÓRIOS ÓRFÃOS ===")
    
    # Verificar acessórios sem produtos vinculados
    acessorios_sem_vinculo = []
    for acessorio in Acessorio.objects.filter(ativo=True):
        if acessorio.produtos_vinculados.count() == 0:
            acessorios_sem_vinculo.append(acessorio)
    
    if acessorios_sem_vinculo:
        print(f"⚠️  {len(acessorios_sem_vinculo)} acessórios sem produtos vinculados:")
        for acessorio in acessorios_sem_vinculo:
            print(f"    - {acessorio.ref_acessorio}: {acessorio.nome}")
    else:
        print("✅ Todos os acessórios têm produtos vinculados")

def simular_api_response():
    """Simula o que a API retorna para um sofá específico"""
    
    print(f"\n=== SIMULAÇÃO DA API RESPONSE ===")
    
    # Pegar o primeiro sofá
    sofa = Produto.objects.filter(id_tipo_produto__nome__icontains='sofá', ativo=True).first()
    if not sofa:
        print("❌ Nenhum sofá encontrado para simulação")
        return
    
    print(f"🎯 Simulando API response para: {sofa.ref_produto} - {sofa.nome_produto}")
    
    # Simular a estrutura de dados que seria retornada
    modulos = []
    for modulo in sofa.modulos.all():
        tamanhos = []
        for tamanho in modulo.tamanhos_detalhados.all():
            tamanhos.append({
                'id': tamanho.id,
                'largura_total': float(tamanho.largura_total) if tamanho.largura_total else 0,
                'preco': float(tamanho.preco) if tamanho.preco else 0.00,
                'descricao': tamanho.descricao or ''
            })
        
        modulos.append({
            'id': modulo.id,
            'nome': modulo.nome,
            'tamanhos': tamanhos
        })
    
    # Buscar acessórios vinculados
    acessorios_vinculados = []
    acessorios = Acessorio.objects.filter(produtos_vinculados=sofa, ativo=True)
    for acessorio in acessorios:
        acessorios_vinculados.append({
            'id': acessorio.id,
            'nome': acessorio.nome,
            'ref': acessorio.ref_acessorio,
            'preco': float(acessorio.preco) if acessorio.preco else 0.00,
            'descricao': acessorio.descricao or '',
            'imagem_principal': acessorio.imagem_principal.url if acessorio.imagem_principal else None
        })
    
    response_data = {
        'produto': {
            'id': sofa.id,
            'nome': sofa.nome_produto,
            'ref': sofa.ref_produto,
            'tipo': 'Sofá',
            'imagem_principal': sofa.imagem_principal.url if sofa.imagem_principal else None,
            'modulos': modulos,
            'acessorios_vinculados': acessorios_vinculados,
        }
    }
    
    print(f"\n📋 Estrutura simulada da API:")
    print(f"    Produto ID: {response_data['produto']['id']}")
    print(f"    Nome: {response_data['produto']['nome']}")
    print(f"    Módulos: {len(response_data['produto']['modulos'])}")
    print(f"    Acessórios vinculados: {len(response_data['produto']['acessorios_vinculados'])}")
    
    if response_data['produto']['acessorios_vinculados']:
        print(f"\n    Acessórios na response:")
        for acc in response_data['produto']['acessorios_vinculados']:
            print(f"        - ID {acc['id']}: {acc['nome']} (R$ {acc['preco']:.2f})")
    
    print(f"\n✅ Simulação concluída!")

if __name__ == "__main__":
    verificar_acessorios_vinculados()
    simular_api_response()
