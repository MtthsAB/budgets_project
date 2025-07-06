#!/usr/bin/env python
import os
import sys
import django

# Adicionar o diretório do projeto ao path
sys.path.append('/home/matas/projetos/Project')

# Configurar o Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema_produtos.settings')
django.setup()

from produtos.models import Item, TipoItem, Modulo, TamanhosModulosDetalhado
from django.contrib.auth import get_user_model
from django.test import RequestFactory
from produtos.views import produto_editar_view
from django.middleware.csrf import get_token

User = get_user_model()

def test_edicao_direta():
    """Testa a edição de produto diretamente na view"""
    
    # Buscar um produto existente
    produto = Item.objects.first()
    if not produto:
        print("Nenhum produto encontrado para editar")
        return
    
    print(f"=== Testando Edição do Produto ===")
    print(f"Produto original: {produto.ref_produto} - {produto.nome_produto}")
    print(f"Módulos atuais: {produto.modulos.count()}")
    
    # Mostrar módulos atuais
    for modulo in produto.modulos.all():
        print(f"  Módulo: {modulo.nome}")
        print(f"    Tamanhos: {modulo.tamanhos_detalhados.count()}")
        for tamanho in modulo.tamanhos_detalhados.all():
            print(f"      {tamanho.nome_tamanho}: {tamanho.largura_total}x{tamanho.altura_cm}x{tamanho.profundidade_cm}cm")
    
    # Criar usuário de teste
    user, created = User.objects.get_or_create(
        email='test@test.com',
        defaults={'first_name': 'Test', 'last_name': 'User'}
    )
    if created:
        user.set_password('testpass123')
        user.save()
    
    # Criar request factory
    factory = RequestFactory()
    
    # Dados para edição - simulando formulário web
    dados_post = {
        'csrfmiddlewaretoken': 'dummy_token',
        'ref_produto': produto.ref_produto + '_EDITADO',
        'nome_produto': produto.nome_produto + ' (Editado)',
        'tipo_produto': str(produto.id_tipo_produto.id),
        'ativo': 'on',
        'tem_cor_tecido': 'on',
        
        # Módulo 1 - editado
        'modulo_nome_1': 'Módulo Principal Editado',
        'modulo_profundidade_1': '95.5',
        'modulo_altura_1': '87.0',
        'modulo_braco_1': '27.5',
        'modulo_descricao_1': 'Descrição do módulo editado',
        
        # Tamanho 1 do módulo 1
        'tamanho_nome_1_1': 'Pequeno Editado',
        'tamanho_largura_total_1_1': '160.0',
        'tamanho_largura_assento_1_1': '120.0',
        'tamanho_altura_1_1': '85.0',
        'tamanho_profundidade_1_1': '90.0',
        'tamanho_tecido_1_1': '3.5',
        'tamanho_volume_1_1': '0.65',
        'tamanho_peso_1_1': '35.0',
        'tamanho_preco_1_1': '999.99',
        'tamanho_descricao_1_1': 'Tamanho pequeno para teste',
        
        # Tamanho 2 do módulo 1
        'tamanho_nome_1_2': 'Grande Editado',
        'tamanho_largura_total_1_2': '200.0',
        'tamanho_largura_assento_1_2': '160.0',
        'tamanho_altura_1_2': '87.0',
        'tamanho_profundidade_1_2': '95.0',
        'tamanho_tecido_1_2': '5.5',
        'tamanho_volume_1_2': '1.2',
        'tamanho_peso_1_2': '55.0',
        'tamanho_preco_1_2': '1499.99',
        'tamanho_descricao_1_2': 'Tamanho grande para teste',
        
        # Módulo 2 - novo
        'modulo_nome_2': 'Módulo Secundário',
        'modulo_profundidade_2': '60.0',
        'modulo_altura_2': '40.0',
        'modulo_braco_2': '0.0',
        'modulo_descricao_2': 'Módulo adicional de teste',
        
        # Tamanho 1 do módulo 2
        'tamanho_nome_2_1': 'Único',
        'tamanho_largura_total_2_1': '80.0',
        'tamanho_largura_assento_2_1': '70.0',
        'tamanho_altura_2_1': '40.0',
        'tamanho_profundidade_2_1': '60.0',
        'tamanho_tecido_2_1': '1.5',
        'tamanho_volume_2_1': '0.25',
        'tamanho_peso_2_1': '12.0',
        'tamanho_preco_2_1': '299.99',
        'tamanho_descricao_2_1': 'Único tamanho do módulo secundário',
    }
    
    # Criar request POST
    request = factory.post(f'/produtos/{produto.id}/editar/', data=dados_post)
    request.user = user
    
    # Executar a view
    try:
        response = produto_editar_view(request, produto.id)
        print(f"✅ View executada com sucesso! Status: {response.status_code}")
        
        # Verificar se foi redirecionamento (sucesso)
        if response.status_code == 302:
            print("✅ Redirecionamento detectado - edição bem-sucedida!")
        
        # Recarregar produto do banco
        produto_atualizado = Item.objects.get(id=produto.id)
        print(f"\n=== Resultado da Edição ===")
        print(f"Produto atualizado: {produto_atualizado.ref_produto} - {produto_atualizado.nome_produto}")
        print(f"Módulos após edição: {produto_atualizado.modulos.count()}")
        
        # Mostrar módulos atualizados
        for i, modulo in enumerate(produto_atualizado.modulos.all(), 1):
            print(f"  Módulo {i}: {modulo.nome}")
            print(f"    Prof: {modulo.profundidade}, Alt: {modulo.altura}, Braço: {modulo.braco}")
            print(f"    Descrição: {modulo.descricao}")
            print(f"    Tamanhos: {modulo.tamanhos_detalhados.count()}")
            
            for j, tamanho in enumerate(modulo.tamanhos_detalhados.all(), 1):
                print(f"      Tamanho {j}: {tamanho.nome_tamanho}")
                print(f"        Dimensões: {tamanho.largura_total}x{tamanho.altura_cm}x{tamanho.profundidade_cm}cm")
                print(f"        Preço: R${tamanho.preco}")
                print(f"        Descrição: {tamanho.descricao}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro ao executar view: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def test_cadastro_direto():
    """Testa o cadastro de produto diretamente"""
    
    from produtos.views import produto_cadastro_view
    
    print(f"\n=== Testando Cadastro de Produto ===")
    
    # Buscar tipo de produto
    tipo = TipoItem.objects.first()
    if not tipo:
        print("Nenhum tipo de produto encontrado")
        return False
    
    # Criar usuário
    user, created = User.objects.get_or_create(
        email='test@test.com',
        defaults={'first_name': 'Test', 'last_name': 'User'}
    )
    
    # Criar request factory
    factory = RequestFactory()
    
    # Dados para cadastro
    import time
    ref_unica = f'TESTE_NOVO_{int(time.time())}'
    
    dados_post = {
        'csrfmiddlewaretoken': 'dummy_token',
        'ref_produto': ref_unica,
        'nome_produto': 'Produto Teste Novo',
        'tipo_produto': str(tipo.id),
        'ativo': 'on',
        'tem_cor_tecido': 'on',
        
        # Dados do módulo para cadastro (diferente da edição)
        'modulo_nome': ['Módulo Teste Cadastro'],
        'modulo_profundidade_1': '100.0',
        'modulo_altura_1': '90.0',
        'modulo_braco_1': '30.0',
        'modulo_descricao_1': 'Módulo de teste para cadastro',
        
        # Tamanhos do módulo para cadastro
        'tamanho_nome_1': ['Médio Teste'],
        'tamanho_largura_total_1': ['180.0'],
        'tamanho_largura_assento_1': ['150.0'],
        'tamanho_altura_1': ['90.0'],
        'tamanho_profundidade_1': ['100.0'],
        'tamanho_tecido_1': ['4.0'],
        'tamanho_volume_1': ['1.0'],
        'tamanho_peso_1': ['50.0'],
        'tamanho_preco_1': ['1299.99'],
        'tamanho_descricao_1': ['Tamanho médio de teste'],
    }
    
    # Criar request POST
    request = factory.post('/produtos/cadastro/', data=dados_post)
    request.user = user
    
    try:
        response = produto_cadastro_view(request)
        print(f"✅ View de cadastro executada! Status: {response.status_code}")
        
        if response.status_code == 302:
            print("✅ Redirecionamento detectado - cadastro bem-sucedido!")
            
            # Buscar produto criado
            produto_novo = Item.objects.filter(ref_produto=ref_unica).first()
            if produto_novo:
                print(f"Produto criado: {produto_novo.ref_produto} - {produto_novo.nome_produto}")
                print(f"Módulos: {produto_novo.modulos.count()}")
                
                for modulo in produto_novo.modulos.all():
                    print(f"  {modulo.nome} (Tamanhos: {modulo.tamanhos_detalhados.count()})")
                    for tamanho in modulo.tamanhos_detalhados.all():
                        print(f"    {tamanho.nome_tamanho}: R${tamanho.preco}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro ao executar cadastro: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    print("=== Teste Direto das Funcionalidades ===")
    
    # Teste de edição
    edicao_ok = test_edicao_direta()
    
    # Teste de cadastro
    cadastro_ok = test_cadastro_direto()
    
    print(f"\n=== Resumo Final ===")
    print(f"Edição funcionando: {'✅ SIM' if edicao_ok else '❌ NÃO'}")
    print(f"Cadastro funcionando: {'✅ SIM' if cadastro_ok else '❌ NÃO'}")
    
    # Estatísticas finais
    total_produtos = Item.objects.count()
    total_modulos = Modulo.objects.count()
    total_tamanhos = TamanhosModulosDetalhado.objects.count()
    
    print(f"\nEstatísticas do banco:")
    print(f"Total de produtos: {total_produtos}")
    print(f"Total de módulos: {total_modulos}")
    print(f"Total de tamanhos: {total_tamanhos}")
