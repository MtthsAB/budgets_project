#!/usr/bin/env python
"""
Script para testar se a edição de produtos está funcionando corretamente
"""
import os
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema_produtos.settings')
django.setup()

from produtos.models import Item, TipoItem, Modulo

def test_edicao_produto():
    """Teste básico do sistema de edição"""
    print("=== TESTE DE EDIÇÃO DE PRODUTOS ===")
    
    # Buscar um produto existente
    produtos = Item.objects.all()
    if not produtos.exists():
        print("❌ Nenhum produto encontrado. Criando produto de teste...")
        
        # Criar tipo se necessário
        tipo, created = TipoItem.objects.get_or_create(
            nome="Sofá",
            defaults={"descricao": "Móveis de sofá"}
        )
        
        # Criar produto de teste
        produto = Item.objects.create(
            ref_produto="TESTE001",
            nome_produto="Produto de Teste",
            id_tipo_produto=tipo,
            ativo=True
        )
        print(f"✅ Produto de teste criado: {produto.ref_produto}")
    else:
        produto = produtos.first()
        print(f"✅ Produto encontrado: {produto.ref_produto}")
    
    # Verificar módulos existentes
    modulos_count = produto.modulos.count()
    print(f"📦 Módulos atuais: {modulos_count}")
    
    # Listar módulos
    for i, modulo in enumerate(produto.modulos.all(), 1):
        print(f"   {i}. {modulo.nome}")
        print(f"      - Profundidade: {modulo.profundidade}")
        print(f"      - Altura: {modulo.altura}")
        print(f"      - Braço: {modulo.braco}")
    
    print("\n=== TESTE CONCLUÍDO ===")
    print(f"🔗 URL de edição: http://localhost:8000/produtos/{produto.id}/editar/")
    
    return produto

if __name__ == "__main__":
    test_edicao_produto()
