#!/usr/bin/env python
"""
Script para testar a correção do erro de template
"""

import requests
import os
import sys

def testar_pagina_sofa():
    """Testa se a página do sofá está funcionando"""
    
    print("=== TESTANDO CORREÇÃO DO TEMPLATE ===\n")
    
    try:
        # Testar a página do sofá
        url = "http://localhost:8000/sofas/7/"
        print(f"Testando URL: {url}")
        
        response = requests.get(url)
        
        if response.status_code == 200:
            print("✓ Página carregada com sucesso!")
            print(f"✓ Status Code: {response.status_code}")
            
            # Verificar se contém as seções esperadas
            content = response.text
            
            sections = [
                ("Detalhes do Sofá", "Título da página"),
                ("Informações Básicas", "Seção de informações"),
                ("Módulos", "Seção de módulos"),
                ("modulo-card", "Classes CSS aplicadas"),
                ("Tamanhos Disponíveis", "Seção de tamanhos")
            ]
            
            print("\n--- VERIFICANDO CONTEÚDO ---")
            for section, description in sections:
                if section in content:
                    print(f"✓ {description}")
                else:
                    print(f"❌ {description} - não encontrado")
            
            print(f"\n✓ Página tem {len(content)} caracteres")
            
        else:
            print(f"❌ Erro na página: Status {response.status_code}")
            print(f"❌ Resposta: {response.text[:500]}...")
            
    except requests.exceptions.ConnectionError:
        print("❌ Erro de conexão - certifique-se de que o servidor está rodando")
    except Exception as e:
        print(f"❌ Erro inesperado: {e}")

def verificar_template_sintaxe():
    """Verifica se há erros de sintaxe no template"""
    
    print("\n=== VERIFICANDO SINTAXE DO TEMPLATE ===")
    
    template_path = "/home/matas/projetos/Project/templates/produtos/sofas/detalhes.html"
    
    try:
        with open(template_path, 'r', encoding='utf-8') as file:
            content = file.read()
            
        # Verificar balanceamento de blocos
        block_starts = content.count('{% block')
        block_ends = content.count('{% endblock')
        
        print(f"Blocos de abertura: {block_starts}")
        print(f"Blocos de fechamento: {block_ends}")
        
        if block_starts == block_ends:
            print("✓ Blocos balanceados")
        else:
            print("❌ Blocos desbalanceados")
            
        # Verificar se há blocos duplicados
        if '{% endblock %}' in content:
            endblock_count = content.count('{% endblock %}')
            print(f"Blocos de fechamento encontrados: {endblock_count}")
            
        # Verificar CSS duplicado
        if content.count('</style>') > 1:
            print("⚠️  Múltiplas tags </style> encontradas")
        else:
            print("✓ Tags </style> corretas")
            
    except FileNotFoundError:
        print("❌ Template não encontrado!")
    except Exception as e:
        print(f"❌ Erro ao verificar: {e}")

if __name__ == "__main__":
    verificar_template_sintaxe()
    testar_pagina_sofa()
