from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from sistema_produtos.mixins import track_user_changes
from authentication.decorators import clientes_access_required
from .models import Cliente
from .forms import ClienteForm


@clientes_access_required
def cliente_lista(request):
    """Lista todos os clientes com busca e paginação"""
    search_query = request.GET.get('search', '')
    clientes = Cliente.objects.all()
    
    if search_query:
        clientes = clientes.filter(
            Q(nome_empresa__icontains=search_query) |
            Q(representante__icontains=search_query) |
            Q(cnpj__icontains=search_query) |
            Q(cidade__icontains=search_query) |
            Q(email__icontains=search_query)
        )
    
    paginator = Paginator(clientes, 10)  # 10 clientes por página
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'search_query': search_query,
        'total_clientes': clientes.count()
    }
    return render(request, 'clientes/lista.html', context)


@clientes_access_required
def cliente_cadastro(request):
    """Cadastra um novo cliente"""
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            cliente = form.save(commit=False)
            # Rastrear usuário
            track_user_changes(cliente, request.user)
            cliente.save()
            messages.success(request, f'Cliente {cliente.nome_empresa} cadastrado com sucesso!')
            return redirect('cliente_detalhes', pk=cliente.pk)
    else:
        form = ClienteForm()
    
    context = {
        'form': form,
        'title': 'Cadastrar Cliente'
    }
    return render(request, 'clientes/cadastro.html', context)


@clientes_access_required
def cliente_detalhes(request, pk):
    """Exibe os detalhes de um cliente"""
    cliente = get_object_or_404(Cliente, pk=pk)
    context = {
        'cliente': cliente
    }
    return render(request, 'clientes/detalhes.html', context)


@clientes_access_required
def cliente_editar(request, pk):
    """Edita um cliente existente"""
    cliente = get_object_or_404(Cliente, pk=pk)
    
    if request.method == 'POST':
        form = ClienteForm(request.POST, instance=cliente)
        if form.is_valid():
            cliente = form.save(commit=False)
            # Rastrear usuário na edição
            track_user_changes(cliente, request.user)
            cliente.save()
            messages.success(request, f'Cliente {cliente.nome_empresa} atualizado com sucesso!')
            return redirect('cliente_detalhes', pk=cliente.pk)
    else:
        form = ClienteForm(instance=cliente)
    
    context = {
        'form': form,
        'cliente': cliente,
        'title': f'Editar Cliente - {cliente.nome_empresa}'
    }
    return render(request, 'clientes/editar.html', context)


@clientes_access_required
def cliente_deletar(request, pk):
    """Deleta um cliente"""
    cliente = get_object_or_404(Cliente, pk=pk)
    
    if request.method == 'POST':
        nome_empresa = cliente.nome_empresa
        cliente.delete()
        messages.success(request, f'Cliente {nome_empresa} deletado com sucesso!')
        return redirect('cliente_lista')
    
    context = {
        'cliente': cliente
    }
    return render(request, 'clientes/deletar.html', context)
