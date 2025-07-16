#!/usr/bin/env python3
"""
Script de validação para verificar a implementação dos novos tipos de produto.
Executa testes básicos para garantir que tudo está funcionando corretamente.
"""

import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema_produtos.settings')
sys.path.append('/home/matas/projetos/Project')
django.setup()

from produtos.models import TipoItem, Poltrona, Pufe, Almofada

def test_tipos_produto():
    """Testa se os tipos de produto foram criados corretamente."""
    print("🔍 Testando tipos de produto...")
    
    tipos_esperados = ['Sofás', 'Acessórios', 'Cadeiras', 'Banquetas', 'Poltronas', 'Pufes', 'Almofadas']
    tipos_encontrados = []
    
    for tipo_nome in tipos_esperados:
        try:
            tipo = TipoItem.objects.get(nome=tipo_nome)
            tipos_encontrados.append(tipo_nome)
            print(f"  ✅ {tipo_nome} (ID: {tipo.id})")
        except TipoItem.DoesNotExist:
            print(f"  ❌ {tipo_nome} - NÃO ENCONTRADO")
    
    if len(tipos_encontrados) == len(tipos_esperados):
        print("✅ Todos os tipos de produto estão configurados corretamente!")
        return True
    else:
        print("❌ Alguns tipos de produto estão faltando!")
        return False

def test_modelos():
    """Testa se os novos modelos podem ser instanciados."""
    print("\n🔍 Testando novos modelos...")
    
    try:
        # Testar Poltrona
        poltrona = Poltrona(
            ref_poltrona="PT001",
            nome="Teste Poltrona",
            largura=70.0,
            profundidade=80.0,
            altura=110.0,
            tecido_metros=2.0,
            volume_m3=0.5,
            peso_kg=20.0,
            preco=1200.0,
            ativo=True
        )
        poltrona.clean()  # Validar sem salvar
        print("  ✅ Modelo Poltrona - OK")
        
        # Testar Pufe
        pufe = Pufe(
            ref_pufe="PF001",
            nome="Teste Pufe",
            largura=40.0,
            profundidade=40.0,
            altura=35.0,
            tecido_metros=0.8,
            volume_m3=0.2,
            peso_kg=6.0,
            preco=450.0,
            ativo=True
        )
        pufe.clean()  # Validar sem salvar
        print("  ✅ Modelo Pufe - OK")
        
        # Testar Almofada (sem profundidade)
        almofada = Almofada(
            ref_almofada="AL001",
            nome="Teste Almofada",
            largura=50.0,
            altura=30.0,  # Sem profundidade!
            tecido_metros=0.3,
            volume_m3=0.05,
            peso_kg=1.0,
            preco=120.0,
            ativo=True
        )
        almofada.clean()  # Validar sem salvar
        print("  ✅ Modelo Almofada - OK")
        
        print("✅ Todos os novos modelos funcionam corretamente!")
        return True
        
    except Exception as e:
        print(f"  ❌ Erro nos modelos: {e}")
        return False

def test_campos_especiais():
    """Testa se os campos especiais das almofadas estão funcionando."""
    print("\n🔍 Testando campos especiais das almofadas...")
    
    try:
        almofada = Almofada(
            ref_almofada="AL002",
            nome="Teste Almofada Especial",
            largura=60.0,
            altura=40.0,
            tecido_metros=0.4,
            volume_m3=0.06,
            peso_kg=1.2,
            preco=150.0,
            ativo=True
        )
        
        # Verificar formatação de dimensões (sem profundidade)
        dimensoes = almofada.get_dimensoes_formatadas()
        expected = "60.0 x 40.0"  # Sem profundidade
        
        if dimensoes == expected:
            print(f"  ✅ Formatação de dimensões: {dimensoes}")
        else:
            print(f"  ❌ Formatação incorreta: {dimensoes} (esperado: {expected})")
            return False
        
        print("✅ Campos especiais das almofadas funcionam corretamente!")
        return True
        
    except Exception as e:
        print(f"  ❌ Erro nos campos especiais: {e}")
        return False

def test_admin_registration():
    """Testa se os modelos estão registrados no admin."""
    print("\n🔍 Testando registro no admin...")
    
    from django.contrib import admin
    
    modelos_esperados = [Poltrona, Pufe, Almofada]
    
    for modelo in modelos_esperados:
        if modelo in admin.site._registry:
            print(f"  ✅ {modelo.__name__} registrado no admin")
        else:
            print(f"  ❌ {modelo.__name__} NÃO registrado no admin")
            return False
    
    print("✅ Todos os modelos estão registrados no admin!")
    return True

def main():
    """Executa todos os testes de validação."""
    print("🚀 Iniciando validação da implementação dos novos tipos de produto...")
    print("=" * 70)
    
    testes = [
        test_tipos_produto,
        test_modelos,
        test_campos_especiais,
        test_admin_registration
    ]
    
    resultados = []
    
    for teste in testes:
        try:
            resultado = teste()
            resultados.append(resultado)
        except Exception as e:
            print(f"❌ Erro inesperado no teste {teste.__name__}: {e}")
            resultados.append(False)
    
    print("\n" + "=" * 70)
    print("📊 RESUMO DOS TESTES:")
    
    if all(resultados):
        print("🎉 TODOS OS TESTES PASSARAM! ✅")
        print("   A implementação está funcionando corretamente.")
        return 0
    else:
        testes_falharam = sum(1 for r in resultados if not r)
        print(f"⚠️  {testes_falharam} TESTE(S) FALHARAM! ❌")
        print("   Verifique os erros acima e corrija antes de prosseguir.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
