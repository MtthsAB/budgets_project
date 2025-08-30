#!/usr/bin/env python
"""
Teste simulando o cadastro via formulário web que estava falhando
"""
import os
import sys
import django

# Configurar Django
sys.path.append('/home/matas/projetos/Project')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema_produtos.settings')
django.setup()

from django.test import RequestFactory, TestCase
from django.contrib.auth import get_user_model
from django.contrib.messages.storage.fallback import FallbackStorage
from django.contrib.sessions.middleware import SessionMiddleware
from produtos.views import produto_cadastro_view
from produtos.models import Produto, Modulo, TipoItem
import json

User = get_user_model()

def simulate_sofa_creation_with_modules():
    """Simula o cadastro de sofá com módulos via POST como estava falhando"""
    print("🧪 Simulando cadastro de sofá com módulos via formulário web...")
    
    try:
        # Criar factory de requisições
        factory = RequestFactory()
        
        # Criar usuário de teste
        user, created = User.objects.get_or_create(
            username='teste_user',
            defaults={'email': 'teste@teste.com', 'password': 'teste123'}
        )
        
        # Buscar ou criar tipo sofá
        tipo_sofa, created = TipoItem.objects.get_or_create(
            nome='Sofás',
            defaults={'nome': 'Sofás'}
        )
        
        # Dados do POST que simulam o formulário web
        post_data = {
            'ref_produto': 'SF001_TESTE',
            'nome_produto': 'Sofá Teste Via Web',
            'tipo_produto': str(tipo_sofa.id),
            'ativo': 'on',
            
            # Dados dos módulos (lista)
            'modulo_nome': ['Módulo Esquerdo', 'Módulo Direito'],
            
            # Dados específicos de cada módulo
            'modulo_profundidade_1': '85.0',
            'modulo_altura_1': '90.0',
            'modulo_braco_1': '25.0',
            'modulo_descricao_1': 'Módulo esquerdo do sofá',
            
            'modulo_profundidade_2': '85.0',
            'modulo_altura_2': '90.0',
            'modulo_braco_2': '25.0',
            'modulo_descricao_2': 'Módulo direito do sofá',
            
            # Dados dos tamanhos para módulo 1
            'tamanho_nome_1': ['200cm', '250cm'],
            'tamanho_largura_total_1': ['200.0', '250.0'],
            'tamanho_largura_assento_1': ['180.0', '230.0'],
            'tamanho_altura_1': ['85.0', '85.0'],
            'tamanho_profundidade_1': ['85.0', '85.0'],
            'tamanho_tecido_1': ['3.5', '4.2'],
            'tamanho_volume_1': ['1.2', '1.8'],
            'tamanho_peso_1': ['45.0', '55.0'],
            'tamanho_preco_1': ['1500.00', '1800.00'],
            'tamanho_descricao_1': ['Tamanho 200cm', 'Tamanho 250cm'],
            
            # Dados dos tamanhos para módulo 2
            'tamanho_nome_2': ['200cm', '250cm'],
            'tamanho_largura_total_2': ['200.0', '250.0'],
            'tamanho_largura_assento_2': ['180.0', '230.0'],
            'tamanho_altura_2': ['85.0', '85.0'],
            'tamanho_profundidade_2': ['85.0', '85.0'],
            'tamanho_tecido_2': ['3.5', '4.2'],
            'tamanho_volume_2': ['1.2', '1.8'],
            'tamanho_peso_2': ['45.0', '55.0'],
            'tamanho_preco_2': ['1500.00', '1800.00'],
            'tamanho_descricao_2': ['Tamanho 200cm', 'Tamanho 250cm'],
        }
        
        # Criar requisição POST
        request = factory.post('/produtos/cadastro/', post_data)
        request.user = user
        
        # Adicionar sessão e mensagens (necessário para o Django)
        middleware = SessionMiddleware(lambda req: None)
        middleware.process_request(request)
        request.session.save()
        
        messages = FallbackStorage(request)
        request._messages = messages
        
        print("✅ Requisição POST criada com dados do formulário")
        print(f"✅ Usuário: {user.username}")
        print(f"✅ Tipo produto: {tipo_sofa.nome} (ID: {tipo_sofa.id})")
        print(f"✅ Módulos: {post_data['modulo_nome']}")
        
        # Contar produtos antes
        produtos_antes = Produto.objects.count()
        modulos_antes = Modulo.objects.count()
        
        print(f"📊 Produtos antes: {produtos_antes}")
        print(f"📊 Módulos antes: {modulos_antes}")
        
        # Chamar a view (aqui era onde ocorria o erro)
        print("🔄 Chamando produto_cadastro_view...")
        response = produto_cadastro_view(request)
        
        # Verificar resultados
        produtos_depois = Produto.objects.count()
        modulos_depois = Modulo.objects.count()
        
        print(f"📊 Produtos depois: {produtos_depois}")
        print(f"📊 Módulos depois: {modulos_depois}")
        
        # Verificar se produto foi criado
        if produtos_depois > produtos_antes:
            produto_criado = Produto.objects.get(ref_produto='SF001_TESTE')
            print(f"✅ Produto criado: {produto_criado.ref_produto} - {produto_criado.nome_produto}")
            
            # Verificar módulos
            modulos = produto_criado.modulos.all()
            print(f"✅ Módulos criados: {modulos.count()}")
            
            for modulo in modulos:
                print(f"  - {modulo.nome}: {modulo.profundidade}cm x {modulo.altura}cm")
                tamanhos = modulo.tamanhos_detalhados.all()
                print(f"    Tamanhos: {tamanhos.count()}")
                for tamanho in tamanhos:
                    print(f"      - {tamanho.largura_total}cm: R$ {tamanho.preco}")
            
            # Limpeza
            produto_criado.delete()
            print("✅ Dados de teste removidos")
            
            print("\n🎉 TESTE DE SIMULAÇÃO WEB PASSOU!")
            print("💡 O erro 'Modulo() got unexpected keyword arguments: item' foi corrigido!")
            return True
        else:
            print("❌ Produto não foi criado")
            return False
            
    except Exception as e:
        print(f"❌ ERRO na simulação: {str(e)}")
        print(f"❌ Tipo do erro: {type(e).__name__}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("🚀 Simulando cadastro via formulário web...")
    print("=" * 60)
    
    success = simulate_sofa_creation_with_modules()
    
    print("\n" + "=" * 60)
    if success:
        print("🎉 SIMULAÇÃO PASSOU!")
        print("✅ O usuário agora pode cadastrar sofás com módulos via formulário")
        print("✅ O erro 'unexpected keyword arguments: item' foi totalmente corrigido")
    else:
        print("❌ SIMULAÇÃO FALHOU!")
        print("💡 Verifique os erros acima para mais detalhes")
