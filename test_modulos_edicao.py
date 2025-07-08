#!/usr/bin/env python3
"""
Script para testar se a seção de módulos está aparecendo na página de edição de sofás
"""

import requests
from bs4 import BeautifulSoup
import time

def test_modulos_section():
    """Testa se a seção de módulos está visível na página de edição"""
    
    print("🧪 Testando seção de módulos na página de edição de sofás...")
    
    try:
        # Fazer requisição para a página de edição
        url = 'http://localhost:8000/sofas/7/editar/'
        
        # Tentar fazer login primeiro se necessário
        session = requests.Session()
        
        # Fazer requisição GET para obter a página
        response = session.get(url, allow_redirects=True, timeout=10)
        
        print(f"Status da resposta: {response.status_code}")
        print(f"URL final: {response.url}")
        
        # Se redirecionou para login, exibir informação
        if 'login' in response.url.lower():
            print("⚠️  Página requer autenticação")
            print("   Verificando se a seção de módulos está presente no template...")
            
            # Ler o template diretamente
            with open('/home/matas/projetos/Project/templates/produtos/sofas/editar.html', 'r') as f:
                template_content = f.read()
            
            print("\n📋 Verificações do template:")
            
            # Verificar se a seção de módulos está incluída
            if 'secao_modulos_sofa.html' in template_content:
                print("✅ Seção de módulos incluída no template")
            else:
                print("❌ Seção de módulos NÃO incluída no template")
            
            # Verificar se o JavaScript está incluído
            if 'sofa_js.html' in template_content:
                print("✅ JavaScript dos sofás incluído no template")
            else:
                print("❌ JavaScript dos sofás NÃO incluído no template")
                
            # Verificar se o select tem os atributos corretos
            if 'data-nome=' in template_content:
                print("✅ Select tem atributo data-nome")
            else:
                print("❌ Select NÃO tem atributo data-nome")
                
            # Verificar se o select tem onchange
            if 'onchange="toggleCamposPorTipo()"' in template_content:
                print("✅ Select tem evento onchange")
            else:
                print("❌ Select NÃO tem evento onchange")
                
            # Verificar se tem id campos-sofa
            if 'id="campos-sofa"' in template_content:
                print("✅ Elemento com id='campos-sofa' presente")
            else:
                print("❌ Elemento com id='campos-sofa' NÃO presente")
            
            return True
            
        else:
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Verificar se a seção de módulos está presente
            secao_modulos = soup.find('div', {'id': 'secao-modulos'})
            
            if secao_modulos:
                print("✅ Seção de módulos encontrada na página")
                
                # Verificar se está visível ou oculta
                style = secao_modulos.get('style', '')
                if 'display: none' in style:
                    print("⚠️  Seção de módulos está oculta (display: none)")
                else:
                    print("✅ Seção de módulos está visível")
                
                # Verificar se há módulos existentes
                modulos_existentes = secao_modulos.find_all('div', class_='modulo-item')
                print(f"📊 Módulos existentes encontrados: {len(modulos_existentes)}")
                
            else:
                print("❌ Seção de módulos NÃO encontrada na página")
                
            # Verificar se o JavaScript está presente
            scripts = soup.find_all('script')
            js_encontrado = False
            for script in scripts:
                if script.string and 'toggleCamposEspecificos' in script.string:
                    js_encontrado = True
                    break
            
            if js_encontrado:
                print("✅ JavaScript dos sofás encontrado na página")
            else:
                print("❌ JavaScript dos sofás NÃO encontrado na página")
            
            return True
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Erro ao fazer requisição: {e}")
        return False
    except Exception as e:
        print(f"❌ Erro inesperado: {e}")
        return False

def test_js_file():
    """Testa se o arquivo JavaScript tem as funções necessárias"""
    
    print("\n🔍 Verificando arquivo JavaScript...")
    
    try:
        with open('/home/matas/projetos/Project/templates/produtos/includes/sofa_js.html', 'r') as f:
            js_content = f.read()
        
        # Verificar funções essenciais
        if 'function toggleCamposEspecificos(' in js_content:
            print("✅ Função toggleCamposEspecificos encontrada")
        else:
            print("❌ Função toggleCamposEspecificos NÃO encontrada")
            
        if 'getElementById(\'secao-modulos\')' in js_content:
            print("✅ Referência ao elemento secao-modulos encontrada")
        else:
            print("❌ Referência ao elemento secao-modulos NÃO encontrada")
            
        if 'DOMContentLoaded' in js_content:
            print("✅ Evento DOMContentLoaded encontrado")
        else:
            print("❌ Evento DOMContentLoaded NÃO encontrado")
            
        return True
        
    except Exception as e:
        print(f"❌ Erro ao ler arquivo JavaScript: {e}")
        return False

def main():
    """Função principal"""
    print("🚀 Iniciando teste da seção de módulos na edição de sofás\n")
    
    # Aguardar um pouco para o servidor inicializar
    time.sleep(2)
    
    # Testar arquivo JavaScript
    test_js_file()
    
    # Testar página
    test_modulos_section()
    
    print("\n✅ Teste concluído!")
    print("\n💡 Para testar completamente, acesse:")
    print("   http://localhost:8000/sofas/7/editar/")
    print("   A seção de módulos deve estar visível após o login")

if __name__ == "__main__":
    main()
