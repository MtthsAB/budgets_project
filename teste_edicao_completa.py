#!/usr/bin/env python3
"""
Teste completo da funcionalidade de edição de produtos com tamanhos
"""
import os
import sys
import django

# Configurar Django
sys.path.append('/home/matas/projetos/Project')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema_produtos.settings')
django.setup()

from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from produtos.models import Item, TipoItem, Modulo, TamanhosModulosDetalhado

User = get_user_model()

def setup_test_data():
    """Cria dados de teste"""
    print("=== Configurando dados de teste ===")
    
    # Criar usuário de teste
    user, created = User.objects.get_or_create(
        email='teste@test.com',
        defaults={
            'first_name': 'Teste',
            'last_name': 'User'
        }
    )
    if created:
        user.set_password('teste123')
        user.save()
    print(f"Usuário: {user.email}")
    
    # Criar tipo de produto
    tipo, created = TipoItem.objects.get_or_create(
        nome='Sofá Teste'
    )
    print(f"Tipo: {tipo.nome}")
    
    # Criar produto de teste
    produto, created = Item.objects.get_or_create(
        ref_produto='TEST_EDIT_001',
        defaults={
            'nome_produto': 'Produto Teste Edição',
            'id_tipo_produto': tipo,
            'ativo': True,
            'tem_cor_tecido': True,
            'tem_difer_desenho_lado_dir_esq': False,
            'tem_difer_desenho_tamanho': True
        }
    )
    print(f"Produto: {produto.nome_produto} (ID: {produto.id})")
    
    # Criar módulo de teste
    modulo, created = Modulo.objects.get_or_create(
        item=produto,
        nome='Módulo Base',
        defaults={
            'profundidade': 80.0,
            'altura': 85.0,
            'braco': 25.0,
            'descricao': 'Módulo base para testes'
        }
    )
    print(f"Módulo: {modulo.nome} (ID: {modulo.id})")
    
    # Criar tamanho de teste
    tamanho_existente = TamanhosModulosDetalhado.objects.filter(id_modulo=modulo).first()
    if not tamanho_existente:
        tamanho = TamanhosModulosDetalhado.objects.create(
            id_modulo=modulo,
            largura_total=120.0,
            largura_assento=100.0,
            tecido_metros=2.5,
            volume_m3=0.85,
            peso_kg=45.0,
            preco=1500.00,
            descricao='Tamanho P'
        )
        print(f"Tamanho criado: Largura {tamanho.largura_total}cm")
    else:
        print(f"Tamanho existente: Largura {tamanho_existente.largura_total}cm")
    
    return user, produto

def test_view_produto_edicao(user, produto):
    """Testa a visualização da página de edição"""
    print("\n=== Testando visualização da página de edição ===")
    
    client = Client()
    client.force_login(user)
    
    # Acessar página de edição
    url = reverse('produto_editar', args=[produto.id])
    response = client.get(url)
    
    print(f"URL: {url}")
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        print("✓ Página de edição carregada com sucesso")
        
        # Verificar se os dados estão sendo passados corretamente
        context = response.context
        produto_context = context.get('produto')
        modulos_context = context.get('modulos')
        
        print(f"Produto no contexto: {produto_context.nome_produto if produto_context else 'None'}")
        print(f"Módulos no contexto: {len(modulos_context) if modulos_context else 0}")
        
        if modulos_context:
            for modulo in modulos_context:
                tamanhos = modulo.tamanhos_detalhados.all()
                print(f"  Módulo: {modulo.nome} - {len(tamanhos)} tamanho(s)")
                for tamanho in tamanhos:
                    print(f"    Tamanho: Largura {tamanho.largura_total}cm")
    else:
        print(f"✗ Erro ao carregar página: {response.status_code}")
        if hasattr(response, 'content'):
            print(f"Conteúdo: {response.content[:500]}")

def test_adicionar_tamanho_via_post(user, produto):
    """Testa a adição de tamanho via POST"""
    print("\n=== Testando adição de tamanho via POST ===")
    
    client = Client()
    client.force_login(user)
    
    # Obter dados do produto atual
    modulo = produto.modulos.first()
    tamanhos_antes = TamanhosModulosDetalhado.objects.filter(id_modulo=modulo).count()
    print(f"Tamanhos antes: {tamanhos_antes}")
    
    # Dados para o POST - simulando adição de novo tamanho
    post_data = {
        'ref_produto': produto.ref_produto,
        'nome_produto': produto.nome_produto,
        'tipo_produto': produto.id_tipo_produto.id,
        'ativo': 'on',
        'tem_cor_tecido': 'on',
        'tem_difer_desenho_tamanho': 'on',
        
        # Módulo existente
        'modulo_nome_1': modulo.nome,
        'modulo_profundidade_1': str(modulo.profundidade),
        'modulo_altura_1': str(modulo.altura),
        'modulo_braco_1': str(modulo.braco),
        'modulo_descricao_1': modulo.descricao or '',
        
        # Tamanho existente (será removido e recriado)
        'tamanho_largura_total_1_1': '120.0',
        'tamanho_largura_assento_1_1': '100.0',
        'tamanho_tecido_1_1': '2.5',
        'tamanho_volume_1_1': '0.85',
        'tamanho_peso_1_1': '45.0',
        'tamanho_preco_1_1': '1500.00',
        'tamanho_descricao_1_1': 'Tamanho P',
        
        # Novo tamanho sendo adicionado
        'tamanho_largura_total_1_2': '150.0',
        'tamanho_largura_assento_1_2': '130.0',
        'tamanho_tecido_1_2': '3.2',
        'tamanho_volume_1_2': '1.10',
        'tamanho_peso_1_2': '55.0',
        'tamanho_preco_1_2': '1800.00',
        'tamanho_descricao_1_2': 'Tamanho M',
    }
    
    print("Dados POST:")
    for key, value in post_data.items():
        if 'tamanho_' in key:
            print(f"  {key}: {value}")
    
    # Fazer a requisição POST
    url = reverse('produto_editar', args=[produto.id])
    response = client.post(url, post_data, follow=True)
    
    print(f"Response status: {response.status_code}")
    
    # Verificar se foi redirecionado com sucesso
    if response.status_code == 200:
        if 'produtos_lista' in str(response.redirect_chain):
            print("✓ Redirecionamento para lista após edição")
        
        # Verificar se os tamanhos foram criados corretamente
        tamanhos_depois = TamanhosModulosDetalhado.objects.filter(id_modulo=modulo).count()
        print(f"Tamanhos depois: {tamanhos_depois}")
        
        if tamanhos_depois == 2:
            print("✓ Novo tamanho adicionado com sucesso!")
            
            # Verificar os dados dos tamanhos
            tamanhos = TamanhosModulosDetalhado.objects.filter(id_modulo=modulo).order_by('largura_total')
            for i, tamanho in enumerate(tamanhos):
                print(f"  Tamanho {i+1}: {tamanho.largura_total}cm - {tamanho.descricao}")
        else:
            print(f"✗ Esperado 2 tamanhos, encontrado {tamanhos_depois}")
    else:
        print(f"✗ Erro na requisição: {response.status_code}")

def test_adicionar_modulo_com_tamanhos(user, produto):
    """Testa adição de novo módulo com tamanhos"""
    print("\n=== Testando adição de novo módulo com tamanhos ===")
    
    client = Client()
    client.force_login(user)
    
    modulos_antes = produto.modulos.count()
    print(f"Módulos antes: {modulos_antes}")
    
    # Dados para adicionar novo módulo com tamanhos
    post_data = {
        'ref_produto': produto.ref_produto,
        'nome_produto': produto.nome_produto,
        'tipo_produto': produto.id_tipo_produto.id,
        'ativo': 'on',
        'tem_cor_tecido': 'on',
        
        # Módulo existente
        'modulo_nome_1': produto.modulos.first().nome,
        'modulo_profundidade_1': '80.0',
        'modulo_altura_1': '85.0',
        'modulo_braco_1': '25.0',
        
        # Novo módulo
        'modulo_nome_2': 'Módulo Chaise',
        'modulo_profundidade_2': '160.0',
        'modulo_altura_2': '85.0',
        'modulo_braco_2': '0.0',
        'modulo_descricao_2': 'Módulo chaise longue',
        
        # Tamanhos do novo módulo
        'tamanho_largura_total_2_1': '180.0',
        'tamanho_largura_assento_2_1': '160.0',
        'tamanho_tecido_2_1': '4.0',
        'tamanho_volume_2_1': '1.5',
        'tamanho_peso_2_1': '65.0',
        'tamanho_preco_2_1': '2200.00',
        'tamanho_descricao_2_1': 'Chaise P',
    }
    
    print("Adicionando novo módulo com tamanho...")
    
    url = reverse('produto_editar', args=[produto.id])
    response = client.post(url, post_data, follow=True)
    
    if response.status_code == 200:
        modulos_depois = produto.modulos.count()
        print(f"Módulos depois: {modulos_depois}")
        
        if modulos_depois == 2:
            print("✓ Novo módulo adicionado com sucesso!")
            
            # Verificar o novo módulo
            novo_modulo = produto.modulos.filter(nome='Módulo Chaise').first()
            if novo_modulo:
                tamanhos_novo_modulo = novo_modulo.tamanhos_detalhados.count()
                print(f"  Novo módulo tem {tamanhos_novo_modulo} tamanho(s)")
                
                if tamanhos_novo_modulo == 1:
                    tamanho = novo_modulo.tamanhos_detalhados.first()
                    print(f"  ✓ Tamanho: {tamanho.largura_total}cm - {tamanho.descricao}")
                else:
                    print("  ✗ Tamanho não foi criado corretamente")
            else:
                print("  ✗ Novo módulo não foi encontrado")
        else:
            print(f"✗ Esperado 2 módulos, encontrado {modulos_depois}")

def main():
    print("=== TESTE COMPLETO DE EDIÇÃO DE PRODUTOS ===")
    
    try:
        # Configurar dados de teste
        user, produto = setup_test_data()
        
        # Executar testes
        test_view_produto_edicao(user, produto)
        test_adicionar_tamanho_via_post(user, produto)
        test_adicionar_modulo_com_tamanhos(user, produto)
        
        print("\n=== RESUMO FINAL ===")
        produto_final = Item.objects.get(id=produto.id)
        print(f"Produto: {produto_final.nome_produto}")
        print(f"Total de módulos: {produto_final.modulos.count()}")
        
        for modulo in produto_final.modulos.all():
            tamanhos = modulo.tamanhos_detalhados.count()
            print(f"  {modulo.nome}: {tamanhos} tamanho(s)")
        
        print("\n✓ Teste completo finalizado!")
        
    except Exception as e:
        print(f"\n✗ Erro durante os testes: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    main()
