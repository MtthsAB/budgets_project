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

def test_produto_creation():
    """Testa a criação de um produto com módulos"""
    
    # Buscar um tipo de produto
    tipo_sofa = TipoItem.objects.filter(nome__icontains='Sofá').first()
    if not tipo_sofa:
        print("Tipo 'Sofá' não encontrado!")
        return
    
    # Criar produto de teste
    produto = Item.objects.create(
        ref_produto='TEST001',
        nome_produto='Sofá de Teste',
        id_tipo_produto=tipo_sofa,
        ativo=True,
        tem_cor_tecido=True,
        tem_difer_desenho_lado_dir_esq=False,
        tem_difer_desenho_tamanho=False
    )
    
    print(f"Produto criado: {produto}")
    
    # Criar módulo
    modulo = Modulo.objects.create(
        item=produto,
        nome='Módulo Principal',
        profundidade=90.0,
        altura=85.0,
        braco=25.0,
        descricao='Módulo principal do sofá'
    )
    
    print(f"Módulo criado: {modulo}")
    
    # Criar tamanho detalhado
    tamanho = TamanhosModulosDetalhado.objects.create(
        id_modulo=modulo,
        nome_tamanho='Médio',
        largura_total=180.0,
        largura_assento=140.0,
        altura_cm=85.0,
        profundidade_cm=90.0,
        tecido_metros=4.5,
        volume_m3=0.8,
        peso_kg=45.0,
        preco=1299.99,
        descricao='Tamanho médio ideal para 3 pessoas'
    )
    
    print(f"Tamanho criado: {tamanho}")
    
    # Verificar se foi salvo corretamente
    produtos = Item.objects.all()
    print(f"\nTotal de produtos no banco: {produtos.count()}")
    
    for p in produtos:
        print(f"- {p.ref_produto}: {p.nome_produto} (Módulos: {p.modulos.count()})")
        for m in p.modulos.all():
            print(f"  * {m.nome} (Tamanhos: {m.tamanhos_detalhados.count()})")
            for t in m.tamanhos_detalhados.all():
                print(f"    - {t.nome_tamanho}: {t.largura_total}x{t.altura_cm}x{t.profundidade_cm}cm")

if __name__ == '__main__':
    test_produto_creation()
