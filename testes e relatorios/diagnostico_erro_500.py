#!/usr/bin/env python3
"""
Script para diagnosticar especificamente o erro 500 na edição de produtos
"""
import os
import sys
import django

# Configurar o Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema_produtos.settings')
django.setup()

from produtos.models import Produto, TipoItem
from django.shortcuts import get_object_or_404
from produtos.views import produto_editar_view
from django.http import HttpRequest
from django.contrib.auth import get_user_model
from authentication.models import CustomUser
import traceback

def test_editar_view():
    """Testa a view de edição diretamente"""
    
    print("=== TESTE DIRETO DA VIEW DE EDIÇÃO ===\n")
    
    # Buscar produtos
    produtos = Produto.objects.all()[:3]
    if not produtos:
        print("❌ Nenhum produto encontrado")
        return
        
    user = CustomUser.objects.filter(is_active=True).first()
    if not user:
        print("❌ Nenhum usuário encontrado")
        return
        
    for produto in produtos:
        print(f"\n--- Testando produto: {produto.ref_produto} ---")
        print(f"ID: {produto.id}")
        print(f"Nome: {produto.nome_produto}")
        print(f"Tipo: {produto.id_tipo_produto.nome if produto.id_tipo_produto else 'Sem tipo'}")
        
        try:
            # Simular request GET
            request = HttpRequest()
            request.method = 'GET'
            request.user = user
            request.META = {'HTTP_HOST': '127.0.0.1:8000'}
            
            # Tentar chamar a view
            response = produto_editar_view(request, produto.id)
            
            if hasattr(response, 'status_code'):
                print(f"✅ View retornou status {response.status_code}")
                if response.status_code == 200:
                    print("✅ Sucesso!")
                elif response.status_code == 500:
                    print("❌ Erro 500!")
                else:
                    print(f"⚠️ Status inesperado: {response.status_code}")
            else:
                print("✅ View executou sem retornar response object")
                
        except Exception as e:
            print(f"❌ ERRO na view: {e}")
            print("Stack trace:")
            traceback.print_exc()
            print()

def check_template_context():
    """Verifica o contexto do template"""
    print("\n=== VERIFICANDO CONTEXTO DO TEMPLATE ===\n")
    
    produto = Produto.objects.first()
    if not produto:
        print("❌ Nenhum produto encontrado")
        return
        
    try:
        print(f"Produto encontrado: {produto.ref_produto}")
        print(f"Módulos: {produto.modulos.count()}")
        print(f"Tipo: {produto.id_tipo_produto}")
        
        # Verificar se o método eh_sofa existe
        if hasattr(produto, 'eh_sofa'):
            print(f"É sofá: {produto.eh_sofa()}")
        else:
            print("⚠️ Método eh_sofa não encontrado")
            
        # Verificar produtos vinculados
        # print(f"Produtos vinculados: {produto.produtos_vinculados.count()}")  # Não existe no modelo Produto
        print("Produtos vinculados: N/A (não aplicável para o modelo Produto)")
        
        # Verificar prefetch dos módulos
        modulos = produto.modulos.prefetch_related('tamanhos_detalhados').all()
        print(f"Módulos com prefetch: {modulos.count()}")
        for i, modulo in enumerate(modulos):
            print(f"  - Módulo {i+1}: {modulo.nome} (tamanhos: {modulo.tamanhos_detalhados.count()})")
        
    except Exception as e:
        print(f"❌ Erro ao verificar contexto: {e}")
        traceback.print_exc()

if __name__ == "__main__":
    test_editar_view()
    check_template_context()
