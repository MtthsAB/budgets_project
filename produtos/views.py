from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.csrf import csrf_protect
from django.db import transaction
from rest_framework import viewsets, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import (
    Item, TipoItem, Linha, Modulo, Acessorio, 
    AcessoriosItens, TamanhosModulos, FaixaTecido, PrecosBase
)

@login_required
def home_view(request):
    """View da página inicial do sistema"""
    context = {
        'total_produtos': Item.objects.count(),
        'total_tipos': TipoItem.objects.count(),
        'total_linhas': Linha.objects.count(),
        'total_modulos': Modulo.objects.count(),
        'produtos_recentes': Item.objects.select_related('id_tipo_produto', 'id_linha').order_by('-created_at')[:5],
    }
    return render(request, 'produtos/home.html', context)

@login_required
def produtos_list_view(request):
    """View para listagem de produtos"""
    produtos = Item.objects.select_related('id_tipo_produto', 'id_linha').all()
    
    # Filtros
    tipo_filtro = request.GET.get('tipo')
    linha_filtro = request.GET.get('linha')
    ativo_filtro = request.GET.get('ativo')
    busca = request.GET.get('busca')
    
    if tipo_filtro:
        produtos = produtos.filter(id_tipo_produto__id=tipo_filtro)
    
    if linha_filtro:
        produtos = produtos.filter(id_linha__id=linha_filtro)
    
    if ativo_filtro:
        produtos = produtos.filter(ativo=ativo_filtro == 'true')
    
    if busca:
        produtos = produtos.filter(
            nome_produto__icontains=busca
        ) | produtos.filter(
            ref_produto__icontains=busca
        )
    
    context = {
        'produtos': produtos,
        'tipos': TipoItem.objects.all(),
        'linhas': Linha.objects.all(),
        'filtros': {
            'tipo': tipo_filtro,
            'linha': linha_filtro,
            'ativo': ativo_filtro,
            'busca': busca,
        }
    }
    return render(request, 'produtos/lista.html', context)

@login_required
@csrf_protect
def produto_cadastro_view(request):
    """View para cadastro de novos produtos"""
    if request.method == 'POST':
        try:
            with transaction.atomic():
                # Dados básicos do produto
                ref_produto = request.POST.get('ref_produto')
                nome_produto = request.POST.get('nome_produto')
                tipo_produto_id = request.POST.get('tipo_produto')
                linha_id = request.POST.get('linha')
                ativo = request.POST.get('ativo') == 'on'
                tem_cor_tecido = request.POST.get('tem_cor_tecido') == 'on'
                tem_difer_desenho_lado = request.POST.get('tem_difer_desenho_lado') == 'on'
                tem_difer_desenho_tamanho = request.POST.get('tem_difer_desenho_tamanho') == 'on'
                
                # Validações básicas
                if not all([ref_produto, nome_produto, tipo_produto_id, linha_id]):
                    messages.error(request, 'Por favor, preencha todos os campos obrigatórios.')
                    raise ValueError('Campos obrigatórios não preenchidos')
                
                if Item.objects.filter(ref_produto=ref_produto).exists():
                    messages.error(request, 'Já existe um produto com esta referência.')
                    raise ValueError('Referência duplicada')
                
                # Criar o produto
                produto = Item.objects.create(
                    ref_produto=ref_produto,
                    nome_produto=nome_produto,
                    id_tipo_produto_id=tipo_produto_id,
                    id_linha_id=linha_id,
                    ativo=ativo,
                    tem_cor_tecido=tem_cor_tecido,
                    tem_difer_desenho_lado_dir_esq=tem_difer_desenho_lado,
                    tem_difer_desenho_tamanho=tem_difer_desenho_tamanho,
                    imagem_principal=request.FILES.get('imagem_principal'),
                    imagem_secundaria=request.FILES.get('imagem_secundaria')
                )
                
                # Processar módulos
                modulos_nomes = request.POST.getlist('modulo_nome')
                
                for i in range(len(modulos_nomes)):
                    if modulos_nomes[i]:  # Se o nome do módulo não estiver vazio
                        modulo = Modulo.objects.create(
                            item=produto,
                            nome=modulos_nomes[i],
                            imagem_principal=request.FILES.get(f'modulo_imagem_principal_{i+1}'),
                            imagem_secundaria=request.FILES.get(f'modulo_imagem_secundaria_{i+1}')
                        )
                        
                        # Processar tamanhos deste módulo
                        modulo_id = i + 1
                        tamanhos_nomes = request.POST.getlist(f'tamanho_nome_{modulo_id}')
                        tamanhos_largura_total = request.POST.getlist(f'tamanho_largura_total_{modulo_id}')
                        tamanhos_largura_assento = request.POST.getlist(f'tamanho_largura_assento_{modulo_id}')
                        tamanhos_altura = request.POST.getlist(f'tamanho_altura_{modulo_id}')
                        tamanhos_profundidade = request.POST.getlist(f'tamanho_profundidade_{modulo_id}')
                        tamanhos_tecido = request.POST.getlist(f'tamanho_tecido_{modulo_id}')
                        tamanhos_volume = request.POST.getlist(f'tamanho_volume_{modulo_id}')
                        tamanhos_peso = request.POST.getlist(f'tamanho_peso_{modulo_id}')
                        tamanhos_preco = request.POST.getlist(f'tamanho_preco_{modulo_id}')
                        tamanhos_descricao = request.POST.getlist(f'tamanho_descricao_{modulo_id}')
                        
                        for j in range(len(tamanhos_nomes)):
                            if tamanhos_nomes[j]:
                                from .models import TamanhosModulosDetalhado
                                TamanhosModulosDetalhado.objects.create(
                                    id_modulo=modulo,
                                    nome_tamanho=tamanhos_nomes[j],
                                    largura_total=float(tamanhos_largura_total[j]) if tamanhos_largura_total[j] else None,
                                    largura_assento=float(tamanhos_largura_assento[j]) if tamanhos_largura_assento[j] else None,
                                    altura_cm=float(tamanhos_altura[j]) if tamanhos_altura[j] else None,
                                    profundidade_cm=float(tamanhos_profundidade[j]) if tamanhos_profundidade[j] else None,
                                    tecido_metros=float(tamanhos_tecido[j]) if tamanhos_tecido[j] else None,
                                    volume_m3=float(tamanhos_volume[j]) if tamanhos_volume[j] else None,
                                    peso_kg=float(tamanhos_peso[j]) if tamanhos_peso[j] else None,
                                    preco=float(tamanhos_preco[j]) if tamanhos_preco[j] else None,
                                    descricao=tamanhos_descricao[j] if tamanhos_descricao[j] else None
                                )
                
                messages.success(request, f'Produto "{produto.nome_produto}" cadastrado com sucesso!')
                return redirect('produtos_lista')
                
        except Exception as e:
            messages.error(request, f'Erro ao cadastrar produto: {str(e)}')
    
    context = {
        'tipos': TipoItem.objects.all(),
        'linhas': Linha.objects.all(),
    }
    return render(request, 'produtos/cadastro.html', context)

@login_required
def produto_editar_view(request, produto_id):
    """View para edição de produtos"""
    produto = get_object_or_404(Item, id=produto_id)
    
    if request.method == 'POST':
        try:
            with transaction.atomic():
                # Atualizar dados básicos
                produto.ref_produto = request.POST.get('ref_produto')
                produto.nome_produto = request.POST.get('nome_produto')
                produto.id_tipo_produto_id = request.POST.get('tipo_produto')
                produto.id_linha_id = request.POST.get('linha')
                produto.ativo = request.POST.get('ativo') == 'on'
                produto.tem_cor_tecido = request.POST.get('tem_cor_tecido') == 'on'
                produto.tem_difer_desenho_lado_dir_esq = request.POST.get('tem_difer_desenho_lado') == 'on'
                produto.tem_difer_desenho_tamanho = request.POST.get('tem_difer_desenho_tamanho') == 'on'
                
                # Atualizar imagens se fornecidas
                if 'imagem_principal' in request.FILES:
                    produto.imagem_principal = request.FILES['imagem_principal']
                if 'imagem_secundaria' in request.FILES:
                    produto.imagem_secundaria = request.FILES['imagem_secundaria']
                    
                produto.save()
                
                # Remover módulos existentes e recriar
                produto.modulos.all().delete()
                
                # Processar novos módulos
                modulos_nomes = request.POST.getlist('modulo_nome')
                
                for i in range(len(modulos_nomes)):
                    if modulos_nomes[i]:
                        modulo = Modulo.objects.create(
                            item=produto,
                            nome=modulos_nomes[i],
                            imagem_principal=request.FILES.get(f'modulo_imagem_principal_{i+1}'),
                            imagem_secundaria=request.FILES.get(f'modulo_imagem_secundaria_{i+1}')
                        )
                        
                        # Processar tamanhos deste módulo
                        modulo_id = i + 1
                        tamanhos_nomes = request.POST.getlist(f'tamanho_nome_{modulo_id}')
                        tamanhos_largura_total = request.POST.getlist(f'tamanho_largura_total_{modulo_id}')
                        tamanhos_largura_assento = request.POST.getlist(f'tamanho_largura_assento_{modulo_id}')
                        tamanhos_altura = request.POST.getlist(f'tamanho_altura_{modulo_id}')
                        tamanhos_profundidade = request.POST.getlist(f'tamanho_profundidade_{modulo_id}')
                        tamanhos_tecido = request.POST.getlist(f'tamanho_tecido_{modulo_id}')
                        tamanhos_volume = request.POST.getlist(f'tamanho_volume_{modulo_id}')
                        tamanhos_peso = request.POST.getlist(f'tamanho_peso_{modulo_id}')
                        tamanhos_preco = request.POST.getlist(f'tamanho_preco_{modulo_id}')
                        tamanhos_descricao = request.POST.getlist(f'tamanho_descricao_{modulo_id}')
                        
                        for j in range(len(tamanhos_nomes)):
                            if tamanhos_nomes[j]:
                                from .models import TamanhosModulosDetalhado
                                TamanhosModulosDetalhado.objects.create(
                                    id_modulo=modulo,
                                    nome_tamanho=tamanhos_nomes[j],
                                    largura_total=float(tamanhos_largura_total[j]) if tamanhos_largura_total[j] else None,
                                    largura_assento=float(tamanhos_largura_assento[j]) if tamanhos_largura_assento[j] else None,
                                    altura_cm=float(tamanhos_altura[j]) if tamanhos_altura[j] else None,
                                    profundidade_cm=float(tamanhos_profundidade[j]) if tamanhos_profundidade[j] else None,
                                    tecido_metros=float(tamanhos_tecido[j]) if tamanhos_tecido[j] else None,
                                    volume_m3=float(tamanhos_volume[j]) if tamanhos_volume[j] else None,
                                    peso_kg=float(tamanhos_peso[j]) if tamanhos_peso[j] else None,
                                    preco=float(tamanhos_preco[j]) if tamanhos_preco[j] else None,
                                    descricao=tamanhos_descricao[j] if tamanhos_descricao[j] else None
                                )
                
                messages.success(request, f'Produto "{produto.nome_produto}" atualizado com sucesso!')
                return redirect('produtos_lista')
                
        except Exception as e:
            messages.error(request, f'Erro ao atualizar produto: {str(e)}')
    
    context = {
        'produto': produto,
        'modulos': produto.modulos.all(),
        'tipos': TipoItem.objects.all(),
        'linhas': Linha.objects.all(),
    }
    return render(request, 'produtos/editar.html', context)

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
    """View para visualização detalhada de um produto"""
    produto = get_object_or_404(Item.objects.select_related('id_tipo_produto', 'id_linha'), id=produto_id)
    modulos = produto.modulos.all()
    
    context = {
        'produto': produto,
        'modulos': modulos,
    }
    return render(request, 'produtos/detalhes.html', context)

def teste_view(request):
    """View de teste para diagnosticar problemas"""
    return render(request, 'teste.html')
