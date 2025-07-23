#!/usr/bin/env python
"""
Teste direto da lógica de salvamento de tamanhos
"""
import os
import sys
import django

# Configurar Django
sys.path.append('/home/matas/projetos/Project')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema_produtos.settings')
django.setup()

from produtos.models import Produto, Modulo, TipoItem, TamanhosModulosDetalhado
from django.contrib.auth import get_user_model

User = get_user_model()

def test_tamanhos_logic():
    """Teste direto da lógica de tamanhos sem passar pela view"""
    print("🧪 Testando lógica de salvamento de tamanhos diretamente")
    
    try:
        # Criar usuário
        user, created = User.objects.get_or_create(
            email='teste@teste.com',
            defaults={'first_name': 'Teste', 'last_name': 'User'}
        )
        
        # Buscar tipo sofá
        tipo_sofa, created = TipoItem.objects.get_or_create(
            nome='Sofás',
            defaults={'nome': 'Sofás'}
        )
        
        # Criar produto
        produto = Produto.objects.create(
            ref_produto='SF_TESTE_LOGIC_001',
            nome_produto='Sofá Teste Lógica',
            id_tipo_produto=tipo_sofa,
            ativo=True
        )
        print(f"✅ Produto criado: {produto.ref_produto}")
        
        # Criar módulos
        modulos_info = [
            {'nome': 'Módulo Esquerdo', 'profundidade': 85.0},
            {'nome': 'Módulo Direito', 'profundidade': 85.0}
        ]
        
        modulos_criados = []
        for info in modulos_info:
            modulo = Modulo.objects.create(
                produto=produto,
                nome=info['nome'],
                profundidade=info['profundidade'],
                altura=90.0,
                braco=25.0
            )
            modulos_criados.append(modulo)
            print(f"✅ Módulo criado: {modulo.nome}")
        
        # Simular dados de tamanhos como vêm do formulário
        tamanhos_data = {
            # Módulo 1 (índice 0 = modulo_id 1)
            'tamanho_largura_total_1': ['200.0', '250.0'],
            'tamanho_largura_assento_1': ['180.0', '230.0'],
            'tamanho_tecido_1': ['3.5', '4.2'],
            'tamanho_volume_1': ['1.2', '1.8'],
            'tamanho_peso_1': ['45.0', '55.0'],
            'tamanho_preco_1': ['1500.00', '1800.00'],
            'tamanho_descricao_1': ['Tamanho 200cm', 'Tamanho 250cm'],
            
            # Módulo 2 (índice 1 = modulo_id 2)
            'tamanho_largura_total_2': ['220.0'],
            'tamanho_largura_assento_2': ['200.0'],
            'tamanho_tecido_2': ['3.8'],
            'tamanho_volume_2': ['1.5'],
            'tamanho_peso_2': ['50.0'],
            'tamanho_preco_2': ['1650.00'],
            'tamanho_descricao_2': ['Tamanho único'],
        }
        
        print("🔄 Processando tamanhos...")
        
        # Aplicar a lógica corrigida
        for i, modulo in enumerate(modulos_criados):
            modulo_id = i + 1
            tamanhos_largura_total = tamanhos_data.get(f'tamanho_largura_total_{modulo_id}', [])
            
            print(f"  Módulo {modulo_id}: {len(tamanhos_largura_total)} tamanhos")
            
            if tamanhos_largura_total and any(largura.strip() for largura in tamanhos_largura_total):
                tamanhos_largura_assento = tamanhos_data.get(f'tamanho_largura_assento_{modulo_id}', [])
                tamanhos_tecido = tamanhos_data.get(f'tamanho_tecido_{modulo_id}', [])
                tamanhos_volume = tamanhos_data.get(f'tamanho_volume_{modulo_id}', [])
                tamanhos_peso = tamanhos_data.get(f'tamanho_peso_{modulo_id}', [])
                tamanhos_preco = tamanhos_data.get(f'tamanho_preco_{modulo_id}', [])
                tamanhos_descricao = tamanhos_data.get(f'tamanho_descricao_{modulo_id}', [])
                
                # Função auxiliar para converter valores
                def safe_float(value):
                    try:
                        return float(value) if value and value.strip() else None
                    except (ValueError, TypeError):
                        return None
                
                for j, largura_total in enumerate(tamanhos_largura_total):
                    if largura_total and largura_total.strip():
                        print(f"    Criando tamanho {j+1}: {largura_total}cm")
                        
                        tamanho_detalhado = TamanhosModulosDetalhado(
                            id_modulo=modulo,
                            largura_total=safe_float(largura_total),
                            largura_assento=safe_float(tamanhos_largura_assento[j] if j < len(tamanhos_largura_assento) else None),
                            tecido_metros=safe_float(tamanhos_tecido[j] if j < len(tamanhos_tecido) else None),
                            volume_m3=safe_float(tamanhos_volume[j] if j < len(tamanhos_volume) else None),
                            peso_kg=safe_float(tamanhos_peso[j] if j < len(tamanhos_peso) else None),
                            preco=safe_float(tamanhos_preco[j] if j < len(tamanhos_preco) else None),
                            descricao=tamanhos_descricao[j] if j < len(tamanhos_descricao) and tamanhos_descricao[j] else None
                        )
                        tamanho_detalhado.save()
                        print(f"      ✅ Salvo: ID {tamanho_detalhado.id}, Preço: R${tamanho_detalhado.preco}")
        
        # Verificar resultados
        total_modulos = produto.modulos.count()
        total_tamanhos = sum(modulo.tamanhos_detalhados.count() for modulo in produto.modulos.all())
        
        print(f"📊 RESULTADOS:")
        print(f"  - Módulos criados: {total_modulos}")
        print(f"  - Tamanhos criados: {total_tamanhos}")
        
        # Listar detalhes
        for modulo in produto.modulos.all():
            tamanhos = modulo.tamanhos_detalhados.all()
            print(f"  - {modulo.nome}: {tamanhos.count()} tamanhos")
            for tamanho in tamanhos:
                print(f"    * {tamanho.largura_total}cm x {tamanho.largura_assento}cm - R${tamanho.preco}")
        
        # Verificações
        expected_tamanhos = 3  # 2 do módulo 1 + 1 do módulo 2
        assert total_modulos == 2, f"Esperado 2 módulos, encontrado {total_modulos}"
        assert total_tamanhos == expected_tamanhos, f"Esperado {expected_tamanhos} tamanhos, encontrado {total_tamanhos}"
        
        # Limpeza
        produto.delete()
        print("✅ Dados de teste removidos")
        
        print("\n🎉 TESTE DE LÓGICA PASSOU!")
        print("💡 A lógica de salvamento está funcionando corretamente!")
        return True
        
    except Exception as e:
        print(f"❌ ERRO: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("🚀 Testando lógica de tamanhos diretamente")
    print("=" * 50)
    
    success = test_tamanhos_logic()
    
    print("\n" + "=" * 50)
    if success:
        print("✅ LÓGICA FUNCIONA!")
        print("💡 O problema deve estar na estrutura dos dados do formulário")
    else:
        print("❌ PROBLEMA NA LÓGICA!")
        print("💡 Verifique os erros acima")
