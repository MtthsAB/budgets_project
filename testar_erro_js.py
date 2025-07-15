#!/usr/bin/env python3
"""
Script para testar se o erro foi corrigido
"""

import os
import sys
import django
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time

# Configurar Django
sys.path.append('/home/matas/projetos/Project')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema_produtos.settings')
django.setup()

def testar_adicionar_item():
    """Testa se a adição de item funciona sem erros JavaScript"""
    
    print("=== TESTE DE ADIÇÃO DE ITEM ===")
    
    # Configurar Chrome headless
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    
    try:
        driver = webdriver.Chrome(options=chrome_options)
        
        print("🌐 Acessando página de novo orçamento...")
        driver.get("http://localhost:8000/orcamentos/novo/")
        
        # Aguardar página carregar
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "modalAdicionarItem"))
        )
        
        # Verificar se há erros JavaScript na página
        logs = driver.get_log('browser')
        erros_js = [log for log in logs if log['level'] == 'SEVERE']
        
        if erros_js:
            print("❌ Erros JavaScript encontrados:")
            for erro in erros_js:
                print(f"   {erro['message']}")
        else:
            print("✅ Nenhum erro JavaScript encontrado na página!")
        
        # Tentar clicar no botão "Adicionar Item"
        print("🔘 Tentando clicar em 'Adicionar Item'...")
        btn_adicionar = driver.find_element(By.ID, "btnAdicionarItem")
        btn_adicionar.click()
        
        # Aguardar modal abrir
        time.sleep(1)
        
        # Verificar novos erros após clique
        logs = driver.get_log('browser')
        erros_js = [log for log in logs if log['level'] == 'SEVERE']
        
        if erros_js:
            print("❌ Erros JavaScript após clicar em 'Adicionar Item':")
            for erro in erros_js:
                print(f"   {erro['message']}")
        else:
            print("✅ Nenhum erro JavaScript após clicar em 'Adicionar Item'!")
        
        print("✅ Teste concluído!")
        
    except Exception as e:
        print(f"❌ Erro no teste: {e}")
    finally:
        if 'driver' in locals():
            driver.quit()

if __name__ == '__main__':
    testar_adicionar_item()
