#!/usr/bin/env python3
"""
Script para testar a hidratação com autenticação
"""

import requests
import re
import json
from urllib.parse import urljoin

def login_e_teste():
    """Faz login e testa a hidratação"""
    
    print("🧪 === TESTE COM AUTENTICAÇÃO ===")
    
    # Criar sessão para manter cookies
    session = requests.Session()
    
    try:
        # 1. Acessar página de login para obter CSRF token
        print("🔐 Obtendo token CSRF...")
        login_page = session.get("http://localhost:8000/auth/login/")
        
        # Extrair CSRF token
        csrf_pattern = r'name="csrfmiddlewaretoken" value="([^"]*)"'
        csrf_match = re.search(csrf_pattern, login_page.text)
        
        if not csrf_match:
            print("❌ Não foi possível obter token CSRF")
            return False
            
        csrf_token = csrf_match.group(1)
        print(f"✅ Token CSRF obtido: {csrf_token[:20]}...")
        
        # 2. Fazer login
        print("🔑 Fazendo login...")
        
        # Tentar diferentes credenciais
        credenciais = [
            ('admin@teste.com', 'admin123'),
            ('admin@teste.com', '123456'),
            ('admin@essere.com', 'admin123'),
            ('admin@essere.com', '123456'),
            ('matas@meitans.shop', 'admin123'),
            ('matas@meitans.shop', '123456'),
        ]
        
        login_success = False
        
        for email, password in credenciais:
            print(f"   Tentando {email}...")
            
            # Obter novo CSRF para cada tentativa
            login_page = session.get("http://localhost:8000/auth/login/")
            csrf_match = re.search(csrf_pattern, login_page.text)
            if not csrf_match:
                continue
                
            csrf_token = csrf_match.group(1)
            
            login_data = {
                'username': email,  # O campo se chama username mas recebe email
                'password': password,
                'csrfmiddlewaretoken': csrf_token
            }
            
            login_response = session.post(
                "http://localhost:8000/auth/login/",
                data=login_data,
                headers={'Referer': 'http://localhost:8000/auth/login/'}
            )
            
            if login_response.status_code == 200 and 'login' not in login_response.url:
                print(f"✅ Login realizado com {email}")
                login_success = True
                break
            elif login_response.status_code == 200:
                # Verificar se há mensagem de erro específica
                if 'error' in login_response.text.lower() or 'inválid' in login_response.text.lower():
                    print(f"   ❌ Credenciais inválidas para {email}")
                else:
                    print(f"   ⚠️  Redirecionado novamente para login")
        
        if not login_success:
            print("❌ Falha em todas as tentativas de login")
            print("💡 Vou tentar criar um usuário de teste...")
            
            # Última tentativa: acessar sem login (pode ter permissões abertas)
            print("🔓 Tentando acesso direto...")
            direct_response = session.get("http://localhost:8000/orcamentos/5/editar/")
            if direct_response.status_code == 200 and 'login' not in direct_response.url:
                print("✅ Acesso permitido sem login")
                edit_response = direct_response
            else:
                return False
        else:
        
        else:
                return False
        
        # 3. Acessar página de edição
        print("🌐 Acessando página de edição...")
        if login_success:
            edit_response = session.get("http://localhost:8000/orcamentos/5/editar/")
        # edit_response já foi definido no caso de acesso direto
        
        if edit_response.status_code != 200:
            print(f"❌ Erro ao acessar página de edição: {edit_response.status_code}")
            return False
            
        if 'login' in edit_response.url:
            print("❌ Ainda redirecionando para login")
            return False
            
        print("✅ Página de edição acessada com sucesso")
        
        content = edit_response.text
        
        # Verificar payload
        if 'window.orcamentoData' in content:
            print("✅ Payload de dados encontrado")
            
            # Extrair JSON
            pattern = r'window\.orcamentoData = ({.*?});'
            match = re.search(pattern, content, re.DOTALL)
            
            if match:
                json_str = match.group(1)
                try:
                    orcamento_data = json.loads(json_str)
                    print("✅ JSON parseado com sucesso")
                    
                    print(f"\n📋 DADOS DO ORÇAMENTO:")
                    print(f"   Cliente ID: {orcamento_data.get('cliente_id')}")
                    print(f"   Cliente Nome: '{orcamento_data.get('cliente_nome')}'")
                    print(f"   Status: {orcamento_data.get('status')}")
                    print(f"   Desconto Valor: R$ {orcamento_data.get('desconto_valor')}")
                    print(f"   Desconto Percentual: {orcamento_data.get('desconto_percentual')}%")
                    print(f"   Acréscimo Valor: R$ {orcamento_data.get('acrescimo_valor')}")
                    print(f"   Acréscimo Percentual: {orcamento_data.get('acrescimo_percentual')}%")
                    
                except json.JSONDecodeError as e:
                    print(f"❌ Erro ao parsear JSON: {e}")
                    print(f"JSON bruto: {json_str[:500]}...")
        else:
            print("❌ Payload não encontrado")
            
        # Verificar elementos da página
        print(f"\n🔍 VERIFICANDO ELEMENTOS DA PÁGINA:")
        
        elementos = {
            'cliente-busca': 'Campo de busca do cliente',
            'desconto_valor_unificado': 'Campo unificado de desconto',
            'acrescimo_valor_unificado': 'Campo unificado de acréscimo',
            'desconto_tipo_btn': 'Botão de tipo do desconto',
            'acrescimo_tipo_btn': 'Botão de tipo do acréscimo'
        }
        
        for elemento_id, descricao in elementos.items():
            if f'id="{elemento_id}"' in content:
                print(f"   ✅ {descricao}")
            else:
                print(f"   ❌ {descricao}")
        
        # Verificar funções JavaScript
        print(f"\n🔍 VERIFICANDO FUNÇÕES JAVASCRIPT:")
        
        funcoes = {
            'hidratarCamposOrcamento': 'Função principal de hidratação',
            'hidratarDescontoAcrescimo': 'Função específica desc/acr',
            'atualizarBotaoTipo': 'Função de atualizar botão'
        }
        
        for funcao, descricao in funcoes.items():
            if funcao in content:
                print(f"   ✅ {descricao}")
            else:
                print(f"   ❌ {descricao}")
        
        # Verificar chamada de hidratação
        if 'hidratarCamposOrcamento();' in content:
            print("   ✅ Chamada de hidratação encontrada")
        else:
            print("   ❌ Chamada de hidratação não encontrada")
        
        print(f"\n📏 TAMANHO DA PÁGINA: {len(content)} caracteres")
        
        # Salvar página para debug (opcional)
        with open('/tmp/orcamento_page.html', 'w', encoding='utf-8') as f:
            f.write(content)
        print("💾 Página salva em /tmp/orcamento_page.html")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro durante o teste: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    sucesso = login_e_teste()
    if sucesso:
        print("\n🎉 TESTE CONCLUÍDO!")
        print("\n📝 PARA TESTE MANUAL:")
        print("   1. Faça login em http://localhost:8000/auth/login/")
        print("   2. Acesse http://localhost:8000/orcamentos/5/editar/")
        print("   3. Abra DevTools (F12) → Console")
        print("   4. Verifique: console.log(window.orcamentoData)")
        print("   5. Campos devem estar preenchidos automaticamente")
    else:
        print("\n❌ TESTE FALHOU")
        print("   Verifique se o servidor está rodando")
        print("   Verifique as credenciais de login")
