#!/usr/bin/env python3
"""
Script simples para verificar a estrutura atual dos sofás.
"""

import os
import sys
import django

# Configurar Django primeiro
sys.path.append('/home/matas/projetos/Project')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema_produtos.settings')
django.setup()

from produtos.models import TipoItem, Produto, Modulo, TamanhosModulosDetalhado

def verificar_estrutura_sofas():
    """Verificar estrutura atual dos sofás"""
    
    print("🔍 Verificando sofás existentes...")
    
    # Buscar sofás
    sofas = Produto.objects.filter(id_tipo_produto__nome__icontains='sofá')
    print(f"📊 Total de sofás: {sofas.count()}")
    
    if sofas.count() == 0:
        print("❌ Nenhum sofá encontrado. Vou criar um para teste.")
        return criar_sofa_teste()
    
    # Examinar primeiro sofá
    sofa = sofas.first()
    print(f"\n🛋️ Analisando: {sofa.ref_produto} - {sofa.nome_produto}")
    
    # Verificar módulos
    modulos = sofa.modulos.all()
    print(f"📦 Módulos: {modulos.count()}")
    
    total_tamanhos = 0
    for i, modulo in enumerate(modulos, 1):
        tamanhos = modulo.tamanhos_detalhados.all()
        total_tamanhos += tamanhos.count()
        print(f"  {i}. {modulo.nome}")
        print(f"     • Profundidade: {modulo.profundidade}cm")
        print(f"     • Altura: {modulo.altura}cm") 
        print(f"     • Braço: {modulo.braco}cm")
        print(f"     • Tamanhos: {tamanhos.count()}")
        
        for j, tamanho in enumerate(tamanhos, 1):
            print(f"       {j}. Largura: {tamanho.largura_total}cm")
            print(f"          Assento: {tamanho.largura_assento}cm")
            print(f"          Preço: R${tamanho.preco}")
            print(f"          Descrição: {tamanho.descricao}")
    
    print(f"\n📊 Resumo:")
    print(f"   - Módulos: {modulos.count()}")
    print(f"   - Tamanhos total: {total_tamanhos}")
    
    return sofa

def criar_sofa_teste():
    """Criar um sofá para teste"""
    from django.contrib.auth import get_user_model
    
    print("\n🔨 Criando sofá de teste...")
    
    # Buscar usuário admin
    User = get_user_model()
    user = User.objects.filter(is_superuser=True).first()
    
    if not user:
        print("❌ Usuário admin não encontrado")
        return None
    
    # Buscar tipo sofá
    tipo_sofa = TipoItem.objects.filter(nome__icontains='sofá').first()
    if not tipo_sofa:
        print("❌ Tipo 'sofá' não encontrado")
        return None
    
    # Criar produto
    sofa = Produto.objects.create(
        ref_produto='SF-TESTE-001',
        nome_produto='Sofá de Teste para Edição',
        id_tipo_produto=tipo_sofa,
        ativo=True,
        created_by=user,
        updated_by=user
    )
    
    print(f"✅ Sofá criado: {sofa.ref_produto}")
    
    # Criar módulos
    modulo1 = Modulo.objects.create(
        produto=sofa,
        nome='Módulo Esquerdo',
        profundidade=85.0,
        altura=90.0,
        braco=25.0,
        descricao='Módulo lateral esquerdo',
        created_by=user,
        updated_by=user
    )
    
    modulo2 = Modulo.objects.create(
        produto=sofa,
        nome='Módulo Direito', 
        profundidade=85.0,
        altura=90.0,
        braco=25.0,
        descricao='Módulo lateral direito',
        created_by=user,
        updated_by=user
    )
    
    print(f"✅ Módulos criados: {modulo1.nome}, {modulo2.nome}")
    
    # Criar tamanhos para módulo 1
    TamanhosModulosDetalhado.objects.create(
        id_modulo=modulo1,
        largura_total=200.0,
        largura_assento=180.0,
        tecido_metros=3.5,
        volume_m3=1.2,
        peso_kg=45.0,
        preco=1500.00,
        descricao='Tamanho 200cm',
        created_by=user,
        updated_by=user
    )
    
    TamanhosModulosDetalhado.objects.create(
        id_modulo=modulo1,
        largura_total=250.0,
        largura_assento=230.0,
        tecido_metros=4.2,
        volume_m3=1.8,
        peso_kg=55.0,
        preco=1800.00,
        descricao='Tamanho 250cm',
        created_by=user,
        updated_by=user
    )
    
    # Criar tamanho para módulo 2
    TamanhosModulosDetalhado.objects.create(
        id_modulo=modulo2,
        largura_total=180.0,
        largura_assento=160.0,
        tecido_metros=3.0,
        volume_m3=1.0,
        peso_kg=40.0,
        preco=1400.00,
        descricao='Tamanho único',
        created_by=user,
        updated_by=user
    )
    
    print(f"✅ Tamanhos criados: 2 para módulo 1, 1 para módulo 2")
    
    return sofa

if __name__ == "__main__":
    sofa = verificar_estrutura_sofas()
    if sofa:
        print(f"\n🎯 Sofá ID {sofa.id} disponível para testes de edição")
    else:
        print("\n❌ Falha ao verificar/criar sofá")
