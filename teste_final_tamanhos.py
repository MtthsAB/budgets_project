#!/usr/bin/env python
"""
Teste final para verificar se os tamanhos dos módulos estão sendo salvos
"""
import os
import sys
import django

# Configurar Django
sys.path.append('/home/matas/projetos/Project')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema_produtos.settings')
django.setup()

from django.test import RequestFactory
from django.contrib.auth import get_user_model
from django.contrib.messages.storage.fallback import FallbackStorage
from django.contrib.sessions.middleware import SessionMiddleware
from produtos.views import produto_cadastro_view
from produtos.models import Produto, Modulo, TipoItem, TamanhosModulosDetalhado

User = get_user_model()

def test_cadastro_sofa_com_tamanhos():
    """Teste completo de cadastro de sofá com módulos e tamanhos"""
    print("🧪 Testando cadastro completo: sofá + módulos + tamanhos")
    
    try:
        # Criar factory de requisições
        factory = RequestFactory()
        
        # Criar ou buscar usuário
        user, created = User.objects.get_or_create(
            email='teste@teste.com',
            defaults={'first_name': 'Teste', 'last_name': 'User'}
        )
        
        # Buscar ou criar tipo sofá
        tipo_sofa, created = TipoItem.objects.get_or_create(
            nome='Sofás',
            defaults={'nome': 'Sofás'}
        )
        
        # Dados do POST simulando o formulário correto
        post_data = {
            'ref_produto': 'SF_TESTE_FINAL_001',
            'nome_produto': 'Sofá Teste Final com Tamanhos',
            'tipo_produto': str(tipo_sofa.id),
            'ativo': 'on',
            
            # Dados dos módulos
            'modulo_nome': ['Módulo Esquerdo', 'Módulo Direito'],
            
            # Dados específicos de cada módulo
            'modulo_profundidade_1': '85.0',
            'modulo_altura_1': '90.0',
            'modulo_braco_1': '25.0',
            'modulo_descricao_1': 'Módulo esquerdo',
            
            'modulo_profundidade_2': '85.0',
            'modulo_altura_2': '90.0',
            'modulo_braco_2': '25.0',
            'modulo_descricao_2': 'Módulo direito',
            
            # Tamanhos para módulo 1 (SEM campo nome - só dados)
            'tamanho_largura_total_1': ['200.0', '250.0'],
            'tamanho_largura_assento_1': ['180.0', '230.0'],
            'tamanho_tecido_1': ['3.5', '4.2'],
            'tamanho_volume_1': ['1.2', '1.8'],
            'tamanho_peso_1': ['45.0', '55.0'],
            'tamanho_preco_1': ['1500.00', '1800.00'],
            'tamanho_descricao_1': ['Tamanho 200cm', 'Tamanho 250cm'],
            
            # Tamanhos para módulo 2
            'tamanho_largura_total_2': ['200.0'],
            'tamanho_largura_assento_2': ['180.0'],
            'tamanho_tecido_2': ['3.5'],
            'tamanho_volume_2': ['1.2'],
            'tamanho_peso_2': ['45.0'],
            'tamanho_preco_2': ['1500.00'],
            'tamanho_descricao_2': ['Tamanho único'],
        }
        
        # Criar requisição POST
        request = factory.post('/produtos/cadastro/', post_data)
        request.user = user
        request.META['HTTP_X_CSRFTOKEN'] = 'test-token'  # Simular CSRF token
        
        # Adicionar sessão e mensagens
        middleware = SessionMiddleware(lambda req: None)
        middleware.process_request(request)
        request.session.save()
        request.session['_csrf_token'] = 'test-token'
        
        messages = FallbackStorage(request)
        request._messages = messages
        
        print(f"✅ Requisição criada com {len(post_data['modulo_nome'])} módulos")
        print(f"✅ Módulo 1: {len(post_data['tamanho_largura_total_1'])} tamanhos")
        print(f"✅ Módulo 2: {len(post_data['tamanho_largura_total_2'])} tamanhos")
        
        # Contar antes
        produtos_antes = Produto.objects.count()
        modulos_antes = Modulo.objects.count()
        tamanhos_antes = TamanhosModulosDetalhado.objects.count()
        
        print(f"📊 Antes - Produtos: {produtos_antes}, Módulos: {modulos_antes}, Tamanhos: {tamanhos_antes}")
        
        # Chamar a view
        print("🔄 Executando cadastro...")
        response = produto_cadastro_view(request)
        
        # Verificar resultados
        produtos_depois = Produto.objects.count()
        modulos_depois = Modulo.objects.count()
        tamanhos_depois = TamanhosModulosDetalhado.objects.count()
        
        print(f"📊 Depois - Produtos: {produtos_depois}, Módulos: {modulos_depois}, Tamanhos: {tamanhos_depois}")
        
        # Verificar se foi criado
        if produtos_depois > produtos_antes:
            produto = Produto.objects.get(ref_produto='SF_TESTE_FINAL_001')
            print(f"✅ Produto criado: {produto.ref_produto}")
            
            # Verificar módulos
            modulos = produto.modulos.all()
            print(f"✅ Módulos criados: {modulos.count()}")
            
            total_tamanhos = 0
            for i, modulo in enumerate(modulos, 1):
                tamanhos = modulo.tamanhos_detalhados.all()
                total_tamanhos += tamanhos.count()
                print(f"  - Módulo {i} ({modulo.nome}): {tamanhos.count()} tamanhos")
                
                for j, tamanho in enumerate(tamanhos, 1):
                    print(f"    * Tamanho {j}: {tamanho.largura_total}cm - R${tamanho.preco}")
            
            # Verificações
            assert modulos.count() == 2, f"Esperado 2 módulos, encontrado {modulos.count()}"
            assert total_tamanhos == 3, f"Esperado 3 tamanhos total, encontrado {total_tamanhos}"
            
            # Limpeza
            produto.delete()
            print("✅ Dados de teste removidos")
            
            print("\n🎉 TESTE COMPLETO PASSOU!")
            print("💡 Sofás com módulos e tamanhos estão sendo salvos corretamente!")
            return True
        else:
            print("❌ Produto não foi criado")
            return False
            
    except Exception as e:
        print(f"❌ ERRO: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("🚀 Teste final: cadastro completo de sofá com tamanhos")
    print("=" * 60)
    
    success = test_cadastro_sofa_com_tamanhos()
    
    print("\n" + "=" * 60)
    if success:
        print("🎉 TODOS OS PROBLEMAS RESOLVIDOS!")
        print("✅ Módulos estão sendo salvos")
        print("✅ Tamanhos estão sendo salvos")
        print("✅ Sistema funcional para N módulos com N tamanhos")
    else:
        print("❌ AINDA HÁ PROBLEMAS!")
        print("💡 Verifique os logs acima")
