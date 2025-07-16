#!/usr/bin/env python3
"""
Script para cadastrar o sofá LE COULTRE - SF939 baseado na imagem anexa.

O sofá será cadastrado com:
- 1 produto (LE COULTRE - SF939)
- 2 módulos: MÓDULO 01 (2 ASSENTOS C/2BR) e MÓD 02 (POLTRONA)
- Primeiro módulo: 4 tamanhos completos
- Segundo módulo: 1 tamanho apenas
- Imagem anexa como imagem principal

Segue rigorosamente as diretrizes do RELATORIO_CONSOLIDADO.md
"""

import os
import sys
import django
from decimal import Decimal
from django.contrib.auth import get_user_model

# Configurar Django
sys.path.append('/home/matas/projetos/Project')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema_produtos.settings')
django.setup()

from produtos.models import TipoItem, Produto, Modulo, TamanhosModulosDetalhado
from django.core.files import File
from django.core.files.storage import default_storage
import shutil

def configurar_usuario():
    """Configura usuário para auditoria"""
    User = get_user_model()
    
    # Tentar pegar um usuário admin existente
    try:
        admin_user = User.objects.filter(is_superuser=True).first()
        if admin_user:
            return admin_user
        else:
            # Se não existe, criar um usuário padrão para o script
            admin_user = User.objects.create_user(
                username='sistema',
                email='sistema@exemplo.com',
                password='senha123'
            )
            return admin_user
    except Exception as e:
        print(f"Erro ao configurar usuário: {e}")
        return None

def associar_imagens_produto(produto, modulo_01, modulo_02):
    """Associa as imagens disponíveis na pasta media/produtos/sofas/sf939/sf939/sf939/"""
    
    # Caminho base das imagens
    base_path = '/home/matas/projetos/Project/media/produtos/sofas/sf939/sf939/sf939'
    
    try:
        # Verificar se as imagens existem
        imagem_principal = f"{base_path}/sf939.jpg"
        imagem_mod01 = f"{base_path}/mod01.png"
        imagem_mod02 = f"{base_path}/mod02.png"
        
        # Verificar se os arquivos existem
        if os.path.exists(imagem_principal):
            # Atualizar imagem principal do produto
            produto.imagem_principal = 'produtos/sofas/sf939/sf939/sf939/sf939.jpg'
            produto.save()
            print(f"✅ Imagem principal associada: sf939.jpg")
        else:
            print(f"⚠️  Imagem principal não encontrada: {imagem_principal}")
        
        # Aqui você pode adicionar lógica para associar imagens aos módulos
        # se o modelo suportar isso
        
        print(f"✅ Processo de associação de imagens concluído")
        
    except Exception as e:
        print(f"❌ Erro ao associar imagens: {str(e)}")

def cadastrar_sofa_le_coultre():
    """Cadastrar o sofá LE COULTRE - SF939 conforme especificações da imagem"""
    
    print("🛋️  Iniciando cadastro do sofá LE COULTRE - SF939...")
    
    try:
        # Configurar usuário
        user = configurar_usuario()
        if not user:
            print("❌ Erro: Não foi possível configurar usuário para auditoria")
            return False
        
        # 1. Buscar o tipo "Sofás"
        try:
            tipo_sofa = TipoItem.objects.get(nome__icontains='sofá')
            print(f"✅ Tipo encontrado: {tipo_sofa.nome}")
        except TipoItem.DoesNotExist:
            print("❌ Erro: Tipo 'Sofás' não encontrado no banco de dados")
            return False
        
        # 2. Verificar se já existe produto com esta referência
        if Produto.objects.filter(ref_produto='SF939').exists():
            print("⚠️  Produto SF939 já existe. Removendo para recriar...")
            Produto.objects.filter(ref_produto='SF939').delete()
        
        # 3. Criar o produto principal
        produto = Produto(
            ref_produto='SF939',
            nome_produto='LE COULTRE',
            id_tipo_produto=tipo_sofa,
            ativo=True,
            tem_cor_tecido=True,  # Padrão para sofás
            tem_difer_desenho_lado_dir_esq=False,
            tem_difer_desenho_tamanho=True,  # Tem diferentes tamanhos
            # Imagem será adicionada manualmente através da interface
        )
        
        # Rastrear usuário
        produto.created_by = user
        produto.updated_by = user
        produto.save()
        
        print(f"✅ Produto criado: {produto.ref_produto} - {produto.nome_produto}")
        
        # 4. Criar MÓDULO 01 - 2 ASSENTOS C/2BR
        modulo_01 = Modulo(
            produto=produto,
            nome='2 ASSENTOS C/2BR',
            profundidade=Decimal('100'),  # Baseado na tabela da imagem
            altura=Decimal('90'),         # Estimativa padrão
            braco=None,                   # Não especificado na imagem
            descricao='Módulo de 2 assentos com 2 braços'
        )
        modulo_01.created_by = user
        modulo_01.updated_by = user
        modulo_01.save()
        
        print(f"✅ Módulo 01 criado: {modulo_01.nome}")
        
        # 5. Criar 4 tamanhos para o MÓDULO 01 (baseados na tabela da imagem)
        tamanhos_modulo_01 = [
            {
                'largura_total': Decimal('232'),
                'largura_assento': Decimal('120'),
                'tecido_metros': Decimal('14.3'),
                'volume_m3': Decimal('2.8'),
                'peso_kg': Decimal('80'),
                'preco': Decimal('5952.00'),
                'descricao': 'Tamanho 232cm - Assentos de 120cm'
            },
            {
                'largura_total': Decimal('212'),
                'largura_assento': Decimal('110'),
                'tecido_metros': Decimal('13.5'),
                'volume_m3': Decimal('2.6'),
                'peso_kg': Decimal('75'),
                'preco': Decimal('5411.00'),
                'descricao': 'Tamanho 212cm - Assentos de 110cm'
            },
            {
                'largura_total': Decimal('252'),
                'largura_assento': Decimal('100'),
                'tecido_metros': Decimal('13.0'),
                'volume_m3': Decimal('2.4'),
                'peso_kg': Decimal('70'),
                'preco': Decimal('5105.00'),
                'descricao': 'Tamanho 252cm - Assentos de 100cm'
            },
            {
                'largura_total': Decimal('232'),
                'largura_assento': Decimal('90'),
                'tecido_metros': Decimal('12.3'),
                'volume_m3': Decimal('2.2'),
                'peso_kg': Decimal('65'),
                'preco': Decimal('4850.00'),
                'descricao': 'Tamanho 232cm - Assentos de 90cm'
            }
        ]
        
        for i, tamanho_data in enumerate(tamanhos_modulo_01, 1):
            tamanho = TamanhosModulosDetalhado(
                id_modulo=modulo_01,
                **tamanho_data
            )
            tamanho.created_by = user
            tamanho.updated_by = user
            tamanho.save()
            print(f"✅ Tamanho {i} criado para Módulo 01: {tamanho_data['largura_total']}cm")
        
        # 6. Criar MÓDULO 02 - POLTRONA
        modulo_02 = Modulo(
            produto=produto,
            nome='POLTRONA',
            profundidade=Decimal('100'),  # Baseado na tabela
            altura=Decimal('90'),         # Estimativa padrão
            braco=None,
            descricao='Módulo poltrona individual'
        )
        modulo_02.created_by = user
        modulo_02.updated_by = user
        modulo_02.save()
        
        print(f"✅ Módulo 02 criado: {modulo_02.nome}")
        
        # 7. Criar 1 tamanho para o MÓDULO 02 (baseado na tabela da imagem)
        tamanho_modulo_02 = TamanhosModulosDetalhado(
            id_modulo=modulo_02,
            largura_total=Decimal('115'),
            largura_assento=Decimal('70'),
            tecido_metros=Decimal('7.0'),
            volume_m3=Decimal('1.5'),
            peso_kg=Decimal('40'),
            preco=Decimal('2822.00'),
            descricao='Poltrona individual 115cm'
        )
        tamanho_modulo_02.created_by = user
        tamanho_modulo_02.updated_by = user
        tamanho_modulo_02.save()
        
        print(f"✅ Tamanho único criado para Módulo 02: {tamanho_modulo_02.largura_total}cm")
        
        # 8. Associar imagens aos produtos e módulos
        associar_imagens_produto(produto, modulo_01, modulo_02)
        
        # 9. Resumo final
        print("\n" + "="*60)
        print("🎉 CADASTRO CONCLUÍDO COM SUCESSO!")
        print("="*60)
        print(f"📦 Produto: {produto.ref_produto} - {produto.nome_produto}")
        print(f"🏷️  Tipo: {produto.id_tipo_produto.nome}")
        print(f"✅ Status: {'Ativo' if produto.ativo else 'Inativo'}")
        print(f"🎨 Tem cor tecido: {'Sim' if produto.tem_cor_tecido else 'Não'}")
        print(f"📏 Diferencia por tamanho: {'Sim' if produto.tem_difer_desenho_tamanho else 'Não'}")
        print(f"\n📋 MÓDULOS CADASTRADOS:")
        print(f"   1. {modulo_01.nome} - {modulo_01.tamanhos_detalhados.count()} tamanhos")
        print(f"   2. {modulo_02.nome} - {modulo_02.tamanhos_detalhados.count()} tamanho")
        print(f"\n💰 TOTAL DE PREÇOS CADASTRADOS:")
        
        total_precos = 0
        for modulo in [modulo_01, modulo_02]:
            for tamanho in modulo.tamanhos_detalhados.all():
                if tamanho.preco:
                    total_precos += 1
                    print(f"   - {modulo.nome}: {tamanho.largura_total}cm = R$ {tamanho.preco}")
        
        print(f"\n📊 ESTATÍSTICAS:")
        print(f"   - Total de módulos: 2")
        print(f"   - Total de tamanhos: {modulo_01.tamanhos_detalhados.count() + modulo_02.tamanhos_detalhados.count()}")
        print(f"   - Total de preços: {total_precos}")
        
        print(f"\n🔗 Para acessar:")
        print(f"   - Lista de produtos: /produtos/")
        print(f"   - Editar produto: /produtos/{produto.id}/editar/")
        print(f"   - Detalhes produto: /produtos/{produto.id}/detalhes/")
        
        print(f"\n📝 PRÓXIMOS PASSOS:")
        print(f"   1. Acessar a interface web")
        print(f"   2. Editar o produto SF939")
        print(f"   3. Fazer upload da imagem anexa como imagem principal")
        print(f"   4. Verificar visualização e edição")
        print(f"   5. Testar fluxo completo de CRUD")
        
        print("\n" + "="*60)
        
        return True
        
    except Exception as e:
        print(f"❌ Erro durante o cadastro: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def validar_cadastro():
    """Valida se o cadastro foi realizado corretamente"""
    print("\n🔍 Validando cadastro...")
    
    try:
        # Verificar produto
        produto = Produto.objects.get(ref_produto='SF939')
        print(f"✅ Produto encontrado: {produto.nome_produto}")
        
        # Verificar módulos
        modulos = produto.modulos.all()
        print(f"✅ Módulos encontrados: {modulos.count()}")
        
        for modulo in modulos:
            tamanhos = modulo.tamanhos_detalhados.all()
            print(f"   - {modulo.nome}: {tamanhos.count()} tamanhos")
            
            for tamanho in tamanhos:
                print(f"     * {tamanho.largura_total}cm - R$ {tamanho.preco or 'N/A'}")
        
        print("✅ Validação concluída com sucesso!")
        return True
        
    except Exception as e:
        print(f"❌ Erro na validação: {str(e)}")
        return False

if __name__ == '__main__':
    print("🚀 Sistema de Cadastro de Produtos - Sofá LE COULTRE")
    print("📋 Baseado no RELATORIO_CONSOLIDADO.md")
    print("-" * 60)
    
    # Executar cadastro
    sucesso = cadastrar_sofa_le_coultre()
    
    if sucesso:
        # Validar cadastro
        validar_cadastro()
        print("\n🎯 Cadastro finalizado! Acesse a interface web para adicionar a imagem.")
    else:
        print("\n❌ Falha no cadastro. Verifique os logs acima.")
        sys.exit(1)
