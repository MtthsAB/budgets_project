#!/usr/bin/env python3
"""
Script para testar a hidratação - versão simplificada
"""

import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema_produtos.settings')
django.setup()

from authentication.models import CustomUser
from orcamentos.models import Orcamento
import requests
import re
import json

def criar_usuario_teste():
    """Cria um usuário de teste se não existir"""
    
    try:
        user = CustomUser.objects.get(email='teste@teste.com')
        print(f"✅ Usuário teste já existe: {user.email}")
        return user
    except CustomUser.DoesNotExist:
        print("👤 Criando usuário de teste...")
        user = CustomUser.objects.create_user(
            email='teste@teste.com',
            password='123456',
            first_name='Teste',
            last_name='Sistema',
            tipo_permissao='admin'
        )
        print(f"✅ Usuário criado: {user.email}")
        return user

def fazer_login_programatico():
    """Faz login programaticamente através do Django"""
    
    from django.test import Client
    from django.contrib.auth import authenticate
    
    # Autenticar usuário
    user = authenticate(email='teste@teste.com', password='123456')
    if not user:
        print("❌ Falha na autenticação")
        return None
        
    print(f"✅ Usuário autenticado: {user.email}")
    
    # Criar cliente de teste
    client = Client()
    client.force_login(user)
    
    return client

def teste_hidratacao_django():
    """Teste usando o cliente Django"""
    
    print("🧪 === TESTE DE HIDRATAÇÃO COM DJANGO CLIENT ===")
    
    # Criar usuário se necessário
    user = criar_usuario_teste()
    
    # Fazer login
    client = fazer_login_programatico()
    if not client:
        return False
    
    # Verificar se existe orçamento para testar
    orcamento = Orcamento.objects.filter(cliente__isnull=False).first()
    if not orcamento:
        print("❌ Nenhum orçamento encontrado para teste")
        return False
    
    print(f"📋 Testando orçamento ID: {orcamento.id}")
    
    # Acessar página de edição
    response = client.get(f'/orcamentos/{orcamento.id}/editar/')
    
    if response.status_code != 200:
        print(f"❌ Erro ao acessar página: {response.status_code}")
        return False
        
    print("✅ Página acessada com sucesso")
    
    content = response.content.decode('utf-8')
    
    # Verificar payload
    if 'window.orcamentoData' in content:
        print("✅ Payload de dados encontrado")
        
        # Extrair JSON
        pattern = r'window\.orcamentoData = ({.*?});'
        match = re.search(pattern, content, re.DOTALL)
        
        if match:
            json_str = match.group(1)
            try:
                orcamento_data = json.loads(json_str)
                print("✅ JSON parseado com sucesso")
                
                print(f"\n📋 DADOS EXTRAÍDOS:")
                for key, value in orcamento_data.items():
                    print(f"   {key}: {value}")
                
                # Verificar dados específicos
                print(f"\n🎯 VALIDAÇÃO DOS DADOS:")
                
                if orcamento_data.get('cliente_id') == orcamento.cliente.id:
                    print("✅ Cliente ID correto")
                else:
                    print("❌ Cliente ID incorreto")
                    
                if orcamento_data.get('cliente_nome') == orcamento.cliente.nome_empresa:
                    print("✅ Cliente nome correto")
                else:
                    print("❌ Cliente nome incorreto")
                
                # Verificar desconto/acréscimo
                desc_valor = float(orcamento.desconto_valor) if orcamento.desconto_valor else 0
                desc_perc = float(orcamento.desconto_percentual) if orcamento.desconto_percentual else 0
                acr_valor = float(orcamento.acrescimo_valor) if orcamento.acrescimo_valor else 0
                acr_perc = float(orcamento.acrescimo_percentual) if orcamento.acrescimo_percentual else 0
                
                if orcamento_data.get('desconto_valor') == desc_valor:
                    print("✅ Desconto valor correto")
                else:
                    print(f"❌ Desconto valor incorreto: esperado {desc_valor}, obtido {orcamento_data.get('desconto_valor')}")
                    
                if orcamento_data.get('desconto_percentual') == desc_perc:
                    print("✅ Desconto percentual correto")
                else:
                    print(f"❌ Desconto percentual incorreto: esperado {desc_perc}, obtido {orcamento_data.get('desconto_percentual')}")
                
                # Determinar que tipo de desconto deve aparecer
                if desc_valor > 0:
                    print(f"💡 Desconto deve aparecer como: {desc_valor} R$")
                elif desc_perc > 0:
                    print(f"💡 Desconto deve aparecer como: {desc_perc} %")
                else:
                    print("💡 Nenhum desconto definido")
                    
                if acr_valor > 0:
                    print(f"💡 Acréscimo deve aparecer como: {acr_valor} R$")
                elif acr_perc > 0:
                    print(f"💡 Acréscimo deve aparecer como: {acr_perc} %")
                else:
                    print("💡 Nenhum acréscimo definido")
                    
            except json.JSONDecodeError as e:
                print(f"❌ Erro ao parsear JSON: {e}")
                print(f"JSON bruto: {json_str[:500]}...")
        else:
            print("❌ Não foi possível extrair JSON")
    else:
        print("❌ Payload não encontrado")
    
    # Verificar elementos HTML
    print(f"\n🔍 VERIFICANDO ELEMENTOS HTML:")
    
    elementos = [
        ('id="cliente-busca"', 'Campo de busca do cliente'),
        ('id="desconto_valor_unificado"', 'Campo unificado de desconto'),
        ('id="acrescimo_valor_unificado"', 'Campo unificado de acréscimo'),
        ('id="desconto_tipo_btn"', 'Botão de tipo do desconto'),
        ('id="acrescimo_tipo_btn"', 'Botão de tipo do acréscimo'),
    ]
    
    for elemento, descricao in elementos:
        if elemento in content:
            print(f"   ✅ {descricao}")
        else:
            print(f"   ❌ {descricao}")
    
    # Verificar funções JavaScript
    print(f"\n🔍 VERIFICANDO FUNÇÕES JAVASCRIPT:")
    
    funcoes = [
        ('hidratarCamposOrcamento', 'Função principal de hidratação'),
        ('hidratarDescontoAcrescimo', 'Função específica desc/acr'),
        ('atualizarBotaoTipo', 'Função de atualizar botão'),
        ('hidratarCamposOrcamento();', 'Chamada da hidratação'),
    ]
    
    for funcao, descricao in funcoes:
        if funcao in content:
            print(f"   ✅ {descricao}")
        else:
            print(f"   ❌ {descricao}")
    
    # Salvar para debug
    with open('/tmp/orcamento_debug.html', 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"\n💾 Página salva para debug: /tmp/orcamento_debug.html")
    
    return True

if __name__ == '__main__':
    sucesso = teste_hidratacao_django()
    if sucesso:
        print("\n🎉 TESTE CONCLUÍDO!")
        print("\n📝 PASSOS PARA TESTE MANUAL:")
        print("   1. Login: teste@teste.com / 123456")
        print("   2. Acesse a página de edição do orçamento")
        print("   3. Verifique se os campos estão preenchidos")
        print("   4. Teste a alternância R$ ↔ %")
    else:
        print("\n❌ TESTE FALHOU")
