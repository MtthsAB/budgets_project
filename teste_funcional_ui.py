#!/usr/bin/env python3
"""
Script para teste funcional das melhorias implementadas.
Cria um produto de teste para verificar se tudo funciona corretamente.
"""

import os
import django
from django.conf import settings

# Configura o Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema_produtos.settings')
django.setup()

from produtos.models import Item, TipoItem

def criar_produto_teste():
    """Cria um produto de teste sem imagens para verificar se funciona"""
    print("🧪 Testando criação de produto sem imagens...")
    
    try:
        # Verifica se já existe um tipo de produto
        tipo_produto, created = TipoItem.objects.get_or_create(
            nome="Teste",
            defaults={"nome": "Teste"}
        )
        
        if created:
            print("✅ Tipo de produto 'Teste' criado")
        else:
            print("✅ Tipo de produto 'Teste' já existe")
        
        # Cria um produto sem imagens (testando se são realmente opcionais)
        produto_teste = Item.objects.create(
            ref_produto="TEST_UI_001",
            nome_produto="Produto Teste UI/UX",
            id_tipo_produto=tipo_produto,
            ativo=True,
            tem_cor_tecido=False,
            tem_difer_desenho_lado_dir_esq=False,
            tem_difer_desenho_tamanho=False,
            # Propositalmente não definindo imagens para testar se são opcionais
        )
        
        print(f"✅ Produto criado com sucesso: {produto_teste.ref_produto}")
        print(f"   Nome: {produto_teste.nome_produto}")
        print(f"   Imagem Principal: {produto_teste.imagem_principal or 'Não definida (OK)'}")
        print(f"   Imagem Secundária: {produto_teste.imagem_secundaria or 'Não definida (OK)'}")
        
        return produto_teste
        
    except Exception as e:
        print(f"❌ Erro ao criar produto teste: {e}")
        return None

def testar_edicao_produto(produto):
    """Testa se é possível editar um produto sem forçar imagens"""
    if not produto:
        return
    
    print("\n🔧 Testando edição de produto...")
    
    try:
        # Edita o produto
        produto.nome_produto = "Produto Teste UI/UX - EDITADO"
        produto.save()
        
        print("✅ Produto editado com sucesso sem problemas com imagens")
        
    except Exception as e:
        print(f"❌ Erro ao editar produto: {e}")

def cleanup_teste():
    """Remove dados de teste"""
    print("\n🧹 Limpando dados de teste...")
    
    try:
        # Remove produtos de teste
        produtos_removidos = Item.objects.filter(ref_produto__startswith="TEST_UI_").delete()
        print(f"✅ {produtos_removidos[0]} produtos de teste removidos")
        
        # Remove tipo de teste se não há outros produtos
        tipo_teste = TipoItem.objects.filter(nome="Teste").first()
        if tipo_teste and not Item.objects.filter(id_tipo_produto=tipo_teste).exists():
            tipo_teste.delete()
            print("✅ Tipo de produto 'Teste' removido")
        
    except Exception as e:
        print(f"❌ Erro ao limpar dados de teste: {e}")

if __name__ == '__main__':
    print("🚀 TESTE FUNCIONAL DAS MELHORIAS")
    print("🎯 Verificando se produtos podem ser criados sem imagens")
    print("=" * 60)
    
    # Teste completo
    produto = criar_produto_teste()
    testar_edicao_produto(produto)
    
    print("\n" + "=" * 60)
    resposta = input("Deseja remover os dados de teste? (s/N): ").lower()
    if resposta in ['s', 'sim', 'y', 'yes']:
        cleanup_teste()
    else:
        print("📝 Dados de teste mantidos. Você pode acessá-los na interface web.")
    
    print("\n✨ Teste funcional concluído!")
    print("🌐 Acesse http://127.0.0.1:8000/produtos/ para ver os resultados.")
