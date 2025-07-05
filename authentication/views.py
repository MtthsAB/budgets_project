from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.csrf import csrf_protect
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from .models import CustomUser

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
    else:
        return Response(
            {'error': 'Email e senha são obrigatórios'}, 
            status=status.HTTP_400_BAD_REQUEST
        )
