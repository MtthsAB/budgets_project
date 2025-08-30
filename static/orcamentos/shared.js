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
    
    const buscaInput = document.getElementById('cliente-busca');
    const resultadosDiv = document.querySelector('.cliente-resultados');
    const selectOriginal = document.getElementById('id_cliente');
    
    if (!buscaInput || !resultadosDiv || !selectOriginal) {
        console.warn('⚠️ Elementos de busca de cliente não encontrados');
        return;
    }
    
    let timeoutId;
    
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
        
        // Aguardar 300ms antes de buscar
        timeoutId = setTimeout(() => {
            buscarClientes(termo, resultadosDiv, selectOriginal);
        }, 300);
    });
    
    // Ocultar resultados ao clicar fora
    document.addEventListener('click', function(e) {
        if (!buscaInput.contains(e.target) && !resultadosDiv.contains(e.target)) {
            resultadosDiv.style.display = 'none';
        }
    });
    
    console.log('✅ Busca de clientes inicializada');
}

/**
 * Realiza busca de clientes no backend
 */
function buscarClientes(termo, resultadosDiv, selectOriginal) {
    console.log(`🔍 Buscando clientes para: "${termo}"`);
    
    fetch(`/api/clientes/buscar/?q=${encodeURIComponent(termo)}`)
        .then(response => response.json())
        .then(data => {
            resultadosDiv.innerHTML = '';
            
            if (data.clientes && data.clientes.length > 0) {
                data.clientes.forEach(cliente => {
                    const item = document.createElement('div');
                    item.className = 'resultado-item';
                    item.innerHTML = `
                        <div class="fw-bold">${cliente.nome_empresa}</div>
                        <small class="text-muted">
                            ${cliente.representante} | ${cliente.cnpj || 'CNPJ não informado'}
                        </small>
                    `;
                    
                    item.addEventListener('click', function() {
                        // Selecionar cliente
                        selectOriginal.value = cliente.id;
                        document.getElementById('cliente-busca').value = cliente.nome_empresa;
                        resultadosDiv.style.display = 'none';
                        
                        console.log(`✅ Cliente selecionado: ${cliente.nome_empresa}`);
                    });
                    
                    resultadosDiv.appendChild(item);
                });
                
                resultadosDiv.style.display = 'block';
            } else {
                resultadosDiv.innerHTML = '<div class="resultado-item text-muted">Nenhum cliente encontrado</div>';
                resultadosDiv.style.display = 'block';
            }
        })
        .catch(error => {
            console.error('❌ Erro ao buscar clientes:', error);
            resultadosDiv.style.display = 'none';
        });
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
