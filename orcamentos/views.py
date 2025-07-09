from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse
from django.core.paginator import Paginator
from django.db.models import Q
from django.utils import timezone
from datetime import timedelta
from decimal import Decimal
import json

from authentication.decorators import orcamentos_access_required
from .models import Orcamento, OrcamentoItem, FaixaPreco, FormaPagamento
from .forms import OrcamentoForm, OrcamentoItemForm, BuscaClienteForm
from clientes.models import Cliente
from produtos.models import Produto


@login_required
@orcamentos_access_required
def listar_orcamentos(request):
    """Lista todos os orçamentos"""
    orcamentos = Orcamento.objects.select_related(
        'cliente', 'vendedor', 'faixa_preco', 'forma_pagamento'
    ).order_by('-created_at')
    
    # Filtros
    busca = request.GET.get('busca', '')
    status = request.GET.get('status', '')
    
    if busca:
        orcamentos = orcamentos.filter(
            Q(numero__icontains=busca) |
            Q(cliente__nome_empresa__icontains=busca) |
            Q(cliente__representante__icontains=busca) |
            Q(vendedor__first_name__icontains=busca) |
            Q(vendedor__last_name__icontains=busca)
        )
    
    if status:
        orcamentos = orcamentos.filter(status=status)
    
    # Paginação
    paginator = Paginator(orcamentos, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'busca': busca,
        'status': status,
        'status_choices': Orcamento.STATUS_CHOICES,
    }
    
    return render(request, 'orcamentos/listar.html', context)


@login_required
@orcamentos_access_required
def novo_orcamento(request):
    """Cria um novo orçamento"""
    if request.method == 'POST':
        form = OrcamentoForm(request.POST)
        if form.is_valid():
            orcamento = form.save(commit=False)
            orcamento.vendedor = request.user
            orcamento.save()
            messages.success(request, 'Orçamento criado com sucesso!')
            return redirect('orcamentos:editar', pk=orcamento.pk)
    else:
        # Criar dados iniciais explícitos
        data_entrega = timezone.now().date() + timedelta(days=30)
        data_validade = timezone.now().date() + timedelta(days=15)
        
        inicial_data = {
            'data_entrega': data_entrega,
            'data_validade': data_validade,
            'status': 'rascunho'
        }
        
        form = OrcamentoForm(initial=inicial_data)
    
    context = {
        'form': form,
        'titulo': 'Novo Orçamento',
    }
    
    return render(request, 'orcamentos/form.html', context)


@login_required
@orcamentos_access_required
def editar_orcamento(request, pk):
    """Edita um orçamento existente"""
    orcamento = get_object_or_404(Orcamento, pk=pk)
    
    if request.method == 'POST':
        form = OrcamentoForm(request.POST, instance=orcamento)
        if form.is_valid():
            form.save()
            messages.success(request, 'Orçamento atualizado com sucesso!')
            return redirect('orcamentos:editar', pk=orcamento.pk)
    else:
        form = OrcamentoForm(instance=orcamento)
    
    # Buscar itens do orçamento
    itens = orcamento.itens.select_related('produto').all()
    
    context = {
        'form': form,
        'orcamento': orcamento,
        'itens': itens,
        'titulo': f'Editar Orçamento {orcamento.numero}',
    }
    
    return render(request, 'orcamentos/form.html', context)


@login_required
@orcamentos_access_required
def visualizar_orcamento(request, pk):
    """Visualiza detalhes de um orçamento"""
    orcamento = get_object_or_404(
        Orcamento.objects.select_related(
            'cliente', 'vendedor', 'faixa_preco', 'forma_pagamento'
        ).prefetch_related('itens__produto'), 
        pk=pk
    )
    
    context = {
        'orcamento': orcamento,
    }
    
    return render(request, 'orcamentos/visualizar.html', context)


@login_required
@orcamentos_access_required
def excluir_orcamento(request, pk):
    """Exclui um orçamento"""
    orcamento = get_object_or_404(Orcamento, pk=pk)
    
    if request.method == 'POST':
        orcamento.delete()
        messages.success(request, 'Orçamento excluído com sucesso!')
        return redirect('orcamentos:listar')
    
    context = {
        'orcamento': orcamento,
    }
    
    return render(request, 'orcamentos/confirmar_exclusao.html', context)


@login_required
@orcamentos_access_required
def buscar_cliente(request):
    """Busca clientes via AJAX"""
    termo = request.GET.get('termo', '')
    iniciais = request.GET.get('iniciais', '')
    
    # Se for solicitação de clientes iniciais
    if iniciais:
        try:
            limite = int(iniciais)
            clientes = Cliente.objects.all().order_by('nome_empresa')[:limite]
            clientes_data = clientes.values('id', 'nome_empresa', 'representante', 'cnpj')
            return JsonResponse({'clientes': list(clientes_data)})
        except ValueError:
            return JsonResponse({'clientes': []})
    
    # Busca normal por termo
    if len(termo) < 2:
        return JsonResponse({'clientes': []})
    
    clientes = Cliente.objects.filter(
        Q(nome_empresa__icontains=termo) |
        Q(representante__icontains=termo) |
        Q(cnpj__icontains=termo)
    ).values('id', 'nome_empresa', 'representante', 'cnpj')[:10]
    
    return JsonResponse({'clientes': list(clientes)})


@login_required
@orcamentos_access_required
def buscar_produto(request):
    """Busca produtos via AJAX"""
    termo = request.GET.get('termo', '')
    
    if len(termo) < 2:
        return JsonResponse({'produtos': []})
    
    produtos = Produto.objects.filter(
        Q(nome_produto__icontains=termo) |
        Q(ref_produto__icontains=termo),
        ativo=True
    ).select_related('id_tipo_produto').values(
        'id', 'nome_produto', 'ref_produto', 'id_tipo_produto__nome'
    )[:10]
    
    return JsonResponse({'produtos': list(produtos)})


@login_required
@orcamentos_access_required
def adicionar_item(request, orcamento_pk):
    """Adiciona item ao orçamento via AJAX"""
    orcamento = get_object_or_404(Orcamento, pk=orcamento_pk)
    
    if request.method == 'POST':
        data = json.loads(request.body)
        
        try:
            produto = Produto.objects.get(pk=data['produto_id'])
            quantidade = int(data.get('quantidade', 1))
            preco_unitario = Decimal(data.get('preco_unitario', '0'))
            observacoes = data.get('observacoes', '')
            
            # Criar item
            item = OrcamentoItem.objects.create(
                orcamento=orcamento,
                produto=produto,
                quantidade=quantidade,
                preco_unitario=preco_unitario,
                observacoes=observacoes
            )
            
            return JsonResponse({
                'success': True,
                'item_id': item.id,
                'message': 'Item adicionado com sucesso!'
            })
            
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': f'Erro ao adicionar item: {str(e)}'
            })
    
    return JsonResponse({'success': False, 'message': 'Método não permitido'})


@login_required
@orcamentos_access_required
def remover_item(request, orcamento_pk, item_pk):
    """Remove item do orçamento"""
    orcamento = get_object_or_404(Orcamento, pk=orcamento_pk)
    item = get_object_or_404(OrcamentoItem, pk=item_pk, orcamento=orcamento)
    
    if request.method == 'POST':
        item.delete()
        return JsonResponse({
            'success': True,
            'message': 'Item removido com sucesso!'
        })
    
    return JsonResponse({'success': False, 'message': 'Método não permitido'})


@login_required
@orcamentos_access_required
def atualizar_item(request, orcamento_pk, item_pk):
    """Atualiza item do orçamento via AJAX"""
    orcamento = get_object_or_404(Orcamento, pk=orcamento_pk)
    item = get_object_or_404(OrcamentoItem, pk=item_pk, orcamento=orcamento)
    
    if request.method == 'POST':
        data = json.loads(request.body)
        
        try:
            item.quantidade = int(data.get('quantidade', item.quantidade))
            item.preco_unitario = Decimal(data.get('preco_unitario', item.preco_unitario))
            item.observacoes = data.get('observacoes', item.observacoes)
            item.save()
            
            return JsonResponse({
                'success': True,
                'message': 'Item atualizado com sucesso!'
            })
            
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': f'Erro ao atualizar item: {str(e)}'
            })
    
    return JsonResponse({'success': False, 'message': 'Método não permitido'})


@login_required
@orcamentos_access_required
def gerar_pdf(request, pk):
    """Gera PDF do orçamento"""
    orcamento = get_object_or_404(
        Orcamento.objects.select_related(
            'cliente', 'vendedor', 'faixa_preco', 'forma_pagamento'
        ).prefetch_related('itens__produto'), 
        pk=pk
    )
    
    # Por enquanto, renderizar template HTML
    # TODO: Implementar geração de PDF real
    context = {
        'orcamento': orcamento,
        'is_pdf': True,
    }
    
    return render(request, 'orcamentos/pdf.html', context)


@login_required
@orcamentos_access_required
def duplicar_orcamento(request, pk):
    """Duplica um orçamento existente"""
    orcamento_original = get_object_or_404(Orcamento, pk=pk)
    
    if request.method == 'POST':
        # Criar novo orçamento
        novo_orcamento = Orcamento.objects.create(
            cliente=orcamento_original.cliente,
            vendedor=request.user,
            faixa_preco=orcamento_original.faixa_preco,
            forma_pagamento=orcamento_original.forma_pagamento,
            desconto_valor=orcamento_original.desconto_valor,
            desconto_percentual=orcamento_original.desconto_percentual,
            acrescimo_valor=orcamento_original.acrescimo_valor,
            acrescimo_percentual=orcamento_original.acrescimo_percentual,
            data_entrega=timezone.now().date() + timedelta(days=30),
            data_validade=timezone.now().date() + timedelta(days=15),
            observacoes=orcamento_original.observacoes
        )
        
        # Duplicar itens
        for item in orcamento_original.itens.all():
            OrcamentoItem.objects.create(
                orcamento=novo_orcamento,
                produto=item.produto,
                quantidade=item.quantidade,
                preco_unitario=item.preco_unitario,
                observacoes=item.observacoes,
                dados_produto=item.dados_produto
            )
        
        messages.success(request, f'Orçamento duplicado com sucesso! Novo número: {novo_orcamento.numero}')
        return redirect('orcamentos:editar', pk=novo_orcamento.pk)
    
    context = {
        'orcamento': orcamento_original,
    }
    
    return render(request, 'orcamentos/confirmar_duplicacao.html', context)


@login_required
@orcamentos_access_required
def calcular_totais(request, pk):
    """Calcula totais do orçamento via AJAX"""
    orcamento = get_object_or_404(Orcamento, pk=pk)
    
    totais = {
        'subtotal': float(orcamento.get_subtotal()),
        'desconto': float(orcamento.get_total_desconto()),
        'acrescimo': float(orcamento.get_total_acrescimo()),
        'total_final': float(orcamento.get_total_final()),
        'peso_total': float(orcamento.get_peso_total()),
        'cubagem_total': float(orcamento.get_cubagem_total()),
    }
    
    return JsonResponse(totais)


@login_required
@orcamentos_access_required
def catalogo_produtos(request):
    """Retorna catálogo completo de produtos para seleção no orçamento"""
    from produtos.models import Banqueta, Cadeira, Poltrona, Pufe, Almofada, Acessorio
    
    tipo_filtro = request.GET.get('tipo', '')
    busca = request.GET.get('busca', '')
    pagina = int(request.GET.get('pagina', 1))
    por_pagina = 12
    
    produtos_lista = []
    
    # Se não há filtro específico, buscar todos os tipos
    if not tipo_filtro or tipo_filtro == 'sofa':
        # Sofás (produtos principais)
        sofas = Produto.objects.filter(ativo=True).select_related('id_tipo_produto')
        if busca:
            sofas = sofas.filter(
                Q(nome_produto__icontains=busca) |
                Q(ref_produto__icontains=busca)
            )
        
        for sofa in sofas:
            produtos_lista.append({
                'id': sofa.id,
                'tipo': 'sofa',
                'referencia': sofa.ref_produto,
                'nome': sofa.nome_produto,
                'tipo_nome': sofa.id_tipo_produto.nome if sofa.id_tipo_produto else 'Sofá',
                'preco': '0.00',  # Preço será calculado pelos módulos
                'imagem': sofa.imagem_principal.url if sofa.imagem_principal else None,
                'tem_modulos': True
            })
    
    if not tipo_filtro or tipo_filtro == 'banqueta':
        # Banquetas
        banquetas = Banqueta.objects.filter(ativo=True)
        if busca:
            banquetas = banquetas.filter(
                Q(nome__icontains=busca) |
                Q(ref_banqueta__icontains=busca)
            )
        
        for banqueta in banquetas:
            produtos_lista.append({
                'id': banqueta.id,
                'tipo': 'banqueta',
                'referencia': banqueta.ref_banqueta,
                'nome': banqueta.nome,
                'tipo_nome': 'Banqueta',
                'preco': str(banqueta.preco),
                'dimensoes': f"{banqueta.largura}x{banqueta.profundidade}x{banqueta.altura}cm",
                'imagem': banqueta.imagem_principal.url if banqueta.imagem_principal else None,
                'tem_modulos': False
            })
    
    if not tipo_filtro or tipo_filtro == 'cadeira':
        # Cadeiras
        cadeiras = Cadeira.objects.filter(ativo=True)
        if busca:
            cadeiras = cadeiras.filter(
                Q(nome__icontains=busca) |
                Q(ref_cadeira__icontains=busca)
            )
        
        for cadeira in cadeiras:
            produtos_lista.append({
                'id': cadeira.id,
                'tipo': 'cadeira',
                'referencia': cadeira.ref_cadeira,
                'nome': cadeira.nome,
                'tipo_nome': 'Cadeira',
                'preco': str(cadeira.preco),
                'dimensoes': f"{cadeira.largura}x{cadeira.profundidade}x{cadeira.altura}cm",
                'imagem': cadeira.imagem_principal.url if cadeira.imagem_principal else None,
                'tem_modulos': False
            })
    
    if not tipo_filtro or tipo_filtro == 'poltrona':
        # Poltronas
        poltronas = Poltrona.objects.filter(ativo=True)
        if busca:
            poltronas = poltronas.filter(
                Q(nome__icontains=busca) |
                Q(ref_poltrona__icontains=busca)
            )
        
        for poltrona in poltronas:
            produtos_lista.append({
                'id': poltrona.id,
                'tipo': 'poltrona',
                'referencia': poltrona.ref_poltrona,
                'nome': poltrona.nome,
                'tipo_nome': 'Poltrona',
                'preco': str(poltrona.preco),
                'dimensoes': f"{poltrona.largura}x{poltrona.profundidade}x{poltrona.altura}cm",
                'imagem': poltrona.imagem_principal.url if poltrona.imagem_principal else None,
                'tem_modulos': False
            })
    
    if not tipo_filtro or tipo_filtro == 'pufe':
        # Pufes
        pufes = Pufe.objects.filter(ativo=True)
        if busca:
            pufes = pufes.filter(
                Q(nome__icontains=busca) |
                Q(ref_pufe__icontains=busca)
            )
        
        for pufe in pufes:
            produtos_lista.append({
                'id': pufe.id,
                'tipo': 'pufe',
                'referencia': pufe.ref_pufe,
                'nome': pufe.nome,
                'tipo_nome': 'Pufe',
                'preco': str(pufe.preco),
                'dimensoes': f"{pufe.largura}x{pufe.profundidade}x{pufe.altura}cm",
                'imagem': pufe.imagem_principal.url if pufe.imagem_principal else None,
                'tem_modulos': False
            })
    
    if not tipo_filtro or tipo_filtro == 'almofada':
        # Almofadas
        almofadas = Almofada.objects.filter(ativo=True)
        if busca:
            almofadas = almofadas.filter(
                Q(nome__icontains=busca) |
                Q(ref_almofada__icontains=busca)
            )
        
        for almofada in almofadas:
            produtos_lista.append({
                'id': almofada.id,
                'tipo': 'almofada',
                'referencia': almofada.ref_almofada,
                'nome': almofada.nome,
                'tipo_nome': 'Almofada',
                'preco': str(almofada.preco),
                'dimensoes': f"{almofada.largura}x{almofada.altura}cm",
                'imagem': almofada.imagem_principal.url if almofada.imagem_principal else None,
                'tem_modulos': False
            })
    
    if not tipo_filtro or tipo_filtro == 'acessorio':
        # Acessórios
        acessorios = Acessorio.objects.filter(ativo=True)
        if busca:
            acessorios = acessorios.filter(
                Q(nome__icontains=busca) |
                Q(ref_acessorio__icontains=busca)
            )
        
        for acessorio in acessorios:
            produtos_lista.append({
                'id': acessorio.id,
                'tipo': 'acessorio',
                'referencia': acessorio.ref_acessorio,
                'nome': acessorio.nome,
                'tipo_nome': 'Acessório',
                'preco': str(acessorio.preco),
                'imagem': acessorio.imagem_principal.url if acessorio.imagem_principal else None,
                'tem_modulos': False
            })
    
    # Paginação
    total_produtos = len(produtos_lista)
    inicio = (pagina - 1) * por_pagina
    fim = inicio + por_pagina
    produtos_pagina = produtos_lista[inicio:fim]
    
    total_paginas = (total_produtos + por_pagina - 1) // por_pagina
    
    return JsonResponse({
        'produtos': produtos_pagina,
        'paginacao': {
            'pagina_atual': pagina,
            'total_paginas': total_paginas,
            'total_produtos': total_produtos,
            'por_pagina': por_pagina
        }
    })


@login_required
@orcamentos_access_required  
def produtos_por_tipo(request):
    """Retorna produtos filtrados por tipo via AJAX"""
    tipo = request.GET.get('tipo', '')
    
    if not tipo:
        return JsonResponse({'produtos': []})
    
    try:
        produtos_com_preco = []
        
        # Buscar produtos específicos baseado no tipo
        if tipo == 'sofa':
            # Buscar na tabela Produto para sofás
            from produtos.models import TipoItem
            tipo_sofa = TipoItem.objects.filter(nome__icontains='Sofá').first()
            
            if tipo_sofa:
                produtos = Produto.objects.filter(
                    id_tipo_produto=tipo_sofa,
                    ativo=True
                ).select_related('id_tipo_produto').order_by('nome_produto')[:50]
                
                for produto in produtos:
                    # Sofás não têm campo preço direto, preço vem dos módulos
                    preco_produto = 0.00
                    
                    produtos_com_preco.append({
                        'id': f'produto_{produto.id}',
                        'nome_produto': produto.nome_produto,
                        'ref_produto': produto.ref_produto,
                        'tipo': 'Sofá',
                        'preco': preco_produto,  # Preço será calculado pelos módulos
                        'tem_modulos': True,
                        'descricao': 'Preço varia conforme módulos selecionados'
                    })
        
        elif tipo == 'cadeira':
            # Buscar na tabela Cadeira
            from produtos.models import Cadeira
            cadeiras = Cadeira.objects.filter(ativo=True).order_by('nome')[:50]
            
            for cadeira in cadeiras:
                produtos_com_preco.append({
                    'id': f'cadeira_{cadeira.id}',
                    'nome_produto': cadeira.nome,
                    'ref_produto': cadeira.ref_cadeira,
                    'tipo': 'Cadeira',
                    'preco': float(cadeira.preco) if cadeira.preco else 0.00,
                    'tem_modulos': False
                })
        
        elif tipo == 'banqueta':
            # Buscar na tabela Banqueta
            from produtos.models import Banqueta
            banquetas = Banqueta.objects.filter(ativo=True).order_by('nome')[:50]
            
            for banqueta in banquetas:
                produtos_com_preco.append({
                    'id': f'banqueta_{banqueta.id}',
                    'nome_produto': banqueta.nome,
                    'ref_produto': banqueta.ref_banqueta,
                    'tipo': 'Banqueta',
                    'preco': float(banqueta.preco) if banqueta.preco else 0.00,
                    'tem_modulos': False
                })
        
        elif tipo == 'poltrona':
            # Buscar na tabela Poltrona
            from produtos.models import Poltrona
            poltronas = Poltrona.objects.filter(ativo=True).order_by('nome')[:50]
            
            for poltrona in poltronas:
                produtos_com_preco.append({
                    'id': f'poltrona_{poltrona.id}',
                    'nome_produto': poltrona.nome,
                    'ref_produto': poltrona.ref_poltrona,
                    'tipo': 'Poltrona',
                    'preco': float(poltrona.preco) if poltrona.preco else 0.00,
                    'tem_modulos': False
                })
        
        elif tipo == 'pufe':
            # Buscar na tabela Pufe
            from produtos.models import Pufe
            pufes = Pufe.objects.filter(ativo=True).order_by('nome')[:50]
            
            for pufe in pufes:
                produtos_com_preco.append({
                    'id': f'pufe_{pufe.id}',
                    'nome_produto': pufe.nome,
                    'ref_produto': pufe.ref_pufe,
                    'tipo': 'Pufe',
                    'preco': float(pufe.preco) if pufe.preco else 0.00,
                    'tem_modulos': False
                })
        
        elif tipo == 'almofada':
            # Buscar na tabela Almofada
            from produtos.models import Almofada
            almofadas = Almofada.objects.filter(ativo=True).order_by('nome')[:50]
            
            for almofada in almofadas:
                produtos_com_preco.append({
                    'id': f'almofada_{almofada.id}',
                    'nome_produto': almofada.nome,
                    'ref_produto': almofada.ref_almofada,
                    'tipo': 'Almofada',
                    'preco': float(almofada.preco) if almofada.preco else 0.00,
                    'tem_modulos': False
                })
        
        elif tipo == 'acessorio':
            # Buscar acessórios na tabela Acessorio
            from produtos.models import Acessorio
            acessorios = Acessorio.objects.filter(ativo=True).order_by('nome')[:50]
            
            for acessorio in acessorios:
                produtos_com_preco.append({
                    'id': f'acessorio_{acessorio.id}',
                    'nome_produto': acessorio.nome,
                    'ref_produto': acessorio.ref_acessorio,
                    'tipo': 'Acessório',
                    'preco': float(acessorio.preco) if acessorio.preco else 0.00,
                    'tem_modulos': False
                })
        
        return JsonResponse({'produtos': produtos_com_preco})
        
    except Exception as e:
        return JsonResponse({'erro': str(e)}, status=500)


@login_required
@orcamentos_access_required
def buscar_produtos_por_tipo(request):
    """Busca produtos filtrados por tipo com busca dinâmica"""
    tipo = request.GET.get('tipo', '')
    busca = request.GET.get('busca', '')
    
    if not tipo:
        return JsonResponse({'produtos': []})
        
    produtos_com_preco = []
    
    try:
        if tipo == 'cadeira':
            # Buscar na tabela Cadeira
            from produtos.models import Cadeira
            cadeiras = Cadeira.objects.filter(ativo=True).order_by('nome')
            
            # Filtrar por busca se fornecida
            if busca:
                cadeiras = cadeiras.filter(
                    Q(nome__icontains=busca) | Q(ref_cadeira__icontains=busca)
                )
            
            # Limitar resultados
            cadeiras = cadeiras[:20]
            
            for cadeira in cadeiras:
                produtos_com_preco.append({
                    'id': f'cadeira_{cadeira.id}',
                    'nome_produto': cadeira.nome,
                    'ref_produto': cadeira.ref_cadeira,
                    'tipo': 'Cadeira',
                    'preco': float(cadeira.preco) if cadeira.preco else 0.00,
                    'tem_modulos': False,
                    'display_name': f"{cadeira.nome} - {cadeira.ref_cadeira}"
                })
        
        elif tipo == 'banqueta':
            # Buscar na tabela Banqueta
            from produtos.models import Banqueta
            banquetas = Banqueta.objects.filter(ativo=True).order_by('nome')
            
            if busca:
                banquetas = banquetas.filter(
                    Q(nome__icontains=busca) | Q(ref_banqueta__icontains=busca)
                )
            
            banquetas = banquetas[:20]
            
            for banqueta in banquetas:
                produtos_com_preco.append({
                    'id': f'banqueta_{banqueta.id}',
                    'nome_produto': banqueta.nome,
                    'ref_produto': banqueta.ref_banqueta,
                    'tipo': 'Banqueta',
                    'preco': float(banqueta.preco) if banqueta.preco else 0.00,
                    'tem_modulos': False,
                    'display_name': f"{banqueta.nome} - {banqueta.ref_banqueta}"
                })
        
        elif tipo == 'poltrona':
            # Buscar na tabela Poltrona
            from produtos.models import Poltrona
            poltronas = Poltrona.objects.filter(ativo=True).order_by('nome')
            
            if busca:
                poltronas = poltronas.filter(
                    Q(nome__icontains=busca) | Q(ref_poltrona__icontains=busca)
                )
            
            poltronas = poltronas[:20]
            
            for poltrona in poltronas:
                produtos_com_preco.append({
                    'id': f'poltrona_{poltrona.id}',
                    'nome_produto': poltrona.nome,
                    'ref_produto': poltrona.ref_poltrona,
                    'tipo': 'Poltrona',
                    'preco': float(poltrona.preco) if poltrona.preco else 0.00,
                    'tem_modulos': False,
                    'display_name': f"{poltrona.nome} - {poltrona.ref_poltrona}"
                })
        
        elif tipo == 'pufe':
            # Buscar na tabela Pufe
            from produtos.models import Pufe
            pufes = Pufe.objects.filter(ativo=True).order_by('nome')
            
            if busca:
                pufes = pufes.filter(
                    Q(nome__icontains=busca) | Q(ref_pufe__icontains=busca)
                )
            
            pufes = pufes[:20]
            
            for pufe in pufes:
                produtos_com_preco.append({
                    'id': f'pufe_{pufe.id}',
                    'nome_produto': pufe.nome,
                    'ref_produto': pufe.ref_pufe,
                    'tipo': 'Pufe',
                    'preco': float(pufe.preco) if pufe.preco else 0.00,
                    'tem_modulos': False,
                    'display_name': f"{pufe.nome} - {pufe.ref_pufe}"
                })
        
        elif tipo == 'almofada':
            # Buscar na tabela Almofada
            from produtos.models import Almofada
            almofadas = Almofada.objects.filter(ativo=True).order_by('nome')
            
            if busca:
                almofadas = almofadas.filter(
                    Q(nome__icontains=busca) | Q(ref_almofada__icontains=busca)
                )
            
            almofadas = almofadas[:20]
            
            for almofada in almofadas:
                produtos_com_preco.append({
                    'id': f'almofada_{almofada.id}',
                    'nome_produto': almofada.nome,
                    'ref_produto': almofada.ref_almofada,
                    'tipo': 'Almofada',
                    'preco': float(almofada.preco) if almofada.preco else 0.00,
                    'tem_modulos': False,
                    'display_name': f"{almofada.nome} - {almofada.ref_almofada}"
                })
        
        # Deixar sofás e acessórios de lado conforme solicitado
        elif tipo in ['sofa', 'acessorio']:
            # Retornar lista vazia para tipos não implementados nesta melhoria
            produtos_com_preco = []
        
        return JsonResponse({'produtos': produtos_com_preco})
        
    except Exception as e:
        return JsonResponse({'erro': str(e)}, status=500)


@login_required
@orcamentos_access_required
def obter_detalhes_produto(request):
    """Retorna detalhes específicos de um produto para o modal"""
    produto_id = request.GET.get('produto_id', '')
    
    if not produto_id:
        return JsonResponse({'erro': 'ID do produto não fornecido'}, status=400)
    
    try:
        # Extrair tipo e ID do produto
        if produto_id.startswith('produto_'):
            # Sofá
            produto_real_id = produto_id.replace('produto_', '')
            produto = Produto.objects.get(id=produto_real_id)
            
            # Buscar módulos disponíveis para o sofá
            modulos = []
            for modulo in produto.modulos.filter(ativo=True):
                # Buscar tamanhos detalhados do módulo
                tamanhos = []
                for tamanho in modulo.tamanhos_detalhados.all():
                    tamanhos.append({
                        'id': tamanho.id,
                        'largura_total': float(tamanho.largura_total) if tamanho.largura_total else 0,
                        'largura_assento': float(tamanho.largura_assento) if tamanho.largura_assento else 0,
                        'preco': float(tamanho.preco) if tamanho.preco else 0.00,
                        'descricao': tamanho.descricao or ''
                    })
                
                modulos.append({
                    'id': modulo.id,
                    'nome': modulo.nome,
                    'descricao': modulo.descricao or '',
                    'tamanhos': tamanhos
                })
            
            return JsonResponse({
                'produto': {
                    'id': produto.id,
                    'nome': produto.nome_produto,
                    'ref': produto.ref_produto,
                    'tipo': 'Sofá',
                    'preco_base': 0.00,
                    'tem_modulos': True,
                    'modulos': modulos,
                    'descricao': 'Selecione os módulos para calcular o preço total'
                }
            })
            
        elif produto_id.startswith('cadeira_'):
            # Cadeira
            from produtos.models import Cadeira
            cadeira_id = produto_id.replace('cadeira_', '')
            cadeira = Cadeira.objects.get(id=cadeira_id)
            
            return JsonResponse({
                'produto': {
                    'id': produto_id,
                    'nome': cadeira.nome,
                    'ref': cadeira.ref_cadeira,
                    'tipo': 'Cadeira',
                    'preco': float(cadeira.preco) if cadeira.preco else 0.00,
                    'tem_modulos': False,
                    'descricao': f'Cadeira {cadeira.nome} - Preço: R$ {cadeira.preco:.2f}'
                }
            })
            
        elif produto_id.startswith('banqueta_'):
            # Banqueta
            from produtos.models import Banqueta
            banqueta_id = produto_id.replace('banqueta_', '')
            banqueta = Banqueta.objects.get(id=banqueta_id)
            
            return JsonResponse({
                'produto': {
                    'id': produto_id,
                    'nome': banqueta.nome,
                    'ref': banqueta.ref_banqueta,
                    'tipo': 'Banqueta',
                    'preco': float(banqueta.preco) if banqueta.preco else 0.00,
                    'tem_modulos': False,
                    'descricao': f'Banqueta {banqueta.nome} - Preço: R$ {banqueta.preco:.2f}'
                }
            })
            
        elif produto_id.startswith('poltrona_'):
            # Poltrona
            from produtos.models import Poltrona
            poltrona_id = produto_id.replace('poltrona_', '')
            poltrona = Poltrona.objects.get(id=poltrona_id)
            
            return JsonResponse({
                'produto': {
                    'id': produto_id,
                    'nome': poltrona.nome,
                    'ref': poltrona.ref_poltrona,
                    'tipo': 'Poltrona',
                    'preco': float(poltrona.preco) if poltrona.preco else 0.00,
                    'tem_modulos': False,
                    'descricao': f'Poltrona {poltrona.nome} - Preço: R$ {poltrona.preco:.2f}'
                }
            })
            
        elif produto_id.startswith('pufe_'):
            # Pufe
            from produtos.models import Pufe
            pufe_id = produto_id.replace('pufe_', '')
            pufe = Pufe.objects.get(id=pufe_id)
            
            return JsonResponse({
                'produto': {
                    'id': produto_id,
                    'nome': pufe.nome,
                    'ref': pufe.ref_pufe,
                    'tipo': 'Pufe',
                    'preco': float(pufe.preco) if pufe.preco else 0.00,
                    'tem_modulos': False,
                    'descricao': f'Pufe {pufe.nome} - Preço: R$ {pufe.preco:.2f}'
                }
            })
            
        elif produto_id.startswith('almofada_'):
            # Almofada
            from produtos.models import Almofada
            almofada_id = produto_id.replace('almofada_', '')
            almofada = Almofada.objects.get(id=almofada_id)
            
            return JsonResponse({
                'produto': {
                    'id': produto_id,
                    'nome': almofada.nome,
                    'ref': almofada.ref_almofada,
                    'tipo': 'Almofada',
                    'preco': float(almofada.preco) if almofada.preco else 0.00,
                    'tem_modulos': False,
                    'descricao': f'Almofada {almofada.nome} - Preço: R$ {almofada.preco:.2f}'
                }
            })
        
        else:
            return JsonResponse({'erro': 'Tipo de produto não reconhecido'}, status=400)
            
    except Exception as e:
        return JsonResponse({'erro': str(e)}, status=500)


@login_required
@orcamentos_access_required
def obter_informacoes_produto(request):
    """Retorna informações básicas de um produto para preview (nome, foto, dimensões)"""
    try:
        produto_id = request.GET.get('produto_id')
        if not produto_id:
            return JsonResponse({'erro': 'ID do produto não fornecido'}, status=400)
        
        # Determinar tipo e buscar produto
        if produto_id.startswith('sofa_'):
            # Sofá
            from produtos.models import Produto
            sofa_id = produto_id.replace('sofa_', '')
            sofa = Produto.objects.get(id=sofa_id)
            
            # Para sofás, não temos dimensões fixas pois dependem dos módulos
            return JsonResponse({
                'produto': {
                    'nome': sofa.nome_produto,
                    'foto': sofa.imagem_principal.url if sofa.imagem_principal else None,
                    'dimensoes': 'Varia conforme módulos selecionados',
                    'tipo': 'Sofá'
                }
            })
            
        elif produto_id.startswith('banqueta_'):
            # Banqueta
            from produtos.models import Banqueta
            banqueta_id = produto_id.replace('banqueta_', '')
            banqueta = Banqueta.objects.get(id=banqueta_id)
            
            return JsonResponse({
                'produto': {
                    'nome': banqueta.nome,
                    'foto': banqueta.imagem_principal.url if banqueta.imagem_principal else None,
                    'dimensoes': f"{banqueta.largura} x {banqueta.profundidade} x {banqueta.altura} cm",
                    'tipo': 'Banqueta'
                }
            })
            
        elif produto_id.startswith('cadeira_'):
            # Cadeira
            from produtos.models import Cadeira
            cadeira_id = produto_id.replace('cadeira_', '')
            cadeira = Cadeira.objects.get(id=cadeira_id)
            
            return JsonResponse({
                'produto': {
                    'nome': cadeira.nome,
                    'foto': cadeira.imagem_principal.url if cadeira.imagem_principal else None,
                    'dimensoes': f"{cadeira.largura} x {cadeira.profundidade} x {cadeira.altura} cm",
                    'tipo': 'Cadeira'
                }
            })
            
        elif produto_id.startswith('poltrona_'):
            # Poltrona
            from produtos.models import Poltrona
            poltrona_id = produto_id.replace('poltrona_', '')
            poltrona = Poltrona.objects.get(id=poltrona_id)
            
            return JsonResponse({
                'produto': {
                    'nome': poltrona.nome,
                    'foto': poltrona.imagem_principal.url if poltrona.imagem_principal else None,
                    'dimensoes': f"{poltrona.largura} x {poltrona.profundidade} x {poltrona.altura} cm",
                    'tipo': 'Poltrona'
                }
            })
            
        elif produto_id.startswith('pufe_'):
            # Pufe
            from produtos.models import Pufe
            pufe_id = produto_id.replace('pufe_', '')
            pufe = Pufe.objects.get(id=pufe_id)
            
            return JsonResponse({
                'produto': {
                    'nome': pufe.nome,
                    'foto': pufe.imagem_principal.url if pufe.imagem_principal else None,
                    'dimensoes': f"{pufe.largura} x {pufe.profundidade} x {pufe.altura} cm",
                    'tipo': 'Pufe'
                }
            })
            
        elif produto_id.startswith('almofada_'):
            # Almofada
            from produtos.models import Almofada
            almofada_id = produto_id.replace('almofada_', '')
            almofada = Almofada.objects.get(id=almofada_id)
            
            return JsonResponse({
                'produto': {
                    'nome': almofada.nome,
                    'foto': almofada.imagem_principal.url if almofada.imagem_principal else None,
                    'dimensoes': f"{almofada.largura} x {almofada.altura} cm (Almofada)",
                    'tipo': 'Almofada'
                }
            })
            
        elif produto_id.startswith('acessorio_'):
            # Acessório
            from produtos.models import Acessorio
            acessorio_id = produto_id.replace('acessorio_', '')
            acessorio = Acessorio.objects.get(id=acessorio_id)
            
            return JsonResponse({
                'produto': {
                    'nome': acessorio.nome,
                    'foto': acessorio.imagem_principal.url if acessorio.imagem_principal else None,
                    'dimensoes': 'Acessório',
                    'tipo': 'Acessório'
                }
            })
            
        else:
            return JsonResponse({'erro': 'Tipo de produto não reconhecido'}, status=400)
            
    except Exception as e:
        return JsonResponse({'erro': str(e)}, status=500)
