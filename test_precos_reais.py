#!/usr/bin/env python
"""
Teste para verificar a funcionalidade dos endpoints de produtos por tipo
com preços reais do banco de dados.
"""

import os
import sys
import django
import json

# Adicionar o diretório do projeto ao path
sys.path.append('/home/matas/projetos/Project')

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema_produtos.settings')
django.setup()

# Importar após configuração do Django
from django.test import RequestFactory
from django.contrib.auth import get_user_model
from orcamentos.views import produtos_por_tipo, obter_detalhes_produto
from produtos.models import Cadeira, Banqueta, Poltrona, Pufe, Almofada, Acessorio

User = get_user_model()

def teste_produtos_por_tipo():
    """Testa se os endpoints retornam preços reais do banco"""
    
    factory = RequestFactory()
    user = User.objects.filter(is_superuser=True).first()
    
    if not user:
        print("❌ Erro: Usuário admin não encontrado")
        return
    
    print("🔍 TESTANDO ENDPOINT DE PRODUTOS POR TIPO")
    print("=" * 50)
    
    # Tipos de produto para testar
    tipos = ['cadeira', 'banqueta', 'poltrona', 'pufe', 'almofada', 'acessorio']
    
    for tipo in tipos:
        print(f"\n📦 Testando tipo: {tipo.upper()}")
        
        # Criar request
        request = factory.get(f'/orcamentos/produtos-por-tipo/?tipo={tipo}')
        request.user = user
        
        try:
            # Chamar view
            response = produtos_por_tipo(request)
            
            if response.status_code == 200:
                data = json.loads(response.content)
                produtos = data.get('produtos', [])
                
                print(f"   ✅ Produtos encontrados: {len(produtos)}")
                
                # Verificar se há produtos
                if produtos:
                    for produto in produtos[:2]:  # Mostrar apenas os primeiros 2
                        nome = produto.get('nome_produto', 'N/A')
                        ref = produto.get('ref_produto', 'N/A')
                        preco = produto.get('preco', 0.00)
                        
                        print(f"   📋 {nome} (Ref: {ref}) - Preço: R$ {preco:.2f}")
                        
                        # Verificar se o preço é real (não é um dos valores padrão antigos)
                        if preco not in [150.00, 120.00, 200.00, 80.00, 50.00, 30.00, 100.00]:
                            print(f"      ✅ Preço real do banco: R$ {preco:.2f}")
                        else:
                            print(f"      ⚠️  Preço pode ser padrão: R$ {preco:.2f}")
                else:
                    print(f"   ⚠️  Nenhum produto encontrado para o tipo {tipo}")
                    
            else:
                print(f"   ❌ Erro na resposta: {response.status_code}")
                
        except Exception as e:
            print(f"   ❌ Erro ao chamar view: {str(e)}")
    
    print("\n" + "=" * 50)
    print("✅ TESTE CONCLUÍDO")

def teste_detalhes_produto():
    """Testa o endpoint de detalhes de produto"""
    
    factory = RequestFactory()
    user = User.objects.filter(is_superuser=True).first()
    
    if not user:
        print("❌ Erro: Usuário admin não encontrado")
        return
    
    print("\n🔍 TESTANDO ENDPOINT DE DETALHES DE PRODUTO")
    print("=" * 50)
    
    # Testar com diferentes tipos de produto
    testes = [
        ('cadeira', Cadeira, 'cadeira_'),
        ('banqueta', Banqueta, 'banqueta_'),
        ('poltrona', Poltrona, 'poltrona_'),
    ]
    
    for tipo_nome, modelo, prefixo in testes:
        print(f"\n📦 Testando detalhes de {tipo_nome.upper()}")
        
        # Buscar um produto deste tipo
        produto = modelo.objects.filter(ativo=True).first()
        
        if produto:
            produto_id = f"{prefixo}{produto.id}"
            
            # Criar request
            request = factory.get(f'/orcamentos/detalhes-produto/?produto_id={produto_id}')
            request.user = user
            
            try:
                # Chamar view
                response = obter_detalhes_produto(request)
                
                if response.status_code == 200:
                    data = json.loads(response.content)
                    produto_data = data.get('produto', {})
                    
                    nome = produto_data.get('nome', 'N/A')
                    ref = produto_data.get('ref', 'N/A')
                    preco = produto_data.get('preco', 0.00)
                    
                    print(f"   ✅ Produto: {nome}")
                    print(f"   📋 Referência: {ref}")
                    print(f"   💰 Preço: R$ {preco:.2f}")
                    print(f"   🔧 Tem módulos: {produto_data.get('tem_modulos', False)}")
                    
                else:
                    print(f"   ❌ Erro na resposta: {response.status_code}")
                    
            except Exception as e:
                print(f"   ❌ Erro ao chamar view: {str(e)}")
        else:
            print(f"   ⚠️  Nenhum produto do tipo {tipo_nome} encontrado")

def verificar_precos_banco():
    """Verifica se há produtos com preços no banco"""
    
    print("\n🔍 VERIFICANDO PREÇOS NO BANCO DE DADOS")
    print("=" * 50)
    
    modelos = [
        ('Cadeiras', Cadeira),
        ('Banquetas', Banqueta),
        ('Poltronas', Poltrona),
        ('Pufes', Pufe),
        ('Almofadas', Almofada),
        ('Acessórios', Acessorio),
    ]
    
    for nome, modelo in modelos:
        produtos = modelo.objects.filter(ativo=True)
        
        print(f"\n📦 {nome}:")
        print(f"   Total de produtos: {produtos.count()}")
        
        if produtos.exists():
            # Verificar produtos com preço
            com_preco = produtos.exclude(preco__isnull=True).exclude(preco=0)
            print(f"   Com preço definido: {com_preco.count()}")
            
            if com_preco.exists():
                produto_exemplo = com_preco.first()
                print(f"   Exemplo: {produto_exemplo.nome} - R$ {produto_exemplo.preco:.2f}")
            else:
                print(f"   ⚠️  Nenhum produto com preço definido")
        else:
            print(f"   ⚠️  Nenhum produto ativo encontrado")

if __name__ == "__main__":
    print("🧪 INICIANDO TESTES DOS ENDPOINTS DE PRODUTOS")
    print("=" * 60)
    
    # Executar testes
    verificar_precos_banco()
    teste_produtos_por_tipo()
    teste_detalhes_produto()
    
    print("\n" + "=" * 60)
    print("🎉 TODOS OS TESTES CONCLUÍDOS!")
    print("\n💡 Lembre-se:")
    print("   - Os preços agora são puxados diretamente do banco de dados")
    print("   - Produtos sem preço retornam R$ 0.00")
    print("   - Sofás podem ter preços calculados pelos módulos")
