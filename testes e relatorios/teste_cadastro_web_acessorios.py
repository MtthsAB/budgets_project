#!/usr/bin/env python
"""
Script para testar o cadastro de sofá com acessórios via interface web
"""

import os
import sys
import django

# Configurar Django
sys.path.append('/home/matas/projetos/Project')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema_produtos.settings')
django.setup()

from django.test import Client
from django.contrib.auth import get_user_model
from produtos.models import Produto, TipoItem, Acessorio, SofaAcessorio

def teste_cadastro_sofa_com_acessorios():
    """Teste do cadastro de sofá com acessórios via POST"""
    
    print("=== TESTE: Cadastro de Sofá com Acessórios via Web ===\n")
    
    # Configurar cliente e usuário
    client = Client()
    User = get_user_model()
    
    # Buscar ou criar usuário admin
    user = User.objects.filter(is_superuser=True).first()
    if not user:
        user = User.objects.create_superuser('admin', 'admin@test.com', 'admin123')
    
    # Fazer login
    client.force_login(user)
    print(f"✅ Login realizado com usuário: {user.email}")
    
    # Obter dados necessários
    tipo_sofa = TipoItem.objects.filter(nome__icontains='sofá').first()
    acessorios = list(Acessorio.objects.filter(ativo=True)[:2])  # Primeiros 2 acessórios
    
    print(f"✅ Tipo sofá: {tipo_sofa}")
    print(f"✅ Acessórios para teste: {[a.nome for a in acessorios]}")
    
    # Dados do POST para criar sofá com acessórios
    post_data = {
        # Dados básicos do produto
        'ref_produto': 'SF_TEST_001',
        'nome_produto': 'Sofá Teste com Acessórios',
        'tipo_produto': tipo_sofa.id,
        'ativo': 'on',
        
        # Campos específicos do sofá
        'tem_cor_tecido': 'on',
        'tem_difer_desenho_lado': '',
        'tem_difer_desenho_tamanho': 'on',
        
        # Management forms do formset de acessórios
        'acessorios-TOTAL_FORMS': '2',
        'acessorios-INITIAL_FORMS': '0',
        'acessorios-MIN_NUM_FORMS': '0',
        'acessorios-MAX_NUM_FORMS': '1000',
        
        # Acessório 1
        'acessorios-0-acessorio': acessorios[0].id,
        'acessorios-0-quantidade': '1',
        'acessorios-0-observacoes': 'Teste acessório 1',
        'acessorios-0-DELETE': '',
        
        # Acessório 2
        'acessorios-1-acessorio': acessorios[1].id,
        'acessorios-1-quantidade': '3',
        'acessorios-1-observacoes': 'Teste acessório 2 com mais quantidade',
        'acessorios-1-DELETE': '',
    }
    
    print("\n🔄 Enviando dados para cadastro...")
    
    # Fazer POST para cadastro
    response = client.post('/produtos/cadastro/', post_data)
    
    print(f"✅ Status da resposta: {response.status_code}")
    
    if response.status_code == 302:  # Redirect após sucesso
        print("✅ Redirect detectado (sucesso esperado)")
        
        # Verificar se o produto foi criado
        produto_criado = Produto.objects.filter(ref_produto='SF_TEST_001').first()
        if produto_criado:
            print(f"✅ Produto criado: {produto_criado}")
            
            # Verificar vinculações de acessórios
            vinculacoes = SofaAcessorio.objects.filter(sofa=produto_criado)
            print(f"✅ Vinculações criadas: {vinculacoes.count()}")
            
            for vinc in vinculacoes:
                print(f"   - {vinc.acessorio.nome}: Qtd {vinc.quantidade}")
                if vinc.observacoes:
                    print(f"     Obs: {vinc.observacoes}")
                    
            # Limpeza - remover produto de teste
            print("\n🧹 Limpando dados de teste...")
            vinculacoes.delete()
            produto_criado.delete()
            print("✅ Dados de teste removidos")
            
        else:
            print("❌ Produto não foi criado!")
            return False
            
    else:
        print("❌ Erro no cadastro!")
        print(f"Content: {response.content.decode()[:500]}...")
        return False
    
    print("\n=== TESTE CONCLUÍDO COM SUCESSO! ===")
    return True

if __name__ == "__main__":
    sucesso = teste_cadastro_sofa_com_acessorios()
    sys.exit(0 if sucesso else 1)
