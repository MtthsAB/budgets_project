#!/usr/bin/env python3
"""
Script para testar a edição de sofá com múltiplos módulos e tamanhos.
"""

import os
import sys
import django
from decimal import Decimal
from django.test import RequestFactory
from django.contrib.sessions.middleware import SessionMiddleware
from django.contrib.messages.storage.fallback import FallbackStorage
from django.contrib.auth import get_user_model

# Configurar Django
sys.path.append('/home/matas/projetos/Project')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema_produtos.settings')
django.setup()

from produtos.models import TipoItem, Produto, Modulo, TamanhosModulosDetalhado
from produtos.views import sofa_editar_view

def debug_edicao_sofa():
    """Debugar edição de sofá"""
    
    # Buscar um sofá existente
    sofa = Produto.objects.filter(id_tipo_produto__nome__icontains='sofá').first()
    
    if not sofa:
        print("❌ Nenhum sofá encontrado para testar edição")
        return
    
    print(f"🛋️ Testando edição do sofá: {sofa.ref_produto} - {sofa.nome_produto}")
    
    # Ver estrutura atual
    modulos = sofa.modulos.all()
    print(f"📦 Módulos existentes: {modulos.count()}")
    
    for i, modulo in enumerate(modulos, 1):
        print(f"  - Módulo {i}: {modulo.nome}")
        tamanhos = modulo.tamanhos_detalhados.all()
        print(f"    • Tamanhos: {tamanhos.count()}")
        for j, tamanho in enumerate(tamanhos, 1):
            print(f"      · Tamanho {j}: {tamanho.largura_total}cm - R${tamanho.preco}")
    
    # Simular POST de edição com múltiplos módulos
    User = get_user_model()
    user = User.objects.filter(is_superuser=True).first()
    
    if not user:
        print("❌ Usuário admin não encontrado")
        return
    
    factory = RequestFactory()
    
    # Dados para edição - adicionar um módulo e modificar tamanhos
    post_data = {
        'ref_produto': sofa.ref_produto,
        'nome_produto': sofa.nome_produto,
        'tipo_produto': str(sofa.id_tipo_produto.id),
        'ativo': 'on',
        'tem_cor_tecido': 'on',
        
        # Módulos existentes + novo módulo
        'modulo_nome': ['Módulo A', 'Módulo B', 'Módulo C'],
        
        # Dados específicos dos módulos
        'modulo_profundidade_1': '85.0',
        'modulo_altura_1': '90.0', 
        'modulo_braco_1': '25.0',
        'modulo_descricao_1': 'Módulo A - editado',
        
        'modulo_profundidade_2': '85.0',
        'modulo_altura_2': '90.0',
        'modulo_braco_2': '25.0', 
        'modulo_descricao_2': 'Módulo B - editado',
        
        'modulo_profundidade_3': '85.0',
        'modulo_altura_3': '90.0',
        'modulo_braco_3': '25.0',
        'modulo_descricao_3': 'Módulo C - novo',
        
        # Tamanhos para módulo 1 (2 tamanhos)
        'tamanho_largura_total_1': ['200.0', '250.0'],
        'tamanho_largura_assento_1': ['180.0', '230.0'],
        'tamanho_tecido_1': ['3.5', '4.2'],
        'tamanho_volume_1': ['1.2', '1.8'],
        'tamanho_peso_1': ['45.0', '55.0'],
        'tamanho_preco_1': ['1500.00', '1800.00'],
        'tamanho_descricao_1': ['Tamanho 200cm', 'Tamanho 250cm'],
        
        # Tamanhos para módulo 2 (1 tamanho)
        'tamanho_largura_total_2': ['220.0'],
        'tamanho_largura_assento_2': ['200.0'],
        'tamanho_tecido_2': ['4.0'],
        'tamanho_volume_2': ['1.5'],
        'tamanho_peso_2': ['50.0'],
        'tamanho_preco_2': ['1700.00'],
        'tamanho_descricao_2': ['Tamanho único'],
        
        # Tamanhos para módulo 3 (3 tamanhos)
        'tamanho_largura_total_3': ['180.0', '210.0', '240.0'],
        'tamanho_largura_assento_3': ['160.0', '190.0', '220.0'],
        'tamanho_tecido_3': ['3.0', '3.8', '4.5'],
        'tamanho_volume_3': ['1.0', '1.3', '1.6'],
        'tamanho_peso_3': ['40.0', '48.0', '58.0'],
        'tamanho_preco_3': ['1400.00', '1650.00', '1900.00'],
        'tamanho_descricao_3': ['Pequeno', 'Médio', 'Grande'],
    }
    
    print(f"\n🔄 Simulando edição com:")
    print(f"   - {len(post_data['modulo_nome'])} módulos")
    print(f"   - Módulo 1: {len(post_data['tamanho_largura_total_1'])} tamanhos")
    print(f"   - Módulo 2: {len(post_data['tamanho_largura_total_2'])} tamanhos")
    print(f"   - Módulo 3: {len(post_data['tamanho_largura_total_3'])} tamanhos")
    
    # Contar antes
    modulos_antes = Modulo.objects.filter(produto=sofa).count()
    tamanhos_antes = TamanhosModulosDetalhado.objects.filter(id_modulo__produto=sofa).count()
    
    print(f"\n📊 Antes da edição:")
    print(f"   - Módulos: {modulos_antes}")
    print(f"   - Tamanhos: {tamanhos_antes}")
    
    # Criar requisição POST
    request = factory.post(f'/produtos/sofas/{sofa.id}/editar/', post_data)
    request.user = user
    
    # Adicionar sessão e mensagens
    middleware = SessionMiddleware(lambda req: None)
    middleware.process_request(request)
    request.session.save()
    
    messages = FallbackStorage(request)
    request._messages = messages
    
    try:
        # Executar edição
        response = sofa_editar_view(request, sofa.id)
        
        # Verificar resultados
        sofa.refresh_from_db()
        modulos_depois = Modulo.objects.filter(produto=sofa).count()
        tamanhos_depois = TamanhosModulosDetalhado.objects.filter(id_modulo__produto=sofa).count()
        
        print(f"\n📊 Depois da edição:")
        print(f"   - Módulos: {modulos_depois}")
        print(f"   - Tamanhos: {tamanhos_depois}")
        
        # Verificar módulos salvos
        modulos_salvos = sofa.modulos.all()
        print(f"\n✅ Módulos salvos:")
        total_tamanhos_salvos = 0
        
        for i, modulo in enumerate(modulos_salvos, 1):
            tamanhos = modulo.tamanhos_detalhados.all()
            total_tamanhos_salvos += tamanhos.count()
            print(f"   {i}. {modulo.nome} ({tamanhos.count()} tamanhos)")
            for j, tamanho in enumerate(tamanhos, 1):
                print(f"      • {j}. {tamanho.largura_total}cm - R${tamanho.preco}")
        
        # Verificações
        assert modulos_depois == 3, f"Esperado 3 módulos, encontrado {modulos_depois}"
        assert total_tamanhos_salvos == 6, f"Esperado 6 tamanhos total, encontrado {total_tamanhos_salvos}"
        
        print(f"\n🎉 SUCESSO! Edição funcionou corretamente")
        print(f"   ✅ Módulos: {modulos_depois}/3")
        print(f"   ✅ Tamanhos: {total_tamanhos_salvos}/6")
        
    except Exception as e:
        print(f"\n❌ ERRO na edição: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    debug_edicao_sofa()
