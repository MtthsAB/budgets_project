#!/usr/bin/env python3
"""
Script para testar o erro 500 na edição de produtos
"""
import os
import sys
import django

# Configurar o Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema_produtos.settings')
django.setup()

from produtos.models import Produto, TipoItem
from django.urls import reverse
from django.test import Client
from authentication.models import CustomUser

def main():
    """Testa a funcionalidade de edição de produtos"""
    
    print("=== TESTE DE EDIÇÃO DE PRODUTOS ===\n")
    
    # Criar cliente de teste
    client = Client()
    
    # Verificar se há usuários
    try:
        user = CustomUser.objects.filter(is_active=True).first()
        if not user:
            print("❌ Nenhum usuário ativo encontrado!")
            return
            
        print(f"✅ Usuário encontrado: {user.email}")
        
        # Login
        client.force_login(user)
        print("✅ Login realizado com sucesso")
        
    except Exception as e:
        print(f"❌ Erro no login: {e}")
        return
    
    # Verificar produtos disponíveis
    try:
        produtos = Produto.objects.all()[:3]  # Pegar apenas os primeiros 3 produtos
        print(f"✅ Produtos encontrados: {produtos.count()}")
        
        if not produtos:
            print("⚠️ Nenhum produto encontrado para testar")
            return
            
        # Testar cada produto
        for produto in produtos:
            print(f"\n--- Testando produto: {produto.ref_produto} - {produto.nome_produto} ---")
            print(f"Tipo: {produto.id_tipo_produto.nome if produto.id_tipo_produto else 'Sem tipo'}")
            
            # Tentar acessar a página de edição
            try:
                # Primeiro, testar a URL genérica
                url_generica = reverse('produto_editar', kwargs={'produto_id': produto.id})
                print(f"Testando URL genérica: {url_generica}")
                
                response = client.get(url_generica)
                print(f"Status da resposta: {response.status_code}")
                
                if response.status_code == 500:
                    print("❌ ERRO 500 encontrado!")
                    print("Detalhes do contexto:")
                    print(f"- ID do produto: {produto.id}")
                    print(f"- Tipo: {produto.id_tipo_produto}")
                    print(f"- Ativo: {produto.ativo}")
                    
                    # Tentar identificar URLs específicas por tipo
                    if produto.id_tipo_produto:
                        tipo_nome = produto.id_tipo_produto.nome.lower()
                        print(f"- Nome do tipo (lowercase): {tipo_nome}")
                        
                        try:
                            if 'sofá' in tipo_nome or 'sofa' in tipo_nome:
                                url_especifica = reverse('sofa_editar', kwargs={'sofa_id': produto.id})
                                print(f"Testando URL de sofá: {url_especifica}")
                                response_especifica = client.get(url_especifica)
                                print(f"Status da URL específica: {response_especifica.status_code}")
                                
                            elif 'acessório' in tipo_nome or 'acessorio' in tipo_nome:
                                url_especifica = reverse('acessorio_editar', kwargs={'acessorio_id': produto.id})
                                print(f"Testando URL de acessório: {url_especifica}")
                                response_especifica = client.get(url_especifica)
                                print(f"Status da URL específica: {response_especifica.status_code}")
                                
                        except Exception as e:
                            print(f"Erro ao testar URL específica: {e}")
                    
                elif response.status_code == 200:
                    print("✅ Página carregou com sucesso")
                    
                elif response.status_code == 404:
                    print("⚠️ Página não encontrada (404)")
                    
                else:
                    print(f"⚠️ Status inesperado: {response.status_code}")
                    
            except Exception as e:
                print(f"❌ Erro ao acessar página de edição: {e}")
                import traceback
                traceback.print_exc()
                
    except Exception as e:
        print(f"❌ Erro geral: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
