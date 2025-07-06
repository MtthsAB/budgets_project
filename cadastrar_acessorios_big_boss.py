#!/usr/bin/env python
"""
Script para cadastrar acessórios do BIG BOSS baseado na imagem fornecida
Dados extraídos da imagem anexa com referências, nomes e valores
"""

import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema_produtos.settings')
django.setup()

from produtos.models import Item, Acessorio

def cadastrar_acessorios_big_boss():
    """Cadastra todos os acessórios do BIG BOSS conforme imagem"""
    
    # Buscar o produto BIG BOSS
    try:
        big_boss = Item.objects.get(nome_produto__icontains='BIG BOSS')
        print(f"✓ Produto encontrado: {big_boss.nome_produto} (ID: {big_boss.id})")
    except Item.DoesNotExist:
        print("✗ ERRO: Produto BIG BOSS não encontrado!")
        return False
    except Item.MultipleObjectsReturned:
        print("✗ ERRO: Múltiplos produtos BIG BOSS encontrados!")
        produtos = Item.objects.filter(nome_produto__icontains='BIG BOSS')
        for p in produtos:
            print(f"   - {p.nome_produto} (ID: {p.id})")
        return False

    # Dados dos acessórios extraídos da imagem
    acessorios_dados = [
        {"referencia": "AC 45", "nome": "Luminária", "valor": 525.00},
        {"referencia": "AC 48", "nome": "Torre USB", "valor": 641.00},
        {"referencia": "AC 56", "nome": "Porta Copos", "valor": 55.00},
        {"referencia": "AC 600", "nome": "AUTOMAÇÃO ASSENTO TOUCH (POR MÓDULO)", "valor": 2062.00},
        {"referencia": "AC 601", "nome": "AUTOMAÇÃO ASSENTO ALEXA (POR MÓDULO)", "valor": 2333.00},
    ]

    print(f"\n🔄 Iniciando cadastro de {len(acessorios_dados)} acessórios...")
    
    acessorios_criados = []
    acessorios_existentes = []
    
    for dados in acessorios_dados:
        # Verificar se o acessório já existe
        acessorio_existente = Acessorio.objects.filter(
            ref_acessorio=dados["referencia"]
        ).first()
        
        if acessorio_existente:
            print(f"⚠️  Acessório já existe: {dados['referencia']} - {dados['nome']}")
            # Verificar se já está vinculado ao BIG BOSS
            if big_boss in acessorio_existente.produtos_vinculados.all():
                print(f"   ✓ Já vinculado ao BIG BOSS")
            else:
                acessorio_existente.produtos_vinculados.add(big_boss)
                print(f"   ✓ Vinculado ao BIG BOSS")
            acessorios_existentes.append(acessorio_existente)
            continue
        
        # Criar novo acessório
        try:
            novo_acessorio = Acessorio.objects.create(
                ref_acessorio=dados["referencia"],
                nome=dados["nome"],
                preco=dados["valor"]
            )
            
            # Vincular ao produto BIG BOSS
            novo_acessorio.produtos_vinculados.add(big_boss)
            
            print(f"✓ Criado: {novo_acessorio.ref_acessorio} - {novo_acessorio.nome} - R$ {novo_acessorio.preco}")
            acessorios_criados.append(novo_acessorio)
            
        except Exception as e:
            print(f"✗ Erro ao criar acessório {dados['referencia']}: {str(e)}")
    
    # Relatório final
    print(f"\n📊 RELATÓRIO FINAL:")
    print(f"   • Acessórios criados: {len(acessorios_criados)}")
    print(f"   • Acessórios já existentes: {len(acessorios_existentes)}")
    print(f"   • Total de acessórios vinculados ao BIG BOSS: {big_boss.acessorio_set.count()}")
    
    if acessorios_criados:
        print(f"\n📝 IDs dos novos acessórios criados:")
        for acessorio in acessorios_criados:
            print(f"   • ID {acessorio.id}: {acessorio.ref_acessorio} - {acessorio.nome}")
    
    return True

def listar_acessorios_big_boss():
    """Lista todos os acessórios vinculados ao BIG BOSS"""
    try:
        big_boss = Item.objects.get(nome_produto__icontains='BIG BOSS')
        acessorios = Acessorio.objects.filter(produtos_vinculados=big_boss).order_by('ref_acessorio')
        
        print(f"\n📋 ACESSÓRIOS DO {big_boss.nome_produto}:")
        print("=" * 80)
        
        for acessorio in acessorios:
            preco_str = f"R$ {acessorio.preco:8.2f}" if acessorio.preco else "N/A"
            print(f"ID {acessorio.id:3d} | {acessorio.ref_acessorio:6s} | {acessorio.nome:35s} | {preco_str}")
        
        print("=" * 80)
        print(f"Total: {acessorios.count()} acessórios")
        
    except Item.DoesNotExist:
        print("✗ Produto BIG BOSS não encontrado!")

if __name__ == "__main__":
    print("🚀 CADASTRO DE ACESSÓRIOS BIG BOSS")
    print("=" * 50)
    
    # Cadastrar acessórios
    sucesso = cadastrar_acessorios_big_boss()
    
    if sucesso:
        print("\n" + "=" * 50)
        # Listar todos os acessórios do BIG BOSS
        listar_acessorios_big_boss()
        
        print(f"\n✅ Script executado com sucesso!")
    else:
        print(f"\n❌ Script falhou!")
        sys.exit(1)
