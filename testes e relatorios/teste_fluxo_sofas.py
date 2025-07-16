#!/usr/bin/env python3
"""
Script para testar o fluxo de seleção de sofás via requests
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

from django.contrib.auth.models import User
from produtos.models import Produto, TipoItem

def main():
    print("🧪 Testando fluxo de seleção de sofás...")
    
    # Verificar dados no banco
    print("\n📊 Verificando dados no banco:")
    
    tipos = TipoItem.objects.all()
    print(f"- Tipos de produto: {tipos.count()}")
    for tipo in tipos:
        print(f"  * {tipo.nome}")
    
    # Buscar produtos do tipo sofá
    try:
        tipo_sofa = TipoItem.objects.get(nome__icontains='sofá')
        sofas = Produto.objects.filter(id_tipo_produto=tipo_sofa)
        print(f"- Sofás (tipo '{tipo_sofa.nome}'): {sofas.count()}")
        for sofa in sofas[:5]:
            print(f"  * {sofa.nome_produto} (ID: {sofa.id})")
    except TipoItem.DoesNotExist:
        print("❌ Tipo 'sofá' não encontrado!")
        sofas = Produto.objects.none()
    
    # Testar endpoints
    print("\n🌐 Testando endpoints...")
    
    session = Session()
    base_url = "http://localhost:8000"
    
    # 1. Login
    print("🔑 Fazendo login...")
    login_url = f"{base_url}/auth/login/"
    
    # Obter CSRF token
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
    
    print(f"✅ CSRF token obtido: {csrf_token[:10]}...")
    
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
        print(f"❌ Erro no login: {response.status_code}, URL: {response.url}")
        return
    
    # 2. Testar endpoint de produtos por tipo
    print("\n🛋️ Testando endpoint de produtos por tipo...")
    produtos_url = f"{base_url}/orcamentos/produtos-por-tipo/?tipo=sofa"
    response = session.get(produtos_url)
    
    if response.status_code == 200:
        try:
            produtos = response.json()
            print(f"✅ Endpoint funcionando! {len(produtos)} produtos encontrados")
            for produto in produtos[:3]:
                print(f"  * {produto.get('nome', 'N/A')} (ID: {produto.get('id', 'N/A')})")
                
            # 3. Testar detalhes de produto
            if produtos:
                primeiro_produto = produtos[0]
                produto_id = f"sofa_{primeiro_produto['id']}"
                
                print(f"\n🔍 Testando detalhes do produto: {produto_id}")
                detalhes_url = f"{base_url}/orcamentos/detalhes-produto/{produto_id}/"
                response = session.get(detalhes_url)
                
                if response.status_code == 200:
                    detalhes = response.json()
                    print("✅ Detalhes obtidos com sucesso!")
                    print(f"  * Nome: {detalhes.get('nome', 'N/A')}")
                    print(f"  * Preço: {detalhes.get('preco', 'N/A')}")
                    print(f"  * Módulos: {len(detalhes.get('modulos', []))}")
                else:
                    print(f"❌ Erro ao obter detalhes: {response.status_code}")
        except Exception as e:
            print(f"❌ Erro ao processar resposta: {e}")
            print(f"Resposta: {response.text[:200]}...")
    else:
        print(f"❌ Erro no endpoint de produtos: {response.status_code}")
        print(f"Resposta: {response.text[:200]}...")
    
    # 4. Testar página de formulário
    print("\n📝 Testando página de formulário...")
    form_url = f"{base_url}/orcamentos/novo/"
    response = session.get(form_url)
    
    if response.status_code == 200:
        print("✅ Página de formulário acessível!")
        
        # Verificar se os elementos estão presentes
        elementos = {
            'tipo-produto': 'id="tipo-produto"' in response.text,
            'produto': 'id="produto"' in response.text,
            'sofa-configuracao': 'id="sofa-configuracao"' in response.text,
            'carregarDetalhesProduto': 'carregarDetalhesProduto' in response.text,
            'debugSofaSelection': 'debugSofaSelection' in response.text,
        }
        
        print("🔍 Elementos encontrados no HTML:")
        for elemento, presente in elementos.items():
            status = "✅" if presente else "❌"
            print(f"  {status} {elemento}")
            
    else:
        print(f"❌ Erro ao acessar formulário: {response.status_code}")
    
    print("\n🎉 Teste completo finalizado!")

if __name__ == "__main__":
    main()
