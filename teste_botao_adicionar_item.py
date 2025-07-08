#!/usr/bin/env python3
"""
Teste para verificar se o botão "Adicionar Item" está funcionando corretamente.
"""

def test_template_adicionar_item():
    """
    Testa se o template tem o botão "Adicionar Item" corretamente configurado.
    """
    print("🔍 Verificando configuração do botão 'Adicionar Item'...")
    
    # Ler o template
    template_path = '/home/matas/projetos/Project/templates/orcamentos/form.html'
    with open(template_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Verificações
    checks = [
        ('Botão "Adicionar Item" existe', 'id="btnAdicionarItem"' in content),
        ('Botão tem data-bs-target correto', 'data-bs-target="#modalAdicionarItem"' in content),
        ('Modal com ID correto existe', 'id="modalAdicionarItem"' in content),
        ('Botão "Confirmar Item" existe', 'id="btn-confirmar-item"' in content),
        ('JavaScript para evento exists', 'btnConfirmar.addEventListener' in content),
        ('Só um modal com mesmo ID', content.count('id="modalAdicionarItem"') == 1),
        ('Função coletarDadosEspecificos existe', 'coletarDadosEspecificos' in content),
        ('Função atualizarTabelaItens existe', 'atualizarTabelaItens' in content),
        ('Função calcularTotais existe', 'calcularTotais' in content),
    ]
    
    all_passed = True
    for desc, check in checks:
        status = "✅" if check else "❌"
        print(f"{status} {desc}")
        if not check:
            all_passed = False
    
    print(f"\n{'✅ Todas as verificações passaram!' if all_passed else '❌ Algumas verificações falharam!'}")
    return all_passed

if __name__ == '__main__':
    test_template_adicionar_item()
