#!/usr/bin/env python3
import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema_produtos.settings')
django.setup()

from produtos.models import Produto

# Testar produto
try:
    produto = Produto.objects.get(id=6)
    print(f"Produto: {produto.nome_produto}")
    print(f"Ref: {produto.ref_produto}")
    print(f"Imagem principal: {produto.imagem_principal}")
    if produto.imagem_principal:
        print(f"URL da imagem: {produto.imagem_principal.url}")
        print(f"Path da imagem: {produto.imagem_principal.path}")
        import os
        print(f"Arquivo existe: {os.path.exists(produto.imagem_principal.path)}")
    else:
        print("Nenhuma imagem principal definida!")
        
except Produto.DoesNotExist:
    print("Produto 6 não encontrado!")
except Exception as e:
    print(f"Erro: {e}")
