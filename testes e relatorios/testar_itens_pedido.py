#!/usr/bin/env python3
"""
Script para testar o novo sistema de itens do pedido
"""
import os
import django
from django.conf import settings

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema_produtos.settings')
django.setup()

from django.urls import reverse
from produtos.models import Produto, TipoProduto

def main():
    print("🧪 TESTE DO SISTEMA DE ITENS DO PEDIDO")
    print("=" * 50)
    
    try:
        # Verificar URL
        url = reverse('orcamentos:produtos_por_tipo')
        print(f"✅ URL produtos-por-tipo: {url}")
        
        # Verificar tipos de produto
        tipos = TipoProduto.objects.all()
        print(f"📋 Tipos de produto disponíveis: {tipos.count()}")
        for tipo in tipos:
            produtos_do_tipo = Produto.objects.filter(id_tipo_produto=tipo, ativo=True).count()
            print(f"   - {tipo.nome}: {produtos_do_tipo} produtos")
        
        # Verificar produtos ativos
        produtos_ativos = Produto.objects.filter(ativo=True).count()
        print(f"📦 Total de produtos ativos: {produtos_ativos}")
        
        print("\n✅ SUCESSO: Sistema de itens implementado!")
        print("🎯 Acesse: http://127.0.0.1:8000/orcamentos/novo/")
        print("🔧 Teste o botão 'Adicionar Item'")
        
    except Exception as e:
        print(f"❌ Erro: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
