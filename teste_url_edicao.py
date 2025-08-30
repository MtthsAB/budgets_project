#!/usr/bin/env python3
"""
Teste simples para verificar se a URL de edição está funcionando
"""

import requests
import re

def testar_url_edicao():
    url = "http://127.0.0.1:8000/orcamentos/5/editar/"
    
    print(f"=== TESTANDO URL: {url} ===")
    
    try:
        # Fazer requisição GET
        response = requests.get(url, timeout=10)
        
        print(f"Status Code: {response.status_code}")
        print(f"Content-Type: {response.headers.get('content-type', 'N/A')}")
        
        if response.status_code == 200:
            print("✓ URL acessível")
            
            # Verificar se contém os dados do orçamento no JavaScript
            html_content = response.text
            
            # Procurar por window.orcamentoData
            if 'window.orcamentoData' in html_content:
                print("✓ window.orcamentoData encontrado no HTML")
                
                # Extrair o JSON
                match = re.search(r'window\.orcamentoData = ({.*?});', html_content, re.DOTALL)
                if match:
                    json_data = match.group(1)
                    print("✓ JSON extraído:")
                    print(json_data)
                else:
                    print("✗ Não foi possível extrair o JSON")
            else:
                print("✗ window.orcamentoData NÃO encontrado no HTML")
            
            # Verificar se contém a função de hidratação
            if 'function hidratarCamposOrcamento' in html_content:
                print("✓ Função hidratarCamposOrcamento encontrada")
            else:
                print("✗ Função hidratarCamposOrcamento NÃO encontrada")
            
            # Verificar se contém campos de formulário
            form_fields = [
                'id_cliente',
                'id_faixa_preco', 
                'id_forma_pagamento',
                'id_status',
                'id_data_entrega',
                'id_data_validade'
            ]
            
            print("\n--- Verificação de campos do formulário ---")
            for field in form_fields:
                if f'id="{field}"' in html_content:
                    print(f"✓ Campo {field} encontrado")
                else:
                    print(f"✗ Campo {field} NÃO encontrado")
            
        elif response.status_code == 404:
            print("✗ URL não encontrada (404)")
        elif response.status_code == 403:
            print("✗ Acesso negado (403)")
        elif response.status_code == 500:
            print("✗ Erro interno do servidor (500)")
            print("Conteúdo da resposta:")
            print(response.text[:1000])  # Primeiros 1000 caracteres
        else:
            print(f"✗ Status inesperado: {response.status_code}")
            
    except requests.exceptions.ConnectionError:
        print("✗ Erro de conexão - servidor não está rodando?")
    except requests.exceptions.Timeout:
        print("✗ Timeout na requisição")
    except Exception as e:
        print(f"✗ Erro inesperado: {e}")

if __name__ == "__main__":
    testar_url_edicao()
