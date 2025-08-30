/**
 * Autocomplete de Cliente para Orçamentos
 * Implementação conforme especificação: busca incremental, navegação por teclado,
 * integração com /novo e /editar
 */

class ClienteAutocomplete {
    constructor() {
        this.input = null;
        this.hiddenInput = null;
        this.resultsContainer = null;
        this.currentIndex = -1;
        this.searchTimeout = null;
        this.results = [];
        this.isInitialized = false;
        
        this.init();
    }
    
    init() {
        // Aguardar DOM estar pronto
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', () => this.setupElements());
        } else {
            this.setupElements();
        }
    }
    
    setupElements() {
        this.input = document.querySelector('[data-testid="cliente-input"]');
        this.hiddenInput = document.querySelector('[data-testid="cliente-id"]');
        this.resultsContainer = document.querySelector('[data-testid="cliente-results"]');
        
        if (!this.input || !this.hiddenInput || !this.resultsContainer) {
            console.warn('⚠️ Elementos do autocomplete de cliente não encontrados');
            return;
        }
        
        this.setupEvents();
        this.setupStyles();
        this.initializeForEditing();
        this.isInitialized = true;
        
        console.log('✅ Cliente autocomplete inicializado');
    }
    
    setupEvents() {
        // Input - busca incremental
        this.input.addEventListener('input', (e) => this.handleInput(e));
        
        // Navegação por teclado
        this.input.addEventListener('keydown', (e) => this.handleKeydown(e));
        
        // Perder foco - fechar lista
        this.input.addEventListener('blur', (e) => this.handleBlur(e));
        
        // Ganhar foco - reativar se necessário
        this.input.addEventListener('focus', (e) => this.handleFocus(e));
        
        // Clique fora - fechar lista
        document.addEventListener('click', (e) => this.handleDocumentClick(e));
    }
    
    setupStyles() {
        // Garantir estilos CSS para o container de resultados
        this.resultsContainer.style.position = 'absolute';
        this.resultsContainer.style.top = '100%';
        this.resultsContainer.style.left = '0';
        this.resultsContainer.style.right = '0';
        this.resultsContainer.style.backgroundColor = '#fff';
        this.resultsContainer.style.border = '1px solid #dee2e6';
        this.resultsContainer.style.borderRadius = '0.375rem';
        this.resultsContainer.style.boxShadow = '0 0.125rem 0.25rem rgba(0,0,0,0.075)';
        this.resultsContainer.style.zIndex = '1000';
        this.resultsContainer.style.maxHeight = '300px';
        this.resultsContainer.style.overflowY = 'auto';
        
        // Posicionar container pai como relative
        const parent = this.input.parentElement;
        if (parent && getComputedStyle(parent).position === 'static') {
            parent.style.position = 'relative';
        }
    }
    
    initializeForEditing() {
        // Se estamos editando e já há um ID selecionado, carregar nome do cliente
        const clienteId = this.hiddenInput.value;
        
        if (clienteId && window.orcamentoData && window.orcamentoData.cliente_nome) {
            // Usar dados já carregados
            this.input.value = window.orcamentoData.cliente_nome;
            console.log('Cliente carregado para edição:', window.orcamentoData.cliente_nome);
        } else if (clienteId) {
            // Buscar dados do cliente via AJAX
            this.loadClienteData(clienteId);
        }
    }
    
    loadClienteData(clienteId) {
        fetch(`/orcamentos/cliente/${clienteId}/`)
            .then(response => response.json())
            .then(data => {
                if (data.nome_empresa) {
                    this.input.value = data.nome_empresa;
                    console.log('Cliente carregado via AJAX:', data.nome_empresa);
                }
            })
            .catch(error => {
                console.error('Erro ao carregar dados do cliente:', error);
            });
    }
    
    handleInput(e) {
        const termo = e.target.value.trim();
        
        // Se o usuário alterou o texto, limpar ID selecionado
        this.clearSelection();
        
        // Cancelar busca anterior
        if (this.searchTimeout) {
            clearTimeout(this.searchTimeout);
        }
        
        // Busca incremental a partir do 1º caractere
        if (termo.length >= 1) {
            // Usar debounce curto conforme especificado
            this.searchTimeout = setTimeout(() => {
                this.searchClientes(termo);
            }, 300);
        } else {
            this.hideResults();
        }
    }
    
    handleKeydown(e) {
        if (!this.isResultsVisible()) {
            return;
        }
        
        switch (e.key) {
            case 'ArrowDown':
                e.preventDefault();
                this.navigateDown();
                break;
                
            case 'ArrowUp':
                e.preventDefault();
                this.navigateUp();
                break;
                
            case 'Enter':
                e.preventDefault();
                this.selectCurrent();
                break;
                
            case 'Escape':
                e.preventDefault();
                this.hideResults();
                this.input.blur();
                break;
        }
    }
    
    handleBlur(e) {
        // Aguardar um pouco para permitir clique em resultado
        setTimeout(() => {
            if (!this.resultsContainer.contains(document.activeElement)) {
                this.hideResults();
            }
        }, 150);
    }
    
    handleFocus(e) {
        // Se houver resultados e termo de busca, mostrar novamente
        const termo = this.input.value.trim();
        if (termo.length >= 1 && this.results.length > 0) {
            this.showResults();
        }
    }
    
    handleDocumentClick(e) {
        if (!this.input.contains(e.target) && !this.resultsContainer.contains(e.target)) {
            this.hideResults();
        }
    }
    
    searchClientes(termo) {
        console.log(`🔍 Buscando clientes: "${termo}"`);
        
        fetch(`/orcamentos/buscar-cliente/?termo=${encodeURIComponent(termo)}`)
            .then(response => response.json())
            .then(data => {
                this.results = data.clientes || [];
                this.renderResults();
            })
            .catch(error => {
                console.error('❌ Erro na busca de clientes:', error);
                this.showError('Erro na busca. Tente novamente.');
            });
    }
    
    renderResults() {
        this.resultsContainer.innerHTML = '';
        this.currentIndex = -1;
        
        if (this.results.length === 0) {
            this.showNoResults();
            return;
        }
        
        this.results.forEach((cliente, index) => {
            const item = this.createResultItem(cliente, index);
            this.resultsContainer.appendChild(item);
        });
        
        this.showResults();
    }
    
    createResultItem(cliente, index) {
        const item = document.createElement('div');
        item.className = 'resultado-item';
        item.dataset.index = index;
        item.style.padding = '0.75rem';
        item.style.cursor = 'pointer';
        item.style.borderBottom = '1px solid #f8f9fa';
        
        item.innerHTML = `
            <div style="font-weight: 600; color: #212529;">
                ${this.escapeHtml(cliente.nome_empresa)}
            </div>
            <small style="color: #6c757d;">
                ${this.escapeHtml(cliente.representante)} | ${this.escapeHtml(cliente.cnpj || 'CNPJ não informado')}
            </small>
        `;
        
        // Eventos de mouse
        item.addEventListener('mouseenter', () => {
            this.setActiveItem(index);
        });
        
        item.addEventListener('click', (e) => {
            e.preventDefault();
            this.selectCliente(cliente);
        });
        
        return item;
    }
    
    showNoResults() {
        const item = document.createElement('div');
        item.className = 'resultado-item no-results';
        item.style.padding = '0.75rem';
        item.style.color = '#6c757d';
        item.style.fontStyle = 'italic';
        item.textContent = 'Nenhum cliente encontrado';
        
        this.resultsContainer.appendChild(item);
        this.showResults();
    }
    
    showError(message) {
        const item = document.createElement('div');
        item.className = 'resultado-item error';
        item.style.padding = '0.75rem';
        item.style.color = '#dc3545';
        item.textContent = message;
        
        this.resultsContainer.innerHTML = '';
        this.resultsContainer.appendChild(item);
        this.showResults();
    }
    
    navigateDown() {
        if (this.currentIndex < this.results.length - 1) {
            this.setActiveItem(this.currentIndex + 1);
        }
    }
    
    navigateUp() {
        if (this.currentIndex > 0) {
            this.setActiveItem(this.currentIndex - 1);
        } else if (this.currentIndex === 0) {
            this.setActiveItem(-1);
        }
    }
    
    setActiveItem(index) {
        // Remover destaque anterior
        const previousActive = this.resultsContainer.querySelector('.active');
        if (previousActive) {
            previousActive.classList.remove('active');
            previousActive.style.backgroundColor = '';
        }
        
        this.currentIndex = index;
        
        if (index >= 0 && index < this.results.length) {
            const items = this.resultsContainer.querySelectorAll('.resultado-item:not(.no-results):not(.error)');
            const currentItem = items[index];
            
            if (currentItem) {
                currentItem.classList.add('active');
                currentItem.style.backgroundColor = '#e9ecef';
                
                // Scroll se necessário
                currentItem.scrollIntoView({ block: 'nearest' });
            }
        }
    }
    
    selectCurrent() {
        if (this.currentIndex >= 0 && this.currentIndex < this.results.length) {
            this.selectCliente(this.results[this.currentIndex]);
        }
    }
    
    selectCliente(cliente) {
        // Preencher campos
        this.input.value = cliente.nome_empresa;
        this.hiddenInput.value = cliente.id;
        
        // Fechar lista
        this.hideResults();
        
        // Log para debug
        console.log(`✅ Cliente selecionado: ${cliente.nome_empresa} (ID: ${cliente.id})`);
        
        // Disparar evento customizado para outros scripts
        const event = new CustomEvent('clienteSelected', {
            detail: { cliente }
        });
        this.input.dispatchEvent(event);
    }
    
    clearSelection() {
        // Só limpar se não estivermos navegando pelos resultados
        if (this.currentIndex === -1) {
            this.hiddenInput.value = '';
        }
    }
    
    showResults() {
        this.resultsContainer.style.display = 'block';
    }
    
    hideResults() {
        this.resultsContainer.style.display = 'none';
        this.currentIndex = -1;
    }
    
    isResultsVisible() {
        return this.resultsContainer.style.display === 'block';
    }
    
    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }
}

// Inicializar autocomplete quando DOM estiver pronto
let clienteAutocomplete = null;

if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', function() {
        clienteAutocomplete = new ClienteAutocomplete();
    });
} else {
    clienteAutocomplete = new ClienteAutocomplete();
}

// Exportar para uso global se necessário
window.ClienteAutocomplete = ClienteAutocomplete;
window.clienteAutocomplete = clienteAutocomplete;

console.log('📦 Cliente Autocomplete script carregado');
