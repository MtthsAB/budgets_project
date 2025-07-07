#!/usr/bin/env python3
"""
Teste para verificar se os botões de módulos estão funcionando
"""

import os
import sys
import django

# Setup Django
sys.path.append('/home/matas/projetos/Project')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema_produtos.settings')
django.setup()

import requests
from bs4 import BeautifulSoup

def test_botoes_modulos():
    """Testa se os elementos de botões estão presentes na página"""
    
    print("=== TESTE: Botões de Módulos ===")
    
    try:
        # Fazer requisição à página
        response = requests.get('http://localhost:8000/sofas/7/editar/', timeout=10)
        
        if response.status_code == 200:
            print("✅ Página carregada com sucesso")
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Verificar botão de toggle
            toggle_btn = soup.find('button', {'id': 'toggleModulosBtn'})
            if toggle_btn:
                print("✅ Botão toggleModulosBtn encontrado")
                print(f"   Classe: {toggle_btn.get('class')}")
                print(f"   Texto: {toggle_btn.get_text().strip()}")
            else:
                print("❌ Botão toggleModulosBtn não encontrado")
            
            # Verificar span do texto
            toggle_text = soup.find('span', {'id': 'toggleModulosText'})
            if toggle_text:
                print("✅ Span toggleModulosText encontrado")
                print(f"   Texto: {toggle_text.get_text().strip()}")
            else:
                print("❌ Span toggleModulosText não encontrado")
            
            # Verificar seção de módulos
            secao_modulos = soup.find('div', {'id': 'secao-modulos'})
            if secao_modulos:
                print("✅ Seção de módulos encontrada")
                print(f"   Display: {secao_modulos.get('style', 'não definido')}")
            else:
                print("❌ Seção de módulos não encontrada")
            
            # Verificar se JavaScript está carregado
            script_tags = soup.find_all('script')
            js_carregado = any('sofa_modulos.js' in str(script) for script in script_tags)
            if js_carregado:
                print("✅ JavaScript sofa_modulos.js está sendo carregado")
            else:
                print("❌ JavaScript sofa_modulos.js não encontrado")
            
            # Verificar módulos existentes
            modulos = soup.find_all('div', {'class': 'modulo-item'})
            print(f"✅ Encontrados {len(modulos)} módulos na página")
            
            return True
        else:
            print(f"❌ Erro HTTP: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Erro durante o teste: {str(e)}")
        return False

if __name__ == '__main__':
    print("🧪 TESTANDO BOTÕES DE MÓDULOS")
    print("=" * 50)
    
    sucesso = test_botoes_modulos()
    
    print("=" * 50)
    if sucesso:
        print("✅ TESTE CONCLUÍDO")
    else:
        print("❌ TESTE FALHOU")
    print("=" * 50)
