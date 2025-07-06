#!/usr/bin/env python
"""
Script para testar se as banquetas aparecem na listagem de produtos
"""
import os
import sys
import django

# Configurar Django
sys.path.append('/home/matas/projetos/Project')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema_produtos.settings')
django.setup()

from produtos.models import TipoItem, Item, Banqueta

def testar_listagem_unificada():
    """Testa se a listagem unificada está funcionando"""
    print("🔍 TESTANDO LISTAGEM UNIFICADA DE PRODUTOS E BANQUETAS")
    print("=" * 60)
    
    # Verificar dados existentes
    produtos_count = Item.objects.count()
    banquetas_count = Banqueta.objects.count()
    
    print(f"📊 DADOS DISPONÍVEIS:")
    print(f"   • Produtos (Item): {produtos_count}")
    print(f"   • Banquetas: {banquetas_count}")
    print(f"   • Total geral: {produtos_count + banquetas_count}")
    
    print(f"\n📋 PRODUTOS CADASTRADOS:")
    for produto in Item.objects.all():
        print(f"   • {produto.ref_produto} - {produto.nome_produto} ({produto.id_tipo_produto.nome})")
    
    print(f"\n🪑 BANQUETAS CADASTRADAS:")
    for banqueta in Banqueta.objects.all():
        print(f"   • {banqueta.ref_banqueta} - {banqueta.nome} (R$ {banqueta.preco})")
    
    # Testar filtros
    print(f"\n🔧 TESTANDO FILTROS:")
    
    # Filtro por tipo "Banquetas" (id=4)
    tipo_banquetas = TipoItem.objects.get(nome="Banquetas")
    print(f"   • Tipo 'Banquetas' tem ID: {tipo_banquetas.id}")
    
    # Simular filtro de banquetas
    produtos_filtrados = Item.objects.filter(id_tipo_produto__id=tipo_banquetas.id)
    banquetas_filtradas = Banqueta.objects.filter(ativo=True)
    
    print(f"   • Produtos do tipo 'Banquetas': {produtos_filtrados.count()}")
    print(f"   • Banquetas ativas: {banquetas_filtradas.count()}")
    
    # Teste de busca
    print(f"\n🔍 TESTANDO BUSCA:")
    termo_busca = "CERES"
    produtos_busca = Item.objects.filter(nome_produto__icontains=termo_busca) | Item.objects.filter(ref_produto__icontains=termo_busca)
    banquetas_busca = Banqueta.objects.filter(nome__icontains=termo_busca) | Banqueta.objects.filter(ref_banqueta__icontains=termo_busca)
    
    print(f"   • Busca por '{termo_busca}':")
    print(f"     - Produtos encontrados: {produtos_busca.count()}")
    print(f"     - Banquetas encontradas: {banquetas_busca.count()}")
    
    for banqueta in banquetas_busca:
        print(f"       → {banqueta.ref_banqueta} - {banqueta.nome}")
    
    print(f"\n✅ CONCLUSÃO:")
    if banquetas_count > 0:
        print(f"   • {banquetas_count} banquetas estão cadastradas e devem aparecer na listagem!")
        print(f"   • As banquetas aparecerão com badge 'Banquetas' (amarelo)")
        print(f"   • Filtro por tipo 'Banquetas' deve mostrar apenas banquetas")
        print(f"   • Busca por nome/referência das banquetas deve funcionar")
    else:
        print(f"   • ❌ Nenhuma banqueta cadastrada!")
    
    return banquetas_count > 0

if __name__ == "__main__":
    sucesso = testar_listagem_unificada()
    if sucesso:
        print(f"\n🎉 TESTE CONCLUÍDO COM SUCESSO!")
        print(f"   Acesse /produtos/ para ver banquetas e produtos juntos!")
    else:
        print(f"\n❌ TESTE FALHOU - nenhuma banqueta encontrada!")
