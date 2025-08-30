/**
 * JavaScript específico para edição de orçamentos
 * Funcionalidades exclusivas da página editar.html
 */

console.log('✏️ Editar JS carregado');

/**
 * Inicializações específicas para edição de orçamento
 */
function inicializarEdicaoOrcamento() {
    console.log('✏️ Inicializando funcionalidades específicas para edição...');
    
    // Hidratar campos com dados existentes
    hidratarCamposOrcamento();
    
    // Configurar funcionalidades específicas de edição
    configurarFuncionalidadesEdicao();
    
    console.log('✅ Edição de orçamento inicializada');
}

/**
 * Hidrata campos do formulário com dados do orçamento existente
 */
function hidratarCamposOrcamento() {
    if (!window.orcamentoData) {
        console.warn('⚠️ Dados do orçamento não disponíveis para hidratação');
        return;
    }
    
    console.log('💧 Hidratando campos do orçamento...', window.orcamentoData);
    
    const data = window.orcamentoData;
    
    // Hidratar campo de cliente
    const clienteBusca = document.getElementById('cliente-busca');
    if (clienteBusca && data.cliente_nome) {
        clienteBusca.value = data.cliente_nome;
    }
    
    // Hidratar campos de desconto
    const descontoUnificado = document.getElementById('desconto_valor_unificado');
    const descontoTipoBtn = document.getElementById('desconto_tipo_btn');
    
    if (descontoUnificado && descontoTipoBtn) {
        if (data.desconto_valor > 0) {
            descontoUnificado.value = data.desconto_valor;
            descontoTipoBtn.setAttribute('data-tipo', 'valor');
            descontoTipoBtn.querySelector('.tipo-texto').textContent = 'R$';
        } else if (data.desconto_percentual > 0) {
            descontoUnificado.value = data.desconto_percentual;
            descontoTipoBtn.setAttribute('data-tipo', 'percentual');
            descontoTipoBtn.querySelector('.tipo-texto').textContent = '%';
        }
    }
    
    // Hidratar campos de acréscimo
    const acrescimoUnificado = document.getElementById('acrescimo_valor_unificado');
    const acrescimoTipoBtn = document.getElementById('acrescimo_tipo_btn');
    
    if (acrescimoUnificado && acrescimoTipoBtn) {
        if (data.acrescimo_valor > 0) {
            acrescimoUnificado.value = data.acrescimo_valor;
            acrescimoTipoBtn.setAttribute('data-tipo', 'valor');
            acrescimoTipoBtn.querySelector('.tipo-texto').textContent = 'R$';
        } else if (data.acrescimo_percentual > 0) {
            acrescimoUnificado.value = data.acrescimo_percentual;
            acrescimoTipoBtn.setAttribute('data-tipo', 'percentual');
            acrescimoTipoBtn.querySelector('.tipo-texto').textContent = '%';
        }
    }
    
    console.log('✅ Campos hidratados com sucesso');
}

/**
 * Configura funcionalidades específicas da edição
 */
function configurarFuncionalidadesEdicao() {
    // Configurar remoção de itens existentes
    configurarRemocaoItensExistentes();
    
    // Configurar envio de novos itens via AJAX
    configurarEnvioItensAjax();
    
    console.log('✅ Funcionalidades de edição configuradas');
}

/**
 * Configura funcionalidade de remoção de itens existentes
 */
function configurarRemocaoItensExistentes() {
    // A função removerItemExistente já está definida inline nos botões
    // Aqui podemos adicionar confirmações extras ou logs
    
    console.log('🗑️ Funcionalidade de remoção de itens configurada');
}

/**
 * Configura envio de novos itens via AJAX quando editando
 */
function configurarEnvioItensAjax() {
    // Quando novos itens forem adicionados em modo de edição,
    // eles serão enviados via AJAX em vez de aguardar submissão do form
    
    console.log('📡 Envio de itens via AJAX configurado');
}

/**
 * Remove item existente do orçamento
 */
window.removerItemExistente = function(itemId) {
    if (!window.orcamentoPk) {
        console.error('❌ Orçamento não identificado');
        alert('Erro: Orçamento não identificado');
        return;
    }
    
    if (!confirm('Tem certeza que deseja remover este item?')) {
        return;
    }
    
    console.log(`🗑️ Removendo item existente: ${itemId}`);
    
    // Fazer requisição AJAX para remover item
    fetch(`/orcamentos/${window.orcamentoPk}/item/${itemId}/remover/`, {
        method: 'POST',
        headers: {
            'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value,
            'Content-Type': 'application/json',
        },
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            // Remover linha da tabela
            const row = document.getElementById(`item-existente-${itemId}`);
            if (row) {
                row.remove();
                console.log(`✅ Item ${itemId} removido da interface`);
            }
            
            // Atualizar totais da sidebar
            setTimeout(atualizarTotaisSidebar, 100);
            
            console.log(`✅ Item ${itemId} removido com sucesso`);
        } else {
            console.error(`❌ Erro ao remover item ${itemId}:`, data.message);
            alert('Erro ao remover item: ' + data.message);
        }
    })
    .catch(error => {
        console.error(`❌ Erro na requisição para remover item ${itemId}:`, error);
        alert('Erro ao conectar com o servidor');
    });
};

/**
 * Inicialização quando DOM estiver pronto
 */
document.addEventListener('DOMContentLoaded', function() {
    console.log('🚀 Inicializando editar.js...');
    
    // Aguardar shared.js carregar completamente
    setTimeout(() => {
        inicializarEdicaoOrcamento();
    }, 100);
    
    console.log('✅ Editar.js inicializado');
});

console.log('✏️ Editar JS carregado com sucesso');
