#!/usr/bin/env python3
"""
Script para testar se a seção de imagens aparece corretamente
ao selecionar diferentes tipos de produto.
"""

import os
import django
import sys

# Configurar Django
sys.path.append('/home/matas/projetos/Project')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema_produtos.settings')
django.setup()

from django.test import Client
from django.contrib.auth import get_user_model
from produtos.models import TipoItem

User = get_user_model()

def test_image_section_visibility():
    """Testa se a seção de imagens está presente no template de cadastro"""
    client = Client()
    
    # Criar usuário de teste se não existir
    try:
        user = User.objects.get(username='testuser')
    except User.DoesNotExist:
        user = User.objects.create_user(username='testuser', password='testpass')
    
    # Fazer login
    client.login(username='testuser', password='testpass')
    
    # Acessar página de cadastro
    response = client.get('/produtos/cadastro/')
    
    print(f"Status da resposta: {response.status_code}")
    
    # Verificar se a página carregou corretamente
    if response.status_code != 200:
        print("❌ Erro: Página de cadastro não carregou corretamente")
        return False
    
    # Converter response para string para análise
    content = response.content.decode('utf-8')
    
    # Verificar se os elementos essenciais estão presentes
    checks = {
        'Seção de imagens': 'id="secao-imagens"' in content,
        'Include de imagens': 'produtos/includes/secao_imagens.html' in content,
        'Função toggleCamposPorTipo': 'function toggleCamposPorTipo()' in content,
        'Select de tipo de produto': 'id="tipo_produto"' in content,
        'Campo imagem principal': 'name="imagem_principal"' in content,
        'Campo imagem secundária': 'name="imagem_secundaria"' in content,
        'Botão adicionar segunda imagem': 'btn_adicionar_segunda_imagem' in content,
        'Preview de imagem': 'function previewImage' in content,
    }
    
    print("\n=== VERIFICAÇÃO DOS ELEMENTOS ===")
    all_ok = True
    for check_name, result in checks.items():
        status = "✅" if result else "❌"
        print(f"{status} {check_name}: {'OK' if result else 'FALTANDO'}")
        if not result:
            all_ok = False
    
    # Verificar tipos de produto disponíveis
    tipos = TipoItem.objects.all()
    print(f"\n=== TIPOS DE PRODUTO DISPONÍVEIS ===")
    for tipo in tipos:
        print(f"- {tipo.nome} (ID: {tipo.id})")
    
    # Verificar se a função JavaScript está correta
    print("\n=== VERIFICAÇÃO DA FUNÇÃO JAVASCRIPT ===")
    js_checks = {
        'Elemento secaoImagens definido': 'secaoImagens = document.getElementById(\'secao-imagens\')' in content,
        'Exibição da seção': 'secaoImagens.style.display = \'block\'' in content,
        'Ocultação inicial': 'secaoImagens.style.display = \'none\'' in content,
    }
    
    for check_name, result in js_checks.items():
        status = "✅" if result else "❌"
        print(f"{status} {check_name}: {'OK' if result else 'FALTANDO'}")
        if not result:
            all_ok = False
    
    return all_ok

def extract_javascript_function():
    """Extrai e mostra a função toggleCamposPorTipo completa"""
    client = Client()
    response = client.get('/produtos/cadastro/')
    content = response.content.decode('utf-8')
    
    # Encontrar a função toggleCamposPorTipo
    start_marker = 'function toggleCamposPorTipo()'
    end_marker = '}'
    
    start_idx = content.find(start_marker)
    if start_idx == -1:
        print("❌ Função toggleCamposPorTipo não encontrada!")
        return
    
    # Encontrar o fim da função (procurar por } que fecha a função)
    brace_count = 0
    func_start = start_idx
    i = func_start
    while i < len(content):
        if content[i] == '{':
            brace_count += 1
        elif content[i] == '}':
            brace_count -= 1
            if brace_count == 0:
                func_end = i + 1
                break
        i += 1
    else:
        print("❌ Não foi possível encontrar o fim da função!")
        return
    
    function_code = content[func_start:func_end]
    print("\n=== FUNÇÃO TOGGLECAMPOSPORTIPO ===")
    print(function_code)

if __name__ == '__main__':
    print("🔍 Testando visibilidade da seção de imagens...")
    
    result = test_image_section_visibility()
    
    if result:
        print("\n✅ TESTE PASSOU: Todos os elementos estão presentes!")
    else:
        print("\n❌ TESTE FALHOU: Alguns elementos estão faltando!")
    
    print("\n" + "="*50)
    extract_javascript_function()
