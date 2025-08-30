/**
 * JavaScript específico para criação de novos orçamentos
 * Funcionalidades exclusivas da página novo.html
 */

console.log('🆕 Novo JS carregado');

/**
 * Inicializações específicas para novo orçamento
 */
function inicializarNovoOrcamento() {
    console.log('🆕 Inicializando funcionalidades específicas para novo orçamento...');
    
    // Preencher datas automáticas
    preencherDatasAutomaticas();
    
    // Configurar comportamento específico do formulário
    configurarFormularioNovo();
    
    console.log('✅ Novo orçamento inicializado');
}

/**
 * Preenche datas automaticamente para novo orçamento
 */
function preencherDatasAutomaticas() {
    const dataEntrega = document.getElementById('id_data_entrega');
    const dataValidade = document.getElementById('id_data_validade');
    
    if (dataEntrega && !dataEntrega.value) {
        // Data de entrega: 30 dias a partir de hoje
        const hoje = new Date();
        const entrega = new Date(hoje);
        entrega.setDate(hoje.getDate() + 30);
        dataEntrega.value = entrega.toISOString().split('T')[0];
        
        console.log(`📅 Data de entrega preenchida: ${dataEntrega.value}`);
    }
    
    if (dataValidade && !dataValidade.value) {
        // Data de validade: 15 dias a partir de hoje
        const hoje = new Date();
        const validade = new Date(hoje);
        validade.setDate(hoje.getDate() + 15);
        dataValidade.value = validade.toISOString().split('T')[0];
        
        console.log(`📅 Data de validade preenchida: ${dataValidade.value}`);
    }
}

/**
 * Configura comportamento específico do formulário de novo orçamento
 */
function configurarFormularioNovo() {
    const form = document.getElementById('orcamento-form');
    
    if (!form) {
        console.warn('⚠️ Formulário de orçamento não encontrado');
        return;
    }
    
    form.addEventListener('submit', function(e) {
        console.log('📝 Submetendo novo orçamento...');
        
        // Sincronizar itens do pedido no campo JSON
        const itensPedidoInput = document.getElementById('itens-pedido-json');
        if (itensPedidoInput && window.itensPedido) {
            itensPedidoInput.value = JSON.stringify(window.itensPedido);
            console.log(`📦 ${window.itensPedido.length} itens serializados para submissão`);
        }
        
        // Validação básica
        if (!window.itensPedido || window.itensPedido.length === 0) {
            console.warn('⚠️ Nenhum item no orçamento');
            // Permitir criação sem itens (podem ser adicionados depois)
        }
    });
    
    console.log('✅ Formulário de novo orçamento configurado');
}

/**
 * Inicialização quando DOM estiver pronto
 */
document.addEventListener('DOMContentLoaded', function() {
    console.log('🚀 Inicializando novo.js...');
    
    // Aguardar shared.js carregar completamente
    setTimeout(() => {
        inicializarNovoOrcamento();
    }, 100);
    
    console.log('✅ Novo.js inicializado');
});

console.log('🆕 Novo JS carregado com sucesso');
