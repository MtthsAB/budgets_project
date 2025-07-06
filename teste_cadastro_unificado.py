#!/usr/bin/env python
"""
Teste do fluxo de cadastro de banquetas via sistema unificado
"""
import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema_produtos.settings')
django.setup()

from django.test import Client
from django.contrib.auth.models import User
from produtos.models import TipoItem, Banqueta

def teste_cadastro_banqueta_unificado():
    print("=== Teste de Cadastro Banqueta via Sistema Unificado ===\n")
    
    # Criar cliente de teste
    client = Client()
    
    # Obter ou criar usuário de teste
    try:
        user = User.objects.get(username='admin')
    except User.DoesNotExist:
        user = User.objects.create_user('admin', 'admin@test.com', 'admin123')
        print("✓ Usuário admin criado para teste")
    
    # Login
    client.login(username='admin', password='admin123')
    
    # Obter ID do tipo Banquetas
    tipo_banqueta = TipoItem.objects.get(nome='Banquetas')
    print(f"✓ Tipo Banquetas encontrado (ID: {tipo_banqueta.id})")
    
    # Dados para cadastrar banqueta
    dados_banqueta = {
        'ref_produto': 'BQ_TESTE_UNIF',
        'nome_produto': 'BANQUETA TESTE UNIFICADO',
        'tipo_produto': tipo_banqueta.id,
        'ativo_banqueta': 'on',
        'largura_banqueta': '50.00',
        'profundidade_banqueta': '55.00',
        'altura_banqueta': '95.00',
        'tecido_metros_banqueta': '1.20',
        'volume_m3_banqueta': '0.30',
        'peso_kg_banqueta': '9.50',
        'preco_banqueta': '750.00',
        'descricao_banqueta': 'Banqueta criada via sistema unificado para teste'
    }
    
    print("✓ Dados preparados para cadastro")
    
    # Verificar se banqueta já existe e remover se necessário
    banquetas_existentes = Banqueta.objects.filter(ref_banqueta='BQ_TESTE_UNIF')
    if banquetas_existentes.exists():
        banquetas_existentes.delete()
        print("✓ Banqueta de teste anterior removida")
    
    print("\n--- Simulando POST para cadastro ---")
    
    # Fazer POST para a view de cadastro
    response = client.post('/produtos/cadastro/', dados_banqueta, follow=True)
    
    print(f"Status da resposta: {response.status_code}")
    
    if response.status_code == 200:
        # Verificar se banqueta foi criada
        try:
            banqueta_criada = Banqueta.objects.get(ref_banqueta='BQ_TESTE_UNIF')
            print(f"✓ Banqueta criada com sucesso!")
            print(f"  - Referência: {banqueta_criada.ref_banqueta}")
            print(f"  - Nome: {banqueta_criada.nome}")
            print(f"  - Dimensões: {banqueta_criada.get_dimensoes_formatadas()}")
            print(f"  - Preço: R$ {banqueta_criada.preco}")
            print(f"  - Ativa: {'Sim' if banqueta_criada.ativo else 'Não'}")
            
            # Limpar teste
            banqueta_criada.delete()
            print("✓ Banqueta de teste removida")
            
            return True
            
        except Banqueta.DoesNotExist:
            print("✗ Banqueta não foi criada")
            print("Possíveis problemas:")
            print("- View não está processando banquetas corretamente")
            print("- Dados não estão sendo enviados corretamente")
            print("- Redirecionamento está ocorrendo antes da criação")
            return False
    else:
        print(f"✗ Erro na requisição: {response.status_code}")
        return False

def teste_listagem_banquetas():
    print("\n=== Teste de Listagem de Banquetas ===")
    
    client = Client()
    user = User.objects.get(username='admin')
    client.login(username='admin', password='admin123')
    
    # Testar listagem específica de banquetas
    response = client.get('/banquetas/')
    print(f"Status da listagem de banquetas: {response.status_code}")
    
    if response.status_code == 200:
        print("✓ Página de listagem de banquetas acessível")
        return True
    else:
        print("✗ Erro ao acessar listagem de banquetas")
        return False

if __name__ == '__main__':
    success = teste_cadastro_banqueta_unificado()
    success &= teste_listagem_banquetas()
    
    if success:
        print("\n=== ✓ SISTEMA TOTALMENTE FUNCIONAL! ===")
        print("\nFluxo completo testado com sucesso:")
        print("• Cadastro via sistema unificado")
        print("• Criação na tabela Banqueta")
        print("• Redirecionamento correto")
        print("• Listagem funcionando")
    else:
        print("\n=== ✗ PROBLEMAS ENCONTRADOS ===")
        print("Verifique os logs acima para detalhes")
