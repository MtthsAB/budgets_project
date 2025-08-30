#!/usr/bin/env python3
"""
Script para verificar a implementação dos campos unificados
de desconto e acréscimo na página de edição de orçamentos.
"""

import requests
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

def teste_campos_edicao():
    """Teste automatizado dos campos de edição"""
    
    print("🧪 === TESTE AUTOMATIZADO DOS CAMPOS DE EDIÇÃO ===")
    
    # Configurar Chrome
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    
    try:
        # Verificar se o servidor está rodando
        try:
            response = requests.get("http://localhost:8000/", timeout=5)
            print("✅ Servidor Django está rodando")
        except requests.exceptions.RequestException:
            print("❌ Servidor Django não está acessível")
            return False
        
        # Inicializar driver
        driver = webdriver.Chrome(options=chrome_options)
        driver.implicitly_wait(10)
        
        # Acessar página de edição
        print("🌐 Acessando página de edição...")
        driver.get("http://localhost:8000/orcamentos/5/editar/")
        
        # Aguardar carregamento da página
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "orcamento-form"))
        )
        
        # Verificar se os dados do orçamento estão carregados
        print("🔍 Verificando dados carregados...")
        
        # Verificar campo cliente
        cliente_busca = driver.find_element(By.ID, "cliente-busca")
        cliente_valor = cliente_busca.get_attribute("value")
        print(f"   Cliente: '{cliente_valor}'")
        
        # Verificar campo desconto
        desconto_campo = driver.find_element(By.ID, "desconto_valor_unificado")
        desconto_valor = desconto_campo.get_attribute("value")
        
        desconto_btn = driver.find_element(By.ID, "desconto_tipo_btn")
        desconto_tipo = desconto_btn.get_attribute("data-tipo")
        desconto_texto = desconto_btn.find_element(By.CLASS_NAME, "tipo-texto").text
        
        print(f"   Desconto: '{desconto_valor}' ({desconto_texto}) - tipo: {desconto_tipo}")
        
        # Verificar campo acréscimo
        acrescimo_campo = driver.find_element(By.ID, "acrescimo_valor_unificado")
        acrescimo_valor = acrescimo_campo.get_attribute("value")
        
        acrescimo_btn = driver.find_element(By.ID, "acrescimo_tipo_btn")
        acrescimo_tipo = acrescimo_btn.get_attribute("data-tipo")
        acrescimo_texto = acrescimo_btn.find_element(By.CLASS_NAME, "tipo-texto").text
        
        print(f"   Acréscimo: '{acrescimo_valor}' ({acrescimo_texto}) - tipo: {acrescimo_tipo}")
        
        # Validar resultados
        sucesso = True
        
        if not cliente_valor or cliente_valor.strip() == "":
            print("❌ Campo cliente não foi hidratado")
            sucesso = False
        else:
            print("✅ Campo cliente hidratado corretamente")
        
        # Verificar desconto (esperamos 15%)
        if desconto_valor == "15" and desconto_texto == "%" and desconto_tipo == "percentual":
            print("✅ Campo desconto hidratado corretamente (15%)")
        else:
            print(f"❌ Campo desconto incorreto - esperado: 15%, obtido: {desconto_valor}{desconto_texto}")
            sucesso = False
            
        # Verificar acréscimo (esperamos 50%)
        if acrescimo_valor == "50" and acrescimo_texto == "%" and acrescimo_tipo == "percentual":
            print("✅ Campo acréscimo hidratado corretamente (50%)")
        else:
            print(f"❌ Campo acréscimo incorreto - esperado: 50%, obtido: {acrescimo_valor}{acrescimo_texto}")
            sucesso = False
        
        # Teste de alternância de tipo
        print("\n🔄 Testando alternância de tipos...")
        
        # Clicar no botão de desconto para alternar
        desconto_btn.click()
        time.sleep(0.5)
        
        # Verificar se mudou para R$
        novo_tipo = desconto_btn.get_attribute("data-tipo")
        novo_texto = desconto_btn.find_element(By.CLASS_NAME, "tipo-texto").text
        
        if novo_tipo == "valor" and novo_texto == "R$":
            print("✅ Alternância de desconto funcionando (% → R$)")
        else:
            print(f"❌ Alternância de desconto falhou - obtido: {novo_texto}")
            sucesso = False
        
        # Voltar para %
        desconto_btn.click()
        time.sleep(0.5)
        
        # Teste com sidebar de totais
        print("\n💰 Verificando sidebar de totais...")
        try:
            sidebar_total = driver.find_element(By.ID, "total-final")
            total_texto = sidebar_total.text
            print(f"   Total encontrado: {total_texto}")
            print("✅ Sidebar de totais carregada")
        except:
            print("⚠️  Sidebar de totais não encontrada (normal se não há itens)")
        
        driver.quit()
        
        if sucesso:
            print("\n🎉 TODOS OS TESTES PASSARAM!")
            print("   ✅ Cliente hidratado corretamente")
            print("   ✅ Desconto hidratado corretamente")
            print("   ✅ Acréscimo hidratado corretamente")
            print("   ✅ Alternância de tipos funcionando")
        else:
            print("\n❌ ALGUNS TESTES FALHARAM")
            
        return sucesso
        
    except Exception as e:
        print(f"❌ Erro durante o teste: {e}")
        import traceback
        traceback.print_exc()
        try:
            driver.quit()
        except:
            pass
        return False

if __name__ == '__main__':
    # Versão simplificada sem Selenium
    print("🧪 === TESTE SIMPLIFICADO DOS CAMPOS DE EDIÇÃO ===")
    
    try:
        response = requests.get("http://localhost:8000/orcamentos/5/editar/", timeout=10)
        if response.status_code == 200:
            content = response.text
            
            # Verificar se o payload está sendo injetado
            if 'window.orcamentoData' in content:
                print("✅ Payload de dados encontrado na página")
                
                # Extrair o JSON (método simples)
                start = content.find('window.orcamentoData = ') + len('window.orcamentoData = ')
                end = content.find('};', start) + 1
                json_data = content[start:end]
                
                print(f"📋 Dados encontrados: {json_data[:200]}...")
                
                # Verificar função de hidratação
                if 'hidratarCamposOrcamento' in content:
                    print("✅ Função de hidratação encontrada")
                else:
                    print("❌ Função de hidratação não encontrada")
                    
                # Verificar função específica de desconto/acréscimo
                if 'hidratarDescontoAcrescimo' in content:
                    print("✅ Função específica de desconto/acréscimo encontrada")
                else:
                    print("❌ Função específica de desconto/acréscimo não encontrada")
                    
            else:
                print("❌ Payload de dados não encontrado na página")
                
        else:
            print(f"❌ Erro ao acessar página: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Erro no teste: {e}")
        
    print("\n📝 Para teste manual:")
    print("   1. Acesse: http://localhost:8000/orcamentos/5/editar/")
    print("   2. Verifique se cliente está preenchido")
    print("   3. Verifique se desconto mostra 15%")
    print("   4. Verifique se acréscimo mostra 50%")
    print("   5. Clique nos botões % para alternar para R$")
    print("   6. Digite novos valores e salve")
