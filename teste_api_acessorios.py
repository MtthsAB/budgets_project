#!/usr/bin/env python3
"""
Script para testar a API endpoint que retorna dados de sofás com acessórios vinculados
"""

import requests
import json

def testar_api_sofa():
    """Testa a API de detalhes do produto para sofás"""
    
    print("=== TESTE DA API DE DETALHES DO PRODUTO ===\n")
    
    base_url = "http://localhost:8000"
    
    # IDs dos sofás para testar (baseado no script anterior)
    sofas_para_testar = [
        ("produto_9", "SF939 - LE COULTRE"),
        ("produto_7", "SF982 - Big Boss")
    ]
    
    for produto_id, nome_sofa in sofas_para_testar:
        print(f"🛋️  Testando: {nome_sofa}")
        print(f"    URL: {base_url}/orcamentos/detalhes-produto/?produto_id={produto_id}")
        
        try:
            response = requests.get(
                f"{base_url}/orcamentos/detalhes-produto/",
                params={'produto_id': produto_id}
            )
            
            if response.status_code == 200:
                data = response.json()
                produto = data.get('produto', {})
                
                print(f"    ✅ Status: {response.status_code} OK")
                print(f"    📦 Nome: {produto.get('nome', 'N/A')}")
                print(f"    🔧 Módulos: {len(produto.get('modulos', []))}")
                
                # Verificar acessórios vinculados
                acessorios_vinculados = produto.get('acessorios_vinculados', [])
                print(f"    🎨 Acessórios vinculados: {len(acessorios_vinculados)}")
                
                if acessorios_vinculados:
                    print(f"    📋 Lista de acessórios:")
                    for acessorio in acessorios_vinculados:
                        nome = acessorio.get('nome', 'N/A')
                        ref = acessorio.get('ref', 'N/A')
                        preco = acessorio.get('preco', 0)
                        print(f"        - {ref}: {nome} (R$ {preco:.2f})")
                else:
                    print(f"    ⚠️  Nenhum acessório vinculado encontrado na API")
                
                # Verificar estrutura da resposta
                campos_esperados = ['id', 'nome', 'tipo', 'modulos', 'acessorios_vinculados']
                campos_encontrados = [campo for campo in campos_esperados if campo in produto]
                print(f"    📊 Campos da API: {len(campos_encontrados)}/{len(campos_esperados)} encontrados")
                
                if len(campos_encontrados) == len(campos_esperados):
                    print(f"    ✅ Estrutura da API está correta")
                else:
                    print(f"    ⚠️  Campos faltando: {set(campos_esperados) - set(campos_encontrados)}")
                
            else:
                print(f"    ❌ Erro HTTP: {response.status_code}")
                print(f"    📄 Resposta: {response.text[:200]}...")
                
        except requests.exceptions.ConnectionError:
            print(f"    ❌ Erro de conexão: Servidor Django não está rodando")
        except requests.exceptions.RequestException as e:
            print(f"    ❌ Erro na requisição: {e}")
        except json.JSONDecodeError as e:
            print(f"    ❌ Erro no JSON: {e}")
        
        print()

def testar_endpoint_produtos_por_tipo():
    """Testa o endpoint que lista produtos por tipo"""
    
    print("=== TESTE DO ENDPOINT PRODUTOS POR TIPO ===\n")
    
    base_url = "http://localhost:8000"
    
    try:
        response = requests.get(f"{base_url}/orcamentos/produtos-por-tipo/?tipo=sofa")
        
        if response.status_code == 200:
            data = response.json()
            produtos = data.get('produtos', [])
            
            print(f"✅ Status: {response.status_code} OK")
            print(f"📊 Sofás encontrados: {len(produtos)}")
            
            for produto in produtos:
                valor = produto.get('value', 'N/A')
                texto = produto.get('text', 'N/A')
                print(f"    - {valor}: {texto}")
        else:
            print(f"❌ Erro HTTP: {response.status_code}")
            
    except requests.exceptions.ConnectionError:
        print(f"❌ Erro de conexão: Servidor Django não está rodando")
    except Exception as e:
        print(f"❌ Erro: {e}")

if __name__ == "__main__":
    testar_endpoint_produtos_por_tipo()
    print("\n" + "="*50 + "\n")
    testar_api_sofa()
    
    print("\n🎉 CONCLUSÃO:")
    print("Se todos os testes passaram, a API está retornando corretamente")
    print("os acessórios vinculados aos sofás para o frontend.")
    print("\nPróximo passo: Testar no navegador em http://localhost:8000/orcamentos/novo/")
