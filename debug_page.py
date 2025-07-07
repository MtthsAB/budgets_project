#!/usr/bin/env python3
"""
Debug para ver o que está sendo retornado pela página
"""

import requests

def debug_page():
    try:
        response = requests.get('http://localhost:8000/produtos/cadastro/')
        print(f"Status: {response.status_code}")
        print(f"URL final: {response.url}")
        print(f"Headers: {dict(response.headers)}")
        print("\n=== PRIMEIRAS 1000 CARACTERES DO CONTEÚDO ===")
        print(response.text[:1000])
        print("\n=== ÚLTIMOS 500 CARACTERES DO CONTEÚDO ===")
        print(response.text[-500:])
        
        # Verificar se há redirecionamento
        if response.history:
            print(f"\n=== HISTÓRICO DE REDIRECIONAMENTOS ===")
            for resp in response.history:
                print(f"- {resp.status_code} -> {resp.url}")
                
    except Exception as e:
        print(f"Erro: {e}")

if __name__ == '__main__':
    debug_page()
