#!/usr/bin/env python
"""
Script para testar POST para edição de produto via programação
"""
import os
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema_produtos.settings')
django.setup()

from django.test import Client
from django.contrib.auth import get_user_model
from produtos.models import Item, TipoItem, Modulo

User = get_user_model()

def test_post_edicao():
    """Teste POST para edição de produto"""
    print("=== TESTE POST EDIÇÃO ===")
    
    # Buscar produto
    produto = Item.objects.first()
    if not produto:
        print("❌ Nenhum produto encontrado")
        return
    
    print(f"🔍 Testando produto: {produto.ref_produto}")
    
    # Criar cliente de teste
    client = Client()
    
    # Simular usuário logado (usar email como identificador)
    user, created = User.objects.get_or_create(
        email='test@example.com',
        defaults={'first_name': 'Test', 'last_name': 'User'}
    )
    if created:
        user.set_password('testpass')
        user.save()
    
    client.force_login(user)
    
    # Dados de teste para edição
    data = {
        'ref_produto': produto.ref_produto,
        'nome_produto': produto.nome_produto,
        'tipo_produto': produto.id_tipo_produto.id,
        'ativo': 'on',
        'tem_cor_tecido': '',
        'tem_difer_desenho_lado': '',
        'tem_difer_desenho_tamanho': '',
        # Teste de módulo
        'modulo_nome_1': 'Módulo Teste',
        'modulo_profundidade_1': '80.0',
        'modulo_altura_1': '85.0',
        'modulo_braco_1': '25.0',
        'modulo_descricao_1': 'Descrição teste',
    }
    
    print("📤 Enviando dados POST...")
    print(f"   Dados: {data}")
    
    # Enviar POST
    response = client.post(f'/produtos/{produto.id}/editar/', data)
    
    print(f"📨 Status da resposta: {response.status_code}")
    
    if response.status_code == 302:
        print(f"✅ Redirecionamento para: {response.url}")
        
        # Verificar se módulo foi criado
        produto_atualizado = Item.objects.get(id=produto.id)
        modulos_count = produto_atualizado.modulos.count()
        print(f"📦 Módulos após edição: {modulos_count}")
        
        if modulos_count > 0:
            modulo = produto_atualizado.modulos.first()
            print(f"   ✅ Primeiro módulo: {modulo.nome}")
            print(f"   ✅ Profundidade: {modulo.profundidade}")
            print(f"   ✅ Altura: {modulo.altura}")
            print(f"   ✅ Braço: {modulo.braco}")
        
    else:
        print(f"❌ Erro no envio: {response.content.decode()[:500]}")
    
    print("\n=== TESTE CONCLUÍDO ===")

if __name__ == "__main__":
    test_post_edicao()
