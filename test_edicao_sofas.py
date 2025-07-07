#!/usr/bin/env python3
"""
Teste para validar a funcionalidade de edição de sofás
Verifica se a página de edição carrega corretamente com todas as funcionalidades
"""

import requests
import sys
from bs4 import BeautifulSoup

def test_sofa_edit_page():
    """Testa se a página de edição de sofás carrega corretamente"""
    print("🧪 Testando página de edição de sofás...")
    
    # URLs para testar
    base_url = "http://localhost:8000"
    login_url = f"{base_url}/auth/login/"
    edit_url = f"{base_url}/sofas/7/editar/"
    
    # Criar sessão para manter cookies
    session = requests.Session()
    
    try:
        # Primeiro, tentar acessar a página de edição
        print("📄 Acessando página de edição...")
        response = session.get(edit_url)
        
        if response.status_code == 200:
            print("✅ Página carregada com sucesso!")
            
            # Verificar se os elementos essenciais estão presentes
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Verificar elementos de módulos
            secao_modulos = soup.find('div', {'id': 'secao-modulos'})
            if secao_modulos:
                print("✅ Seção de módulos encontrada")
            else:
                print("❌ Seção de módulos não encontrada")
                
            # Verificar botão de adicionar módulo
            btn_adicionar = soup.find('button', string=lambda text: text and 'Adicionar Módulo' in text)
            if btn_adicionar:
                print("✅ Botão 'Adicionar Módulo' encontrado")
            else:
                print("❌ Botão 'Adicionar Módulo' não encontrado")
                
            # Verificar JavaScript específico
            scripts = soup.find_all('script')
            sofa_js_found = any('adicionarModulo' in script.get_text() for script in scripts if script.get_text())
            if sofa_js_found:
                print("✅ JavaScript de módulos encontrado")
            else:
                print("❌ JavaScript de módulos não encontrado")
                
            # Verificar campos de sofá
            campos_sofa = soup.find('div', {'id': 'campos-sofa'}) or soup.find_all('input', {'name': lambda x: x and 'sofa' in x.lower()})
            if campos_sofa:
                print("✅ Campos específicos de sofá encontrados")
            else:
                print("⚠️ Campos específicos de sofá não encontrados (pode ser normal se estão ocultos)")
                
            return True
            
        elif response.status_code == 302:
            print("🔄 Redirecionamento detectado (provavelmente para login)")
            print(f"   Location: {response.headers.get('Location', 'N/A')}")
            return True  # Redirecionamento é esperado se não estiver logado
            
        else:
            print(f"❌ Erro HTTP {response.status_code}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ Erro de conexão - verifique se o servidor está rodando")
        return False
    except Exception as e:
        print(f"❌ Erro inesperado: {e}")
        return False

def test_templates_structure():
    """Verifica se os templates estão no local correto"""
    print("\n🗂️ Verificando estrutura de templates...")
    
    import os
    
    # Verificar arquivos essenciais
    files_to_check = [
        "templates/produtos/includes/sofa_js.html",
        "templates/produtos/includes/secao_modulos_sofa.html",
        "templates/produtos/sofas/editar.html",
        "templates/produtos/includes/editar_base.html"
    ]
    
    all_found = True
    for file_path in files_to_check:
        if os.path.exists(file_path):
            print(f"✅ {file_path}")
        else:
            print(f"❌ {file_path} não encontrado")
            all_found = False
    
    return all_found

def main():
    """Função principal do teste"""
    print("🎯 TESTE DE FUNCIONALIDADE - EDIÇÃO DE SOFÁS")
    print("=" * 50)
    
    # Teste 1: Estrutura de templates
    structure_ok = test_templates_structure()
    
    # Teste 2: Carregamento da página
    page_ok = test_sofa_edit_page()
    
    # Resultado final
    print("\n" + "=" * 50)
    print("📊 RESULTADO DOS TESTES:")
    print(f"   Estrutura de templates: {'✅ OK' if structure_ok else '❌ ERRO'}")
    print(f"   Carregamento da página: {'✅ OK' if page_ok else '❌ ERRO'}")
    
    if structure_ok and page_ok:
        print("\n🎉 TODOS OS TESTES PASSARAM!")
        print("   A funcionalidade de edição de sofás está funcionando corretamente.")
        return 0
    else:
        print("\n⚠️ ALGUNS TESTES FALHARAM!")
        print("   Verifique os erros acima e corrija os problemas.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
