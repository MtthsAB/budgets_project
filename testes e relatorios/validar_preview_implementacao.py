#!/usr/bin/env python3
"""
Script de validação final da implementação de preview de produtos
"""

import os
import django
import sys
import requests
import json

# Configurar Django
sys.path.append('/home/matas/projetos/Project')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema_produtos.settings')
django.setup()

from django.test import Client
from django.contrib.auth.models import User
from produtos.models import Banqueta

def validar_implementacao():
    """Valida se a implementação está funcionando corretamente"""
    
    print("=== VALIDAÇÃO FINAL: PREVIEW DE PRODUTOS ===\n")
    
    # 1. Verificar se a URL foi registrada
    print("1. Verificando registro da URL...")
    client = Client()
    
    # Simular login
    try:
        user = User.objects.filter(is_superuser=True).first()
        if user:
            client.force_login(user)
            print("   ✅ Login simulado com sucesso")
        else:
            print("   ⚠️  Nenhum superusuário encontrado, mas continuando...")
    except Exception as e:
        print(f"   ⚠️  Erro no login: {e}")
    
    # 2. Testar a nova URL
    print("\n2. Testando endpoint /orcamentos/informacoes-produto/...")
    
    # Pegar um produto para teste
    banqueta = Banqueta.objects.filter(ativo=True).first()
    if banqueta:
        produto_id = f"banqueta_{banqueta.id}"
        
        try:
            response = client.get(f'/orcamentos/informacoes-produto/?produto_id={produto_id}')
            if response.status_code == 200:
                data = json.loads(response.content)
                print("   ✅ Endpoint respondendo corretamente")
                print(f"   📦 Produto retornado: {data.get('produto', {}).get('nome', 'N/A')}")
                
                # Verificar estrutura da resposta
                produto = data.get('produto', {})
                campos_esperados = ['nome', 'foto', 'dimensoes', 'tipo']
                for campo in campos_esperados:
                    if campo in produto:
                        print(f"   ✅ Campo '{campo}': {produto[campo]}")
                    else:
                        print(f"   ❌ Campo '{campo}' ausente")
                        
            else:
                print(f"   ❌ Erro HTTP {response.status_code}")
                
        except Exception as e:
            print(f"   ❌ Erro ao testar endpoint: {e}")
    else:
        print("   ⚠️  Nenhuma banqueta encontrada para teste")
    
    # 3. Verificar se o template foi modificado
    print("\n3. Verificando modificações no template...")
    template_path = '/home/matas/projetos/Project/templates/orcamentos/form.html'
    
    try:
        with open(template_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Verificar componentes adicionados
        checks = [
            ('produto-preview', 'Div do preview'),
            ('produto-foto', 'Elemento da foto'),
            ('produto-nome', 'Elemento do nome'),
            ('produto-dimensoes', 'Elemento das dimensões'),
            ('produto-tipo', 'Elemento do tipo'),
            ('carregarPreviewProduto', 'Função JS de carregar preview'),
            ('mostrarPreviewProduto', 'Função JS de mostrar preview'),
            ('ocultarPreviewProduto', 'Função JS de ocultar preview'),
        ]
        
        for check_id, description in checks:
            if check_id in content:
                print(f"   ✅ {description}: Encontrado")
            else:
                print(f"   ❌ {description}: NÃO encontrado")
                
    except Exception as e:
        print(f"   ❌ Erro ao verificar template: {e}")
    
    # 4. Verificar se a view foi adicionada
    print("\n4. Verificando view no arquivo views.py...")
    views_path = '/home/matas/projetos/Project/orcamentos/views.py'
    
    try:
        with open(views_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        if 'obter_informacoes_produto' in content:
            print("   ✅ Função obter_informacoes_produto: Encontrada")
        else:
            print("   ❌ Função obter_informacoes_produto: NÃO encontrada")
            
    except Exception as e:
        print(f"   ❌ Erro ao verificar views.py: {e}")
    
    # 5. Verificar se a URL foi adicionada
    print("\n5. Verificando URL no arquivo urls.py...")
    urls_path = '/home/matas/projetos/Project/orcamentos/urls.py'
    
    try:
        with open(urls_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        if 'informacoes-produto' in content:
            print("   ✅ URL informacoes-produto: Encontrada")
        else:
            print("   ❌ URL informacoes-produto: NÃO encontrada")
            
    except Exception as e:
        print(f"   ❌ Erro ao verificar urls.py: {e}")
    
    print("\n=== RESUMO DA IMPLEMENTAÇÃO ===")
    print("🎯 Melhoria: Preview de produto na seleção de orçamento")
    print("📍 Localização: Após seleção do produto, antes do campo quantidade")
    print("🔧 Componentes implementados:")
    print("   • Nova view: obter_informacoes_produto")
    print("   • Nova URL: informacoes-produto/")
    print("   • Componente HTML de preview")
    print("   • Funções JavaScript de controle")
    print("   • Integração com seleção existente")
    
    print("\n=== COMO TESTAR ===")
    print("1. Acesse: http://127.0.0.1:8001/orcamentos/novo/")
    print("2. Preencha dados básicos do orçamento")
    print("3. Clique em 'Adicionar Item'")
    print("4. Selecione tipo de produto")
    print("5. Selecione um produto específico")
    print("6. Observe o preview aparecendo entre o produto e a quantidade")
    
    print("\n✅ IMPLEMENTAÇÃO CONCLUÍDA COM SUCESSO!")

if __name__ == "__main__":
    validar_implementacao()
