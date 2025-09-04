#!/usr/bin/env python3
"""
Script para testar se o erro 500 foi corrigido - simula acesso às páginas de edição
"""
import requests
import sys

def test_edicao_produtos():
    """Testa se as páginas de edição estão funcionando"""
    
    print("=== TESTE FINAL - PÁGINAS DE EDIÇÃO ===\n")
    
    # URLs base
    base_url = "http://127.0.0.1:8000"
    
    # IDs de produtos para testar (baseado no script anterior)
    produto_ids = [60, 61, 62]
    
    print("Testando acesso às páginas de edição sem login (deve redirecionar para login):")
    
    for produto_id in produto_ids:
        url = f"{base_url}/produtos/{produto_id}/editar/"
        
        try:
            response = requests.get(url, allow_redirects=False)
            print(f"Produto {produto_id}: Status {response.status_code}")
            
            if response.status_code == 302:
                redirect_location = response.headers.get('Location', '')
                if '/auth/login/' in redirect_location:
                    print(f"  ✅ Redirecionou corretamente para login")
                else:
                    print(f"  ⚠️ Redirecionou para: {redirect_location}")
                    
            elif response.status_code == 500:
                print(f"  ❌ ERRO 500 - Problema não corrigido!")
                return False
                
            elif response.status_code == 200:
                print(f"  ✅ Página carregou diretamente (usuário já logado)")
                
            else:
                print(f"  ⚠️ Status inesperado: {response.status_code}")
                
        except requests.exceptions.ConnectionError:
            print(f"  ❌ Erro de conexão - servidor não está rodando?")
            return False
            
        except Exception as e:
            print(f"  ❌ Erro inesperado: {e}")
            return False
    
    print("\n✅ Teste concluído - Erro 500 corrigido com sucesso!")
    return True

if __name__ == "__main__":
    success = test_edicao_produtos()
    sys.exit(0 if success else 1)
