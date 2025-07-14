#!/usr/bin/env python3

import os
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema_produtos.settings')
django.setup()

from produtos.models import Produto

print("=== Verificação de Imagens de Sofás ===\n")

# Buscar todos os produtos do tipo sofá
produtos = Produto.objects.filter(ativo=True)
print(f"Total de produtos ativos: {produtos.count()}")

for produto in produtos:
    print(f"\nProduto ID: {produto.id}")
    print(f"Nome: {produto.nome_produto}")
    print(f"Ref: {produto.ref_produto}")
    print(f"Tipo: {produto.id_tipo_produto}")
    print(f"Imagem principal: {produto.imagem_principal}")
    if produto.imagem_principal:
        print(f"URL da imagem: {produto.imagem_principal.url}")
        # Verificar se o arquivo existe
        caminho_completo = os.path.join('/home/matas/projetos/Project/media', str(produto.imagem_principal))
        existe = os.path.exists(caminho_completo)
        print(f"Arquivo existe: {existe}")
        if existe:
            tamanho = os.path.getsize(caminho_completo)
            print(f"Tamanho: {tamanho} bytes")
    else:
        print("❌ SEM IMAGEM PRINCIPAL")
    
    print("-" * 50)

# Verificar imagens disponíveis
print("\n=== Imagens Disponíveis na Pasta Media ===")
import glob
imagens_sofas = glob.glob('/home/matas/projetos/Project/media/produtos/sofas/**/*.{jpg,png,jpeg}', recursive=True)
for img in imagens_sofas:
    print(img)
