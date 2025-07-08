from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.csrf import csrf_protect
from django.db import transaction
from django.db import models
from django.http import JsonResponse, Http404
from django.core.paginator import Paginator
from rest_framework import viewsets, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
import logging
from sistema_produtos.mixins import track_user_changes
from authentication.decorators import admin_or_master_required, produtos_access_required
from .models import (
    Produto, TipoItem, Linha, Modulo, Acessorio, 
    TamanhosModulos, TamanhosModulosDetalhado, FaixaTecido, PrecosBase,
    Banqueta, Cadeira, Poltrona, Pufe, Almofada
)
from .forms import AcessorioForm, BanquetaForm, CadeiraForm, PoltronaForm, PufeForm, AlmofadaForm

logger = logging.getLogger(__name__)

@login_required
def home_view(request):
    """View da página inicial do sistema"""
    # Verificar se o usuário tem permissão para acessar o home
    if not request.user.can_access_home():
        # Redirecionar baseado no tipo de permissão
        if request.user.tipo_permissao == 'vendedor':
            return redirect('orcamentos:listar')
        elif request.user.tipo_permissao == 'operador_produtos':
            return redirect('produtos_lista')
        else:
            # Fallback para produtos se não conseguir determinar
            return redirect('produtos_lista')
    
    context = {
        'total_produtos': Produto.objects.count(),
        'total_tipos': TipoItem.objects.count(),
        'total_modulos': Modulo.objects.count(),
        'produtos_recentes': Produto.objects.select_related('id_tipo_produto').order_by('-created_at')[:5],
    }
    return render(request, 'produtos/home.html', context)

@produtos_access_required
def produtos_list_view(request):
    """View para listagem de produtos unificada (inclui todos os tipos)"""
    # Buscar produtos da nova tabela Produto (apenas dados básicos)
    produtos = Produto.objects.select_related('id_tipo_produto').all()
    
    # Buscar produtos das tabelas específicas
    banquetas = Banqueta.objects.filter(ativo=True).all()
    cadeiras = Cadeira.objects.filter(ativo=True).all()
    poltronas = Poltrona.objects.filter(ativo=True).all()
    pufes = Pufe.objects.filter(ativo=True).all()
    almofadas = Almofada.objects.filter(ativo=True).all()
    
    # Filtros
    tipo_filtro = request.GET.get('tipo')
    ativo_filtro = request.GET.get('ativo')
    busca = request.GET.get('busca')
    
    # Parâmetros de ordenação
    ordenar_por = request.GET.get('ordenar_por', 'referencia')  # campo padrão
    direcao = request.GET.get('direcao', 'asc')  # asc ou desc
    
    if tipo_filtro:
        # Filtrar produtos por tipo
        produtos = produtos.filter(id_tipo_produto__id=tipo_filtro)
        
        # Se o filtro for por tipo específico, mostrar apenas esse tipo
        if tipo_filtro == '4':  # Banquetas
            produtos = Produto.objects.none()
            cadeiras = Cadeira.objects.none()
            poltronas = Poltrona.objects.none()
            pufes = Pufe.objects.none()
            almofadas = Almofada.objects.none()
        elif tipo_filtro == '3':  # Cadeiras
            produtos = Produto.objects.none()
            banquetas = Banqueta.objects.none()
            poltronas = Poltrona.objects.none()
            pufes = Pufe.objects.none()
            almofadas = Almofada.objects.none()
        elif tipo_filtro == '5':  # Poltronas (assumindo ID 5)
            produtos = Produto.objects.none()
            banquetas = Banqueta.objects.none()
            cadeiras = Cadeira.objects.none()
            pufes = Pufe.objects.none()
            almofadas = Almofada.objects.none()
        elif tipo_filtro == '6':  # Pufes (assumindo ID 6)
            produtos = Produto.objects.none()
            banquetas = Banqueta.objects.none()
            cadeiras = Cadeira.objects.none()
            poltronas = Poltrona.objects.none()
            almofadas = Almofada.objects.none()
        elif tipo_filtro == '7':  # Almofadas (assumindo ID 7)
            produtos = Produto.objects.none()
            banquetas = Banqueta.objects.none()
            cadeiras = Cadeira.objects.none()
            poltronas = Poltrona.objects.none()
            pufes = Pufe.objects.none()
        else:
            # Para outros tipos, não mostrar produtos das tabelas específicas
            banquetas = Banqueta.objects.none()
            cadeiras = Cadeira.objects.none()
            poltronas = Poltrona.objects.none()
            pufes = Pufe.objects.none()
            almofadas = Almofada.objects.none()
    
    if ativo_filtro:
        produtos = produtos.filter(ativo=ativo_filtro == 'true')
        banquetas = banquetas.filter(ativo=ativo_filtro == 'true')
        cadeiras = cadeiras.filter(ativo=ativo_filtro == 'true')
        poltronas = poltronas.filter(ativo=ativo_filtro == 'true')
        pufes = pufes.filter(ativo=ativo_filtro == 'true')
        almofadas = almofadas.filter(ativo=ativo_filtro == 'true')
    
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
        cadeiras = cadeiras.filter(
            nome__icontains=busca
        ) | cadeiras.filter(
            ref_cadeira__icontains=busca
        )
        poltronas = poltronas.filter(
            nome__icontains=busca
        ) | poltronas.filter(
            ref_poltrona__icontains=busca
        )
        pufes = pufes.filter(
            nome__icontains=busca
        ) | pufes.filter(
            ref_pufe__icontains=busca
        )
        almofadas = almofadas.filter(
            nome__icontains=busca
        ) | almofadas.filter(
            ref_almofada__icontains=busca
        )
    
    # Aplicar ordenação
    # Mapeamento de campos para ordenação
    campos_ordenacao = {
        'referencia': {
            'Produto': 'ref_produto',
            'Banqueta': 'ref_banqueta', 
            'Cadeira': 'ref_cadeira',
            'Poltrona': 'ref_poltrona',
            'Pufe': 'ref_pufe',
            'Almofada': 'ref_almofada'
        },
        'nome': {
            'Produto': 'nome_produto',
            'Banqueta': 'nome',
            'Cadeira': 'nome', 
            'Poltrona': 'nome',
            'Pufe': 'nome',
            'Almofada': 'nome'
        },
        'tipo': {
            'Produto': 'id_tipo_produto__nome',
            'Banqueta': 'created_at',  # Banquetas sempre terão tipo fixo
            'Cadeira': 'created_at',   # Cadeiras sempre terão tipo fixo
            'Poltrona': 'created_at',  # Poltronas sempre terão tipo fixo
            'Pufe': 'created_at',      # Pufes sempre terão tipo fixo
            'Almofada': 'created_at'   # Almofadas sempre terão tipo fixo
        },
        'status': {
            'Produto': 'ativo',
            'Banqueta': 'ativo',
            'Cadeira': 'ativo',
            'Poltrona': 'ativo', 
            'Pufe': 'ativo',
            'Almofada': 'ativo'
        },
        'created_at': {
            'Produto': 'created_at',
            'Banqueta': 'created_at',
            'Cadeira': 'created_at',
            'Poltrona': 'created_at',
            'Pufe': 'created_at', 
            'Almofada': 'created_at'
        },
        'created_by': {
            'Produto': 'created_by__email',
            'Banqueta': 'created_by__email',
            'Cadeira': 'created_by__email',
            'Poltrona': 'created_by__email',
            'Pufe': 'created_by__email',
            'Almofada': 'created_by__email'
        }
    }
    
    if ordenar_por in campos_ordenacao:
        # Aplicar ordenação para cada tipo de produto
        campo_produto = campos_ordenacao[ordenar_por]['Produto']
        campo_banqueta = campos_ordenacao[ordenar_por]['Banqueta']
        campo_cadeira = campos_ordenacao[ordenar_por]['Cadeira']
        campo_poltrona = campos_ordenacao[ordenar_por]['Poltrona']
        campo_pufe = campos_ordenacao[ordenar_por]['Pufe']
        campo_almofada = campos_ordenacao[ordenar_por]['Almofada']
        
        if direcao == 'desc':
            campo_produto = '-' + campo_produto
            campo_banqueta = '-' + campo_banqueta
            campo_cadeira = '-' + campo_cadeira
            campo_poltrona = '-' + campo_poltrona
            campo_pufe = '-' + campo_pufe
            campo_almofada = '-' + campo_almofada
        
        produtos = produtos.order_by(campo_produto)
        banquetas = banquetas.order_by(campo_banqueta)
        cadeiras = cadeiras.order_by(campo_cadeira)
        poltronas = poltronas.order_by(campo_poltrona)
        pufes = pufes.order_by(campo_pufe)
        almofadas = almofadas.order_by(campo_almofada)
    
    context = {
        'produtos': produtos,
        'banquetas': banquetas,
        'cadeiras': cadeiras,
        'poltronas': poltronas,
        'pufes': pufes,
        'almofadas': almofadas,
        'total_itens': produtos.count() + banquetas.count() + cadeiras.count() + poltronas.count() + pufes.count() + almofadas.count(),
        'tipos': TipoItem.objects.all(),
        'filtros': {
            'tipo': tipo_filtro,
            'ativo': ativo_filtro,
            'busca': busca,
        },
        'ordenacao': {
            'campo': ordenar_por,
            'direcao': direcao,
        }
    }
    return render(request, 'produtos/lista.html', context)

@produtos_access_required
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
                if Produto.objects.filter(ref_produto=ref_produto).exists():
                    messages.error(request, 'Já existe um produto com esta referência.')
                    raise ValueError('Referência duplicada')
                
                # Verificar tipo de produto
                tipo_produto = get_object_or_404(TipoItem, id=tipo_produto_id)
                eh_acessorio = tipo_produto.nome.lower() == 'acessórios'
                eh_banqueta = tipo_produto.nome.lower() == 'banquetas'
                eh_cadeira = tipo_produto.nome.lower() == 'cadeiras'
                eh_poltrona = tipo_produto.nome.lower() == 'poltronas'
                eh_pufe = tipo_produto.nome.lower() == 'pufes'
                eh_almofada = tipo_produto.nome.lower() == 'almofadas'
                
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
                    
                elif eh_cadeira:
                    # Processar como cadeira usando o modelo específico
                    largura = request.POST.get('largura_cadeira')
                    profundidade = request.POST.get('profundidade_cadeira')
                    altura = request.POST.get('altura_cadeira')
                    tecido_metros = request.POST.get('tecido_metros_cadeira')
                    volume_m3 = request.POST.get('volume_m3_cadeira')
                    peso_kg = request.POST.get('peso_kg_cadeira')
                    preco = request.POST.get('preco_cadeira')
                    ativo = request.POST.get('ativo_cadeira') == 'on'
                    descricao = request.POST.get('descricao_cadeira')
                    
                    # Validar campos obrigatórios para cadeiras
                    if not all([largura, profundidade, altura, tecido_metros, volume_m3, peso_kg, preco]):
                        messages.error(request, 'Por favor, preencha todos os campos obrigatórios para cadeiras.')
                        raise ValueError('Campos obrigatórios da cadeira não preenchidos')
                    
                    # Criar cadeira
                    cadeira = Cadeira(
                        ref_cadeira=ref_produto,
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
                    track_user_changes(cadeira, request.user)
                    cadeira.save()
                    
                    messages.success(request, f'Cadeira "{cadeira.ref_cadeira} - {cadeira.nome}" cadastrada com sucesso!')
                    return redirect('cadeiras_lista')
                
                elif eh_poltrona:
                    # Processar como poltrona usando o modelo específico
                    largura = request.POST.get('largura_poltrona')
                    profundidade = request.POST.get('profundidade_poltrona')
                    altura = request.POST.get('altura_poltrona')
                    tecido_metros = request.POST.get('tecido_metros_poltrona')
                    volume_m3 = request.POST.get('volume_m3_poltrona')
                    peso_kg = request.POST.get('peso_kg_poltrona')
                    preco = request.POST.get('preco_poltrona')
                    ativo = request.POST.get('ativo_poltrona') == 'on'
                    descricao = request.POST.get('descricao_poltrona')
                    
                    # Validar campos obrigatórios para poltronas
                    if not all([largura, profundidade, altura, tecido_metros, volume_m3, peso_kg, preco]):
                        messages.error(request, 'Por favor, preencha todos os campos obrigatórios para poltronas.')
                        raise ValueError('Campos obrigatórios da poltrona não preenchidos')
                    
                    # Criar poltrona
                    poltrona = Poltrona(
                        ref_poltrona=ref_produto,
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
                    track_user_changes(poltrona, request.user)
                    poltrona.save()
                    
                    messages.success(request, f'Poltrona "{poltrona.ref_poltrona} - {poltrona.nome}" cadastrada com sucesso!')
                    return redirect('produtos_lista')
                    
                elif eh_pufe:
                    # Processar como pufe usando o modelo específico
                    largura = request.POST.get('largura_pufe')
                    profundidade = request.POST.get('profundidade_pufe')
                    altura = request.POST.get('altura_pufe')
                    tecido_metros = request.POST.get('tecido_metros_pufe')
                    volume_m3 = request.POST.get('volume_m3_pufe')
                    peso_kg = request.POST.get('peso_kg_pufe')
                    preco = request.POST.get('preco_pufe')
                    ativo = request.POST.get('ativo_pufe') == 'on'
                    descricao = request.POST.get('descricao_pufe')
                    
                    # Validar campos obrigatórios para pufes
                    if not all([largura, profundidade, altura, tecido_metros, volume_m3, peso_kg, preco]):
                        messages.error(request, 'Por favor, preencha todos os campos obrigatórios para pufes.')
                        raise ValueError('Campos obrigatórios do pufe não preenchidos')
                    
                    # Criar pufe
                    pufe = Pufe(
                        ref_pufe=ref_produto,
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
                    track_user_changes(pufe, request.user)
                    pufe.save()
                    
                    messages.success(request, f'Pufe "{pufe.ref_pufe} - {pufe.nome}" cadastrado com sucesso!')
                    return redirect('produtos_lista')
                    
                elif eh_almofada:
                    # Processar como almofada usando o modelo específico (sem profundidade)
                    largura = request.POST.get('largura_almofada')
                    altura = request.POST.get('altura_almofada')
                    tecido_metros = request.POST.get('tecido_metros_almofada')
                    volume_m3 = request.POST.get('volume_m3_almofada')
                    peso_kg = request.POST.get('peso_kg_almofada')
                    preco = request.POST.get('preco_almofada')
                    ativo = request.POST.get('ativo_almofada') == 'on'
                    descricao = request.POST.get('descricao_almofada')
                    
                    # Validar campos obrigatórios para almofadas (sem profundidade)
                    if not all([largura, altura, tecido_metros, volume_m3, peso_kg, preco]):
                        messages.error(request, 'Por favor, preencha todos os campos obrigatórios para almofadas.')
                        raise ValueError('Campos obrigatórios da almofada não preenchidos')
                    
                    # Criar almofada
                    almofada = Almofada(
                        ref_almofada=ref_produto,
                        nome=nome_produto,
                        largura=float(largura),
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
                    track_user_changes(almofada, request.user)
                    almofada.save()
                    
                    messages.success(request, f'Almofada "{almofada.ref_almofada} - {almofada.nome}" cadastrada com sucesso!')
                    return redirect('produtos_lista')
                    
                elif eh_acessorio:
                    # Processar como acessório usando os modelos separados
                    ativo = request.POST.get('ativo_acessorio') == 'on'
                    preco = request.POST.get('preco_acessorio')
                    descricao = request.POST.get('descricao_acessorio')
                    produtos_vinculados = request.POST.getlist('produtos_vinculados')
                    
                    # Criar produto básico primeiro
                    produto = Produto(
                        ref_produto=ref_produto,
                        nome_produto=nome_produto,
                        id_tipo_produto_id=tipo_produto_id,
                        ativo=ativo,
                        imagem_principal=request.FILES.get('imagem_principal'),
                        imagem_secundaria=request.FILES.get('imagem_secundaria')
                    )
                    track_user_changes(produto, request.user)
                    produto.save()
                    
                    # Criar acessório vinculado
                    acessorio = Acessorio(
                        ref_acessorio=ref_produto,
                        nome=nome_produto,
                        ativo=ativo,
                        preco=float(preco) if preco else None,
                        descricao=descricao if descricao else None,
                        imagem_principal=request.FILES.get('imagem_principal'),
                        imagem_secundaria=request.FILES.get('imagem_secundaria')
                    )
                    track_user_changes(acessorio, request.user)
                    acessorio.save()
                    
                    # Vincular produtos se selecionados
                    if produtos_vinculados:
                        for produto_id in produtos_vinculados:
                            if produto_id:
                                try:
                                    produto_vinculado = Produto.objects.get(id=produto_id)
                                    acessorio.produtos_vinculados.add(produto_vinculado)
                                except Produto.DoesNotExist:
                                    continue
                    
                    messages.success(request, f'Acessório "{produto.ref_produto} - {produto.nome_produto}" cadastrado com sucesso!')
                    return redirect('produtos_lista')
                    
                else:
                    # Processar como produto normal (sofá, cadeira, etc.)
                    ativo = request.POST.get('ativo') == 'on'
                    
                    # Criar o produto básico (sem campos específicos de Item)
                    produto = Produto(
                        ref_produto=ref_produto,
                        nome_produto=nome_produto,
                        id_tipo_produto_id=tipo_produto_id,
                        ativo=ativo,
                        imagem_principal=request.FILES.get('imagem_principal'),
                        imagem_secundaria=request.FILES.get('imagem_secundaria')
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
        'produtos_disponiveis': Produto.objects.filter(ativo=True).order_by('ref_produto'),
    }
    return render(request, 'produtos/cadastro_unificado.html', context)

@produtos_access_required
def produto_editar_view(request, produto_id):
    """View para edição de produtos (incluindo acessórios)"""
    produto = get_object_or_404(Produto, id=produto_id)
    
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
                                    produto_vinculado = Produto.objects.get(id=produto_id_vinc)
                                    produto.produtos_vinculados.add(produto_vinculado)
                                    logger.info(f"Produto {produto_vinculado.ref_produto} vinculado com sucesso")
                                except Produto.DoesNotExist:
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
        'produtos_disponiveis': Produto.objects.filter(ativo=True).exclude(id=produto.id).order_by('ref_produto'),
        'produtos_vinculados_ids': list(produto.produtos_vinculados.values_list('id', flat=True)),
    }
    return render(request, 'produtos/sofas/editar_unificado.html', context)

@produtos_access_required
def produto_excluir_view(request, produto_id):
    """View para exclusão de produtos"""
    produto = get_object_or_404(Produto, id=produto_id)
    
    if request.method == 'POST':
        try:
            nome_produto = produto.nome_produto
            produto.delete()
            messages.success(request, f'Produto "{nome_produto}" excluído com sucesso!')
        except Exception as e:
            messages.error(request, f'Erro ao excluir produto: {str(e)}')
    
    return redirect('produtos_lista')

@produtos_access_required
def produto_detalhes_view(request, produto_id):
    """View para visualização detalhada de um produto (inclui banquetas)"""
    # Primeiro, tentar buscar na tabela Produto
    try:
        produto = Produto.objects.select_related('id_tipo_produto').get(id=produto_id)
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
        
    except Produto.DoesNotExist:
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

@produtos_access_required
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

@produtos_access_required
def teste_cadastro_view(request):
    """View de teste para cadastro simples"""
    context = {
        'tipos': TipoItem.objects.all(),
    }
    return render(request, 'produtos/teste_cadastro.html', context)

@produtos_access_required
def teste_tamanhos_edicao_view(request):
    """View de teste para verificar funcionalidade de tamanhos na edição"""
    return render(request, 'produtos/teste_tamanhos_edicao.html')

@produtos_access_required
def api_produtos_disponiveis(request):
    """API para carregar produtos disponíveis para vinculação"""
    produtos = Produto.objects.filter(ativo=True).exclude(
        id_tipo_produto__nome__iexact='acessórios'
    ).values('id', 'ref_produto', 'nome_produto').order_by('ref_produto')
    
    return JsonResponse(list(produtos), safe=False)

@produtos_access_required
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

@produtos_access_required
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

@produtos_access_required
def acessorio_detalhes_view(request, acessorio_id):
    """View para visualizar detalhes de um acessório"""
    acessorio = get_object_or_404(Acessorio, id=acessorio_id)
    produtos_vinculados = acessorio.produtos_vinculados.all()
    
    context = {
        'acessorio': acessorio,
        'produtos_vinculados': produtos_vinculados,
    }
    return render(request, 'produtos/acessorios/detalhes.html', context)

@produtos_access_required
@csrf_protect
def acessorio_editar_view(request, acessorio_id):
    """View para editar um acessório - busca por ID do Produto"""
    # Primeiro buscar o produto correspondente
    produto = get_object_or_404(Produto, id=acessorio_id)
    
    # Depois buscar o acessório correspondente
    try:
        acessorio = Acessorio.objects.get(ref_acessorio=produto.ref_produto)
    except Acessorio.DoesNotExist:
        # Se não existir acessório, criar um baseado no produto
        acessorio = Acessorio.objects.create(
            ref_acessorio=produto.ref_produto,
            nome=produto.nome_produto,
            ativo=produto.ativo,
            imagem_principal=produto.imagem_principal,
            imagem_secundaria=produto.imagem_secundaria
        )
        messages.info(request, f'Acessório criado automaticamente para {produto.ref_produto}')
    
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
    return render(request, 'produtos/acessorios/editar.html', context)

@produtos_access_required
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

@produtos_access_required
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

@produtos_access_required
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

@produtos_access_required
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

@produtos_access_required
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

@produtos_access_required
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

# ============================================================================
# VIEWS PARA CADEIRAS
# ============================================================================

@produtos_access_required
def cadeiras_list_view(request):
    """View para listagem de cadeiras"""
    # Buscar cadeiras da tabela Cadeira
    cadeiras = Cadeira.objects.filter(ativo=True).all()
    
    # Filtros
    busca = request.GET.get('busca')
    
    if busca:
        cadeiras = cadeiras.filter(
            nome__icontains=busca
        ) | cadeiras.filter(
            ref_cadeira__icontains=busca
        )
    
    # Paginação
    from django.core.paginator import Paginator
    paginator = Paginator(cadeiras, 12)  # 12 cadeiras por página
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'cadeiras': page_obj,
        'busca': busca,
        'total_cadeiras': cadeiras.count(),
        'page_obj': page_obj,
    }
    return render(request, 'produtos/cadeiras/lista.html', context)

@produtos_access_required
@csrf_protect
def cadeira_cadastro_view(request):
    """View para cadastro de cadeiras"""
    if request.method == 'POST':
        form = CadeiraForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                with transaction.atomic():
                    cadeira = form.save(commit=False)
                    # Rastrear usuário
                    track_user_changes(cadeira, request.user)
                    cadeira.save()
                    
                    messages.success(request, f'Cadeira "{cadeira.ref_cadeira} - {cadeira.nome}" cadastrada com sucesso!')
                    return redirect('cadeira_detalhes', cadeira_id=cadeira.id)
            except Exception as e:
                logger.error(f"Erro ao cadastrar cadeira: {str(e)}")
                messages.error(request, f'Erro ao cadastrar cadeira: {str(e)}')
    else:
        form = CadeiraForm()
    
    context = {
        'form': form,
        'title': 'Cadastrar Nova Cadeira'
    }
    return render(request, 'produtos/cadeiras/cadastro.html', context)

@produtos_access_required
def cadeira_detalhes_view(request, cadeira_id):
    """View para exibir detalhes de uma cadeira"""
    cadeira = get_object_or_404(Cadeira, id=cadeira_id)
    
    context = {
        'cadeira': cadeira,
    }
    return render(request, 'produtos/cadeiras/detalhes.html', context)

@produtos_access_required
def cadeira_teste_imagem_view(request, cadeira_id):
    """View para testar exibição de imagem de cadeira"""
    cadeira = get_object_or_404(Cadeira, id=cadeira_id)
    return render(request, 'produtos/cadeiras/teste_imagem.html', {'cadeira': cadeira})

@produtos_access_required
@csrf_protect
def cadeira_editar_view(request, cadeira_id):
    """View para editar cadeiras"""
    cadeira = get_object_or_404(Cadeira, id=cadeira_id)
    
    if request.method == 'POST':
        form = CadeiraForm(request.POST, request.FILES, instance=cadeira)
        if form.is_valid():
            try:
                with transaction.atomic():
                    cadeira = form.save(commit=False)
                    # Rastrear usuário
                    track_user_changes(cadeira, request.user)
                    cadeira.save()
                    
                    messages.success(request, f'Cadeira "{cadeira.ref_cadeira} - {cadeira.nome}" atualizada com sucesso!')
                    return redirect('cadeira_detalhes', cadeira_id=cadeira.id)
            except Exception as e:
                logger.error(f"Erro ao editar cadeira: {str(e)}")
                messages.error(request, f'Erro ao editar cadeira: {str(e)}')
    else:
        form = CadeiraForm(instance=cadeira)
    
    context = {
        'form': form,
        'cadeira': cadeira,
        'title': f'Editar Cadeira {cadeira.ref_cadeira}'
    }
    return render(request, 'produtos/cadeiras/editar.html', context)

@produtos_access_required
@csrf_protect
def cadeira_excluir_view(request, cadeira_id):
    """View para excluir cadeiras"""
    cadeira = get_object_or_404(Cadeira, id=cadeira_id)
    
    if request.method == 'POST':
        try:
            nome_cadeira = f"{cadeira.ref_cadeira} - {cadeira.nome}"
            cadeira.delete()
            messages.success(request, f'Cadeira "{nome_cadeira}" excluída com sucesso!')
            return redirect('cadeiras_lista')
        except Exception as e:
            logger.error(f"Erro ao excluir cadeira: {str(e)}")
            messages.error(request, f'Erro ao excluir cadeira: {str(e)}')
            return redirect('cadeira_detalhes', cadeira_id=cadeira.id)
    
    context = {
        'cadeira': cadeira,
    }
    return render(request, 'produtos/cadeiras/confirmar_exclusao.html', context)


# ================================
# VIEWS PARA POLTRONAS 
# ================================

def poltronas_list_view(request):
    """View para listar poltronas"""
    poltronas = Poltrona.objects.filter(ativo=True).order_by('ref_poltrona')
    
    # Busca
    busca = request.GET.get('busca', '').strip()
    if busca:
        poltronas = poltronas.filter(
            models.Q(nome__icontains=busca) |
            models.Q(ref_poltrona__icontains=busca)
        )
    
    # Paginação
    paginator = Paginator(poltronas, 12)  # 12 poltronas por página
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'poltronas': page_obj,
        'busca': busca,
        'total_poltronas': poltronas.count(),
    }
    return render(request, 'produtos/poltronas/lista.html', context)


def poltrona_cadastro_view(request):
    """View para cadastrar nova poltrona"""
    if request.method == 'POST':
        form = PoltronaForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                poltrona = form.save()
                messages.success(request, f'Poltrona "{poltrona.ref_poltrona} - {poltrona.nome}" cadastrada com sucesso!')
                return redirect('poltrona_detalhes', poltrona_id=poltrona.id)
            except Exception as e:
                logger.error(f"Erro ao cadastrar poltrona: {str(e)}")
                messages.error(request, f'Erro ao cadastrar poltrona: {str(e)}')
        else:
            logger.warning(f"Formulário de poltrona inválido: {form.errors}")
    else:
        form = PoltronaForm()
    
    context = {
        'form': form,
    }
    return render(request, 'produtos/poltronas/cadastro.html', context)


def poltrona_detalhes_view(request, poltrona_id):
    """View para visualizar detalhes da poltrona"""
    poltrona = get_object_or_404(Poltrona, id=poltrona_id)
    
    context = {
        'poltrona': poltrona,
    }
    return render(request, 'produtos/poltronas/detalhes.html', context)


def poltrona_teste_imagem_view(request, poltrona_id):
    """View para testar imagem da poltrona"""
    poltrona = get_object_or_404(Poltrona, id=poltrona_id)
    return JsonResponse({
        'imagem_url': poltrona.imagem_principal.url if poltrona.imagem_principal else None
    })


def poltrona_editar_view(request, poltrona_id):
    """View para editar poltrona"""
    poltrona = get_object_or_404(Poltrona, id=poltrona_id)
    
    if request.method == 'POST':
        form = PoltronaForm(request.POST, request.FILES, instance=poltrona)
        if form.is_valid():
            try:
                poltrona = form.save()
                messages.success(request, f'Poltrona "{poltrona.ref_poltrona} - {poltrona.nome}" atualizado com sucesso!')
                return redirect('poltrona_detalhes', poltrona_id=poltrona.id)
            except Exception as e:
                logger.error(f"Erro ao editar poltrona: {str(e)}")
                messages.error(request, f'Erro ao editar poltrona: {str(e)}')
        else:
            logger.warning(f"Formulário de edição de poltrona inválido: {form.errors}")
    else:
        form = PoltronaForm(instance=poltrona)
    
    context = {
        'form': form,
        'poltrona': poltrona,
    }
    return render(request, 'produtos/poltronas/editar.html', context)


def poltrona_excluir_view(request, poltrona_id):
    """View para excluir poltronas"""
    poltrona = get_object_or_404(Poltrona, id=poltrona_id)
    
    if request.method == 'POST':
        try:
            nome_poltrona = f"{poltrona.ref_poltrona} - {poltrona.nome}"
            poltrona.delete()
            messages.success(request, f'Poltrona "{nome_poltrona}" excluída com sucesso!')
            return redirect('poltronas_lista')
        except Exception as e:
            logger.error(f"Erro ao excluir poltrona: {str(e)}")
            messages.error(request, f'Erro ao excluir poltrona: {str(e)}')
            return redirect('poltrona_detalhes', poltrona_id=poltrona.id)
    
    context = {
        'poltrona': poltrona,
    }
    return render(request, 'produtos/poltronas/confirmar_exclusao.html', context)

# =============================================================================
# VIEWS PARA PUFES
# =============================================================================

@produtos_access_required
def pufes_list_view(request):
    """View para listagem de pufes"""
    pufes = Pufe.objects.all().order_by('ref_pufe')
    
    context = {
        'pufes': pufes,
        'total_pufes': pufes.count(),
    }
    return render(request, 'produtos/pufes/lista.html', context)

@produtos_access_required
def pufe_cadastro_view(request):
    """View para cadastro de pufes"""
    if request.method == 'POST':
        form = PufeForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                pufe = form.save()
                track_user_changes(pufe, request.user)
                messages.success(request, f'Pufe "{pufe.ref_pufe} - {pufe.nome}" cadastrado com sucesso!')
                return redirect('pufe_detalhes', pufe_id=pufe.id)
            except Exception as e:
                logger.error(f"Erro ao cadastrar pufe: {str(e)}")
                messages.error(request, f'Erro ao cadastrar pufe: {str(e)}')
        else:
            logger.warning(f"Formulário de cadastro de pufe inválido: {form.errors}")
    else:
        form = PufeForm()
    
    context = {
        'form': form,
    }
    return render(request, 'produtos/pufes/cadastro.html', context)

@produtos_access_required
def pufe_detalhes_view(request, pufe_id):
    """View para detalhes de pufe"""
    pufe = get_object_or_404(Pufe, id=pufe_id)
    
    context = {
        'pufe': pufe,
    }
    return render(request, 'produtos/pufes/detalhes.html', context)

@produtos_access_required
def pufe_editar_view(request, pufe_id):
    """View para editar pufe"""
    pufe = get_object_or_404(Pufe, id=pufe_id)
    
    if request.method == 'POST':
        form = PufeForm(request.POST, request.FILES, instance=pufe)
        if form.is_valid():
            try:
                pufe = form.save()
                messages.success(request, f'Pufe "{pufe.ref_pufe} - {pufe.nome}" atualizado com sucesso!')
                return redirect('pufe_detalhes', pufe_id=pufe.id)
            except Exception as e:
                logger.error(f"Erro ao editar pufe: {str(e)}")
                messages.error(request, f'Erro ao editar pufe: {str(e)}')
        else:
            logger.warning(f"Formulário de edição de pufe inválido: {form.errors}")
    else:
        form = PufeForm(instance=pufe)
    
    context = {
        'form': form,
        'pufe': pufe,
    }
    return render(request, 'produtos/pufes/editar.html', context)

@produtos_access_required
def pufe_excluir_view(request, pufe_id):
    """View para excluir pufes"""
    pufe = get_object_or_404(Pufe, id=pufe_id)
    
    if request.method == 'POST':
        try:
            nome_pufe = f"{pufe.ref_pufe} - {pufe.nome}"
            pufe.delete()
            messages.success(request, f'Pufe "{nome_pufe}" excluído com sucesso!')
            return redirect('pufes_lista')
        except Exception as e:
            logger.error(f"Erro ao excluir pufe: {str(e)}")
            messages.error(request, f'Erro ao excluir pufe: {str(e)}')
            return redirect('pufe_detalhes', pufe_id=pufe.id)
    
    context = {
        'pufe': pufe,
    }
    return render(request, 'produtos/pufes/confirmar_exclusao.html', context)

@produtos_access_required
def pufe_teste_imagem_view(request, pufe_id):
    """View de teste para imagens de pufes"""
    pufe = get_object_or_404(Pufe, id=pufe_id)
    return render(request, 'produtos/pufes/teste_imagem.html', {'pufe': pufe})

# =====================================================================
# VIEWS PARA ALMOFADAS
# =====================================================================

@produtos_access_required
def almofadas_list_view(request):
    """View para listagem de almofadas"""
    almofadas = Almofada.objects.all().order_by('ref_almofada')
    
    context = {
        'almofadas': almofadas,
        'total_almofadas': almofadas.count(),
    }
    return render(request, 'produtos/almofadas/lista.html', context)

@produtos_access_required
def almofada_cadastro_view(request):
    """View para cadastro de almofadas"""
    if request.method == 'POST':
        form = AlmofadaForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                almofada = form.save()
                track_user_changes(almofada, request.user)
                messages.success(request, f'Almofada "{almofada.ref_almofada} - {almofada.nome}" cadastrada com sucesso!')
                return redirect('almofada_detalhes', almofada_id=almofada.id)
            except Exception as e:
                logger.error(f"Erro ao cadastrar almofada: {str(e)}")
                messages.error(request, f'Erro ao cadastrar almofada: {str(e)}')
        else:
            logger.warning(f"Formulário de cadastro de almofada inválido: {form.errors}")
    else:
        form = AlmofadaForm()
    
    context = {
        'form': form,
    }
    return render(request, 'produtos/almofadas/cadastro.html', context)

@produtos_access_required
def almofada_detalhes_view(request, almofada_id):
    """View para detalhes de almofada"""
    almofada = get_object_or_404(Almofada, id=almofada_id)
    
    context = {
        'almofada': almofada,
    }
    return render(request, 'produtos/almofadas/detalhes.html', context)

@produtos_access_required
def almofada_editar_view(request, almofada_id):
    """View para editar almofada"""
    almofada = get_object_or_404(Almofada, id=almofada_id)
    
    if request.method == 'POST':
        form = AlmofadaForm(request.POST, request.FILES, instance=almofada)
        if form.is_valid():
            try:
                almofada = form.save()
                messages.success(request, f'Almofada "{almofada.ref_almofada} - {almofada.nome}" atualizada com sucesso!')
                return redirect('almofada_detalhes', almofada_id=almofada.id)
            except Exception as e:
                logger.error(f"Erro ao editar almofada: {str(e)}")
                messages.error(request, f'Erro ao editar almofada: {str(e)}')
        else:
            logger.warning(f"Formulário de edição de almofada inválido: {form.errors}")
    else:
        form = AlmofadaForm(instance=almofada)
    
    context = {
        'form': form,
        'almofada': almofada,
    }
    return render(request, 'produtos/almofadas/editar.html', context)

@produtos_access_required
def almofada_excluir_view(request, almofada_id):
    """View para excluir almofadas"""
    almofada = get_object_or_404(Almofada, id=almofada_id)
    
    if request.method == 'POST':
        try:
            nome_almofada = f"{almofada.ref_almofada} - {almofada.nome}"
            almofada.delete()
            messages.success(request, f'Almofada "{nome_almofada}" excluída com sucesso!')
            return redirect('almofadas_lista')
        except Exception as e:
            logger.error(f"Erro ao excluir almofada: {str(e)}")
            messages.error(request, f'Erro ao excluir almofada: {str(e)}')
            return redirect('almofada_detalhes', almofada_id=almofada.id)
    
    context = {
        'almofada': almofada,
    }
    return render(request, 'produtos/almofadas/confirmar_exclusao.html', context)

@produtos_access_required
def almofada_teste_imagem_view(request, almofada_id):
    """View de teste para imagens de almofadas"""
    almofada = get_object_or_404(Almofada, id=almofada_id)
    return render(request, 'produtos/almofadas/teste_imagem.html', {'almofada': almofada})

# =====================================================================
# VIEWS PARA SOFÁS (ADEQUAÇÃO AO NOVO PADRÃO)
# =====================================================================

@produtos_access_required
def sofas_list_view(request):
    """View para listagem específica de sofás"""
    sofas = Produto.objects.filter(id_tipo_produto__nome__icontains='sofá').order_by('ref_produto')
    
    context = {
        'sofas': sofas,
        'total_sofas': sofas.count(),
    }
    return render(request, 'produtos/sofas/lista.html', context)

@produtos_access_required
def sofa_cadastro_view(request):
    """View para cadastro específico de sofás"""
    return redirect('produto_cadastro')  # Redireciona para o cadastro unificado por enquanto

@produtos_access_required
def sofa_detalhes_view(request, sofa_id):
    """View para detalhes específicos de sofás"""
    sofa = get_object_or_404(Produto, id=sofa_id, id_tipo_produto__nome__icontains='sofá')
    modulos = sofa.modulos.prefetch_related('tamanhos_detalhados').all()
    
    # Buscar acessórios vinculados a este sofá
    acessorios_vinculados = Acessorio.objects.filter(produtos_vinculados=sofa).order_by('ref_acessorio')
    
    context = {
        'sofa': sofa,
        'produto': sofa,  # Para compatibilidade com templates existentes
        'modulos': modulos,
        'acessorios_vinculados': acessorios_vinculados,
        'eh_sofa': True,
    }
    return render(request, 'produtos/sofas/detalhes.html', context)

@produtos_access_required
def sofa_editar_view(request, sofa_id):
    """View para edição específica de sofás"""
    sofa = get_object_or_404(Produto, id=sofa_id, id_tipo_produto__nome__icontains='sofá')
    modulos = sofa.modulos.all() if hasattr(sofa, 'modulos') else []
    
    # Buscar tamanhos detalhados de todos os módulos
    tamanhos_detalhados = []
    for modulo in modulos:
        tamanhos_detalhados.extend(modulo.tamanhos_detalhados.all())
    
    if request.method == 'POST':
        try:
            with transaction.atomic():
                # Atualizar dados básicos do produto
                sofa.ref_produto = request.POST.get('ref_produto')
                sofa.nome_produto = request.POST.get('nome_produto')
                sofa.id_tipo_produto_id = request.POST.get('tipo_produto')
                sofa.ativo = request.POST.get('ativo') == 'on'
                
                # Atualizar campos específicos de sofás
                sofa.tem_cor_tecido = request.POST.get('tem_cor_tecido') == 'on'
                sofa.tem_difer_desenho_lado_dir_esq = request.POST.get('tem_difer_desenho_lado') == 'on'
                sofa.tem_difer_desenho_tamanho = request.POST.get('tem_difer_desenho_tamanho') == 'on'
                
                # Atualizar imagens se fornecidas
                if 'imagem_principal' in request.FILES:
                    sofa.imagem_principal = request.FILES['imagem_principal']
                if 'imagem_secundaria' in request.FILES:
                    sofa.imagem_secundaria = request.FILES['imagem_secundaria']
                
                track_user_changes(sofa, request.user)
                sofa.save()
                
                # Processar módulos (se houver)
                modulos_nomes = request.POST.getlist('modulo_nome')
                if modulos_nomes:
                    # Remover módulos existentes para recriar
                    sofa.modulos.all().delete()
                    
                    for i, nome_modulo in enumerate(modulos_nomes):
                        if nome_modulo.strip():  # Se o nome do módulo não estiver vazio
                            # Obter dados do módulo
                            profundidade = request.POST.get(f'modulo_profundidade_{i+1}')
                            altura = request.POST.get(f'modulo_altura_{i+1}')
                            braco = request.POST.get(f'modulo_braco_{i+1}')
                            descricao = request.POST.get(f'modulo_descricao_{i+1}')
                            
                            modulo = Modulo(
                                produto=sofa,
                                nome=nome_modulo,
                                profundidade=float(profundidade) if profundidade else None,
                                altura=float(altura) if altura else None,
                                braco=float(braco) if braco else None,
                                descricao=descricao if descricao else None,
                                imagem_principal=request.FILES.get(f'modulo_imagem_principal_{i+1}')
                            )
                            track_user_changes(modulo, request.user)
                            modulo.save()
                
                messages.success(request, f'Sofá "{sofa.ref_produto} - {sofa.nome_produto}" atualizado com sucesso!')
                return redirect('sofa_detalhes', sofa_id=sofa.id)
        except Exception as e:
            logger.error(f"Erro ao editar sofá: {str(e)}")
            messages.error(request, f'Erro ao editar sofá: {str(e)}')
    
    context = {
        'sofa': sofa,
        'produto': sofa,  # Para compatibilidade com templates
        'modulos': modulos,
        'tamanhos_detalhados': tamanhos_detalhados,
        'tipos': TipoItem.objects.all(),
        'eh_edicao': True,
        'produto_id': sofa.id
    }
    return render(request, 'produtos/sofas/editar.html', context)

@produtos_access_required
def sofa_excluir_view(request, sofa_id):
    """View para exclusão específica de sofás"""
    sofa = get_object_or_404(Produto, id=sofa_id, id_tipo_produto__nome__icontains='sofá')
    
    if request.method == 'POST':
        try:
            nome_sofa = f"{sofa.ref_produto} - {sofa.nome_produto}"
            sofa.delete()
            messages.success(request, f'Sofá "{nome_sofa}" excluído com sucesso!')
            return redirect('sofas_lista')
        except Exception as e:
            logger.error(f"Erro ao excluir sofá: {str(e)}")
            messages.error(request, f'Erro ao excluir sofá: {str(e)}')
            return redirect('sofa_detalhes', sofa_id=sofa.id)
    
    context = {
        'sofa': sofa,
    }
    return render(request, 'produtos/sofas/confirmar_exclusao.html', context)
