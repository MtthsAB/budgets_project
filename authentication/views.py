from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.http import require_POST
from django.http import HttpResponse
from django.core.paginator import Paginator
from django.db.models import Q
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from .models import CustomUser, TipoPermissao
from .forms import CustomUserCreationForm, UserUpdateForm, PasswordChangeForm
from .decorators import master_required

@csrf_protect
def login_view(request):
    """View para login de usuários"""
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        if email and password:
            user = authenticate(request, username=email, password=password)
            if user is not None:
                login(request, user)
                next_url = request.GET.get('next', 'home')
                
                # Redirecionar baseado no tipo de permissão
                if user.tipo_permissao == TipoPermissao.VENDEDOR:
                    # Redirecionar para módulo de orçamentos
                    return redirect('orcamentos:listar')
                elif user.tipo_permissao == TipoPermissao.OPERADOR_PRODUTOS:
                    return redirect('produtos_lista')
                else:
                    return redirect(next_url)
            else:
                messages.error(request, 'Email ou senha inválidos.')
        else:
            messages.error(request, 'Por favor, preencha todos os campos.')
    
    return render(request, 'authentication/login.html')

@login_required
def logout_view(request):
    """View para logout de usuários"""
    logout(request)
    messages.success(request, 'Logout realizado com sucesso.')
    return redirect('login')


@csrf_protect
@require_POST
def logout_beacon(request):
    """Logout rápido para uso em unload/reload via beacon/keepalive."""
    if request.user.is_authenticated:
        logout(request)
    return HttpResponse(status=204)

@csrf_protect
def register_view(request):
    """View para registro de novos usuários"""
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        password_confirm = request.POST.get('password_confirm')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        
        if not all([email, password, password_confirm, first_name, last_name]):
            messages.error(request, 'Por favor, preencha todos os campos.')
        elif password != password_confirm:
            messages.error(request, 'As senhas não coincidem.')
        elif CustomUser.objects.filter(email=email).exists():
            messages.error(request, 'Este email já está cadastrado.')
        else:
            try:
                user = CustomUser.objects.create_user(
                    email=email,
                    password=password,
                    first_name=first_name,
                    last_name=last_name
                )
                messages.success(request, 'Usuário cadastrado com sucesso! Faça login.')
                return redirect('login')
            except Exception as e:
                messages.error(request, f'Erro ao cadastrar usuário: {str(e)}')
    
    return render(request, 'authentication/register.html')

# API Views para autenticação JWT
@api_view(['POST'])
@permission_classes([AllowAny])
def api_login(request):
    """API endpoint para login com JWT"""
    email = request.data.get('email')
    password = request.data.get('password')
    
    if email and password:
        user = authenticate(username=email, password=password)
        if user:
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'user': {
                    'id': user.id,
                    'email': user.email,
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                }
            })
        else:
            return Response(
                {'error': 'Credenciais inválidas'}, 
                status=status.HTTP_401_UNAUTHORIZED
            )
    else:            return Response(
                {'error': 'Email e senha são obrigatórios'}, 
                status=status.HTTP_400_BAD_REQUEST
            )

# Views para gerenciamento de usuários
@master_required
def usuarios_lista(request):
    """View para listagem de usuários"""
    usuarios = CustomUser.objects.all().order_by('-created_at')
    
    # Filtros
    search = request.GET.get('search', '')
    tipo_filtro = request.GET.get('tipo', '')
    ativo_filtro = request.GET.get('ativo', '')
    
    if search:
        usuarios = usuarios.filter(
            Q(email__icontains=search) |
            Q(first_name__icontains=search) |
            Q(last_name__icontains=search)
        )
    
    if tipo_filtro:
        usuarios = usuarios.filter(tipo_permissao=tipo_filtro)
    
    if ativo_filtro:
        usuarios = usuarios.filter(is_active=ativo_filtro == 'true')
    
    # Paginação
    paginator = Paginator(usuarios, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'usuarios': page_obj,
        'search': search,
        'tipo_filtro': tipo_filtro,
        'ativo_filtro': ativo_filtro,
        'tipos_permissao': TipoPermissao.choices,
    }
    
    return render(request, 'authentication/usuarios_lista.html', context)

@master_required
@csrf_protect
def usuario_novo(request):
    """View para criação de novo usuário"""
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            try:
                user = form.save()
                messages.success(request, f'Usuário {user.get_full_name()} criado com sucesso!')
                return redirect('usuarios_lista')
            except Exception as e:
                messages.error(request, f'Erro ao criar usuário: {str(e)}')
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'authentication/usuario_form.html', {
        'form': form,
        'title': 'Novo Usuário',
        'action': 'Criar'
    })

@master_required
def usuario_detalhe(request, pk):
    """View para visualização de detalhes do usuário"""
    usuario = get_object_or_404(CustomUser, pk=pk)
    
    context = {
        'usuario': usuario,
        'tipo_permissao_display': usuario.get_tipo_permissao_display(),
    }
    
    return render(request, 'authentication/usuario_detalhe.html', context)

@master_required
@csrf_protect
def usuario_editar(request, pk):
    """View para edição de usuário"""
    usuario = get_object_or_404(CustomUser, pk=pk)
    
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=usuario)
        form.current_user = request.user  # Para evitar auto-edição problemática
        
        if form.is_valid():
            try:
                form.save()
                messages.success(request, f'Usuário {usuario.get_full_name()} atualizado com sucesso!')
                return redirect('usuarios_lista')
            except Exception as e:
                messages.error(request, f'Erro ao atualizar usuário: {str(e)}')
    else:
        form = UserUpdateForm(instance=usuario)
        form.current_user = request.user
    
    return render(request, 'authentication/usuario_form.html', {
        'form': form,
        'usuario': usuario,
        'title': 'Editar Usuário',
        'action': 'Atualizar'
    })

@master_required
@csrf_protect
def usuario_alterar_senha(request, pk):
    """View para alteração de senha do usuário"""
    usuario = get_object_or_404(CustomUser, pk=pk)
    
    if request.method == 'POST':
        form = PasswordChangeForm(request.POST)
        if form.is_valid():
            try:
                usuario.set_password(form.cleaned_data['new_password1'])
                usuario.save()
                messages.success(request, f'Senha do usuário {usuario.get_full_name()} alterada com sucesso!')
                return redirect('usuario_detalhe', pk=pk)
            except Exception as e:
                messages.error(request, f'Erro ao alterar senha: {str(e)}')
    else:
        form = PasswordChangeForm()
    
    return render(request, 'authentication/usuario_alterar_senha.html', {
        'form': form,
        'usuario': usuario,
    })

@master_required
@csrf_protect
def usuario_toggle_ativo(request, pk):
    """View para ativar/desativar usuário"""
    usuario = get_object_or_404(CustomUser, pk=pk)
    
    # Não permitir desativar a si mesmo
    if usuario == request.user:
        messages.error(request, 'Você não pode desativar sua própria conta.')
        return redirect('usuarios_lista')
    
    usuario.is_active = not usuario.is_active
    usuario.save()
    
    status_text = 'ativado' if usuario.is_active else 'desativado'
    messages.success(request, f'Usuário {usuario.get_full_name()} {status_text} com sucesso!')
    
    return redirect('usuarios_lista')
