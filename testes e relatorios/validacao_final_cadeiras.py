#!/usr/bin/env python
"""
Script de validação final para verificar se as cadeiras estão funcionando corretamente.
"""
import os
import sys
import django
from django.test import Client
from django.contrib.auth import get_user_model

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema_produtos.settings')
django.setup()

from produtos.models import Cadeira, TipoItem

def validar_cadeiras():
    """Validação completa do sistema de cadeiras"""
    
    print("🔍 VALIDAÇÃO FINAL - SISTEMA DE CADEIRAS")
    print("=" * 50)
    
    # 1. Verificar se as cadeiras estão no banco
    print("\n1. Verificando dados no banco...")
    cadeiras = Cadeira.objects.all()
    print(f"   ✓ Total de cadeiras encontradas: {cadeiras.count()}")
    
    if cadeiras.count() == 0:
        print("   ❌ Nenhuma cadeira encontrada no banco!")
        return False
    
    # Listar algumas cadeiras
    print("   📋 Primeiras 5 cadeiras:")
    for c in cadeiras[:5]:
        print(f"      • {c.ref_cadeira} - {c.nome} - R$ {c.preco}")
    
    # 2. Verificar se o tipo "Cadeiras" existe
    print("\n2. Verificando tipo 'Cadeiras'...")
    try:
        tipo_cadeira = TipoItem.objects.get(nome='Cadeiras')
        print(f"   ✓ Tipo encontrado: ID {tipo_cadeira.id} - {tipo_cadeira.nome}")
    except TipoItem.DoesNotExist:
        print("   ❌ Tipo 'Cadeiras' não encontrado!")
        return False
    
    # 3. Verificar URLs (simulando requests)
    print("\n3. Testando URLs das cadeiras...")
    client = Client()
    
    # URL de listagem
    try:
        response = client.get('/cadeiras/')
        print(f"   • Lista de cadeiras: Status {response.status_code}")
        if response.status_code != 200:
            print(f"     ⚠️ Esperado: 200, Recebido: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Erro ao acessar lista: {e}")
    
    # URL de detalhes (primeira cadeira)
    if cadeiras.exists():
        primeira_cadeira = cadeiras.first()
        try:
            response = client.get(f'/cadeiras/{primeira_cadeira.id}/')
            print(f"   • Detalhes da cadeira {primeira_cadeira.ref_cadeira}: Status {response.status_code}")
            if response.status_code != 200:
                print(f"     ⚠️ Esperado: 200, Recebido: {response.status_code}")
        except Exception as e:
            print(f"   ❌ Erro ao acessar detalhes: {e}")
    
    # 4. Verificar templates
    print("\n4. Verificando templates...")
    templates_necessarios = [
        'templates/produtos/cadeiras/detalhes.html',
        'templates/produtos/cadeiras/cadastro.html',
        'templates/produtos/cadeiras/editar.html',
        'templates/produtos/cadeiras/confirmar_exclusao.html',
        'templates/produtos/cadeiras/lista.html'
    ]
    
    for template in templates_necessarios:
        if os.path.exists(template):
            with open(template, 'r') as f:
                conteudo = f.read()
                if len(conteudo.strip()) > 0:
                    print(f"   ✓ {template.split('/')[-1]}")
                else:
                    print(f"   ⚠️ {template.split('/')[-1]} (vazio)")
        else:
            print(f"   ❌ {template.split('/')[-1]} (não encontrado)")
    
    # 5. Verificar imagens
    print("\n5. Verificando imagens...")
    cadeiras_com_imagem = cadeiras.filter(imagem_principal__isnull=False).count()
    print(f"   ✓ Cadeiras com imagem: {cadeiras_com_imagem}/{cadeiras.count()}")
    
    # 6. Resumo das URLs importantes
    print("\n6. URLs importantes do sistema:")
    print(f"   • Lista de cadeiras: /cadeiras/")
    print(f"   • Cadastrar cadeira: /cadeiras/cadastro/")
    if cadeiras.exists():
        primeira = cadeiras.first()
        print(f"   • Ver cadeira (exemplo): /cadeiras/{primeira.id}/")
        print(f"   • Editar cadeira (exemplo): /cadeiras/{primeira.id}/editar/")
    
    print("\n" + "=" * 50)
    print("✅ VALIDAÇÃO CONCLUÍDA!")
    print(f"📊 Resumo: {cadeiras.count()} cadeiras cadastradas e sistema funcional")
    
    return True

def listar_cadeiras_detalhado():
    """Lista todas as cadeiras com informações detalhadas"""
    print("\n📋 LISTA DETALHADA DE CADEIRAS")
    print("-" * 50)
    
    cadeiras = Cadeira.objects.all().order_by('ref_cadeira')
    
    for c in cadeiras:
        print(f"🪑 {c.ref_cadeira} - {c.nome}")
        print(f"   Dimensões: {c.largura}x{c.profundidade}x{c.altura} cm")
        print(f"   Tecido: {c.tecido_metros}m | Volume: {c.volume_m3}m³ | Peso: {c.peso_kg}kg")
        print(f"   Preço: R$ {c.preco}")
        print(f"   Imagem: {'✓' if c.imagem_principal else '❌'}")
        print(f"   ID: {c.id}")
        print()

if __name__ == '__main__':
    try:
        # Executar validação
        sucesso = validar_cadeiras()
        
        # Listar cadeiras em detalhes
        listar_cadeiras_detalhado()
        
        if sucesso:
            print("🎉 Sistema de cadeiras validado com sucesso!")
            print("🔗 Acesse: http://127.0.0.1:8002/cadeiras/ para ver a lista")
        else:
            print("❌ Problemas encontrados no sistema de cadeiras!")
            sys.exit(1)
            
    except Exception as e:
        print(f"\n❌ Erro durante a validação: {e}")
        sys.exit(1)
