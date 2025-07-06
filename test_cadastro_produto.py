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
from django.test import Client
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()

def test_edicao_produto():
    """Testa a edição de produto via interface web"""
    
    # Criar usuário de teste se não existir
    user, created = User.objects.get_or_create(
        email='testuser@test.com',
        defaults={'first_name': 'Test', 'last_name': 'User', 'password': 'testpass123'}
    )
    if created:
        user.set_password('testpass123')
        user.save()
        print(f"Usuário de teste criado: {user.email}")
    
    # Criar cliente de teste
    client = Client()
    
    # Fazer login
    login_success = client.login(email='testuser@test.com', password='testpass123')
    if not login_success:
        print("Erro: Não foi possível fazer login")
        return
    
    print("Login realizado com sucesso")
    
    # Buscar um produto existente para editar
    produto = Item.objects.first()
    if not produto:
        print("Nenhum produto encontrado para editar")
        return
    
    print(f"Produto selecionado para edição: {produto.ref_produto} - {produto.nome_produto}")
    print(f"Módulos atuais: {produto.modulos.count()}")
    
    # Dados para edição
    dados_edicao = {
        'ref_produto': produto.ref_produto + '_EDITADO',
        'nome_produto': produto.nome_produto + ' (Editado)',
        'tipo_produto': produto.id_tipo_produto.id,
        'ativo': 'on',
        'tem_cor_tecido': 'on',
        'tem_difer_desenho_lado': '',
        'tem_difer_desenho_tamanho': '',
        
        # Módulo 1
        'modulo_nome_1': 'Módulo Editado 1',
        'modulo_profundidade_1': '95.5',
        'modulo_altura_1': '87.0',
        'modulo_braco_1': '27.5',
        'modulo_descricao_1': 'Módulo principal editado',
        
        # Tamanho 1 do Módulo 1
        'tamanho_nome_1_1': 'Pequeno Editado',
        'tamanho_largura_total_1_1': '160.0',
        'tamanho_largura_assento_1_1': '120.0',
        'tamanho_altura_1_1': '85.0',
        'tamanho_profundidade_1_1': '90.0',
        'tamanho_tecido_1_1': '3.5',
        'tamanho_volume_1_1': '0.65',
        'tamanho_peso_1_1': '35.0',
        'tamanho_preco_1_1': '999.99',
        'tamanho_descricao_1_1': 'Tamanho pequeno editado',
        
        # Tamanho 2 do Módulo 1
        'tamanho_nome_1_2': 'Grande Editado',
        'tamanho_largura_total_1_2': '200.0',
        'tamanho_largura_assento_1_2': '160.0',
        'tamanho_altura_1_2': '87.0',
        'tamanho_profundidade_1_2': '95.0',
        'tamanho_tecido_1_2': '5.5',
        'tamanho_volume_1_2': '1.2',
        'tamanho_peso_1_2': '55.0',
        'tamanho_preco_1_2': '1499.99',
        'tamanho_descricao_1_2': 'Tamanho grande editado',
        
        # Módulo 2
        'modulo_nome_2': 'Módulo Adicional',
        'modulo_profundidade_2': '80.0',
        'modulo_altura_2': '45.0',
        'modulo_braco_2': '0.0',
        'modulo_descricao_2': 'Módulo adicional novo',
        
        # Tamanho 1 do Módulo 2
        'tamanho_nome_2_1': 'Único',
        'tamanho_largura_total_2_1': '80.0',
        'tamanho_largura_assento_2_1': '70.0',
        'tamanho_altura_2_1': '45.0',
        'tamanho_profundidade_2_1': '80.0',
        'tamanho_tecido_2_1': '1.5',
        'tamanho_volume_2_1': '0.3',
        'tamanho_peso_2_1': '15.0',
        'tamanho_preco_2_1': '299.99',
        'tamanho_descricao_2_1': 'Tamanho único do módulo adicional',
    }
    
    # Fazer requisição POST para editar o produto
    url_edicao = reverse('produto_editar', args=[produto.id])
    response = client.post(url_edicao, dados_edicao)
    
    print(f"Status da resposta: {response.status_code}")
    
    if response.status_code == 302:  # Redirecionamento após sucesso
        print("✅ Edição realizada com sucesso!")
        
        # Verificar se o produto foi atualizado
        produto_atualizado = Item.objects.get(id=produto.id)
        print(f"Produto atualizado: {produto_atualizado.ref_produto} - {produto_atualizado.nome_produto}")
        print(f"Módulos após edição: {produto_atualizado.modulos.count()}")
        
        # Verificar módulos e tamanhos
        for modulo in produto_atualizado.modulos.all():
            print(f"  Módulo: {modulo.nome}")
            print(f"    Profundidade: {modulo.profundidade}, Altura: {modulo.altura}, Braço: {modulo.braco}")
            print(f"    Descrição: {modulo.descricao}")
            print(f"    Tamanhos: {modulo.tamanhos_detalhados.count()}")
            
            for tamanho in modulo.tamanhos_detalhados.all():
                print(f"      {tamanho.nome_tamanho}: {tamanho.largura_total}x{tamanho.altura_cm}x{tamanho.profundidade_cm}cm - R${tamanho.preco}")
                print(f"        Descrição: {tamanho.descricao}")
        
    else:
        print(f"❌ Erro na edição. Status: {response.status_code}")
        if hasattr(response, 'content'):
            print(f"Conteúdo da resposta: {response.content.decode('utf-8')[:500]}...")

def test_cadastro_novo_produto():
    """Testa o cadastro de um novo produto"""
    
    # Criar cliente de teste
    client = Client()
    
    # Fazer login
    client.login(email='testuser@test.com', password='testpass123')
    
    # Buscar tipo de produto
    tipo_sofa = TipoItem.objects.first()
    if not tipo_sofa:
        print("Nenhum tipo de produto encontrado")
        return
    
    # Dados para novo produto
    dados_produto = {
        'ref_produto': f'TEST_NOVO_{int(__import__("time").time())}',
        'nome_produto': 'Produto de Teste Novo',
        'tipo_produto': tipo_sofa.id,
        'ativo': 'on',
        'tem_cor_tecido': 'on',
        
        # Módulo 1
        'modulo_nome': ['Módulo Teste Novo'],
        'modulo_profundidade_1': '100.0',
        'modulo_altura_1': '90.0',
        'modulo_braco_1': '30.0',
        'modulo_descricao_1': 'Módulo de teste para cadastro',
        
        # Tamanhos do módulo
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
    
    # Fazer requisição POST para cadastrar
    url_cadastro = reverse('produto_cadastro')
    response = client.post(url_cadastro, dados_produto)
    
    print(f"Status do cadastro: {response.status_code}")
    
    if response.status_code == 302:  # Redirecionamento após sucesso
        print("✅ Cadastro realizado com sucesso!")
        
        # Buscar o produto criado
        produto_novo = Item.objects.filter(ref_produto=dados_produto['ref_produto']).first()
        if produto_novo:
            print(f"Produto criado: {produto_novo.ref_produto} - {produto_novo.nome_produto}")
            print(f"Módulos: {produto_novo.modulos.count()}")
            
            for modulo in produto_novo.modulos.all():
                print(f"  Módulo: {modulo.nome} (Tamanhos: {modulo.tamanhos_detalhados.count()})")
    else:
        print(f"❌ Erro no cadastro. Status: {response.status_code}")

if __name__ == '__main__':
    print("=== Teste de Edição de Produto ===")
    test_edicao_produto()
    
    print("\n=== Teste de Cadastro de Produto ===")
    test_cadastro_novo_produto()
    
    print("\n=== Resumo Final ===")
    total_produtos = Item.objects.count()
    total_modulos = Modulo.objects.count()
    total_tamanhos = TamanhosModulosDetalhado.objects.count()
    
    print(f"Total de produtos: {total_produtos}")
    print(f"Total de módulos: {total_modulos}")
    print(f"Total de tamanhos: {total_tamanhos}")
