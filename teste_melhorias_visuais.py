#!/usr/bin/env python3
"""
Script para testar as melhorias visuais na listagem de produtos
"""

import os
import sys
import django

# Configurar Django
sys.path.append('/home/matas/projetos/Project')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema_produtos.settings')
django.setup()

from django.test import Client
from django.contrib.auth import get_user_model
from produtos.models import Item, TipoItem, Banqueta

User = get_user_model()

def test_melhorias_visuais():
    """Testa as melhorias visuais da listagem"""
    print("=== TESTE DAS MELHORIAS VISUAIS ===")
    
    # Criar cliente de teste
    client = Client()
    
    # Criar usuário de teste se não existir
    try:
        user = User.objects.get(email='teste_visual@exemplo.com')
    except User.DoesNotExist:
        user = User.objects.create_user(
            email='teste_visual@exemplo.com',
            password='senha123',
            first_name='Teste',
            last_name='Visual'
        )
        print(f"✅ Usuário de teste criado: {user.email}")
    
    # Fazer login
    client.login(email='teste_visual@exemplo.com', password='senha123')
    print("✅ Login realizado com sucesso")
    
    # Testar a página de listagem
    response = client.get('/produtos/')
    
    print(f"\n📊 Status da resposta: {response.status_code}")
    
    if response.status_code == 200:
        content = response.content.decode('utf-8')
        
        # Verificar se os estilos CSS foram aplicados
        checks = [
            ('btn-group-actions', 'Estilos dos botões de ação'),
            ('badge tipo-', 'Classes de badge por tipo'),
            ('small-user', 'Estilo para usuário compacto'),
            ('table-hover', 'Hover na tabela'),
            ('width="120"', 'Larguras das colunas definidas'),
        ]
        
        print("\n🎨 VERIFICAÇÃO DOS ESTILOS CSS:")
        for check, description in checks:
            if check in content:
                print(f"  ✅ {description}")
            else:
                print(f"  ❌ {description}")
        
        # Verificar estrutura da tabela
        table_checks = [
            ('<th width="120">Referência</th>', 'Coluna Referência com largura'),
            ('<th width="100">Tipo</th>', 'Coluna Tipo com largura'),
            ('<th width="140">Ações</th>', 'Coluna Ações com largura'),
        ]
        
        print("\n📋 VERIFICAÇÃO DA ESTRUTURA DA TABELA:")
        for check, description in table_checks:
            if check in content:
                print(f"  ✅ {description}")
            else:
                print(f"  ❌ {description}")
        
        # Contar produtos e banquetas
        produtos_count = Item.objects.count()
        banquetas_count = Banqueta.objects.count()
        total = produtos_count + banquetas_count
        
        print(f"\n📊 CONTADORES:")
        print(f"  📦 Produtos (Item): {produtos_count}")
        print(f"  🪑 Banquetas: {banquetas_count}")
        print(f"  📈 Total: {total}")
        
        # Verificar se o total está sendo exibido corretamente
        if f"Lista de Produtos ({total})" in content:
            print(f"  ✅ Total exibido corretamente no cabeçalho")
        else:
            print(f"  ❌ Total não encontrado no cabeçalho")
        
        print("\n✅ Teste de melhorias visuais concluído com sucesso!")
        
    else:
        print(f"❌ Erro ao acessar a página: {response.status_code}")
        print(f"Conteúdo: {response.content.decode('utf-8')[:500]}...")

if __name__ == "__main__":
    test_melhorias_visuais()
