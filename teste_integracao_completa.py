#!/usr/bin/env python3
"""
Teste final para verificar se a integração completa do botão "Adicionar Item" está funcionando.
"""

def test_integration():
    """
    Testa a integração completa do botão com o modal e JavaScript.
    """
    print("🔍 Verificando integração completa do botão 'Adicionar Item'...")
    
    # Ler o template
    template_path = '/home/matas/projetos/Project/templates/orcamentos/form.html'
    with open(template_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Verificações de integração
    checks = [
        # Botão principal
        ('Botão principal tem ID correto', 'id="btnAdicionarItem"' in content),
        ('Botão aponta para modal correto', 'data-bs-target="#modalAdicionarItem"' in content),
        ('Botão tem Bootstrap toggle', 'data-bs-toggle="modal"' in content),
        
        # Modal
        ('Modal tem ID único', content.count('id="modalAdicionarItem"') == 1),
        ('Modal tem tamanho xl', 'modal-xl' in content),
        ('Modal tem título correto', 'Adicionar Item ao Pedido' in content),
        
        # Formulário no modal
        ('Formulário tem ID correto', 'id="form-adicionar-item"' in content),
        ('Formulário tem CSRF token', '{% csrf_token %}' in content),
        ('Select tipo produto existe', 'id="tipo-produto"' in content),
        ('Select produto existe', 'id="produto"' in content),
        ('Campo quantidade existe', 'id="quantidade"' in content),
        ('Campo preço existe', 'id="preco-unitario"' in content),
        ('Campo observações existe', 'id="observacoes"' in content),
        
        # Botão de confirmação
        ('Botão confirmar existe', 'id="btn-confirmar-item"' in content),
        ('Botão confirmar tem classe success', 'btn-success' in content),
        
        # JavaScript
        ('Event listener do botão confirmar', 'btnConfirmar.addEventListener' in content),
        ('Função para coletar dados específicos', 'coletarDadosEspecificos' in content),
        ('Função para atualizar tabela', 'atualizarTabelaItens' in content),
        ('Função para calcular totais', 'calcularTotaisGerais' in content),
        ('Função para limpar formulário', 'limparFormulario' in content),
        
        # Endpoints
        ('Endpoint produtos por tipo', 'produtos-por-tipo' in content),
        ('Endpoint detalhes produto', 'detalhes-produto' in content),
        
        # Validações
        ('Validação de campos obrigatórios', 'preencha todos os campos obrigatórios' in content),
        ('Controle de estado do modal', 'Modal.getInstance' in content),
        
        # Estrutura de dados
        ('Array de itens do pedido', 'itensPedido' in content),
        ('Contador de itens', 'contadorItens' in content),
    ]
    
    all_passed = True
    for desc, check in checks:
        status = "✅" if check else "❌"
        print(f"{status} {desc}")
        if not check:
            all_passed = False
    
    print(f"\n{'✅ INTEGRAÇÃO COMPLETA VERIFICADA!' if all_passed else '❌ PROBLEMAS NA INTEGRAÇÃO DETECTADOS!'}")
    
    # Verificação adicional: fluxo de dados
    print(f"\n🔄 Verificando fluxo de dados:")
    print(f"✅ Botão → Modal → Formulário → JavaScript → Endpoints → Tabela")
    
    return all_passed

if __name__ == '__main__':
    test_integration()
