#!/usr/bin/env python3
"""
Script para testar a view adicionar_item diretamente
"""

import os
import sys
import django
import json

# Configurar Django
sys.path.append('/home/matas/projetos/Project')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema_produtos.settings')
django.setup()

from orcamentos.models import Orcamento, OrcamentoItem
from produtos.models import Cadeira
from django.test import RequestFactory
from django.contrib.auth.models import AnonymousUser
from authentication.models import CustomUser
from orcamentos.views import adicionar_item

def main():
    print("=== TESTE DIRETO DA VIEW ADICIONAR_ITEM ===")
    
    # Buscar orçamento
    orcamento = Orcamento.objects.order_by('-id').first()
    print(f"📋 Orçamento: {orcamento.numero}")
    
    # Buscar cadeira
    cadeira = Cadeira.objects.filter(ativo=True).first()
    print(f"🪑 Cadeira: {cadeira.nome} - R$ {cadeira.preco}")
    
    # Preparar dados
    data = {
        'produto_id': f'cadeira_{cadeira.id}',
        'quantidade': 1,
        'preco_unitario': str(cadeira.preco),
        'observacoes': 'Teste direto da view',
        'dados_especificos': {'tipo': 'cadeira'}
    }
    
    # Criar request
    factory = RequestFactory()
    request = factory.post(
        f'/orcamentos/{orcamento.id}/adicionar-item/',
        data=json.dumps(data),
        content_type='application/json'
    )
    
    # Simular usuário logado
    user = CustomUser.objects.filter(is_superuser=True).first()
    request.user = user if user else AnonymousUser()
    
    try:
        # Chamar view
        response = adicionar_item(request, orcamento.pk)
        
        print(f"📤 Response status: {response.status_code}")
        print(f"📄 Response content: {response.content.decode()}")
        
        # Verificar se item foi criado
        items_count = orcamento.itens.count()
        print(f"📊 Items no orçamento: {items_count}")
        
        if items_count > 0:
            último_item = orcamento.itens.last()
            print(f"✅ Último item: {último_item.produto.nome_produto} - R$ {último_item.preco_unitario}")
        
    except Exception as e:
        print(f"❌ Erro: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    main()
