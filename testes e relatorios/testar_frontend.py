#!/usr/bin/env python3
"""
Script para testar especificamente os problemas de JavaScript/Frontend
"""
import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema_produtos.settings')
django.setup()

from django.test import Client
from django.contrib.auth import get_user_model
from orcamentos.models import Orcamento
import re

User = get_user_model()

def testar_frontend():
    print("🎨 TESTANDO PROBLEMAS DE FRONTEND")
    print("=" * 50)
    
    # Preparar dados
    client = Client()
    user = User.objects.filter(is_superuser=True).first()
    client.force_login(user)
    
    # Buscar último orçamento criado
    orcamento = Orcamento.objects.order_by('-created_at').first()
    
    print(f"📋 Testando com orçamento ID {orcamento.pk}")
    
    # Teste 1: Verificar se as páginas carregam sem erros críticos
    print(f"\n1️⃣ VERIFICAÇÃO: Páginas carregam corretamente")
    
    urls_teste = [
        ('/orcamentos/novo/', 'Novo orçamento'),
        (f'/orcamentos/{orcamento.pk}/editar/', 'Editar orçamento'),
    ]
    
    for url, nome in urls_teste:
        response = client.get(url)
        if response.status_code == 200:
            print(f"  ✅ {nome}: Carregou (200)")
        else:
            print(f"  ❌ {nome}: Erro {response.status_code}")
    
    # Teste 2: Verificar estrutura do JavaScript na página novo
    print(f"\n2️⃣ ANÁLISE: JavaScript na página NOVO")
    response = client.get('/orcamentos/novo/')
    content = response.content.decode('utf-8')
    
    # Verificar problemas específicos encontrados anteriormente
    problemas_js = [
        ('Template literals não processados', r'\$\{[^}]+\}'),
        ('Elementos com IDs inválidos', r'id="\$\{[^}]+\}"'),
        ('Referências a variáveis undefined', r'typeof [^=]+ !== [\'"]undefined[\'"]'),
    ]
    
    for nome, pattern in problemas_js:
        matches = re.findall(pattern, content)
        if matches:
            print(f"  ❌ {nome}: {len(matches)} ocorrências")
            for match in matches[:3]:  # Mostrar só as primeiras 3
                print(f"    - {match}")
        else:
            print(f"  ✅ {nome}: OK")
    
    # Teste 3: Verificar se campos críticos estão presentes e com IDs corretos
    print(f"\n3️⃣ VERIFICAÇÃO: Campos críticos na página NOVO")
    
    campos_criticos = [
        ('cliente-busca', 'Campo de busca do cliente'),
        ('id_cliente', 'Select do cliente'),
        ('desconto_valor_unificado', 'Campo unificado de desconto'),
        ('desconto_tipo_btn', 'Botão de tipo de desconto'),
        ('acrescimo_valor_unificado', 'Campo unificado de acréscimo'),
        ('acrescimo_tipo_btn', 'Botão de tipo de acréscimo'),
    ]
    
    for id_campo, desc in campos_criticos:
        if f'id="{id_campo}"' in content:
            print(f"  ✅ {desc}: Presente")
        else:
            print(f"  ❌ {desc}: AUSENTE")
    
    # Teste 4: Verificar hidratação na página de edição
    print(f"\n4️⃣ VERIFICAÇÃO: Hidratação na página EDITAR")
    response = client.get(f'/orcamentos/{orcamento.pk}/editar/')
    content = response.content.decode('utf-8')
    
    verificacoes_edicao = [
        (f'window.orcamentoPk = {orcamento.pk}', 'ID do orçamento'),
        ('window.orcamentoData = {', 'Início dos dados JSON'),
        ('"cliente_id":', 'Campo cliente_id no JSON'),
        ('"status":', 'Campo status no JSON'),
        ('hidratarCamposOrcamento()', 'Chamada da função de hidratação'),
    ]
    
    for busca, desc in verificacoes_edicao:
        if busca in content:
            print(f"  ✅ {desc}: Presente")
        else:
            print(f"  ❌ {desc}: AUSENTE")
    
    # Teste 5: Verificar se há console.log para debug
    print(f"\n5️⃣ DEBUG: Verificar logs de debug")
    
    logs_debug = [
        ('console.log(\'DOM carregado', 'Log de inicialização'),
        ('console.log(\'Dados do orçamento carregados', 'Log dos dados do orçamento'),
        ('console.log(\'=== INICIANDO HIDRATAÇÃO', 'Log de início da hidratação'),
        ('console.log(\'Inicializando campos unificados', 'Log dos campos unificados'),
    ]
    
    for busca, desc in logs_debug:
        if busca in content:
            print(f"  ✅ {desc}: Presente")
        else:
            print(f"  ❌ {desc}: AUSENTE")
    
    # Teste 6: Procurar por erros óbvios no HTML
    print(f"\n6️⃣ VERIFICAÇÃO: Erros óbvios no HTML")
    
    # Response da página de edição
    response = client.get(f'/orcamentos/{orcamento.pk}/editar/')
    content = response.content.decode('utf-8')
    
    erros_obvios = [
        ('<script></script>', 'Scripts vazios'),
        ('undefined', 'Strings "undefined"'),
        ('null.', 'Acessos a null'),
        ('NaN', 'Valores NaN'),
        ('${', 'Template literals não processados'),
    ]
    
    for busca, desc in erros_obvios:
        count = content.count(busca)
        if count > 0:
            print(f"  ⚠️  {desc}: {count} ocorrências")
        else:
            print(f"  ✅ {desc}: OK")
    
    print(f"\n" + "=" * 50)
    print("🎨 ANÁLISE DE FRONTEND CONCLUÍDA")

if __name__ == '__main__':
    testar_frontend()
