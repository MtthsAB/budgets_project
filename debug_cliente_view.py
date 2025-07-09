#!/usr/bin/env python3
"""
Criar uma versão simplificada da view de cadastro para debug
"""
import os
import sys
import django

# Configurar o Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema_produtos.settings')
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
django.setup()

from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse
from clientes.forms import ClienteForm
from clientes.models import Cliente

def cliente_cadastro_debug(request):
    """View simplificada para debug"""
    if request.method == 'POST':
        print("🔍 POST recebido!")
        print(f"Dados POST: {dict(request.POST)}")
        
        form = ClienteForm(request.POST)
        print(f"Formulário válido: {form.is_valid()}")
        
        if form.is_valid():
            print("✅ Salvando cliente...")
            cliente = form.save()
            print(f"✅ Cliente salvo: {cliente.nome_empresa}")
            return HttpResponse(f"Cliente {cliente.nome_empresa} cadastrado com sucesso! ID: {cliente.id}")
        else:
            print(f"❌ Erros no formulário: {form.errors}")
            return HttpResponse(f"Erros no formulário: {form.errors}")
    else:
        print("📝 GET - Exibindo formulário")
        form = ClienteForm()
        
    # Template mínimo
    template = '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Debug - Cadastro Cliente</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    </head>
    <body>
        <div class="container mt-4">
            <h2>🔧 Debug - Cadastro de Cliente</h2>
            <form method="post" style="border: 2px solid red; padding: 20px;">
                <input type="hidden" name="csrfmiddlewaretoken" value="{{ csrf_token }}">
                
                <div class="mb-3">
                    <label>Nome da Empresa:</label>
                    {{ form.nome_empresa }}
                </div>
                
                <div class="mb-3">
                    <label>Representante:</label>
                    {{ form.representante }}
                </div>
                
                <div class="mb-3">
                    <label>CNPJ:</label>
                    {{ form.cnpj }}
                </div>
                
                <div class="mb-3">
                    <label>E-mail:</label>
                    {{ form.email }}
                </div>
                
                <div class="mb-3">
                    <label>Telefone:</label>
                    {{ form.telefone }}
                </div>
                
                <div class="mb-3">
                    <label>Logradouro:</label>
                    {{ form.logradouro }}
                </div>
                
                <div class="mb-3">
                    <label>Número:</label>
                    {{ form.numero }}
                </div>
                
                <div class="mb-3">
                    <label>Bairro:</label>
                    {{ form.bairro }}
                </div>
                
                <div class="mb-3">
                    <label>Cidade:</label>
                    {{ form.cidade }}
                </div>
                
                <div class="mb-3">
                    <label>Estado:</label>
                    {{ form.estado }}
                </div>
                
                <div class="mb-3">
                    <label>CEP:</label>
                    {{ form.cep }}
                </div>
                
                <button type="submit" class="btn btn-primary btn-lg" style="background: red;">
                    🔧 SALVAR CLIENTE DEBUG
                </button>
            </form>
            
            <hr>
            <h3>Instruções de Teste:</h3>
            <ol>
                <li>Preencha TODOS os campos obrigatórios</li>
                <li>Clique no botão vermelho</li>
                <li>Se não funcionar, abra DevTools e veja erros no Console</li>
                <li>Verifique aba Network para ver se requisição POST é enviada</li>
            </ol>
        </div>
        
        <script>
            console.log('🔧 Debug script carregado');
            document.querySelector('form').addEventListener('submit', function(e) {
                console.log('🔧 Submit interceptado pelo debug');
                console.log('Dados do formulário:', new FormData(this));
            });
        </script>
    </body>
    </html>
    '''
    
    from django.template import Template, Context
    from django.middleware.csrf import get_token
    
    t = Template(template)
    c = Context({'form': form, 'csrf_token': get_token(request)})
    return HttpResponse(t.render(c))

# Criar arquivo de URL temporário
url_content = '''
from django.urls import path
from debug_cliente_view import cliente_cadastro_debug

urlpatterns = [
    path('debug-cliente/', cliente_cadastro_debug, name='debug_cliente'),
]
'''

with open('/home/matas/projetos/Project/debug_urls.py', 'w') as f:
    f.write(url_content)

print("✅ View de debug criada!")
print("Para testar:")
print("1. Adicione a URL ao urls.py principal:")
print("   path('', include('debug_urls')),")
print("2. Acesse: http://localhost:8000/debug-cliente/")
print("3. Teste o formulário simplificado")

if __name__ == '__main__':
    pass
