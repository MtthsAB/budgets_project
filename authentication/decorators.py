from functools import wraps
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect
from django.contrib import messages
from django.urls import reverse

def permission_required(permission):
    """
    Decorator para verificar permissões específicas
    """
    def decorator(view_func):
        @wraps(view_func)
        @login_required
        def wrapper(request, *args, **kwargs):
            if not request.user.has_permission(permission):
                messages.error(request, 'Você não tem permissão para acessar esta página.')
                return redirect('home')
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator

def master_required(view_func):
    """
    Decorator para exigir permissão de Master
    """
    @wraps(view_func)
    @login_required
    def wrapper(request, *args, **kwargs):
        if not request.user.can_manage_users():
            messages.error(request, 'Você não tem permissão para acessar esta página.')
            return redirect('home')
        return view_func(request, *args, **kwargs)
    return wrapper

def admin_or_master_required(view_func):
    """
    Decorator para exigir permissão de Admin ou Master
    """
    @wraps(view_func)
    @login_required
    def wrapper(request, *args, **kwargs):
        if not request.user.can_access_home():
            messages.error(request, 'Você não tem permissão para acessar esta página.')
            return redirect('home')
        return view_func(request, *args, **kwargs)
    return wrapper

def produtos_access_required(view_func):
    """
    Decorator para exigir acesso aos produtos
    """
    @wraps(view_func)
    @login_required
    def wrapper(request, *args, **kwargs):
        if not request.user.can_access_produtos():
            messages.error(request, 'Você não tem permissão para acessar esta página.')
            return redirect('home')
        return view_func(request, *args, **kwargs)
    return wrapper

def clientes_access_required(view_func):
    """
    Decorator para exigir acesso aos clientes
    """
    @wraps(view_func)
    @login_required
    def wrapper(request, *args, **kwargs):
        if not request.user.can_access_clientes():
            messages.error(request, 'Você não tem permissão para acessar esta página.')
            return redirect('home')
        return view_func(request, *args, **kwargs)
    return wrapper

def orcamentos_access_required(view_func):
    """
    Decorator para exigir acesso aos orçamentos
    """
    @wraps(view_func)
    @login_required
    def wrapper(request, *args, **kwargs):
        if not request.user.can_access_orcamentos():
            messages.error(request, 'Você não tem permissão para acessar esta página.')
            return redirect('home')
        return view_func(request, *args, **kwargs)
    return wrapper
