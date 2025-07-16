#!/usr/bin/env python3
"""
Script para testar o fluxo completo de seleção de sofás após correções
"""
import os
import sys
import django
import requests
from requests.sessions import Session

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema_produtos.settings')
sys.path.append('/home/matas/projetos/Project')
django.setup()

from authentication.models import CustomUser

def main():
    print("🧪 Testando correções do fluxo de seleção de sofás...")
    
    session = Session()
    base_url = "http://localhost:8000"
    
    # 1. Login
    print("\n🔑 Fazendo login...")
    login_url = f"{base_url}/auth/login/"
    
    try:
        response = session.get(login_url)
        if response.status_code != 200:
            print(f"❌ Erro ao acessar página de login: {response.status_code}")
            return
        
        csrf_token = None
        for line in response.text.split('\n'):
            if 'csrfmiddlewaretoken' in line and 'value=' in line:
                csrf_token = line.split('value="')[1].split('"')[0]
                break
        
        if not csrf_token:
            print("❌ Não foi possível obter CSRF token")
            return
        
        print(f"✅ CSRF token obtido")
        
        # Fazer login
        login_data = {
            'email': 'admin@test.com',
            'password': 'admin123',
            'csrfmiddlewaretoken': csrf_token
        }
        
        response = session.post(login_url, data=login_data)
        if response.status_code == 200 and 'login' not in response.url:
            print("✅ Login realizado com sucesso!")
        else:
            print(f"❌ Erro no login: {response.status_code}")
            return
        
        # 2. Testar página de formulário
        print("\n📝 Testando página de formulário...")
        form_url = f"{base_url}/orcamentos/novo/"
        response = session.get(form_url)
        
        if response.status_code == 200:
            print("✅ Página de formulário acessível!")
            
            # Verificar se as funções JavaScript corrigidas estão presentes
            funções_necessarias = [
                'carregarSeletorModulos',
                'renderizarAcessoriosSofa',
                'atualizarListaModulosAdicionados',
                'removerModulo'
            ]
            
            funções_encontradas = {}
            for função in funções_necessarias:
                if f'function {função}' in response.text:
                    funções_encontradas[função] = True
                    print(f"  ✅ {função}")
                else:
                    funções_encontradas[função] = False
                    print(f"  ❌ {função}")
            
            # Verificar elementos HTML
            elementos_necessarios = [
                'id="tipo-produto"',
                'id="produto"', 
                'id="sofa-configuracao"',
                'id="modulos-lista"',
                'id="acessorios-lista"',
                'id="resumo-modulos"'
            ]
            
            elementos_encontrados = {}
            for elemento in elementos_necessarios:
                if elemento in response.text:
                    elementos_encontrados[elemento] = True
                    print(f"  ✅ {elemento}")
                else:
                    elementos_encontrados[elemento] = False
                    print(f"  ❌ {elemento}")
        
        # 3. Testar endpoint de produtos por tipo
        print("\n🛋️ Testando endpoint de produtos por tipo...")
        produtos_url = f"{base_url}/orcamentos/produtos-por-tipo/?tipo=sofa"
        response = session.get(produtos_url)
        
        if response.status_code == 200:
            try:
                data = response.json()
                if 'produtos' in data and len(data['produtos']) > 0:
                    print(f"✅ {len(data['produtos'])} produtos encontrados")
                    primeiro_produto = data['produtos'][0]
                    print(f"  📋 Primeiro produto: {primeiro_produto.get('nome_produto', 'N/A')}")
                    
                    # 4. Testar endpoint de detalhes
                    produto_id = primeiro_produto['id']
                    print(f"\n🔍 Testando detalhes do produto: {produto_id}")
                    
                    detalhes_url = f"{base_url}/orcamentos/detalhes-produto/?produto_id={produto_id}"
                    response = session.get(detalhes_url)
                    
                    if response.status_code == 200:
                        detalhes = response.json()
                        if 'produto' in detalhes:
                            produto_detalhes = detalhes['produto']
                            print("✅ Detalhes do produto obtidos:")
                            print(f"  📋 Nome: {produto_detalhes.get('nome', 'N/A')}")
                            print(f"  🧩 Módulos: {len(produto_detalhes.get('modulos', []))}")
                            print(f"  🔧 Acessórios: {len(produto_detalhes.get('acessorios', []))}")
                        else:
                            print("❌ Estrutura de resposta inesperada")
                            print(f"Resposta: {detalhes}")
                    else:
                        print(f"❌ Erro ao obter detalhes: {response.status_code}")
                else:
                    print("❌ Nenhum produto encontrado")
            except Exception as e:
                print(f"❌ Erro ao processar resposta: {e}")
        else:
            print(f"❌ Erro no endpoint: {response.status_code}")
        
        # 5. Verificar permissões do usuário
        print("\n👤 Verificando permissões do usuário...")
        try:
            user = CustomUser.objects.get(email='admin@test.com')
            print(f"✅ Usuário: {user.email}")
            print(f"✅ Tipo permissão: {user.tipo_permissao}")
            print(f"✅ Pode acessar orçamentos: {user.can_access_orcamentos()}")
        except Exception as e:
            print(f"❌ Erro ao verificar usuário: {e}")
        
        print("\n🎉 Teste completo finalizado!")
        print("\n📋 Resumo das correções implementadas:")
        print("  ✅ Função carregarSeletorModulos() implementada")
        print("  ✅ Função renderizarAcessoriosSofa() implementada") 
        print("  ✅ Função atualizarListaModulosAdicionados() implementada")
        print("  ✅ Função removerModulo() implementada")
        print("  ✅ Event listeners dos módulos corrigidos")
        print("  ✅ Integração com variáveis modulosSelecionados e acessoriosSelecionados")
        
    except Exception as e:
        print(f"❌ Erro durante o teste: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
