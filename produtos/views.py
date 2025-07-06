from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.csrf import csrf_protect
from django.db import transaction
from django.http import JsonResponse, Http404
from rest_framework import viewsets, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
import logging
from sistema_produtos.mixins import track_user_changes
from .models import (
    Item, TipoItem, Linha, Modulo, Acessorio, 
    TamanhosModulos, TamanhosModulosDetalhado, FaixaTecido, PrecosBase,
    Banqueta
)
from .forms import AcessorioForm, BanquetaForm

logger = logging.getLogger(__name__)

@login_required
def home_view(request):
    """View da página inicial do sistema"""
    context = {
        'total_produtos': Item.objects.count(),
        'total_tipos': TipoItem.objects.count(),
        'total_modulos': Modulo.objects.count(),
        'produtos_recentes': Item.objects.select_related('id_tipo_produto').order_by('-created_at')[:5],
    }
    return render(request, 'produtos/home.html', context)

@login_required
def produtos_list_view(request):
    """View para listagem de produtos unificada (inclui banquetas)"""
    # Buscar produtos da tabela Item
    produtos = Item.objects.select_related('id_tipo_produto').prefetch_related('modulos').all()
    
    # Buscar banquetas da tabela Banqueta
    banquetas = Banqueta.objects.filter(ativo=True).all()
    
    # Filtros
    tipo_filtro = request.GET.get('tipo')
    ativo_filtro = request.GET.get('ativo')
    busca = request.GET.get('busca')
    
    if tipo_filtro:
        # Filtrar produtos por tipo
        produtos = produtos.filter(id_tipo_produto__id=tipo_filtro)
        
        # Se o filtro for por "Banquetas" (id=4), mostrar apenas banquetas
        if tipo_filtro == '4':
            produtos = Item.objects.none()  # Não mostrar produtos da tabela Item
        else:
            banquetas = Banqueta.objects.none()  # Não mostrar banquetas se filtro não for banquetas
    
    if ativo_filtro:
        produtos = produtos.filter(ativo=ativo_filtro == 'true')
        banquetas = banquetas.filter(ativo=ativo_filtro == 'true')
    
    if busca:
        produtos = produtos.filter(
            nome_produto__icontains=busca
        ) | produtos.filter(
            ref_produto__icontains=busca
        )
        banquetas = banquetas.filter(
            nome__icontains=busca
        ) | banquetas.filter(
            ref_banqueta__icontains=busca
        )
    
    context = {
        'produtos': produtos,
        'banquetas': banquetas,
        'total_itens': produtos.count() + banquetas.count(),
        'tipos': TipoItem.objects.all(),
        'filtros': {
            'tipo': tipo_filtro,
            'ativo': ativo_filtro,
            'busca': busca,
        }
    }
    return render(request, 'produtos/lista.html', context)

@login_required
@csrf_protect
def produto_cadastro_view(request):
    """View para cadastro de novos produtos (incluindo acessórios)"""
    if request.method == 'POST':
        try:
            with transaction.atomic():
                # Dados básicos do produto
                ref_produto = request.POST.get('ref_produto')
                nome_produto = request.POST.get('nome_produto')
                tipo_produto_id = request.POST.get('tipo_produto')
                
                # Validações básicas
                if not all([ref_produto, nome_produto, tipo_produto_id]):
                    messages.error(request, 'Por favor, preencha todos os campos obrigatórios.')
                    raise ValueError('Campos obrigatórios não preenchidos')
                
                # Verificar se já existe produto com esta referência
                if Item.objects.filter(ref_produto=ref_produto).exists():
                    messages.error(request, 'Já existe um produto com esta referência.')
                    raise ValueError('Referência duplicada')
                
                # Verificar tipo de produto
                tipo_produto = get_object_or_404(TipoItem, id=tipo_produto_id)
                eh_acessorio = tipo_produto.nome.lower() == 'acessórios'
                eh_banqueta = tipo_produto.nome.lower() == 'banquetas'
                
                if eh_banqueta:
                    # Processar como banqueta usando o modelo específico
                    largura = request.POST.get('largura_banqueta')
                    profundidade = request.POST.get('profundidade_banqueta')
                    altura = request.POST.get('altura_banqueta')
                    tecido_metros = request.POST.get('tecido_metros_banqueta')
                    volume_m3 = request.POST.get('volume_m3_banqueta')
                    peso_kg = request.POST.get('peso_kg_banqueta')
                    preco = request.POST.get('preco_banqueta')
                    ativo = request.POST.get('ativo_banqueta') == 'on'
                    descricao = request.POST.get('descricao_banqueta')
                    
                    # Validar campos obrigatórios para banquetas
                    if not all([largura, profundidade, altura, tecido_metros, volume_m3, peso_kg, preco]):
                        messages.error(request, 'Por favor, preencha todos os campos obrigatórios para banquetas.')
                        raise ValueError('Campos obrigatórios da banqueta não preenchidos')
                    
                    # Criar banqueta
                    banqueta = Banqueta(
                        ref_banqueta=ref_produto,
                        nome=nome_produto,
                        largura=float(largura),
                        profundidade=float(profundidade),
                        altura=float(altura),
                        tecido_metros=float(tecido_metros),
                        volume_m3=float(volume_m3),
                        peso_kg=float(peso_kg),
                        preco=float(preco),
                        ativo=ativo,
                        imagem_principal=request.FILES.get('imagem_principal'),
                        imagem_secundaria=request.FILES.get('imagem_secundaria'),
                        descricao=descricao if descricao else None
                    )
                    # Rastrear usuário
                    track_user_changes(banqueta, request.user)
                    banqueta.save()
                    
                    messages.success(request, f'Banqueta "{banqueta.ref_banqueta} - {banqueta.nome}" cadastrada com sucesso!')
                    return redirect('banquetas_lista')
                    
                elif eh_acessorio:
                    # Processar como acessório usando o modelo Item unificado
                    ativo = request.POST.get('ativo_acessorio') == 'on'
                    preco = request.POST.get('preco_acessorio')
                    descricao = request.POST.get('descricao_acessorio')
                    produtos_vinculados = request.POST.getlist('produtos_vinculados')
                    
                    # Criar produto/acessório
                    produto = Item(
                        ref_produto=ref_produto,
                        nome_produto=nome_produto,
                        id_tipo_produto_id=tipo_produto_id,
                        ativo=ativo,
                        preco_acessorio=float(preco) if preco else None,
                        descricao_acessorio=descricao if descricao else None,
                        imagem_principal=request.FILES.get('imagem_principal'),
                        imagem_secundaria=request.FILES.get('imagem_secundaria'),
                        # Campos específicos de sofás são False para acessórios
                        tem_cor_tecido=False,
                        tem_difer_desenho_lado_dir_esq=False,
                        tem_difer_desenho_tamanho=False
                    )
                    # Rastrear usuário
                    track_user_changes(produto, request.user)
                    produto.save()
                    
                    # Vincular produtos se selecionados
                    if produtos_vinculados:
                        for produto_id in produtos_vinculados:
                            if produto_id:
                                try:
                                    produto_vinculado = Item.objects.get(id=produto_id)
                                    produto.produtos_vinculados.add(produto_vinculado)
                                except Item.DoesNotExist:
                                    continue
                    
                    messages.success(request, f'Acessório "{produto.ref_produto} - {produto.nome_produto}" cadastrado com sucesso!')
                    return redirect('produtos_lista')
                    
                else:
                    # Processar como produto normal (sofá, cadeira, etc.)
                    ativo = request.POST.get('ativo') == 'on'
                    tem_cor_tecido = request.POST.get('tem_cor_tecido') == 'on'
                    tem_difer_desenho_lado = request.POST.get('tem_difer_desenho_lado') == 'on'
                    tem_difer_desenho_tamanho = request.POST.get('tem_difer_desenho_tamanho') == 'on'
                    
                    # Criar o produto
                    produto = Item(
                        ref_produto=ref_produto,
                        nome_produto=nome_produto,
                        id_tipo_produto_id=tipo_produto_id,
                        ativo=ativo,
                        tem_cor_tecido=tem_cor_tecido,
                        tem_difer_desenho_lado_dir_esq=tem_difer_desenho_lado,
                        tem_difer_desenho_tamanho=tem_difer_desenho_tamanho,
                        imagem_principal=request.FILES.get('imagem_principal'),
                        imagem_secundaria=request.FILES.get('imagem_secundaria'),
                        # Campos específicos de acessórios são None para produtos normais
                        preco_acessorio=None,
                        descricao_acessorio=None
                    )
                    # Rastrear usuário
                    track_user_changes(produto, request.user)
                    produto.save()
                
                # Processar módulos (apenas para não-acessórios)
                modulos_nomes = request.POST.getlist('modulo_nome')
                logger.info(f"Módulos recebidos: {modulos_nomes}")
                
                for i, nome_modulo in enumerate(modulos_nomes):
                    if nome_modulo.strip():  # Se o nome do módulo não estiver vazio
                        # Obter dados do módulo
                        profundidade = request.POST.get(f'modulo_profundidade_{i+1}')
                        altura = request.POST.get(f'modulo_altura_{i+1}')
                        braco = request.POST.get(f'modulo_braco_{i+1}')
                        descricao = request.POST.get(f'modulo_descricao_{i+1}')
                        
                        logger.info(f"Criando módulo {i+1}: {nome_modulo}")
                        
                        modulo = Modulo(
                            item=produto,
                            nome=nome_modulo,
                            profundidade=float(profundidade) if profundidade else None,
                            altura=float(altura) if altura else None,
                            braco=float(braco) if braco else None,
                            descricao=descricao if descricao else None,
                            imagem_principal=request.FILES.get(f'modulo_imagem_principal_{i+1}')
                        )
                        # Rastrear usuário
                        track_user_changes(modulo, request.user)
                        modulo.save()
                        
                        # Processar tamanhos deste módulo
                        modulo_id = i + 1
                        tamanhos_nomes = request.POST.getlist(f'tamanho_nome_{modulo_id}')
                        
                        logger.info(f"Tamanhos para módulo {modulo_id}: {tamanhos_nomes}")
                        
                        if tamanhos_nomes:
                            tamanhos_largura_total = request.POST.getlist(f'tamanho_largura_total_{modulo_id}')
                            tamanhos_largura_assento = request.POST.getlist(f'tamanho_largura_assento_{modulo_id}')
                            tamanhos_altura = request.POST.getlist(f'tamanho_altura_{modulo_id}')
                            tamanhos_profundidade = request.POST.getlist(f'tamanho_profundidade_{modulo_id}')
                            tamanhos_tecido = request.POST.getlist(f'tamanho_tecido_{modulo_id}')
                            tamanhos_volume = request.POST.getlist(f'tamanho_volume_{modulo_id}')
                            tamanhos_peso = request.POST.getlist(f'tamanho_peso_{modulo_id}')
                            tamanhos_preco = request.POST.getlist(f'tamanho_preco_{modulo_id}')
                            tamanhos_descricao = request.POST.getlist(f'tamanho_descricao_{modulo_id}')
                            
                            for j, nome_tamanho in enumerate(tamanhos_nomes):
                                if nome_tamanho.strip():
                                    from .models import TamanhosModulosDetalhado
                                    
                                    # Função auxiliar para converter valores
                                    def safe_float(value):
                                        try:
                                            return float(value) if value and value.strip() else None
                                        except (ValueError, TypeError):
                                            return None
                                    
                                    tamanho_detalhado = TamanhosModulosDetalhado(
                                        id_modulo=modulo,
                                        largura_total=safe_float(tamanhos_largura_total[j] if j < len(tamanhos_largura_total) else None),
                                        largura_assento=safe_float(tamanhos_largura_assento[j] if j < len(tamanhos_largura_assento) else None),
                                        tecido_metros=safe_float(tamanhos_tecido[j] if j < len(tamanhos_tecido) else None),
                                        volume_m3=safe_float(tamanhos_volume[j] if j < len(tamanhos_volume) else None),
                                        peso_kg=safe_float(tamanhos_peso[j] if j < len(tamanhos_peso) else None),
                                        preco=safe_float(tamanhos_preco[j] if j < len(tamanhos_preco) else None),
                                        descricao=tamanhos_descricao[j] if j < len(tamanhos_descricao) and tamanhos_descricao[j] else None
                                    )
                                    # Rastrear usuário
                                    track_user_changes(tamanho_detalhado, request.user)
                                    tamanho_detalhado.save()
                
                messages.success(request, f'Produto "{produto.nome_produto}" cadastrado com sucesso!')
                return redirect('produtos_lista')
                
        except ValueError as e:
            logger.error(f"Erro de validação no cadastro: {str(e)}")
            # A mensagem de erro já foi adicionada antes do raise
        except Exception as e:
            logger.error(f"Erro inesperado no cadastro: {str(e)}", exc_info=True)
            messages.error(request, f'Erro ao cadastrar produto: {str(e)}')
    
    context = {
        'tipos': TipoItem.objects.all(),
        'produtos_disponiveis': Item.objects.filter(ativo=True).order_by('ref_produto'),
    }
    return render(request, 'produtos/sofas/cadastro.html', context)

@login_required
def produto_editar_view(request, produto_id):
    """View para edição de produtos (incluindo acessórios)"""
    produto = get_object_or_404(Item, id=produto_id)
    
    if request.method == 'POST':
        try:
            with transaction.atomic():
                logger.info(f"Dados POST recebidos para edição do produto {produto_id}: {dict(request.POST)}")
                logger.info(f"Arquivos recebidos: {list(request.FILES.keys())}")
                
                # Verificar tipo de produto
                tipo_produto_id = request.POST.get('tipo_produto')
                tipo_produto = get_object_or_404(TipoItem, id=tipo_produto_id)
                eh_acessorio = tipo_produto.nome.lower() == 'acessórios'
                eh_banqueta = tipo_produto.nome.lower() == 'banquetas'
                
                # Atualizar dados básicos
                produto.ref_produto = request.POST.get('ref_produto')
                produto.nome_produto = request.POST.get('nome_produto')
                produto.id_tipo_produto_id = request.POST.get('tipo_produto')
                
                if eh_banqueta:
                    # Se o produto foi convertido para banqueta, criar nova entrada na tabela Banqueta
                    # e manter a entrada em Item apenas para histórico/compatibilidade
                    largura = request.POST.get('largura_banqueta')
                    profundidade = request.POST.get('profundidade_banqueta')
                    altura = request.POST.get('altura_banqueta')
                    tecido_metros = request.POST.get('tecido_metros_banqueta')
                    volume_m3 = request.POST.get('volume_m3_banqueta')
                    peso_kg = request.POST.get('peso_kg_banqueta')
                    preco = request.POST.get('preco_banqueta')
                    ativo = request.POST.get('ativo_banqueta') == 'on'
                    descricao = request.POST.get('descricao_banqueta')
                    
                    # Validar campos obrigatórios para banquetas
                    if not all([largura, profundidade, altura, tecido_metros, volume_m3, peso_kg, preco]):
                        messages.error(request, 'Por favor, preencha todos os campos obrigatórios para banquetas.')
                        raise ValueError('Campos obrigatórios da banqueta não preenchidos')
                    
                    # Verificar se já existe uma banqueta com esta referência
                    banqueta_existente = Banqueta.objects.filter(ref_banqueta=produto.ref_produto).first()
                    
                    if banqueta_existente:
                        # Atualizar banqueta existente
                        banqueta_existente.nome = produto.nome_produto
                        banqueta_existente.largura = float(largura)
                        banqueta_existente.profundidade = float(profundidade)
                        banqueta_existente.altura = float(altura)
                        banqueta_existente.tecido_metros = float(tecido_metros)
                        banqueta_existente.volume_m3 = float(volume_m3)
                        banqueta_existente.peso_kg = float(peso_kg)
                        banqueta_existente.preco = float(preco)
                        banqueta_existente.ativo = ativo
                        banqueta_existente.descricao = descricao if descricao else None
                        
                        # Atualizar imagens se fornecidas
                        if 'imagem_principal' in request.FILES:
                            banqueta_existente.imagem_principal = request.FILES['imagem_principal']
                        if 'imagem_secundaria' in request.FILES:
                            banqueta_existente.imagem_secundaria = request.FILES['imagem_secundaria']
                        
                        track_user_changes(banqueta_existente, request.user)
                        banqueta_existente.save()
                        banqueta = banqueta_existente
                    else:
                        # Criar nova banqueta
                        banqueta = Banqueta(
                            ref_banqueta=produto.ref_produto,
                            nome=produto.nome_produto,
                            largura=float(largura),
                            profundidade=float(profundidade),
                            altura=float(altura),
                            tecido_metros=float(tecido_metros),
                            volume_m3=float(volume_m3),
                            peso_kg=float(peso_kg),
                            preco=float(preco),
                            ativo=ativo,
                            imagem_principal=request.FILES.get('imagem_principal'),
                            imagem_secundaria=request.FILES.get('imagem_secundaria'),
                            descricao=descricao if descricao else None
                        )
                        track_user_changes(banqueta, request.user)
                        banqueta.save()
                    
                    # Atualizar o produto Item para manter compatibilidade
                    produto.ativo = ativo
                    produto.tem_cor_tecido = False
                    produto.tem_difer_desenho_lado_dir_esq = False
                    produto.tem_difer_desenho_tamanho = False
                    produto.preco_acessorio = None
                    produto.descricao_acessorio = None
                    
                    # Limpar módulos e vinculações
                    produto.modulos.all().delete()
                    produto.produtos_vinculados.clear()
                    
                    track_user_changes(produto, request.user)
                    produto.save()
                    
                    messages.success(request, f'Banqueta "{banqueta.ref_banqueta} - {banqueta.nome}" atualizada com sucesso!')
                    return redirect('produto_detalhes', produto_id=banqueta.id)
                    
                elif eh_acessorio:
                    # Atualizar como acessório
                    produto.ativo = request.POST.get('ativo') == 'on'
                    preco = request.POST.get('preco_acessorio')
                    produto.preco_acessorio = float(preco) if preco else None
                    produto.descricao_acessorio = request.POST.get('descricao_acessorio')
                    
                    # Limpar campos específicos de sofás
                    produto.tem_cor_tecido = False
                    produto.tem_difer_desenho_lado_dir_esq = False
                    produto.tem_difer_desenho_tamanho = False
                    
                    # Atualizar imagens se fornecidas
                    if 'imagem_principal' in request.FILES:
                        produto.imagem_principal = request.FILES['imagem_principal']
                    if 'imagem_secundaria' in request.FILES:
                        produto.imagem_secundaria = request.FILES['imagem_secundaria']
                    
                    # Rastrear usuário na edição
                    track_user_changes(produto, request.user)
                    produto.save()
                    
                    # Atualizar vinculações
                    produtos_vinculados = request.POST.getlist('produtos_vinculados')
                    logger.info(f"Produtos vinculados recebidos: {produtos_vinculados}")
                    produto.produtos_vinculados.clear()
                    if produtos_vinculados:
                        for produto_id_vinc in produtos_vinculados:
                            if produto_id_vinc:
                                try:
                                    produto_vinculado = Item.objects.get(id=produto_id_vinc)
                                    produto.produtos_vinculados.add(produto_vinculado)
                                    logger.info(f"Produto {produto_vinculado.ref_produto} vinculado com sucesso")
                                except Item.DoesNotExist:
                                    logger.warning(f"Produto com ID {produto_id_vinc} não encontrado")
                                    continue
                    logger.info(f"Total de produtos vinculados após atualização: {produto.produtos_vinculados.count()}")
                    
                    # Remover módulos se produto foi convertido para acessório
                    produto.modulos.all().delete()
                    
                    messages.success(request, f'Acessório "{produto.ref_produto} - {produto.nome_produto}" atualizado com sucesso!')
                    return redirect('produtos_lista')
                        
                else:
                    # Atualizar como produto normal
                    produto.ativo = request.POST.get('ativo') == 'on'
                    produto.tem_cor_tecido = request.POST.get('tem_cor_tecido') == 'on'
                    produto.tem_difer_desenho_lado_dir_esq = request.POST.get('tem_difer_desenho_lado') == 'on'
                    produto.tem_difer_desenho_tamanho = request.POST.get('tem_difer_desenho_tamanho') == 'on'
                    
                    # Limpar campos específicos de acessórios
                    produto.preco_acessorio = None
                    produto.descricao_acessorio = None
                    
                    # Atualizar imagem principal se fornecida
                    if 'imagem_principal' in request.FILES:
                        produto.imagem_principal = request.FILES['imagem_principal']
                    
                    # Atualizar segunda imagem se fornecida
                    if 'imagem_secundaria' in request.FILES:
                        produto.imagem_secundaria = request.FILES['imagem_secundaria']
                        
                    # Rastrear usuário na edição
                    track_user_changes(produto, request.user)
                    produto.save()
                    logger.info(f"Produto básico atualizado: {produto.ref_produto}")
                    
                    # Limpar vinculações de produtos se foi convertido de acessório
                    produto.produtos_vinculados.clear()
                    
                    # Salvar imagens dos módulos antigos antes de deletar
                    modulos_anteriores = {m.nome: m.imagem_principal for m in produto.modulos.all()}
                    produto.modulos.all().delete()
                    logger.info("Módulos existentes removidos")

                def safe_float(value):
                    try:
                        return float(value) if value and value.strip() else None
                    except (ValueError, TypeError):
                        return None

                modulo_counter = 1
                while True:
                    nome_modulo = request.POST.get(f'modulo_nome_{modulo_counter}')
                    if not nome_modulo:
                        break

                    if nome_modulo.strip():
                        logger.info(f"Processando módulo {modulo_counter}: {nome_modulo}")

                        profundidade = request.POST.get(f'modulo_profundidade_{modulo_counter}')
                        altura = request.POST.get(f'modulo_altura_{modulo_counter}')
                        braco = request.POST.get(f'modulo_braco_{modulo_counter}')
                        descricao = request.POST.get(f'modulo_descricao_{modulo_counter}')

                        # Se não houver upload de nova imagem, tenta manter a anterior pelo nome
                        imagem_modulo = request.FILES.get(f'modulo_imagem_principal_{modulo_counter}')
                        if not imagem_modulo:
                            imagem_modulo = modulos_anteriores.get(nome_modulo)

                        # Processar imagem secundária do módulo
                        imagem_secundaria_modulo = request.FILES.get(f'modulo_imagem_secundaria_{modulo_counter}')

                        modulo = Modulo(
                            item=produto,
                            nome=nome_modulo,
                            profundidade=safe_float(profundidade),
                            altura=safe_float(altura),
                            braco=safe_float(braco),
                            descricao=descricao if descricao else None,
                            imagem_principal=imagem_modulo,
                            imagem_secundaria=imagem_secundaria_modulo
                        )
                        # Rastrear usuário
                        track_user_changes(modulo, request.user)
                        modulo.save()
                        logger.info(f"Módulo criado: {modulo.nome}")

                        # Processar tamanhos deste módulo
                        tamanhos_largura_total = request.POST.getlist(f'tamanho_largura_total_{modulo_counter}')
                        tamanhos_largura_assento = request.POST.getlist(f'tamanho_largura_assento_{modulo_counter}')
                        tamanhos_tecido = request.POST.getlist(f'tamanho_tecido_{modulo_counter}')
                        tamanhos_volume = request.POST.getlist(f'tamanho_volume_{modulo_counter}')
                        tamanhos_peso = request.POST.getlist(f'tamanho_peso_{modulo_counter}')
                        tamanhos_preco = request.POST.getlist(f'tamanho_preco_{modulo_counter}')
                        tamanhos_descricao = request.POST.getlist(f'tamanho_descricao_{modulo_counter}')
                        
                        # Filtrar apenas valores não vazios de largura_total (campo obrigatório)
                        larguras_validas = [lt for lt in tamanhos_largura_total if lt and lt.strip()]
                        
                        # Para cada largura válida, criar um tamanho
                        for i, largura_total in enumerate(larguras_validas):
                            logger.info(f"Processando tamanho {i+1} do módulo {modulo_counter}")
                            
                            from .models import TamanhosModulosDetalhado
                            
                            # Garantir que temos valores para todos os campos
                            largura_assento = tamanhos_largura_assento[i] if i < len(tamanhos_largura_assento) else ''
                            tecido = tamanhos_tecido[i] if i < len(tamanhos_tecido) else ''
                            volume = tamanhos_volume[i] if i < len(tamanhos_volume) else ''
                            peso = tamanhos_peso[i] if i < len(tamanhos_peso) else ''
                            preco = tamanhos_preco[i] if i < len(tamanhos_preco) else ''
                            descricao = tamanhos_descricao[i] if i < len(tamanhos_descricao) else ''
                            
                            tamanho_detalhado = TamanhosModulosDetalhado(
                                id_modulo=modulo,
                                largura_total=safe_float(largura_total),
                                largura_assento=safe_float(largura_assento),
                                tecido_metros=safe_float(tecido),
                                volume_m3=safe_float(volume),
                                peso_kg=safe_float(peso),
                                preco=safe_float(preco),
                                descricao=descricao.strip() if descricao else None
                            )
                            # Rastrear usuário
                            track_user_changes(tamanho_detalhado, request.user)
                            tamanho_detalhado.save()
                            logger.info(f"Tamanho {i+1} criado para módulo {modulo.nome}")
                    
                    modulo_counter += 1
                
                messages.success(request, f'Produto "{produto.nome_produto}" atualizado com sucesso!')
                logger.info(f"Produto {produto.ref_produto} atualizado com sucesso - {produto.modulos.count()} módulos")
                return redirect('produtos_lista')
                
        except Exception as e:
            logger.error(f"Erro ao atualizar produto {produto_id}: {str(e)}", exc_info=True)
            messages.error(request, f'Erro ao atualizar produto: {str(e)}')
    
    context = {
        'produto': produto,
        'modulos': produto.modulos.prefetch_related('tamanhos_detalhados').all(),
        'tipos': TipoItem.objects.all(),
        'produtos_disponiveis': Item.objects.filter(ativo=True).exclude(id=produto.id).order_by('ref_produto'),
        'produtos_vinculados_ids': list(produto.produtos_vinculados.values_list('id', flat=True)),
    }
    return render(request, 'produtos/sofas/editar_unificado.html', context)

@login_required
def produto_excluir_view(request, produto_id):
    """View para exclusão de produtos"""
    produto = get_object_or_404(Item, id=produto_id)
    
    if request.method == 'POST':
        try:
            nome_produto = produto.nome_produto
            produto.delete()
            messages.success(request, f'Produto "{nome_produto}" excluído com sucesso!')
        except Exception as e:
            messages.error(request, f'Erro ao excluir produto: {str(e)}')
    
    return redirect('produtos_lista')

@login_required
def produto_detalhes_view(request, produto_id):
    """View para visualização detalhada de um produto (inclui banquetas)"""
    # Primeiro, tentar buscar na tabela Item
    try:
        produto = Item.objects.select_related('id_tipo_produto').get(id=produto_id)
        modulos = produto.modulos.prefetch_related('tamanhos_detalhados').all()
        
        # Buscar acessórios vinculados a este produto
        acessorios_vinculados = Acessorio.objects.filter(produtos_vinculados=produto).order_by('ref_acessorio')
        
        # Verificar se é um produto do tipo acessório
        eh_acessorio = produto.id_tipo_produto.nome.lower() == 'acessórios'
        
        context = {
            'produto': produto,
            'modulos': modulos,
            'acessorios_vinculados': acessorios_vinculados,
            'eh_acessorio': eh_acessorio,
            'eh_banqueta': False,
        }
        return render(request, 'produtos/detalhes.html', context)
        
    except Item.DoesNotExist:
        # Se não encontrou na tabela Item, tentar buscar na tabela Banqueta
        try:
            banqueta = Banqueta.objects.get(id=produto_id)
            context = {
                'banqueta': banqueta,
                'eh_banqueta': True,
            }
            return render(request, 'produtos/banquetas/detalhes.html', context)
            
        except Banqueta.DoesNotExist:
            # Se não encontrou em nenhuma tabela, retornar 404
            raise Http404("Produto não encontrado")

def teste_view(request):
    """View de teste para diagnosticar problemas"""
    return render(request, 'teste.html')

def teste_imagem_view(request):
    """View de teste para upload de imagem"""
    if request.method == 'POST':
        if 'imagem_teste' in request.FILES:
            return render(request, 'produtos/teste_imagem.html', {
                'sucesso': 'Imagem recebida com sucesso!',
                'arquivo': request.FILES['imagem_teste'].name
            })
    
    return render(request, 'produtos/teste_imagem.html')

@login_required
@csrf_protect
def debug_cadastro_view(request):
    """View de debug para verificar dados POST"""
    if request.method == 'POST':
        debug_info = {
            'POST_data': dict(request.POST),
            'FILES_data': list(request.FILES.keys()),
            'method': request.method,
        }
        logger.info(f"Debug cadastro - Dados recebidos: {debug_info}")
        messages.info(request, f"Debug: {debug_info}")
        return JsonResponse(debug_info)
    
    return render(request, 'produtos/debug_cadastro.html', {
        'tipos': TipoItem.objects.all()
    })

@login_required
def teste_cadastro_view(request):
    """View de teste para cadastro simples"""
    context = {
        'tipos': TipoItem.objects.all(),
    }
    return render(request, 'produtos/teste_cadastro.html', context)

@login_required
def teste_tamanhos_edicao_view(request):
    """View de teste para verificar funcionalidade de tamanhos na edição"""
    return render(request, 'produtos/teste_tamanhos_edicao.html')

@login_required
def api_produtos_disponiveis(request):
    """API para carregar produtos disponíveis para vinculação"""
    produtos = Item.objects.filter(ativo=True).exclude(
        id_tipo_produto__nome__iexact='acessórios'
    ).values('id', 'ref_produto', 'nome_produto').order_by('ref_produto')
    
    return JsonResponse(list(produtos), safe=False)

@login_required
def acessorios_list_view(request):
    """View para listagem de acessórios"""
    acessorios = Acessorio.objects.prefetch_related('produtos_vinculados').all()
    
    # Filtros
    ativo_filtro = request.GET.get('ativo')
    busca = request.GET.get('busca')
    
    if ativo_filtro:
        acessorios = acessorios.filter(ativo=ativo_filtro == 'true')
    
    if busca:
        acessorios = acessorios.filter(
            nome__icontains=busca
        ) | acessorios.filter(
            ref_acessorio__icontains=busca
        )
    
    context = {
        'acessorios': acessorios,
        'ativo_filtro': ativo_filtro,
        'busca': busca,
    }
    return render(request, 'produtos/acessorios/lista.html', context)

@login_required
@csrf_protect
def acessorio_cadastro_view(request):
    """View para cadastro de acessórios"""
    if request.method == 'POST':
        form = AcessorioForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                with transaction.atomic():
                    acessorio = form.save(commit=False)
                    # Rastrear usuário
                    track_user_changes(acessorio, request.user)
                    acessorio.save()
                    messages.success(
                        request, 
                        f'Acessório "{acessorio.ref_acessorio} - {acessorio.nome}" cadastrado com sucesso!'
                    )
                    return redirect('acessorio_detalhes', acessorio_id=acessorio.id)
            except Exception as e:
                logger.error(f"Erro ao cadastrar acessório: {str(e)}")
                messages.error(request, f'Erro ao cadastrar acessório: {str(e)}')
        else:
            logger.warning(f"Formulário de acessório inválido: {form.errors}")
            messages.error(request, 'Erro no formulário. Verifique os dados informados.')
    else:
        form = AcessorioForm()
    
    context = {
        'form': form,
        'titulo': 'Cadastro de Acessório',
        'action_url': 'acessorio_cadastro',
    }
    return render(request, 'produtos/acessorios/formulario.html', context)

@login_required
def acessorio_detalhes_view(request, acessorio_id):
    """View para visualizar detalhes de um acessório"""
    acessorio = get_object_or_404(Acessorio, id=acessorio_id)
    produtos_vinculados = acessorio.produtos_vinculados.all()
    
    context = {
        'acessorio': acessorio,
        'produtos_vinculados': produtos_vinculados,
    }
    return render(request, 'produtos/acessorios/detalhes.html', context)

@login_required
@csrf_protect
def acessorio_editar_view(request, acessorio_id):
    """View para editar um acessório"""
    acessorio = get_object_or_404(Acessorio, id=acessorio_id)
    
    if request.method == 'POST':
        form = AcessorioForm(request.POST, request.FILES, instance=acessorio)
        if form.is_valid():
            try:
                with transaction.atomic():
                    acessorio = form.save(commit=False)
                    # Rastrear usuário na edição
                    track_user_changes(acessorio, request.user)
                    acessorio.save()
                    messages.success(
                        request, 
                        f'Acessório "{acessorio.ref_acessorio} - {acessorio.nome}" atualizado com sucesso!'
                    )
                    return redirect('acessorio_detalhes', acessorio_id=acessorio.id)
            except Exception as e:
                logger.error(f"Erro ao editar acessório: {str(e)}")
                messages.error(request, f'Erro ao editar acessório: {str(e)}')
        else:
            logger.warning(f"Formulário de acessório inválido: {form.errors}")
            messages.error(request, 'Erro no formulário. Verifique os dados informados.')
    else:
        form = AcessorioForm(instance=acessorio)
    
    context = {
        'form': form,
        'acessorio': acessorio,
        'titulo': f'Editar Acessório - {acessorio.ref_acessorio}',
        'action_url': 'acessorio_editar',
        'action_id': acessorio.id,
    }
    return render(request, 'produtos/acessorios/formulario.html', context)

@login_required
@csrf_protect
def acessorio_excluir_view(request, acessorio_id):
    """View para excluir um acessório"""
    acessorio = get_object_or_404(Acessorio, id=acessorio_id)
    
    if request.method == 'POST':
        try:
            nome_acessorio = f"{acessorio.ref_acessorio} - {acessorio.nome}"
            acessorio.delete()
            messages.success(request, f'Acessório "{nome_acessorio}" excluído com sucesso!')
            return redirect('acessorios_lista')
        except Exception as e:
            logger.error(f"Erro ao excluir acessório: {str(e)}")
            messages.error(request, f'Erro ao excluir acessório: {str(e)}')
            return redirect('acessorio_detalhes', acessorio_id=acessorio.id)
    
    context = {
        'acessorio': acessorio,
    }
    return render(request, 'produtos/acessorios/confirmar_exclusao.html', context)

# ===== VIEWS PARA BANQUETAS =====

@login_required
def banquetas_list_view(request):
    """View para listagem de banquetas"""
    banquetas = Banqueta.objects.all()
    
    # Filtros
    ativo_filtro = request.GET.get('ativo')
    busca = request.GET.get('busca')
    
    if ativo_filtro:
        banquetas = banquetas.filter(ativo=ativo_filtro == 'true')
    
    if busca:
        banquetas = banquetas.filter(
            nome__icontains=busca
        ) | banquetas.filter(
            ref_banqueta__icontains=busca
        )
    
    context = {
        'banquetas': banquetas,
        'filtros': {
            'ativo': ativo_filtro,
            'busca': busca,
        }
    }
    return render(request, 'produtos/banquetas/lista.html', context)

@login_required
@csrf_protect
def banqueta_cadastro_view(request):
    """View para cadastro de banquetas"""
    if request.method == 'POST':
        form = BanquetaForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                with transaction.atomic():
                    banqueta = form.save(commit=False)
                    # Rastrear usuário
                    track_user_changes(banqueta, request.user)
                    banqueta.save()
                    
                    messages.success(request, f'Banqueta "{banqueta.ref_banqueta} - {banqueta.nome}" cadastrada com sucesso!')
                    return redirect('banquetas_lista')
            except Exception as e:
                logger.error(f"Erro ao cadastrar banqueta: {str(e)}")
                messages.error(request, f'Erro ao cadastrar banqueta: {str(e)}')
    else:
        form = BanquetaForm()
    
    context = {
        'form': form,
        'title': 'Cadastrar Nova Banqueta'
    }
    return render(request, 'produtos/banquetas/cadastro.html', context)

@login_required
def banqueta_detalhes_view(request, banqueta_id):
    """View para exibir detalhes de uma banqueta"""
    banqueta = get_object_or_404(Banqueta, id=banqueta_id)
    
    context = {
        'banqueta': banqueta,
    }
    return render(request, 'produtos/banquetas/detalhes.html', context)

def banqueta_teste_imagem_view(request, banqueta_id):
    """View de teste para imagens de banquetas"""
    banqueta = get_object_or_404(Banqueta, id=banqueta_id)
    
    context = {
        'banqueta': banqueta,
    }
    return render(request, 'produtos/banquetas/teste_imagem.html', context)

@login_required
@csrf_protect
def banqueta_editar_view(request, banqueta_id):
    """View para editar banquetas"""
    banqueta = get_object_or_404(Banqueta, id=banqueta_id)
    
    if request.method == 'POST':
        form = BanquetaForm(request.POST, request.FILES, instance=banqueta)
        if form.is_valid():
            try:
                with transaction.atomic():
                    banqueta = form.save(commit=False)
                    # Rastrear usuário
                    track_user_changes(banqueta, request.user)
                    banqueta.save()
                    
                    messages.success(request, f'Banqueta "{banqueta.ref_banqueta} - {banqueta.nome}" atualizada com sucesso!')
                    return redirect('produto_detalhes', produto_id=banqueta.id)
            except Exception as e:
                logger.error(f"Erro ao editar banqueta: {str(e)}")
                messages.error(request, f'Erro ao editar banqueta: {str(e)}')
    else:
        form = BanquetaForm(instance=banqueta)
    
    context = {
        'form': form,
        'banqueta': banqueta,
        'title': f'Editar Banqueta {banqueta.ref_banqueta}'
    }
    return render(request, 'produtos/banquetas/editar.html', context)

@login_required
@csrf_protect
def banqueta_excluir_view(request, banqueta_id):
    """View para excluir banquetas"""
    banqueta = get_object_or_404(Banqueta, id=banqueta_id)
    
    if request.method == 'POST':
        try:
            nome_banqueta = f"{banqueta.ref_banqueta} - {banqueta.nome}"
            banqueta.delete()
            messages.success(request, f'Banqueta "{nome_banqueta}" excluída com sucesso!')
            return redirect('banquetas_lista')
        except Exception as e:
            logger.error(f"Erro ao excluir banqueta: {str(e)}")
            messages.error(request, f'Erro ao excluir banqueta: {str(e)}')
            return redirect('produto_detalhes', produto_id=banqueta.id)
    
    context = {
        'banqueta': banqueta,
    }
    return render(request, 'produtos/banquetas/confirmar_exclusao.html', context)
