#!/usr/bin/env python
"""
Script CORRIGIDO para cadastrar acessórios do BIG BOSS como Item (produtos)
para que apareçam na listagem principal da interface
"""

import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema_produtos.settings')
django.setup()

from produtos.models import Item, TipoItem

def cadastrar_acessorios_como_produtos():
    """Cadastra os acessórios como produtos (Item) para aparecerem na listagem"""
    
    print("🔧 CADASTRANDO ACESSÓRIOS COMO PRODUTOS")
    print("=" * 60)
    
    # Buscar o tipo "Acessórios"
    try:
        tipo_acessorios = TipoItem.objects.get(nome="Acessórios")
        print(f"✓ Tipo 'Acessórios' encontrado (ID: {tipo_acessorios.id})")
    except TipoItem.DoesNotExist:
        print("❌ Tipo 'Acessórios' não encontrado!")
        return False
    
    # Buscar o produto BIG BOSS para vinculação
    try:
        big_boss = Item.objects.get(nome_produto__icontains='BIG BOSS')
        print(f"✓ Produto BIG BOSS encontrado: {big_boss.nome_produto} (ID: {big_boss.id})")
    except Item.DoesNotExist:
        print("❌ Produto BIG BOSS não encontrado!")
        return False
    
    # Dados dos acessórios da imagem
    acessorios_dados = [
        {"referencia": "AC 45", "nome": "Luminária", "valor": 525.00},
        {"referencia": "AC 48", "nome": "Torre USB", "valor": 641.00},
        {"referencia": "AC 56", "nome": "Porta Copos", "valor": 55.00},
        {"referencia": "AC 600", "nome": "AUTOMAÇÃO ASSENTO TOUCH (POR MÓDULO)", "valor": 2062.00},
        {"referencia": "AC 601", "nome": "AUTOMAÇÃO ASSENTO ALEXA (POR MÓDULO)", "valor": 2333.00},
    ]
    
    print(f"\n🔄 Iniciando cadastro de {len(acessorios_dados)} acessórios como produtos...")
    
    produtos_criados = []
    produtos_existentes = []
    
    for dados in acessorios_dados:
        # Verificar se já existe um produto com esta referência
        produto_existente = Item.objects.filter(
            ref_produto=dados["referencia"]
        ).first()
        
        if produto_existente:
            print(f"⚠️  Produto já existe: {dados['referencia']} - {dados['nome']}")
            
            # Atualizar se necessário
            if produto_existente.id_tipo_produto != tipo_acessorios:
                produto_existente.id_tipo_produto = tipo_acessorios
                produto_existente.save()
                print(f"   ✓ Tipo atualizado para 'Acessórios'")
            
            # Verificar se já está vinculado ao BIG BOSS
            if big_boss in produto_existente.produtos_vinculados.all():
                print(f"   ✓ Já vinculado ao BIG BOSS")
            else:
                produto_existente.produtos_vinculados.add(big_boss)
                print(f"   ✓ Vinculado ao BIG BOSS")
            
            produtos_existentes.append(produto_existente)
            continue
        
        # Criar novo produto/acessório
        try:
            novo_produto = Item.objects.create(
                ref_produto=dados["referencia"],
                nome_produto=dados["nome"],
                id_tipo_produto=tipo_acessorios,
                ativo=True,
                preco_acessorio=dados["valor"],
                # Campos específicos de sofás devem ser False para acessórios
                tem_cor_tecido=False,
                tem_difer_desenho_lado_dir_esq=False,
                tem_difer_desenho_tamanho=False
            )
            
            # Vincular ao produto BIG BOSS
            novo_produto.produtos_vinculados.add(big_boss)
            
            print(f"✓ Criado: {novo_produto.ref_produto} - {novo_produto.nome_produto} - R$ {novo_produto.preco_acessorio}")
            produtos_criados.append(novo_produto)
            
        except Exception as e:
            print(f"✗ Erro ao criar produto {dados['referencia']}: {str(e)}")
    
    # Relatório final
    print(f"\n📊 RELATÓRIO FINAL:")
    print(f"   • Produtos criados: {len(produtos_criados)}")
    print(f"   • Produtos já existentes: {len(produtos_existentes)}")
    
    # Verificar listagem atual
    acessorios_na_listagem = Item.objects.filter(id_tipo_produto=tipo_acessorios)
    print(f"   • Total de acessórios na listagem: {acessorios_na_listagem.count()}")
    
    if produtos_criados:
        print(f"\n📝 IDs dos novos produtos criados:")
        for produto in produtos_criados:
            print(f"   • ID {produto.id}: {produto.ref_produto} - {produto.nome_produto}")
    
    print(f"\n🌐 Verificar em: http://localhost:8000/produtos/")
    
    return True

def listar_acessorios_na_interface():
    """Lista como os acessórios aparecerão na interface"""
    try:
        tipo_acessorios = TipoItem.objects.get(nome="Acessórios")
        acessorios = Item.objects.filter(id_tipo_produto=tipo_acessorios).order_by('ref_produto')
        
        print(f"\n📋 ACESSÓRIOS NA LISTAGEM PRINCIPAL:")
        print("=" * 80)
        print("REF     | NOME                                | PREÇO      | STATUS")
        print("-" * 80)
        
        for acessorio in acessorios:
            preco_str = f"R$ {acessorio.preco_acessorio:8.2f}" if acessorio.preco_acessorio else "N/A"
            status = "Ativo" if acessorio.ativo else "Inativo"
            print(f"{acessorio.ref_produto:7s} | {acessorio.nome_produto:35s} | {preco_str:10s} | {status}")
        
        print("=" * 80)
        print(f"Total: {acessorios.count()} acessórios")
        
    except TipoItem.DoesNotExist:
        print("❌ Tipo 'Acessórios' não encontrado!")

def remover_acessorios_duplicados():
    """Remove os acessórios do modelo Acessorio para evitar duplicação"""
    from produtos.models import Acessorio
    
    print(f"\n🗑️  LIMPEZA DE DUPLICADOS:")
    print("-" * 40)
    
    acessorios_antigos = Acessorio.objects.all()
    
    if acessorios_antigos.exists():
        print(f"Encontrados {acessorios_antigos.count()} acessórios no modelo antigo")
        
        resposta = input("Deseja remover os acessórios do modelo antigo? (s/N): ").lower()
        if resposta == 's':
            count = acessorios_antigos.count()
            acessorios_antigos.delete()
            print(f"✓ {count} acessórios removidos do modelo antigo")
        else:
            print("⚠️  Acessórios mantidos (pode haver duplicação)")
    else:
        print("✓ Nenhum acessório duplicado encontrado")

if __name__ == "__main__":
    # Cadastrar acessórios como produtos
    sucesso = cadastrar_acessorios_como_produtos()
    
    if sucesso:
        # Mostrar como ficará na listagem
        listar_acessorios_na_interface()
        
        # Opção de limpeza
        remover_acessorios_duplicados()
        
        print(f"\n✅ Script executado com sucesso!")
        print(f"🌐 Acesse http://localhost:8000/produtos/ para ver os acessórios na listagem")
    else:
        print(f"\n❌ Script falhou!")
        sys.exit(1)
