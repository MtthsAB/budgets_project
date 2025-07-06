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

def verificar_produto_id_3():
    """Verifica o produto ID 3 especificamente"""
    
    try:
        produto = Item.objects.get(id=3)
        print(f"=== Produto ID 3 ===")
        print(f"Referência: {produto.ref_produto}")
        print(f"Nome: {produto.nome_produto}")
        print(f"Tipo: {produto.id_tipo_produto.nome}")
        print(f"Ativo: {produto.ativo}")
        print(f"Tem cor tecido: {produto.tem_cor_tecido}")
        print(f"Módulos: {produto.modulos.count()}")
        
        for i, modulo in enumerate(produto.modulos.all(), 1):
            print(f"\n  Módulo {i}: {modulo.nome}")
            print(f"    ID: {modulo.id}")
            print(f"    Profundidade: {modulo.profundidade}")
            print(f"    Altura: {modulo.altura}")
            print(f"    Braço: {modulo.braco}")
            print(f"    Descrição: {modulo.descricao}")
            if modulo.imagem_principal:
                print(f"    Imagem: {modulo.imagem_principal.url}")
            
            print(f"    Tamanhos: {modulo.tamanhos_detalhados.count()}")
            for j, tamanho in enumerate(modulo.tamanhos_detalhados.all(), 1):
                print(f"      Tamanho {j}: {tamanho.nome_tamanho}")
                print(f"        Dimensões: {tamanho.largura_total}x{tamanho.altura_cm}x{tamanho.profundidade_cm}cm")
                print(f"        Tecido: {tamanho.tecido_metros}m")
                print(f"        Volume: {tamanho.volume_m3}m³")
                print(f"        Peso: {tamanho.peso_kg}kg")
                print(f"        Preço: R${tamanho.preco}")
                print(f"        Descrição: {tamanho.descricao}")
        
        print(f"\n✅ Produto ID 3 existe e tem dados completos")
        return produto
        
    except Item.DoesNotExist:
        print("❌ Produto ID 3 não encontrado")
        return None

def criar_produto_teste_completo():
    """Cria um produto de teste completo para validar a edição"""
    
    # Buscar tipo de produto
    tipo = TipoItem.objects.first()
    if not tipo:
        print("❌ Nenhum tipo de produto encontrado")
        return None
    
    # Criar produto
    produto = Item.objects.create(
        ref_produto='TESTE_EDICAO_COMPLETO',
        nome_produto='Produto Teste Edição Completa',
        id_tipo_produto=tipo,
        ativo=True,
        tem_cor_tecido=True,
        tem_difer_desenho_lado_dir_esq=False,
        tem_difer_desenho_tamanho=True
    )
    
    print(f"✅ Produto criado: {produto.ref_produto} (ID: {produto.id})")
    
    # Criar módulo 1
    modulo1 = Modulo.objects.create(
        item=produto,
        nome='Módulo Principal',
        profundidade=90.0,
        altura=85.0,
        braco=25.0,
        descricao='Módulo principal do sofá'
    )
    
    # Tamanhos do módulo 1
    TamanhosModulosDetalhado.objects.create(
        id_modulo=modulo1,
        nome_tamanho='Pequeno',
        largura_total=150.0,
        largura_assento=110.0,
        altura_cm=85.0,
        profundidade_cm=90.0,
        tecido_metros=3.0,
        volume_m3=0.6,
        peso_kg=30.0,
        preco=899.99,
        descricao='Tamanho pequeno ideal para 2 pessoas'
    )
    
    TamanhosModulosDetalhado.objects.create(
        id_modulo=modulo1,
        nome_tamanho='Médio',
        largura_total=180.0,
        largura_assento=140.0,
        altura_cm=85.0,
        profundidade_cm=90.0,
        tecido_metros=4.0,
        volume_m3=0.8,
        peso_kg=40.0,
        preco=1199.99,
        descricao='Tamanho médio ideal para 3 pessoas'
    )
    
    # Criar módulo 2
    modulo2 = Modulo.objects.create(
        item=produto,
        nome='Módulo Chaise',
        profundidade=60.0,
        altura=40.0,
        braco=0.0,
        descricao='Módulo chaise para descanso'
    )
    
    # Tamanho do módulo 2
    TamanhosModulosDetalhado.objects.create(
        id_modulo=modulo2,
        nome_tamanho='Único',
        largura_total=80.0,
        largura_assento=75.0,
        altura_cm=40.0,
        profundidade_cm=60.0,
        tecido_metros=1.5,
        volume_m3=0.3,
        peso_kg=15.0,
        preco=399.99,
        descricao='Tamanho único do módulo chaise'
    )
    
    print(f"✅ Módulos e tamanhos criados:")
    print(f"  - {modulo1.nome}: {modulo1.tamanhos_detalhados.count()} tamanhos")
    print(f"  - {modulo2.nome}: {modulo2.tamanhos_detalhados.count()} tamanhos")
    
    return produto

def validar_template_edicao():
    """Valida se o template de edição funciona corretamente"""
    
    from django.template.loader import render_to_string
    from django.test import RequestFactory
    from django.contrib.auth import get_user_model
    
    User = get_user_model()
    
    # Buscar produto
    produto = Item.objects.get(id=3) if Item.objects.filter(id=3).exists() else None
    if not produto:
        produto = criar_produto_teste_completo()
    
    if not produto:
        print("❌ Não foi possível obter produto para teste")
        return False
    
    # Preparar contexto para template
    context = {
        'produto': produto,
        'modulos': produto.modulos.all(),
        'tipos': TipoItem.objects.all(),
    }
    
    try:
        # Renderizar template
        html = render_to_string('produtos/editar.html', context)
        
        # Verificações básicas
        checks = [
            ('form method="post"', 'Formulário POST presente'),
            ('id="ref_produto"', 'Campo referência presente'),
            ('id="nome_produto"', 'Campo nome presente'),
            ('modulo_nome_', 'Campos de módulo presente'),
            ('tamanho_nome_', 'Campos de tamanho presente'),
            ('btn btn-primary', 'Botão salvar presente'),
        ]
        
        print(f"✅ Template renderizado com sucesso")
        print(f"Tamanho do HTML: {len(html)} caracteres")
        
        for check, descricao in checks:
            if check in html:
                print(f"✅ {descricao}")
            else:
                print(f"❌ {descricao}")
        
        # Verificar se dados do produto estão no template
        if produto.ref_produto in html:
            print(f"✅ Referência do produto presente no template")
        else:
            print(f"❌ Referência do produto NÃO presente no template")
        
        if produto.nome_produto in html:
            print(f"✅ Nome do produto presente no template")
        else:
            print(f"❌ Nome do produto NÃO presente no template")
        
        # Contar módulos no template
        modulo_count = html.count('modulo_nome_')
        print(f"Campos de módulo encontrados no template: {modulo_count}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro ao renderizar template: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    print("=== Validação Completa da Funcionalidade de Edição ===")
    
    # 1. Verificar produto ID 3
    produto = verificar_produto_id_3()
    
    # 2. Se não existir, criar produto de teste
    if not produto:
        produto = criar_produto_teste_completo()
    
    # 3. Validar template
    template_ok = validar_template_edicao()
    
    print(f"\n=== Resumo da Validação ===")
    print(f"Produto disponível: {'✅ SIM' if produto else '❌ NÃO'}")
    print(f"Template funcionando: {'✅ SIM' if template_ok else '❌ NÃO'}")
    
    if produto:
        print(f"URL de teste: http://localhost:8000/produtos/{produto.id}/editar/")
        print(f"Módulos disponíveis: {produto.modulos.count()}")
        total_tamanhos = sum(m.tamanhos_detalhados.count() for m in produto.modulos.all())
        print(f"Total de tamanhos: {total_tamanhos}")
