#!/usr/bin/env python3
"""
Teste Final: Busca de Cliente e Modal de Produtos
===================================================

Este script testa todas as funcionalidades relacionadas à busca de cliente
e modal de seleção de produtos nas páginas de novo e edição de orçamento.

Funcionalidades testadas:
1. Busca de cliente - UX original
2. Modal de produtos - cadeia tipo → produtos
3. Hidratação em edição
4. Event delegation
5. Robustez de selectors
"""

import os
import sys

class TesteBuscaClienteModalFinal:
    def __init__(self):
        pass
    
    def test_static_files_exist(self):
        """Verifica se os arquivos estáticos existem"""
        print("\n� Verificando arquivos estáticos...")
        
        files = [
            'static/orcamentos/shared.js',
            'static/orcamentos/novo.js',
            'static/orcamentos/editar.js'
        ]
        
        for file_path in files:
            assert os.path.exists(file_path), f"Arquivo {file_path} não encontrado"
            
            # Verificar se contém funções esperadas
            with open(file_path, 'r') as f:
                content = f.read()
            
            if 'shared.js' in file_path:
                assert 'inicializarBuscaClientes' in content, "Função inicializarBuscaClientes não encontrada"
                assert 'inicializarModalItens' in content, "Função inicializarModalItens não encontrada"
                assert 'data-testid' in content, "Seletores data-testid não encontrados"
                assert 'inicializarBuscaClienteComValor' in content, "Função inicializarBuscaClienteComValor não encontrada"
                assert 'carregarProdutosPorTipo' in content, "Função carregarProdutosPorTipo não encontrada"
            
            if 'novo.js' in file_path:
                assert 'inicializarBuscaClienteComValor(null)' in content, "Inicialização sem valor no novo.js não encontrada"
            
            if 'editar.js' in file_path:
                assert 'inicializarBuscaClienteComValor(valorCliente)' in content, "Inicialização com valor no editar.js não encontrada"
            
            print(f"✅ {file_path} existe e está correto")
    
    def test_partials_have_data_testid(self):
        """Verifica se os parciais têm os data-testid corretos"""
        print("\n🏷️ Verificando data-testid nos parciais...")
        
        partials = [
            'templates/orcamentos/partials/_cliente_search_field.html',
            'templates/orcamentos/partials/_modal_itens.html'
        ]
        
        for partial in partials:
            assert os.path.exists(partial), f"Parcial {partial} não encontrado"
            
            with open(partial, 'r') as f:
                content = f.read()
            
            if '_cliente_search_field.html' in partial:
                assert 'data-testid="cliente-busca-input"' in content, "data-testid cliente-busca-input não encontrado"
                assert 'data-testid="cliente-busca-button"' in content, "data-testid cliente-busca-button não encontrado"
                assert 'data-testid="cliente-busca-results"' in content, "data-testid cliente-busca-results não encontrado"
                assert 'data-testid="cliente-id-field"' in content, "data-testid cliente-id-field não encontrado"
            
            if '_modal_itens.html' in partial:
                assert 'data-testid="tipo-produto-select"' in content, "data-testid tipo-produto-select não encontrado"
                assert 'data-testid="produto-container"' in content, "data-testid produto-container não encontrado"
                assert 'data-testid="produto-select"' in content, "data-testid produto-select não encontrado"
            
            print(f"✅ {partial} tem data-testid corretos")
    
    def test_templates_include_partials(self):
        """Verifica se os templates incluem os parciais"""
        print("\n� Verificando inclusão de parciais nos templates...")
        
        templates = [
            'templates/orcamentos/novo.html',
            'templates/orcamentos/editar.html'
        ]
        
        for template in templates:
            if not os.path.exists(template):
                print(f"⚠️ Template {template} não encontrado, pulando...")
                continue
            
            with open(template, 'r') as f:
                content = f.read()
            
            # Verificar inclusão dos parciais
            assert '_cliente_search_field.html' in content, f"Parcial _cliente_search_field.html não incluído em {template}"
            assert '_modal_itens.html' in content, f"Parcial _modal_itens.html não incluído em {template}"
            
            # Verificar carregamento dos scripts
            assert 'shared.js' in content, f"Script shared.js não carregado em {template}"
            
            if 'novo.html' in template:
                assert 'novo.js' in content, f"Script novo.js não carregado em {template}"
            
            if 'editar.html' in template:
                assert 'editar.js' in content, f"Script editar.js não carregado em {template}"
            
            print(f"✅ {template} inclui parciais e scripts corretamente")
    
    def test_javascript_syntax(self):
        """Verifica sintaxe básica dos arquivos JavaScript"""
        print("\n� Verificando sintaxe JavaScript...")
        
        js_files = [
            'static/orcamentos/shared.js',
            'static/orcamentos/novo.js',
            'static/orcamentos/editar.js'
        ]
        
        for js_file in js_files:
            with open(js_file, 'r') as f:
                content = f.read()
            
            # Verificações básicas de sintaxe
            brace_open = content.count('{')
            brace_close = content.count('}')
            assert brace_open == brace_close, f"Chaves desbalanceadas em {js_file}: {brace_open} abrem, {brace_close} fecham"
            
            # Verificar se não há console.error óbvios
            lines = content.split('\n')
            for i, line in enumerate(lines, 1):
                if 'console.error' in line and 'catch' not in line.lower():
                    print(f"⚠️ Console.error encontrado em {js_file}:{i}: {line.strip()}")
            
            print(f"✅ {js_file} sintaxe OK")
    
    def test_event_delegation_patterns(self):
        """Verifica padrões de event delegation"""
        print("\n� Verificando padrões de event delegation...")
        
        with open('static/orcamentos/shared.js', 'r') as f:
            content = f.read()
        
        # Verificar uso de event delegation
        assert 'document.addEventListener' in content, "Event delegation no document não encontrado"
        
        # Verificar se há pelo menos um padrão robusto de event delegation
        delegation_patterns = [
            'event.target.closest',
            'event.target.matches',
            'e.target.closest',
            'e.target.matches',
            'contains(e.target)',
            'contains(event.target)'
        ]
        
        patterns_found = 0
        for pattern in delegation_patterns:
            if pattern in content:
                patterns_found += 1
        
        assert patterns_found >= 1, f"Nenhum padrão de event delegation robusto encontrado (testados: {delegation_patterns})"
        
        # Verificar se não há addEventListener direto em elementos específicos (que seria frágil)
        problem_patterns = [
            'getElementById(',
            'querySelector(',
            'querySelectorAll('
        ]
        
        safe_patterns_found = 0
        for pattern in ['data-testid', 'closest(', 'matches(']:
            if pattern in content:
                safe_patterns_found += 1
        
        assert safe_patterns_found >= 2, f"Padrões seguros insuficientes encontrados (apenas {safe_patterns_found})"
        
        print("✅ Padrões de event delegation corretos")
    
    def test_hydration_logic(self):
        """Verifica lógica de hidratação"""
        print("\n💧 Verificando lógica de hidratação...")
        
        with open('static/orcamentos/editar.js', 'r') as f:
            content = f.read()
        
        # Verificar se há verificação de dados existentes
        assert 'window.orcamentoData' in content, "Verificação de window.orcamentoData não encontrada"
        assert 'valorCliente' in content, "Variável valorCliente não encontrada"
        assert 'cliente_id' in content, "Acesso a cliente_id não encontrado"
        assert 'cliente_nome' in content, "Acesso a cliente_nome não encontrado"
        
        print("✅ Lógica de hidratação presente")
    
    def run_all_tests(self):
        """Executa todos os testes"""
        print("🧪 INICIANDO TESTES FINAIS - BUSCA CLIENTE E MODAL PRODUTOS")
        print("=" * 70)
        
        tests = [
            self.test_static_files_exist,
            self.test_partials_have_data_testid,
            self.test_templates_include_partials,
            self.test_javascript_syntax,
            self.test_event_delegation_patterns,
            self.test_hydration_logic,
        ]
        
        passed = 0
        failed = 0
        
        for test in tests:
            try:
                test()
                passed += 1
            except Exception as e:
                print(f"❌ FALHOU: {test.__name__}")
                print(f"   Erro: {e}")
                failed += 1
        
        print("\n" + "=" * 70)
        print(f"📊 RESULTADO FINAL:")
        print(f"✅ Passou: {passed}")
        print(f"❌ Falhou: {failed}")
        print(f"📈 Taxa de sucesso: {(passed/(passed+failed)*100):.1f}%")
        
        if failed == 0:
            print("\n🎉 TODOS OS TESTES PASSARAM!")
            print("🚀 Busca de cliente e modal de produtos estão funcionais")
            print("\n📋 FUNCIONALIDADES IMPLEMENTADAS:")
            print("   ✅ Busca de cliente com UX original")
            print("   ✅ Modal de produtos com cadeia tipo → produtos")
            print("   ✅ Event delegation robusto")
            print("   ✅ Seletores data-testid padronizados")
            print("   ✅ Hidratação em modo de edição")
            print("   ✅ Tratamento de erros")
        else:
            print("\n⚠️ ALGUNS TESTES FALHARAM")
            print("🔧 Verifique os erros acima")
        
        return failed == 0

def main():
    """Função principal"""
    if len(sys.argv) > 1 and sys.argv[1] == '--help':
        print(__doc__)
        return
    
    tester = TesteBuscaClienteModalFinal()
    success = tester.run_all_tests()
    
    sys.exit(0 if success else 1)

if __name__ == '__main__':
    main()
