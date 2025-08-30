#!/usr/bin/env python
"""
Teste para verificar se os tamanhos dos módulos estão sendo salvos
"""
import os
import sys
import django

# Configurar Django
sys.path.append('/home/matas/projetos/Project')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema_produtos.settings')
django.setup()

from produtos.models import Produto, Modulo, TipoItem, TamanhosModulosDetalhado

def test_tamanhos_saving():
    """Teste para verificar se os tamanhos estão sendo salvos corretamente"""
    print("🧪 Testando salvamento de tamanhos dos módulos...")
    
    try:
        # Criar tipo sofá
        tipo_sofa, created = TipoItem.objects.get_or_create(
            nome='Sofás',
            defaults={'nome': 'Sofás'}
        )
        
        # Criar produto
        produto = Produto.objects.create(
            ref_produto='TEST_TAMANHOS_001',
            nome_produto='Sofá Teste Tamanhos',
            id_tipo_produto=tipo_sofa,
            ativo=True
        )
        print(f"✅ Produto criado: {produto.ref_produto}")
        
        # Criar módulo
        modulo = Modulo.objects.create(
            produto=produto,
            nome='Módulo Central',
            profundidade=85.0,
            altura=90.0,
            braco=25.0
        )
        print(f"✅ Módulo criado: {modulo.nome}")
        
        # Verificar se módulo foi salvo
        assert Modulo.objects.filter(id=modulo.id).exists()
        print(f"✅ Módulo confirmado no banco: ID {modulo.id}")
        
        # Criar tamanhos
        tamanhos_info = [
            {
                'largura_total': 200.0,
                'largura_assento': 180.0,
                'tecido_metros': 3.5,
                'volume_m3': 1.2,
                'peso_kg': 45.0,
                'preco': 1500.00,
                'descricao': 'Tamanho 200cm'
            },
            {
                'largura_total': 250.0,
                'largura_assento': 230.0,
                'tecido_metros': 4.2,
                'volume_m3': 1.8,
                'peso_kg': 55.0,
                'preco': 1800.00,
                'descricao': 'Tamanho 250cm'
            }
        ]
        
        print("🔄 Criando tamanhos detalhados...")
        tamanhos_criados = []
        
        for i, info in enumerate(tamanhos_info):
            print(f"  Criando tamanho {i+1}: {info['largura_total']}cm")
            
            tamanho = TamanhosModulosDetalhado(
                id_modulo=modulo,
                largura_total=info['largura_total'],
                largura_assento=info['largura_assento'],
                tecido_metros=info['tecido_metros'],
                volume_m3=info['volume_m3'],
                peso_kg=info['peso_kg'],
                preco=info['preco'],
                descricao=info['descricao']
            )
            tamanho.save()
            tamanhos_criados.append(tamanho)
            print(f"    ✅ Tamanho salvo com ID: {tamanho.id}")
        
        # Verificar se tamanhos foram salvos
        tamanhos_salvos = TamanhosModulosDetalhado.objects.filter(id_modulo=modulo)
        print(f"✅ Tamanhos encontrados no banco: {tamanhos_salvos.count()}")
        
        # Verificar relação via módulo
        tamanhos_via_modulo = modulo.tamanhos_detalhados.all()
        print(f"✅ Tamanhos via relação do módulo: {tamanhos_via_modulo.count()}")
        
        # Listar tamanhos
        for tamanho in tamanhos_via_modulo:
            print(f"  - {tamanho.largura_total}cm x {tamanho.largura_assento}cm: R$ {tamanho.preco}")
        
        # Verificar dados específicos
        assert tamanhos_salvos.count() == 2
        assert tamanhos_via_modulo.count() == 2
        
        primeiro_tamanho = tamanhos_salvos.first()
        print(f"✅ Primeiro tamanho - Largura: {primeiro_tamanho.largura_total}, Preço: {primeiro_tamanho.preco}")
        
        # Limpeza
        produto.delete()
        print("✅ Dados de teste removidos")
        
        print("\n🎉 TESTE DE TAMANHOS PASSOU!")
        print("💡 Os tamanhos estão sendo salvos corretamente a nível de código")
        return True
        
    except Exception as e:
        print(f"❌ ERRO no teste: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def debug_form_data_structure():
    """Simula a estrutura de dados que vem do formulário"""
    print("\n🔍 DEBUG: Estrutura esperada dos dados do formulário:")
    print("=" * 50)
    
    print("📝 Nomes dos campos esperados:")
    print("- modulo_nome: ['Módulo 1', 'Módulo 2']")
    print("- tamanho_nome_1: ['200cm', '250cm']")
    print("- tamanho_largura_total_1: ['200.0', '250.0']")
    print("- tamanho_largura_assento_1: ['180.0', '230.0']")
    print("- tamanho_tecido_1: ['3.5', '4.2']")
    print("- tamanho_volume_1: ['1.2', '1.8']")
    print("- tamanho_peso_1: ['45.0', '55.0']")
    print("- tamanho_preco_1: ['1500.00', '1800.00']")
    print("- tamanho_descricao_1: ['Tamanho 200cm', 'Tamanho 250cm']")
    print("\n💡 Se os dados não chegam nessa estrutura, os tamanhos não são salvos!")

if __name__ == "__main__":
    print("🚀 Verificando salvamento de tamanhos dos módulos...")
    print("=" * 60)
    
    success = test_tamanhos_saving()
    debug_form_data_structure()
    
    print("\n" + "=" * 60)
    if success:
        print("✅ TESTE PASSOU - Tamanhos funcionam a nível de código")
        print("💡 Se não funcionam no formulário, o problema é nos dados enviados pelo frontend")
    else:
        print("❌ TESTE FALHOU - Há problema no código de salvamento")
