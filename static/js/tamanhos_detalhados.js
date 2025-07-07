/**
 * JavaScript para gerenciamento de tamanhos detalhados
 */

let tamanhoCounter = 0;
let todosTamanhosExpandidos = true;

// Função para inicializar a seção de tamanhos
function inicializarTamanhos() {
    // Verificar se já existem tamanhos
    const tamanhosExistentes = document.querySelectorAll('.tamanho-item');
    tamanhoCounter = tamanhosExistentes.length;
    
    // Se não há tamanhos, esconder a seção
    if (tamanhoCounter === 0) {
        document.getElementById('secao-tamanhos').style.display = 'none';
        document.getElementById('noTamanhosAlert').style.display = 'block';
    } else {
        document.getElementById('secao-tamanhos').style.display = 'block';
        document.getElementById('noTamanhosAlert').style.display = 'none';
    }
}

// Função para toggle de um tamanho específico
function toggleTamanho(id, tipo) {
    const content = document.getElementById(`content-tamanho-${tipo}-${id}`);
    const icon = document.getElementById(`toggle-tamanho-${tipo}-${id}`);
    
    if (content.style.display === 'none') {
        content.style.display = 'block';
        icon.classList.remove('bi-chevron-right');
        icon.classList.add('bi-chevron-down');
    } else {
        content.style.display = 'none';
        icon.classList.remove('bi-chevron-down');
        icon.classList.add('bi-chevron-right');
    }
}

// Função para expandir/recolher todos os tamanhos
function toggleTodosTamanhos() {
    const contents = document.querySelectorAll('.tamanho-content');
    const icons = document.querySelectorAll('#secao-tamanhos .toggle-icon');
    const toggleBtn = document.getElementById('toggleTamanhosBtn');
    
    contents.forEach(content => {
        if (todosTamanhosExpandidos) {
            content.style.display = 'none';
        } else {
            content.style.display = 'block';
        }
    });
    
    icons.forEach(icon => {
        if (todosTamanhosExpandidos) {
            icon.classList.remove('bi-chevron-down');
            icon.classList.add('bi-chevron-right');
        } else {
            icon.classList.remove('bi-chevron-right');
            icon.classList.add('bi-chevron-down');
        }
    });
    
    if (todosTamanhosExpandidos) {
        toggleBtn.innerHTML = '<i class="bi bi-arrows-collapse"></i> Expandir Todos';
        todosTamanhosExpandidos = false;
    } else {
        toggleBtn.innerHTML = '<i class="bi bi-arrows-expand"></i> Recolher Todos';
        todosTamanhosExpandidos = true;
    }
}

// Função para adicionar um novo tamanho detalhado
function adicionarTamanhoDetalhado() {
    tamanhoCounter++;
    
    const container = document.getElementById('tamanhosContainer');
    const tamanhoHtml = `
        <div class="tamanho-item border rounded mb-3" id="tamanho-${tamanhoCounter}">
            <div class="tamanho-header d-flex justify-content-between align-items-center p-3 bg-light rounded-top" 
                 style="cursor: pointer;" onclick="toggleTamanho(${tamanhoCounter}, 'novo')">
                <h6 class="mb-0">
                    <i class="bi bi-rulers text-primary"></i> Tamanho ${tamanhoCounter}
                    <i class="bi bi-chevron-down ms-2 toggle-icon" id="toggle-tamanho-novo-${tamanhoCounter}"></i>
                </h6>
                <button type="button" class="btn btn-sm btn-outline-danger" onclick="event.stopPropagation(); removerTamanho(${tamanhoCounter})">
                    <i class="bi bi-trash"></i> Remover
                </button>
            </div>
            
            <div class="tamanho-content p-3" id="content-tamanho-novo-${tamanhoCounter}">
                <div class="row">
                    <div class="col-md-6">
                        <div class="form-floating mb-3">
                            <select class="form-select" name="tamanho_modulo_${tamanhoCounter}" required>
                                <option value="">Selecione o módulo</option>
                                <!-- Módulos serão carregados dinamicamente -->
                            </select>
                            <label>Módulo *</label>
                        </div>
                    </div>
                    <div class="col-md-6">
                        <div class="form-floating mb-3">
                            <input type="number" step="0.01" class="form-control" name="tamanho_largura_total_${tamanhoCounter}" 
                                   placeholder="Largura Total">
                            <label>Largura Total (cm)</label>
                        </div>
                    </div>
                </div>
                
                <div class="row">
                    <div class="col-md-4">
                        <div class="form-floating mb-3">
                            <input type="number" step="0.01" class="form-control" name="tamanho_largura_assento_${tamanhoCounter}" 
                                   placeholder="Largura do Assento">
                            <label>Largura do Assento (cm)</label>
                        </div>
                    </div>
                    <div class="col-md-4">
                        <div class="form-floating mb-3">
                            <input type="number" step="0.01" class="form-control" name="tamanho_tecido_metros_${tamanhoCounter}" 
                                   placeholder="Tecido">
                            <label>Tecido (metros)</label>
                        </div>
                    </div>
                    <div class="col-md-4">
                        <div class="form-floating mb-3">
                            <input type="number" step="0.001" class="form-control" name="tamanho_volume_m3_${tamanhoCounter}" 
                                   placeholder="Volume">
                            <label>Volume (m³)</label>
                        </div>
                    </div>
                </div>
                
                <div class="row">
                    <div class="col-md-4">
                        <div class="form-floating mb-3">
                            <input type="number" step="0.01" class="form-control" name="tamanho_peso_kg_${tamanhoCounter}" 
                                   placeholder="Peso">
                            <label>Peso (kg)</label>
                        </div>
                    </div>
                    <div class="col-md-4">
                        <div class="form-floating mb-3">
                            <input type="number" step="0.01" class="form-control" name="tamanho_preco_${tamanhoCounter}" 
                                   placeholder="Preço">
                            <label>Preço (R$)</label>
                        </div>
                    </div>
                    <div class="col-md-4">
                        <div class="mb-3">
                            <label class="form-label">Descrição</label>
                            <textarea class="form-control" name="tamanho_descricao_${tamanhoCounter}" 
                                      rows="2" placeholder="Descrição do tamanho"></textarea>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    `;
    
    container.insertAdjacentHTML('beforeend', tamanhoHtml);
    
    // Mostrar a seção de tamanhos
    document.getElementById('secao-tamanhos').style.display = 'block';
    document.getElementById('noTamanhosAlert').style.display = 'none';
    
    // Carregar opções de módulos no novo select
    carregarModulosNoSelect(`tamanho_modulo_${tamanhoCounter}`);
}

// Função para remover um tamanho
function removerTamanho(id) {
    const tamanho = document.getElementById(`tamanho-${id}`);
    if (tamanho) {
        tamanho.remove();
        
        // Verificar se ainda há tamanhos
        const tamanhosRestantes = document.querySelectorAll('.tamanho-item');
        if (tamanhosRestantes.length === 0) {
            document.getElementById('secao-tamanhos').style.display = 'none';
            document.getElementById('noTamanhosAlert').style.display = 'block';
        }
    }
}

// Função para remover um tamanho existente
function removerTamanhoExistente(id) {
    const tamanho = document.getElementById(`tamanho-existente-${id}`);
    if (tamanho) {
        tamanho.remove();
        
        // Verificar se ainda há tamanhos
        const tamanhosRestantes = document.querySelectorAll('.tamanho-item');
        if (tamanhosRestantes.length === 0) {
            document.getElementById('secao-tamanhos').style.display = 'none';
            document.getElementById('noTamanhosAlert').style.display = 'block';
        }
    }
}

// Função para carregar módulos no select
function carregarModulosNoSelect(selectId) {
    const select = document.getElementById(selectId);
    const modulosContainer = document.getElementById('modulosContainer');
    
    // Limpar opções existentes exceto a primeira
    while (select.children.length > 1) {
        select.removeChild(select.lastChild);
    }
    
    // Buscar módulos existentes
    const modulosExistentes = modulosContainer.querySelectorAll('.modulo-item');
    modulosExistentes.forEach((modulo, index) => {
        const nomeInput = modulo.querySelector('input[name="modulo_nome"]');
        if (nomeInput && nomeInput.value.trim()) {
            const option = document.createElement('option');
            option.value = `novo_${index + 1}`;
            option.textContent = nomeInput.value;
            select.appendChild(option);
        }
    });
}

// Inicializar quando a página carrega
document.addEventListener('DOMContentLoaded', function() {
    inicializarTamanhos();
});
