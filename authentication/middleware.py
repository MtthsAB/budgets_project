from django.shortcuts import redirect
from django.urls import reverse
from django.contrib.auth import logout
from django.contrib import messages

class PermissionMiddleware:
    """
    Middleware para controlar acesso baseado em permissões
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Verificar se o usuário está autenticado
        if request.user.is_authenticated:
            # URLs que não precisam de verificação de permissão
            allowed_urls = [
                '/auth/logout/',
                '/admin/',
                '/static/',
                '/media/',
            ]
            
            # Verificar se a URL atual está nas URLs permitidas
            if any(request.path.startswith(url) for url in allowed_urls):
                response = self.get_response(request)
                return response
            
            # URLs específicas por tipo de usuário
            if request.user.tipo_permissao == 'vendedor':
                # Vendedores só podem acessar orçamentos (futuro)
                if not request.path.startswith('/orcamentos/'):
                    # Por enquanto, redirecionar para home
                    if request.path != reverse('home'):
                        return redirect('home')
            
            elif request.user.tipo_permissao == 'operador_produtos':
                # Operadores de produtos só podem acessar produtos
                if not (request.path.startswith('/produtos/') or 
                        request.path.startswith('/') and request.path == reverse('produtos_lista')):
                    # Se não for a página inicial ou produtos, redirecionar
                    if request.path != reverse('produtos_lista'):
                        return redirect('produtos_lista')
        
        response = self.get_response(request)
        return response
