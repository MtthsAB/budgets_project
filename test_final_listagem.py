#!/usr/bin/env python
"""
Teste final para validar se os acessórios estão aparecendo corretamente na listagem
"""

import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema_produtos.settings')
django.setup()

from produtos.models import Item, TipoItem

def test_acessorios_na_listagem():
    """Testa se os acessórios aparecem na listagem principal"""
    
    print("🧪 TESTE FINAL - ACESSÓRIOS NA LISTAGEM")
    print("=" * 60)
    
    # 1. Verificar se existem acessórios na listagem
    try:
        tipo_acessorios = TipoItem.objects.get(nome="Acessórios")
        acessorios = Item.objects.filter(id_tipo_produto=tipo_acessorios)
        
        print(f"✅ 1. Acessórios encontrados na listagem: {acessorios.count()}")
        
        # Referencias esperadas da imagem
        refs_esperadas = ["AC 45", "AC 48", "AC 56", "AC 600", "AC 601"]
        
        print(f"\n✅ 2. Verificando acessórios específicos da imagem:")
        todos_encontrados = True
        
        for ref in refs_esperadas:
            acessorio = acessorios.filter(ref_produto=ref).first()
            if acessorio:
                print(f"   ✓ {ref}: {acessorio.nome_produto} - R$ {acessorio.preco_acessorio}")
            else:
                print(f"   ❌ {ref}: NÃO ENCONTRADO!")
                todos_encontrados = False
        
        # 3. Verificar vinculação com BIG BOSS
        print(f"\n✅ 3. Verificando vinculação com BIG BOSS:")
        
        try:
            big_boss = Item.objects.get(nome_produto__icontains='BIG BOSS')
            
            for ref in refs_esperadas:
                acessorio = acessorios.filter(ref_produto=ref).first()
                if acessorio and big_boss in acessorio.produtos_vinculados.all():
                    print(f"   ✓ {ref}: Vinculado ao BIG BOSS")
                else:
                    print(f"   ❌ {ref}: NÃO vinculado ao BIG BOSS")
                    todos_encontrados = False
        
        except Item.DoesNotExist:
            print(f"   ❌ BIG BOSS não encontrado!")
            todos_encontrados = False
        
        # 4. Simular como aparece na interface
        print(f"\n✅ 4. Simulação da listagem na interface:")
        print("-" * 60)
        
        todos_produtos = Item.objects.all().order_by('ref_produto')
        for produto in todos_produtos:
            tipo_badge = f"[{produto.id_tipo_produto.nome}]"
            status = "Ativo" if produto.ativo else "Inativo"
            print(f"   {produto.ref_produto:6s} | {produto.nome_produto:30s} | {tipo_badge:12s} | {status}")
        
        print("-" * 60)
        
        # 5. Resultado final
        if todos_encontrados and acessorios.count() >= len(refs_esperadas):
            print(f"\n🎉 TESTE PASSOU! Todos os acessórios estão na listagem!")
            return True
        else:
            print(f"\n❌ TESTE FALHOU! Alguns acessórios não foram encontrados.")
            return False
            
    except TipoItem.DoesNotExist:
        print("❌ Tipo 'Acessórios' não encontrado!")
        return False

def test_acesso_interface():
    """Teste de como os dados serão exibidos na view da interface"""
    
    print(f"\n🌐 TESTE DE INTERFACE:")
    print("-" * 40)
    
    # Simular a query da view produtos_list_view
    produtos = Item.objects.select_related('id_tipo_produto').prefetch_related('modulos').all()
    
    print(f"Query da interface retorna {produtos.count()} produtos:")
    
    for produto in produtos:
        modulos_count = produto.modulos.count() if hasattr(produto, 'modulos') else 0
        print(f"   • {produto.ref_produto} - {produto.nome_produto}")
        print(f"     Tipo: {produto.id_tipo_produto.nome}")
        print(f"     Módulos: {modulos_count}")
        print(f"     Status: {'Ativo' if produto.ativo else 'Inativo'}")
        print()

if __name__ == "__main__":
    sucesso = test_acessorios_na_listagem()
    
    if sucesso:
        test_acesso_interface()
        print(f"\n✅ TUDO OK! Os acessórios devem aparecer na listagem agora.")
        print(f"🌐 Acesse: http://localhost:8000/produtos/")
    else:
        print(f"\n❌ Há problemas que precisam ser corrigidos.")
        sys.exit(1)
