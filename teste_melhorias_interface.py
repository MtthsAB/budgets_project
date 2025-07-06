#!/usr/bin/env python3
"""
Script para testar as melhorias de interface implementadas na página de edição de produtos.

Funcionalidades testadas:
1. Substituição do título "Módulo X" pelo nome real do módulo
2. Botão de expandir/recolher módulos
3. Atualização dinâmica do título ao digitar
4. Feedback visual do status do módulo
"""

import os
import django
import sys

# Configurar Django
sys.path.append('/home/matas/projetos/Project')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema_produtos.settings')
django.setup()

from produtos.models import Item, Modulo, TipoItem

def testar_melhorias_interface():
    """Testa as melhorias implementadas na interface"""
    
    print("🔍 TESTANDO MELHORIAS DE INTERFACE")
    print("=" * 60)
    
    # Buscar um produto existente com módulos
    produtos_com_modulos = Item.objects.filter(modulos__isnull=False).distinct()
    
    if produtos_com_modulos.exists():
        produto = produtos_com_modulos.first()
        print(f"✅ Produto encontrado: {produto.nome_produto} (ID: {produto.id})")
        print(f"📦 Módulos: {produto.modulos.count()}")
        
        # Listar módulos
        for i, modulo in enumerate(produto.modulos.all(), 1):
            nome_display = modulo.nome if modulo.nome else f"Módulo {i}"
            print(f"   {i}. {nome_display}")
            if modulo.nome:
                print(f"      ✅ Nome preenchido: '{modulo.nome}'")
            else:
                print(f"      ⚠️  Sem nome - aparecerá como 'Módulo {i}'")
        
        print(f"\n🌐 URL para teste: http://localhost:8000/produtos/{produto.id}/editar/")
        
    else:
        print("⚠️  Nenhum produto com módulos encontrado.")
        print("   Criando produto de teste...")
        
        # Criar produto de teste
        tipo_produto = TipoItem.objects.first()
        if not tipo_produto:
            tipo_produto = TipoItem.objects.create(nome="Teste")
        
        produto = Item.objects.create(
            ref_produto="TEST-001",
            nome_produto="Produto Teste Interface",
            id_tipo_produto=tipo_produto,
            ativo=True
        )
        
        # Criar módulos de teste
        Modulo.objects.create(
            item=produto,
            nome="Módulo com Nome",
            profundidade=50.0,
            altura=80.0,
            braco=20.0,
            descricao="Este módulo tem nome definido"
        )
        
        Modulo.objects.create(
            item=produto,
            nome="",  # Módulo sem nome
            profundidade=60.0,
            altura=90.0
        )
        
        print(f"✅ Produto de teste criado: {produto.nome_produto} (ID: {produto.id})")
        print(f"🌐 URL para teste: http://localhost:8000/produtos/{produto.id}/editar/")
    
    print("\n📋 CHECKLIST DE TESTE:")
    print("□ 1. Abrir a URL no navegador")
    print("□ 2. Verificar se módulos com nome mostram o nome real no título")
    print("□ 3. Verificar se módulos sem nome mostram 'Módulo X'")
    print("□ 4. Testar botão expandir/recolher (+ / -)")
    print("□ 5. Digitar nome em módulo sem nome e ver atualização dinâmica")
    print("□ 6. Verificar indicador visual verde para módulos com nome")
    print("□ 7. Adicionar novo módulo e testar funcionalidades")
    
    print("\n🎨 RECURSOS IMPLEMENTADOS:")
    print("• Título dinâmico dos módulos")
    print("• Botão expandir/recolher com animações")
    print("• Indicador visual de status (ponto verde)")
    print("• Atualização em tempo real ao digitar")
    print("• Estilos visuais melhorados")
    print("• Animações suaves de transição")

if __name__ == "__main__":
    testar_melhorias_interface()
