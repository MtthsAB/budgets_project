/**
 * Script de correção para valores com vírgulas em campos numéricos
 * Aplica automaticamente a conversão de vírgulas para pontos
 */

// Função para corrigir valores com vírgulas em campos numéricos
function corrigirCamposNumericos() {
    console.log('🔧 Iniciando correção de campos numéricos...');
    
    // Selecionar todos os inputs do tipo number
    const inputsNumber = document.querySelectorAll('input[type="number"]');
    let contadorCorrigidos = 0;
    
    inputsNumber.forEach(function(input) {
        if (input.value && typeof input.value === 'string' && input.value.includes(',')) {
            const valorOriginal = input.value;
            
            // Substituir vírgulas por pontos
            const valorCorrigido = input.value.replace(/,/g, '.');
            
            // Verificar se é um número válido após a correção
            if (!isNaN(parseFloat(valorCorrigido))) {
                input.value = valorCorrigido;
                contadorCorrigidos++;
                
                console.log(`✅ Corrigido: "${valorOriginal}" → "${valorCorrigido}" (campo: ${input.name || input.id || 'sem nome'})`);
                
                // Disparar evento de mudança para atualizar validações
                input.dispatchEvent(new Event('change', { bubbles: true }));
            } else {
                console.warn(`⚠️ Valor inválido após correção: "${valorCorrigido}" (campo: ${input.name || input.id || 'sem nome'})`);
            }
        }
    });
    
    console.log(`✅ Correção concluída: ${contadorCorrigidos} campos corrigidos de ${inputsNumber.length} campos numéricos`);
    
    return contadorCorrigidos;
}

// Executar correção quando o DOM estiver carregado
document.addEventListener('DOMContentLoaded', function() {
    // Executar correção inicial
    corrigirCamposNumericos();
    
    // Configurar observer para detectar novos elementos adicionados dinamicamente
    const observer = new MutationObserver(function(mutations) {
        let novosInputs = false;
        
        mutations.forEach(function(mutation) {
            if (mutation.type === 'childList' && mutation.addedNodes.length > 0) {
                mutation.addedNodes.forEach(function(node) {
                    if (node.nodeType === 1) { // Element node
                        // Verificar se o próprio nó é um input number
                        if (node.matches && node.matches('input[type="number"]')) {
                            novosInputs = true;
                        }
                        
                        // Verificar se há inputs number dentro do nó
                        const inputsInternos = node.querySelectorAll && node.querySelectorAll('input[type="number"]');
                        if (inputsInternos && inputsInternos.length > 0) {
                            novosInputs = true;
                        }
                    }
                });
            }
        });
        
        // Se novos inputs foram detectados, executar correção
        if (novosInputs) {
            setTimeout(corrigirCamposNumericos, 100); // Pequeno delay para garantir que os valores sejam preenchidos
        }
    });
    
    // Observar mudanças no DOM
    observer.observe(document.body, {
        childList: true,
        subtree: true
    });
    
    console.log('🎯 Sistema de correção de vírgulas ativado e monitorando o DOM');
});

// Também executar a correção quando a página for totalmente carregada
window.addEventListener('load', function() {
    setTimeout(corrigirCamposNumericos, 500); // Delay adicional para garantir que todos os dados foram carregados
});
