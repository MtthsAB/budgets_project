#!/usr/bin/env python
"""
Teste completo do sistema de banquetas
"""
import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema_produtos.settings')
django.setup()

from produtos.models import TipoItem, Banqueta
from django.contrib.auth.models import User

def teste_banco_banquetas():
    print("=== Teste Completo do Sistema de Banquetas ===\n")
    
    # 1. Verificar se o tipo "Banquetas" existe
    print("1. Verificando tipo 'Banquetas' no banco...")
    try:
        tipo_banqueta = TipoItem.objects.get(nome='Banquetas')
        print(f"   ✓ Tipo encontrado: {tipo_banqueta.nome} (ID: {tipo_banqueta.id})")
    except TipoItem.DoesNotExist:
        print("   ✗ Tipo 'Banquetas' não encontrado!")
        return False
    
    # 2. Verificar se o modelo Banqueta está funcionando
    print("\n2. Testando modelo Banqueta...")
    try:
        # Criar uma banqueta de teste
        banqueta_teste = Banqueta(
            ref_banqueta='BQ_TESTE',
            nome='BANQUETA TESTE',
            largura=42.50,
            profundidade=50.99,
            altura=99.00,
            tecido_metros=0.90,
            volume_m3=0.24,
            peso_kg=8.00,
            preco=658.00,
            ativo=True,
            descricao='Banqueta criada para teste'
        )
        banqueta_teste.save()
        print(f"   ✓ Banqueta criada: {banqueta_teste}")
        
        # Testar o método de dimensões formatadas
        dimensoes = banqueta_teste.get_dimensoes_formatadas()
        print(f"   ✓ Dimensões formatadas: {dimensoes}")
        
        # Limpar teste
        banqueta_teste.delete()
        print("   ✓ Banqueta de teste removida")
        
    except Exception as e:
        print(f"   ✗ Erro ao testar modelo: {e}")
        return False
    
    # 3. Verificar banquetas existentes
    print("\n3. Listando banquetas existentes...")
    banquetas = Banqueta.objects.all()
    if banquetas.exists():
        for banqueta in banquetas:
            print(f"   - {banqueta.ref_banqueta}: {banqueta.nome}")
            print(f"     Dimensões: {banqueta.get_dimensoes_formatadas()}")
            print(f"     Preço: R$ {banqueta.preco}")
            print(f"     Ativa: {'Sim' if banqueta.ativo else 'Não'}")
    else:
        print("   Nenhuma banqueta cadastrada")
    
    # 4. Verificar imports das views
    print("\n4. Testando imports das views...")
    try:
        from produtos.views import banqueta_cadastro_view, banqueta_editar_view
        from produtos.forms import BanquetaForm
        print("   ✓ Views e forms importados com sucesso")
    except ImportError as e:
        print(f"   ✗ Erro ao importar: {e}")
        return False
    
    # 5. Testar formulário
    print("\n5. Testando formulário BanquetaForm...")
    try:
        form_data = {
            'ref_banqueta': 'BQ_FORM_TEST',
            'nome': 'TESTE FORMULÁRIO',
            'largura': 40.0,
            'profundidade': 45.0,
            'altura': 85.0,
            'tecido_metros': 0.8,
            'volume_m3': 0.2,
            'peso_kg': 7.5,
            'preco': 550.0,
            'ativo': True
        }
        
        form = BanquetaForm(data=form_data)
        if form.is_valid():
            print("   ✓ Formulário válido")
        else:
            print(f"   ✗ Formulário inválido: {form.errors}")
            return False
            
    except Exception as e:
        print(f"   ✗ Erro ao testar formulário: {e}")
        return False
    
    print("\n=== ✓ TODOS OS TESTES PASSARAM! ===")
    print("\nSistema de banquetas está funcionando corretamente:")
    print("• Banco de dados configurado")
    print("• Modelo Banqueta funcionando")
    print("• Formulários validando")
    print("• Views importando corretamente")
    print("\nPróximos passos:")
    print("• Testar cadastro via interface web")
    print("• Testar edição via interface web")
    print("• Validar fluxo completo")
    
    return True

if __name__ == '__main__':
    teste_banco_banquetas()
