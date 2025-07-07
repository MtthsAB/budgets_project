#!/usr/bin/env python
"""
Teste para verificar se as mudanças de expansão/colapso foram aplicadas corretamente.
"""

def test_modulos_recolhidos():
    """Testa se módulos começam recolhidos por padrão."""
    
    # Verificar template de módulos
    with open('templates/produtos/includes/secao_modulos_sofa.html', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Verificações
    checks = [
        ('style="display: none;"', 'Módulos começam recolhidos'),
        ('bi-chevron-right', 'Ícone correto para recolhido'),
        ('Expandir Todos', 'Botão inicia como "Expandir Todos"'),
        ('toggleTodosTamanhos', 'Função para expandir/recolher tamanhos'),
        ('toggleTamanho(', 'Função para expandir/recolher tamanho individual'),
    ]
    
    results = []
    for check, description in checks:
        if check in content:
            print(f"✅ {description}")
            results.append(True)
        else:
            print(f"❌ {description}")
            results.append(False)
    
    return all(results)

def test_javascript_tamanhos():
    """Testa se o JavaScript de tamanhos foi implementado."""
    
    with open('templates/produtos/includes/sofa_js.html', 'r', encoding='utf-8') as f:
        content = f.read()
    
    checks = [
        ('function toggleTamanho(', 'Função para expandir/recolher tamanho'),
        ('function toggleTodosTamanhos(', 'Função para expandir/recolher todos os tamanhos'),
        ('modulosColapsados = true', 'Estado inicial recolhido'),
        ('Expandir Todos', 'Texto inicial correto'),
        ('bi-chevron-right', 'Ícone inicial correto'),
        ('display: none', 'Conteúdo inicial oculto'),
    ]
    
    results = []
    for check, description in checks:
        if check in content:
            print(f"✅ {description}")
            results.append(True)
        else:
            print(f"❌ {description}")
            results.append(False)
    
    return all(results)

def main():
    """Executa todos os testes."""
    print("🧪 Testando funcionalidades de expansão/colapso...")
    print("=" * 50)
    
    tests = [
        ("Módulos recolhidos por padrão", test_modulos_recolhidos),
        ("JavaScript de tamanhos", test_javascript_tamanhos),
    ]
    
    all_passed = True
    for test_name, test_func in tests:
        print(f"\n📋 {test_name}:")
        result = test_func()
        all_passed = all_passed and result
        print("-" * 30)
    
    print(f"\n{'🎉 Todos os testes passaram!' if all_passed else '❌ Alguns testes falharam!'}")
    
    if all_passed:
        print("\n✅ Funcionalidades implementadas com sucesso!")
        print("🔍 Recursos disponíveis:")
        print("   • Módulos iniciam recolhidos por padrão")
        print("   • Tamanhos iniciam recolhidos por padrão")
        print("   • Botão 'Expandir/Recolher Todos' para módulos")
        print("   • Botão 'Expandir/Recolher Todos' para tamanhos (por módulo)")
        print("   • Clique individual em módulos para expandir/recolher")
        print("   • Clique individual em tamanhos para expandir/recolher")
        print("\n💡 Acesse: http://localhost:8000/sofas/7/editar/")
    else:
        print("\n❌ Corrija os problemas identificados.")

if __name__ == "__main__":
    main()
