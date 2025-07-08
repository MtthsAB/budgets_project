#!/usr/bin/env python
"""
Teste específico para validar funcionalidades de sofás e módulos.
"""

import os
import sys
import django
import json

# Configurar Django
sys.path.append('/home/matas/projetos/Project')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema_produtos.settings')
django.setup()

from django.test import RequestFactory
from django.contrib.auth import get_user_model
from orcamentos.views import produtos_por_tipo, obter_detalhes_produto
from produtos.models import Produto, TipoItem, Modulo, TamanhosModulosDetalhado

User = get_user_model()

def teste_sofas_completo():
    """Teste completo das funcionalidades de sofás"""
    
    print("🛋️ TESTE ESPECÍFICO PARA SOFÁS E MÓDULOS")
    print("=" * 50)
    
    factory = RequestFactory()
    user = User.objects.filter(is_superuser=True).first()
    
    if not user:
        print("❌ Erro: Usuário admin não encontrado")
        return
    
    # Teste 1: Verificar estrutura de sofás no banco
    print("\n1️⃣ VERIFICANDO ESTRUTURA DE SOFÁS")
    print("-" * 30)
    
    tipo_sofa = TipoItem.objects.filter(nome__icontains='Sofá').first()
    if tipo_sofa:
        print(f"✅ Tipo de sofá encontrado: {tipo_sofa.nome}")
        
        sofas = Produto.objects.filter(id_tipo_produto=tipo_sofa, ativo=True)
        print(f"📦 Sofás ativos: {sofas.count()}")
        
        for sofa in sofas:
            print(f"   🛋️ {sofa.ref_produto} - {sofa.nome_produto}")
            
            # Verificar módulos
            modulos = sofa.modulos.filter(ativo=True)
            print(f"      📦 Módulos: {modulos.count()}")
            
            for modulo in modulos:
                print(f"         • {modulo.nome}")
                tamanhos = modulo.tamanhos_detalhados.all()
                print(f"           Tamanhos: {tamanhos.count()}")
                
                for tamanho in tamanhos[:2]:  # Mostrar apenas os primeiros 2
                    preco = tamanho.preco if tamanho.preco else 0
                    largura = tamanho.largura_total if tamanho.largura_total else 'N/A'
                    print(f"             - Largura: {largura}cm, Preço: R$ {preco:.2f}")
    else:
        print("❌ Tipo de sofá não encontrado")
        return
    
    # Teste 2: Endpoint produtos por tipo para sofás
    print("\n2️⃣ TESTANDO ENDPOINT PRODUTOS POR TIPO - SOFÁS")
    print("-" * 40)
    
    request = factory.get('/orcamentos/produtos-por-tipo/?tipo=sofa')
    request.user = user
    
    try:
        response = produtos_por_tipo(request)
        if response.status_code == 200:
            data = json.loads(response.content)
            produtos = data.get('produtos', [])
            
            print(f"✅ Sofás retornados pelo endpoint: {len(produtos)}")
            
            for produto in produtos:
                print(f"   🛋️ {produto['nome_produto']} (Ref: {produto['ref_produto']})")
                print(f"      💰 Preço: R$ {produto['preco']:.2f}")
                print(f"      🔧 Tem módulos: {produto.get('tem_modulos', False)}")
                print(f"      📝 Descrição: {produto.get('descricao', 'N/A')}")
                
        else:
            print(f"❌ Erro no endpoint: {response.status_code}")
    except Exception as e:
        print(f"❌ Erro no teste: {str(e)}")
    
    # Teste 3: Endpoint detalhes de produto para sofá
    print("\n3️⃣ TESTANDO ENDPOINT DETALHES DE PRODUTO - SOFÁ")
    print("-" * 40)
    
    primeiro_sofa = sofas.first()
    if primeiro_sofa:
        produto_id = f"produto_{primeiro_sofa.id}"
        request = factory.get(f'/orcamentos/detalhes-produto/?produto_id={produto_id}')
        request.user = user
        
        try:
            response = obter_detalhes_produto(request)
            if response.status_code == 200:
                data = json.loads(response.content)
                produto = data.get('produto', {})
                
                print(f"✅ Detalhes carregados para: {produto.get('nome', 'N/A')}")
                print(f"   🏷️ Referência: {produto.get('ref', 'N/A')}")
                print(f"   🔧 Tem módulos: {produto.get('tem_modulos', False)}")
                print(f"   📝 Descrição: {produto.get('descricao', 'N/A')}")
                
                modulos = produto.get('modulos', [])
                print(f"   📦 Módulos disponíveis: {len(modulos)}")
                
                for modulo in modulos:
                    print(f"      • {modulo['nome']}")
                    tamanhos = modulo.get('tamanhos', [])
                    print(f"        Tamanhos: {len(tamanhos)}")
                    
                    for tamanho in tamanhos[:2]:  # Mostrar apenas os primeiros 2
                        largura = tamanho.get('largura_total', 'N/A')
                        preco = tamanho.get('preco', 0)
                        print(f"          - Largura: {largura}cm, Preço: R$ {preco:.2f}")
                        
            else:
                print(f"❌ Erro ao carregar detalhes: {response.status_code}")
        except Exception as e:
            print(f"❌ Erro no teste de detalhes: {str(e)}")
    
    # Teste 4: Validar estrutura JSON para frontend
    print("\n4️⃣ VALIDANDO ESTRUTURA JSON PARA FRONTEND")
    print("-" * 40)
    
    campos_esperados_produto = ['id', 'nome_produto', 'ref_produto', 'tipo', 'preco', 'tem_modulos']
    campos_esperados_modulo = ['id', 'nome', 'tamanhos']
    campos_esperados_tamanho = ['id', 'largura_total', 'preco']
    
    if produtos:
        produto_teste = produtos[0]
        print("📋 Validando estrutura do produto:")
        
        for campo in campos_esperados_produto:
            if campo in produto_teste:
                print(f"   ✅ Campo '{campo}' presente")
            else:
                print(f"   ❌ Campo '{campo}' ausente")
    
    print("\n" + "=" * 50)
    print("🎉 TESTE DE SOFÁS CONCLUÍDO!")
    
    # Resumo
    print(f"\n📊 RESUMO:")
    print(f"   🛋️ Sofás no banco: {sofas.count()}")
    print(f"   📦 Total de módulos: {sum(s.modulos.filter(ativo=True).count() for s in sofas)}")
    print(f"   📏 Total de tamanhos: {TamanhosModulosDetalhado.objects.count()}")
    print(f"   🔗 Endpoint funcionando: {'✅' if response.status_code == 200 else '❌'}")

if __name__ == "__main__":
    teste_sofas_completo()
