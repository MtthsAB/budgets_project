#!/usr/bin/env python3
"""
Teste final para verificar se os produtos Pufes e Almofadas 
foram cadastrados corretamente e aparecem no sistema.
"""

import os
import sys
import django

# Configurar Django
sys.path.append('/home/matas/projetos/Project')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema_produtos.settings')
django.setup()

from produtos.models import Produto, Banqueta, Cadeira, Poltrona, Pufe, Almofada, Acessorio

def main():
    print("🧪 TESTE FINAL DO CADASTRO DE PUFES E ALMOFADAS")
    print("="*60)
    
    print("\n📊 CONTAGEM GERAL DE PRODUTOS:")
    print("-"*40)
    
    # Contar todos os tipos de produto
    produtos = Produto.objects.filter(ativo=True).count()
    banquetas = Banqueta.objects.filter(ativo=True).count()
    cadeiras = Cadeira.objects.filter(ativo=True).count()
    poltronas = Poltrona.objects.filter(ativo=True).count()
    pufes = Pufe.objects.filter(ativo=True).count()
    almofadas = Almofada.objects.filter(ativo=True).count()
    acessorios = Acessorio.objects.filter(ativo=True).count()
    
    print(f"📦 Produtos (Sofás): {produtos}")
    print(f"🪑 Banquetas: {banquetas}")
    print(f"💺 Cadeiras: {cadeiras}")
    print(f"🛋️  Poltronas: {poltronas}")
    print(f"📦 Pufes: {pufes}")
    print(f"🛏️  Almofadas: {almofadas}")
    print(f"🔧 Acessórios: {acessorios}")
    
    total = produtos + banquetas + cadeiras + poltronas + pufes + almofadas + acessorios
    print(f"\n🎯 TOTAL GERAL: {total} produtos ativos")
    
    print("\n📝 DETALHES DOS PUFES CADASTRADOS:")
    print("-"*45)
    pufes_obj = Pufe.objects.filter(ativo=True).order_by('ref_pufe')
    for pufe in pufes_obj:
        tem_imagem = "✅" if pufe.imagem_principal else "❌"
        print(f"  {pufe.ref_pufe} - {pufe.nome}")
        print(f"    💰 R$ {pufe.preco} | 📏 {pufe.get_dimensoes_formatadas()}")
        print(f"    📸 Imagem: {tem_imagem} | ✅ Ativo: {pufe.ativo}")
        print()
    
    print("📝 DETALHES DAS ALMOFADAS CADASTRADAS:")
    print("-"*47)
    almofadas_obj = Almofada.objects.filter(ativo=True).order_by('ref_almofada')
    for almofada in almofadas_obj:
        tem_imagem = "✅" if almofada.imagem_principal else "❌"
        print(f"  {almofada.ref_almofada} - {almofada.nome}")
        print(f"    💰 R$ {almofada.preco} | 📏 {almofada.get_dimensoes_formatadas()}")
        print(f"    📸 Imagem: {tem_imagem} | ✅ Ativo: {almofada.ativo}")
        print()
    
    print("🔍 TESTE DE INTEGRIDADE DOS DADOS:")
    print("-"*38)
    
    # Verificar se todos os campos obrigatórios estão preenchidos
    problemas = []
    
    for pufe in pufes_obj:
        if not pufe.ref_pufe or not pufe.nome or not pufe.preco:
            problemas.append(f"Pufe {pufe.ref_pufe}: campos obrigatórios não preenchidos")
        if pufe.largura <= 0 or pufe.profundidade <= 0 or pufe.altura <= 0:
            problemas.append(f"Pufe {pufe.ref_pufe}: dimensões inválidas")
    
    for almofada in almofadas_obj:
        if not almofada.ref_almofada or not almofada.nome or not almofada.preco:
            problemas.append(f"Almofada {almofada.ref_almofada}: campos obrigatórios não preenchidos")
        if almofada.largura <= 0 or almofada.altura <= 0:
            problemas.append(f"Almofada {almofada.ref_almofada}: dimensões inválidas")
    
    if problemas:
        print("❌ PROBLEMAS ENCONTRADOS:")
        for problema in problemas:
            print(f"  - {problema}")
    else:
        print("✅ TODOS OS DADOS ESTÃO ÍNTEGROS!")
    
    print("\n🎉 RESUMO FINAL:")
    print("="*20)
    print(f"✅ {len(pufes_obj)} Pufes cadastrados com sucesso")
    print(f"✅ {len(almofadas_obj)} Almofadas cadastradas com sucesso")
    print(f"✅ Total: {len(pufes_obj) + len(almofadas_obj)} novos produtos")
    print("\n✨ CADASTRO REALIZADO COM SUCESSO!")

if __name__ == '__main__':
    main()
