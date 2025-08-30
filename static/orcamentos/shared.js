/**
 * Funções JavaScript compartilhadas entre novo.html e editar.html
 * Versão modular - evita conflitos e problemas de sintaxe
 */

// Variáveis globais compartilhadas
window.itensPedido = window.itensPedido || [];
window.contadorItens = window.contadorItens || 0;
window.produtoSelecionado = window.produtoSelecionado || null;

console.log('📦 Shared JS carregado');

/**
 * Inicializa campos unificados de desconto e acréscimo
 */
function inicializarCamposUnificados() {
    console.log('🔄 Inicializando campos unificados...');
    
    // Configurar campo desconto
    const descontoInput = document.getElementById('desconto_valor_unificado');
    const descontoBtn = document.getElementById('desconto_tipo_btn');
    const descontoOriginalValor = document.getElementById('id_desconto_valor');
    const descontoOriginalPerc = document.getElementById('id_desconto_percentual');
    
    if (descontoInput && descontoBtn) {
        // Event listener para troca de tipo
        descontoBtn.addEventListener('click', function() {
            const tipoAtual = this.getAttribute('data-tipo');
            const novoTipo = tipoAtual === 'valor' ? 'percentual' : 'valor';
            
            this.setAttribute('data-tipo', novoTipo);
            this.querySelector('.tipo-texto').textContent = novoTipo === 'valor' ? 'R$' : '%';
            
            // Limpar campos originais
            if (descontoOriginalValor) descontoOriginalValor.value = '';
            if (descontoOriginalPerc) descontoOriginalPerc.value = '';
            
            console.log(`Desconto alterado para: ${novoTipo}`);
        });
        
        // Event listener para mudança de valor
        descontoInput.addEventListener('input', function() {
            const valor = parseFloat(this.value) || 0;
            const tipo = descontoBtn.getAttribute('data-tipo');
            
            if (tipo === 'valor' && descontoOriginalValor) {
                descontoOriginalValor.value = valor;
                if (descontoOriginalPerc) descontoOriginalPerc.value = '';
            } else if (tipo === 'percentual' && descontoOriginalPerc) {
                descontoOriginalPerc.value = valor;
                if (descontoOriginalValor) descontoOriginalValor.value = '';
            }
            
            // Atualizar totais
            setTimeout(atualizarTotaisSidebar, 100);
        });
    }
    
    // Configurar campo acréscimo (similar ao desconto)
    const acrescimoInput = document.getElementById('acrescimo_valor_unificado');
    const acrescimoBtn = document.getElementById('acrescimo_tipo_btn');
    const acrescimoOriginalValor = document.getElementById('id_acrescimo_valor');
    const acrescimoOriginalPerc = document.getElementById('id_acrescimo_percentual');
    
    if (acrescimoInput && acrescimoBtn) {
        // Event listener para troca de tipo
        acrescimoBtn.addEventListener('click', function() {
            const tipoAtual = this.getAttribute('data-tipo');
            const novoTipo = tipoAtual === 'valor' ? 'percentual' : 'valor';
            
            this.setAttribute('data-tipo', novoTipo);
            this.querySelector('.tipo-texto').textContent = novoTipo === 'valor' ? 'R$' : '%';
            
            // Limpar campos originais
            if (acrescimoOriginalValor) acrescimoOriginalValor.value = '';
            if (acrescimoOriginalPerc) acrescimoOriginalPerc.value = '';
            
            console.log(`Acréscimo alterado para: ${novoTipo}`);
        });
        
        // Event listener para mudança de valor
        acrescimoInput.addEventListener('input', function() {
            const valor = parseFloat(this.value) || 0;
            const tipo = acrescimoBtn.getAttribute('data-tipo');
            
            if (tipo === 'valor' && acrescimoOriginalValor) {
                acrescimoOriginalValor.value = valor;
                if (acrescimoOriginalPerc) acrescimoOriginalPerc.value = '';
            } else if (tipo === 'percentual' && acrescimoOriginalPerc) {
                acrescimoOriginalPerc.value = valor;
                if (acrescimoOriginalValor) acrescimoOriginalValor.value = '';
            }
            
            // Atualizar totais
            setTimeout(atualizarTotaisSidebar, 100);
        });
    }
    
    console.log('✅ Campos unificados inicializados');
}

/**
 * Atualiza totais na sidebar
 */
function atualizarTotaisSidebar() {
    console.log('🧮 Atualizando totais da sidebar...');
    
    // Calcular subtotal dos itens
    let subtotal = 0;
    if (window.itensPedido && Array.isArray(window.itensPedido)) {
        subtotal = window.itensPedido.reduce((acc, item) => acc + (item.preco_total || 0), 0);
    }
    
    // Obter desconto e acréscimo
    const descontoValor = parseFloat(document.getElementById('id_desconto_valor')?.value || 0);
    const descontoPerc = parseFloat(document.getElementById('id_desconto_percentual')?.value || 0);
    const acrescimoValor = parseFloat(document.getElementById('id_acrescimo_valor')?.value || 0);
    const acrescimoPerc = parseFloat(document.getElementById('id_acrescimo_percentual')?.value || 0);
    
    // Calcular desconto total
    let descontoTotal = descontoValor;
    if (descontoPerc > 0) {
        descontoTotal = (subtotal * descontoPerc) / 100;
    }
    
    // Calcular acréscimo total
    let acrescimoTotal = acrescimoValor;
    if (acrescimoPerc > 0) {
        acrescimoTotal = (subtotal * acrescimoPerc) / 100;
    }
    
    // Calcular total final
    const totalFinal = subtotal - descontoTotal + acrescimoTotal;
    
    // Atualizar elementos da sidebar
    const totalItensEl = document.getElementById('total-itens');
    const subtotalEl = document.getElementById('subtotal-itens');
    const descontoEl = document.getElementById('desconto-aplicado');
    const acrescimoEl = document.getElementById('acrescimo-aplicado');
    const totalFinalEl = document.getElementById('total-final');
    
    if (totalItensEl) totalItensEl.textContent = window.itensPedido.length;
    if (subtotalEl) subtotalEl.textContent = `R$ ${subtotal.toFixed(2)}`;
    if (descontoEl) descontoEl.textContent = `- R$ ${descontoTotal.toFixed(2)}`;
    if (acrescimoEl) acrescimoEl.textContent = `+ R$ ${acrescimoTotal.toFixed(2)}`;
    if (totalFinalEl) totalFinalEl.textContent = `R$ ${totalFinal.toFixed(2)}`;
    
    console.log(`📊 Totais: Subtotal: R$ ${subtotal.toFixed(2)}, Total: R$ ${totalFinal.toFixed(2)}`);
}

/**
 * Busca dinâmica de clientes
 */
function inicializarBuscaClientes() {
    console.log('🔍 Inicializando busca de clientes...');
    
    const buscaInput = document.querySelector('[data-testid="cliente-input"]');
    const buscaBtn = document.querySelector('[data-testid="cliente-buscar-btn"]');
    const resultadosDiv = document.querySelector('[data-testid="cliente-results"]');
    const clienteIdInput = document.querySelector('[data-testid="cliente-id"]');
    
    if (!buscaInput || !buscaBtn || !resultadosDiv || !clienteIdInput) {
        console.warn('⚠️ Elementos de busca de cliente não encontrados');
        return;
    }
    
    let timeoutId;
    
    // Event listener para o botão buscar
    buscaBtn.addEventListener('click', function() {
        const termo = buscaInput.value.trim();
        if (termo.length >= 2) {
            buscarClientes(termo, resultadosDiv, clienteIdInput, buscaInput);
        } else {
            alert('Digite pelo menos 2 caracteres para buscar');
        }
    });
    
    // Event listener para busca com Enter
    buscaInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            e.preventDefault();
            buscaBtn.click();
        }
    });
    
    // Event listener para busca com debounce no input
    buscaInput.addEventListener('input', function() {
        const termo = this.value.trim();
        
        // Limpar timeout anterior
        if (timeoutId) {
            clearTimeout(timeoutId);
        }
        
        if (termo.length < 2) {
            resultadosDiv.style.display = 'none';
            return;
        }
        
        // Aguardar 500ms antes de buscar automaticamente
        timeoutId = setTimeout(() => {
            buscarClientes(termo, resultadosDiv, clienteIdInput, buscaInput);
        }, 500);
    });
    
    // Ocultar resultados ao clicar fora
    document.addEventListener('click', function(e) {
        if (!buscaInput.contains(e.target) && !resultadosDiv.contains(e.target) && !buscaBtn.contains(e.target)) {
            resultadosDiv.style.display = 'none';
        }
    });
    
    console.log('✅ Busca de clientes inicializada');
}

/**
 * Realiza busca de clientes no backend
 */
function buscarClientes(termo, resultadosDiv, clienteIdInput, buscaInput) {
    console.log(`🔍 Buscando clientes para: "${termo}"`);
    
    // Mostrar loading
    resultadosDiv.innerHTML = '<div class="p-3 text-center"><i class="bi bi-hourglass-split"></i> Buscando...</div>';
    resultadosDiv.style.display = 'block';
    
    fetch(`/orcamentos/buscar-cliente/?termo=${encodeURIComponent(termo)}`)
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            resultadosDiv.innerHTML = '';
            
            if (data.clientes && data.clientes.length > 0) {
                data.clientes.forEach(cliente => {
                    const item = document.createElement('div');
                    item.className = 'resultado-item p-3 border-bottom cursor-pointer';
                    item.style.cursor = 'pointer';
                    item.innerHTML = `
                        <div class="fw-bold">${cliente.nome_empresa}</div>
                        <small class="text-muted">
                            ${cliente.representante || 'Sem representante'} | ${cliente.cnpj || 'CNPJ não informado'}
                        </small>
                    `;
                    
                    item.addEventListener('click', function() {
                        // Selecionar cliente
                        clienteIdInput.value = cliente.id;
                        buscaInput.value = cliente.nome_empresa;
                        resultadosDiv.style.display = 'none';
                        
                        // Emitir evento customizado
                        const event = new CustomEvent('cliente:selected', {
                            detail: { 
                                id: cliente.id, 
                                nome: cliente.nome_empresa,
                                representante: cliente.representante,
                                cnpj: cliente.cnpj
                            }
                        });
                        document.dispatchEvent(event);
                        
                        console.log(`✅ Cliente selecionado: ${cliente.nome_empresa}`);
                    });
                    
                    resultadosDiv.appendChild(item);
                });
                
                resultadosDiv.style.display = 'block';
            } else {
                resultadosDiv.innerHTML = '<div class="p-3 text-muted text-center">Nenhum cliente encontrado</div>';
                resultadosDiv.style.display = 'block';
            }
        })
        .catch(error => {
            console.error('❌ Erro ao buscar clientes:', error);
            resultadosDiv.innerHTML = '<div class="p-3 text-danger text-center">Erro ao buscar clientes. Tente novamente.</div>';
            resultadosDiv.style.display = 'block';
        });
}

/**
 * Inicializa busca de clientes com valor inicial (para edição)
 */
function inicializarBuscaClienteComValor(valorInicial = null) {
    inicializarBuscaClientes();
    
    if (valorInicial && valorInicial.id && valorInicial.nome) {
        const buscaInput = document.querySelector('[data-testid="cliente-input"]');
        const clienteIdInput = document.querySelector('[data-testid="cliente-id"]');
        
        if (buscaInput && clienteIdInput) {
            buscaInput.value = valorInicial.nome;
            clienteIdInput.value = valorInicial.id;
            console.log(`💧 Cliente hidratado: ${valorInicial.nome} (ID: ${valorInicial.id})`);
        }
    }
}

/**
 * Inicializa modal de adicionar itens
 */
function inicializarModalItens() {
    console.log('🔄 Inicializando modal de itens...');
    
    const modal = document.getElementById('modalAdicionarItem');
    const btnConfirmar = document.getElementById('btn-confirmar-item');
    
    if (!modal || !btnConfirmar) {
        console.warn('⚠️ Modal de adicionar itens não encontrado');
        return;
    }
    
    // Configurar modal com event delegation
    configurarModalProdutos(modal);
    
    btnConfirmar.addEventListener('click', function() {
        console.log('🔄 Confirmando adição de item...');
        
        // Aqui será implementada a lógica de adicionar item
        // Por enquanto, apenas fechar o modal
        const bootstrapModal = bootstrap.Modal.getInstance(modal);
        if (bootstrapModal) {
            bootstrapModal.hide();
        }
        
        console.log('✅ Item adicionado (funcionalidade em desenvolvimento)');
    });
    
    console.log('✅ Modal de itens inicializado');
}

/**
 * Configura funcionalidade de produtos no modal
 */
function configurarModalProdutos(modal) {
    console.log('🛒 Configurando seleção de produtos no modal...');
    
    // Event delegation para mudança de tipo de produto
    modal.addEventListener('change', function(e) {
        if (e.target.matches('[data-testid="tipo-produto"]')) {
            const tipoSelecionado = e.target.value;
            const produtoContainer = modal.querySelector('[data-testid="produto-container"]');
            
            if (!produtoContainer) {
                console.warn('⚠️ Container de produtos não encontrado');
                return;
            }
            
            if (!tipoSelecionado) {
                produtoContainer.innerHTML = '';
                return;
            }
            
            console.log(`📦 Carregando produtos do tipo: ${tipoSelecionado}`);
            carregarProdutosPorTipo(tipoSelecionado, produtoContainer);
        }
    });
    
    console.log('✅ Modal de produtos configurado');
}

/**
 * Carrega produtos por tipo via AJAX
 */
function carregarProdutosPorTipo(tipo, container) {
    console.log(`🔍 Buscando produtos do tipo: ${tipo}`);
    
    // Mostrar loading
    container.innerHTML = `
        <div class="text-center p-3">
            <i class="bi bi-hourglass-split"></i> Carregando produtos...
        </div>
    `;
    
    fetch(`/orcamentos/produtos-por-tipo/?tipo=${encodeURIComponent(tipo)}`)
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            container.innerHTML = '';
            
            if (data.produtos && data.produtos.length > 0) {
                // Criar label
                const label = document.createElement('label');
                label.className = 'form-label';
                label.innerHTML = '<i class="bi bi-box-seam"></i> Produto *';
                container.appendChild(label);
                
                // Criar select
                const select = document.createElement('select');
                select.className = 'form-select';
                select.setAttribute('data-testid', 'produto-select');
                select.required = true;
                
                // Opção padrão
                const defaultOption = document.createElement('option');
                defaultOption.value = '';
                defaultOption.textContent = 'Selecione o produto...';
                select.appendChild(defaultOption);
                
                // Adicionar produtos
                data.produtos.forEach(produto => {
                    const option = document.createElement('option');
                    option.value = produto.id;
                    option.textContent = `${produto.nome} - R$ ${parseFloat(produto.preco).toFixed(2)}`;
                    option.setAttribute('data-preco', produto.preco);
                    option.setAttribute('data-referencia', produto.referencia || '');
                    select.appendChild(option);
                });
                
                container.appendChild(select);
                
                console.log(`✅ ${data.produtos.length} produtos carregados`);
            } else {
                container.innerHTML = `
                    <div class="alert alert-warning">
                        <i class="bi bi-exclamation-triangle"></i>
                        Nenhum produto encontrado para o tipo "${tipo}".
                    </div>
                `;
            }
        })
        .catch(error => {
            console.error(`❌ Erro ao carregar produtos do tipo ${tipo}:`, error);
            container.innerHTML = `
                <div class="alert alert-danger">
                    <i class="bi bi-exclamation-circle"></i>
                    Erro ao carregar produtos. Tente novamente.
                </div>
            `;
        });
}

/**
 * Inicialização principal quando DOM estiver pronto
 */
document.addEventListener('DOMContentLoaded', function() {
    console.log('🚀 Inicializando shared JS...');
    
    // Inicializar funcionalidades básicas
    inicializarCamposUnificados();
    inicializarBuscaClientes();
    inicializarModalItens();
    
    // Atualizar totais iniciais
    setTimeout(atualizarTotaisSidebar, 500);
    
    console.log('✅ Shared JS inicializado com sucesso');
});

console.log('📦 Shared JS carregado com sucesso');
