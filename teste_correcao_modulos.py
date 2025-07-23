#!/usr/bin/env python
"""
Teste para verificar se a correção do bug dos módulos está funcionando
"""
import os
import sys
import django

# Configurar Django
sys.path.append('/home/matas/projetos/Project')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema_produtos.settings')
django.setup()

from produtos.models import Produto, Modulo, TipoItem, TamanhosModulosDetalhado
from django.contrib.auth.models import User

def test_modulo_creation():
    """Teste para verificar se módulos podem ser criados corretamente"""
    print("🧪 Testando criação de módulos...")
    
    try:
        # Criar ou buscar tipo de produto "sofás"
        tipo_sofa, created = TipoItem.objects.get_or_create(
            nome='Sofás',
            defaults={'nome': 'Sofás'}
        )
        print(f"✅ Tipo de produto: {tipo_sofa.nome}")
        
        # Criar produto de teste
        produto_teste = Produto.objects.create(
            ref_produto='TESTE_SOFA_001',
            nome_produto='Sofá Teste com Módulos',
            id_tipo_produto=tipo_sofa,
            ativo=True
        )
        print(f"✅ Produto criado: {produto_teste.ref_produto} - {produto_teste.nome_produto}")
        
        # Criar módulo de teste - AQUI ESTAVA O BUG
        modulo_teste = Modulo.objects.create(
            produto=produto_teste,  # Era 'item' antes da correção
            nome='Módulo Central',
            profundidade=80.5,
            altura=85.0,
            braco=20.0,
            descricao='Módulo central do sofá de teste'
        )
        print(f"✅ Módulo criado: {modulo_teste.nome}")
        
        # Criar tamanho detalhado para o módulo
        tamanho_teste = TamanhosModulosDetalhado.objects.create(
            id_modulo=modulo_teste,
            largura_total=200.0,
            largura_assento=180.0,
            tecido_metros=3.5,
            volume_m3=1.2,
            peso_kg=45.0,
            preco=1500.00,
            descricao='Tamanho padrão do módulo'
        )
        print(f"✅ Tamanho criado: {tamanho_teste.largura_total}cm de largura")
        
        # Verificar se as relações estão corretas
        assert produto_teste.modulos.count() == 1
        assert modulo_teste.tamanhos_detalhados.count() == 1
        
        print(f"✅ Produto tem {produto_teste.modulos.count()} módulo(s)")
        print(f"✅ Módulo tem {modulo_teste.tamanhos_detalhados.count()} tamanho(s)")
        
        # Limpeza - remover dados de teste
        produto_teste.delete()
        print("✅ Dados de teste removidos")
        
        print("\n🎉 TESTE PASSOU! O bug dos módulos foi corrigido com sucesso!")
        return True
        
    except Exception as e:
        print(f"❌ ERRO no teste: {str(e)}")
        print(f"❌ Tipo do erro: {type(e).__name__}")
        return False

def test_multiple_modules():
    """Teste para criar produto com múltiplos módulos"""
    print("\n🧪 Testando criação de produto com múltiplos módulos...")
    
    try:
        # Buscar tipo sofá
        tipo_sofa = TipoItem.objects.get(nome='Sofás')
        
        # Criar produto
        produto = Produto.objects.create(
            ref_produto='TESTE_MULTI_001',
            nome_produto='Sofá Multi-Módulos',
            id_tipo_produto=tipo_sofa,
            ativo=True
        )
        
        # Criar múltiplos módulos
        modulos_info = [
            {'nome': 'Módulo Esquerdo', 'profundidade': 80, 'altura': 85, 'braco': 25},
            {'nome': 'Módulo Central', 'profundidade': 85, 'altura': 85, 'braco': 0},
            {'nome': 'Módulo Direito', 'profundidade': 80, 'altura': 85, 'braco': 25}
        ]
        
        for info in modulos_info:
            modulo = Modulo.objects.create(
                produto=produto,
                nome=info['nome'],
                profundidade=info['profundidade'],
                altura=info['altura'],
                braco=info['braco']
            )
            print(f"✅ Criado: {modulo.nome}")
        
        print(f"✅ Produto criado com {produto.modulos.count()} módulos")
        
        # Limpeza
        produto.delete()
        print("✅ Dados de teste removidos")
        
        print("🎉 TESTE DE MÚLTIPLOS MÓDULOS PASSOU!")
        return True
        
    except Exception as e:
        print(f"❌ ERRO no teste de múltiplos módulos: {str(e)}")
        return False

if __name__ == "__main__":
    print("🚀 Iniciando testes de correção dos módulos...")
    print("=" * 50)
    
    # Executar testes
    test1_ok = test_modulo_creation()
    test2_ok = test_multiple_modules()
    
    print("\n" + "=" * 50)
    print("📊 RESUMO DOS TESTES:")
    print(f"✅ Teste básico de módulo: {'PASSOU' if test1_ok else 'FALHOU'}")
    print(f"✅ Teste múltiplos módulos: {'PASSOU' if test2_ok else 'FALHOU'}")
    
    if test1_ok and test2_ok:
        print("\n🎉 TODOS OS TESTES PASSARAM!")
        print("💡 O sistema agora pode cadastrar sofás com módulos sem problemas.")
    else:
        print("\n❌ ALGUNS TESTES FALHARAM!")
        print("💡 Verifique os erros acima para mais detalhes.")
