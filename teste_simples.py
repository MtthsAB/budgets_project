#!/usr/bin/env python
import os
import sys
import django

# Adicionar o diretório do projeto ao path
sys.path.append('/home/matas/projetos/Project')

# Configurar o Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema_produtos.settings')
django.setup()

from produtos.models import Item, TipoItem, Modulo, TamanhosModulosDetalhado

def teste_rapido():
    """Teste rápido da funcionalidade"""
    
    print("=== Teste Rápido de Funcionalidade ===")
    
    # Buscar produto existente
    produto = Item.objects.first()
    if not produto:
        print("❌ Nenhum produto encontrado")
        return
    
    print(f"Produto encontrado: {produto.ref_produto} - {produto.nome_produto}")
    print(f"Módulos atuais: {produto.modulos.count()}")
    
    # Mostrar módulos atuais
    for modulo in produto.modulos.all():
        print(f"  - {modulo.nome} (Tamanhos: {modulo.tamanhos_detalhados.count()})")
    
    # Simular adição de módulo
    try:
        novo_modulo = Modulo.objects.create(
            item=produto,
            nome='Módulo Teste Edição',
            profundidade=85.0,
            altura=80.0,
            braco=25.0,
            descricao='Módulo criado para teste da edição'
        )
        print(f"✅ Módulo criado: {novo_modulo.nome}")
        
        # Adicionar tamanho ao módulo
        novo_tamanho = TamanhosModulosDetalhado.objects.create(
            id_modulo=novo_modulo,
            nome_tamanho='Teste Edição',
            largura_total=170.0,
            altura_cm=80.0,
            profundidade_cm=85.0,
            preco=1199.99,
            descricao='Tamanho criado para teste'
        )
        print(f"✅ Tamanho criado: {novo_tamanho.nome_tamanho}")
        
        # Verificar se foi salvo
        produto_atualizado = Item.objects.get(id=produto.id)
        print(f"✅ Produto após adição: {produto_atualizado.modulos.count()} módulos")
        
        # Listar todos os módulos
        for i, modulo in enumerate(produto_atualizado.modulos.all(), 1):
            print(f"  Módulo {i}: {modulo.nome}")
            for j, tamanho in enumerate(modulo.tamanhos_detalhados.all(), 1):
                print(f"    Tamanho {j}: {tamanho.nome_tamanho} - R${tamanho.preco}")
        
        print("✅ Teste de edição/adição funcionando corretamente!")
        return True
        
    except Exception as e:
        print(f"❌ Erro no teste: {str(e)}")
        return False

if __name__ == '__main__':
    teste_rapido()
