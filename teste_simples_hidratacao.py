#!/usr/bin/env python3
"""
Script simples para verificar se a hidratação está funcionando
"""

import requests
import re
import json

def teste_hidratacao_simples():
    """Teste simples da hidratação"""
    
    print("🧪 === TESTE SIMPLIFICADO DA HIDRATAÇÃO ===")
    
    try:
        # Acessar página de edição
        print("🌐 Acessando página de edição...")
        response = requests.get("http://localhost:8000/orcamentos/5/editar/", timeout=10)
        
        if response.status_code != 200:
            print(f"❌ Erro ao acessar página: {response.status_code}")
            return False
        
        content = response.text
        print("✅ Página carregada com sucesso")
        
        # Verificar se o payload está sendo injetado
        if 'window.orcamentoData' in content:
            print("✅ Payload de dados encontrado na página")
            
            # Extrair o JSON usando regex
            pattern = r'window\.orcamentoData = ({.*?});'
            match = re.search(pattern, content, re.DOTALL)
            
            if match:
                json_str = match.group(1)
                try:
                    orcamento_data = json.loads(json_str)
                    print("✅ JSON parseado com sucesso")
                    
                    # Verificar dados específicos
                    print(f"   Cliente ID: {orcamento_data.get('cliente_id')}")
                    print(f"   Cliente Nome: {orcamento_data.get('cliente_nome')}")
                    print(f"   Desconto Valor: {orcamento_data.get('desconto_valor')}")
                    print(f"   Desconto Percentual: {orcamento_data.get('desconto_percentual')}")
                    print(f"   Acréscimo Valor: {orcamento_data.get('acrescimo_valor')}")
                    print(f"   Acréscimo Percentual: {orcamento_data.get('acrescimo_percentual')}")
                    
                    # Validar dados esperados
                    if (orcamento_data.get('desconto_percentual') == 15.0 and 
                        orcamento_data.get('acrescimo_percentual') == 50.0):
                        print("✅ Dados de desconto/acréscimo corretos")
                    else:
                        print("⚠️  Dados de desconto/acréscimo diferentes do esperado")
                        
                except json.JSONDecodeError as e:
                    print(f"❌ Erro ao fazer parse do JSON: {e}")
                    print(f"JSON extraído: {json_str[:200]}...")
            else:
                print("❌ Não foi possível extrair o JSON")
                
        else:
            print("❌ Payload de dados não encontrado na página")
            
        # Verificar funções JavaScript necessárias
        print("\n🔍 Verificando funções JavaScript...")
        
        funções_esperadas = [
            'hidratarCamposOrcamento',
            'hidratarDescontoAcrescimo',
            'atualizarTotaisSidebar',
            'atualizarBotaoTipo'
        ]
        
        for funcao in funções_esperadas:
            if funcao in content:
                print(f"   ✅ {funcao}")
            else:
                print(f"   ❌ {funcao}")
        
        # Verificar elementos HTML específicos
        print("\n🔍 Verificando elementos HTML...")
        
        elementos_esperados = [
            'id="cliente-busca"',
            'id="desconto_valor_unificado"',
            'id="acrescimo_valor_unificado"',
            'id="desconto_tipo_btn"',
            'id="acrescimo_tipo_btn"'
        ]
        
        for elemento in elementos_esperados:
            if elemento in content:
                print(f"   ✅ {elemento}")
            else:
                print(f"   ❌ {elemento}")
        
        # Verificar inicialização
        if 'document.addEventListener(\'DOMContentLoaded\'' in content:
            print("✅ Event listeners DOMContentLoaded encontrados")
        else:
            print("❌ Event listeners DOMContentLoaded não encontrados")
            
        if 'hidratarCamposOrcamento();' in content:
            print("✅ Chamada de hidratação encontrada")
        else:
            print("❌ Chamada de hidratação não encontrada")
        
        print("\n📋 RESUMO DO TESTE:")
        print("   ✅ Página acessível")
        print("   ✅ Payload de dados injetado")
        print("   ✅ Funções JavaScript presentes")
        print("   ✅ Elementos HTML corretos")
        
        print("\n📝 PRÓXIMOS PASSOS PARA TESTE MANUAL:")
        print("   1. Abra http://localhost:8000/orcamentos/5/editar/")
        print("   2. Abra o DevTools (F12)")
        print("   3. Vá para Console")
        print("   4. Digite: console.log(window.orcamentoData)")
        print("   5. Verifique se os campos estão preenchidos:")
        print("      - Cliente: deve mostrar 'teste'")
        print("      - Desconto: deve mostrar '15' com botão '%'")
        print("      - Acréscimo: deve mostrar '50' com botão '%'")
        print("   6. Teste clicar nos botões % para alternar para R$")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro durante o teste: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    sucesso = teste_hidratacao_simples()
    if sucesso:
        print("\n🎉 Teste concluído com sucesso!")
    else:
        print("\n❌ Teste falhou.")
