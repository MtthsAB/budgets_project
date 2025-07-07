/**
 * JavaScript para gerenciamento de módulos de sofás
 */

let moduloCounter = 0;
let todosExpandidos = true;

// Função para inicializar a seção de módulos
function inicializarModulos() {
    // Verificar se já existem módulos
    const modulosExistentes = document.querySelectorAll('.modulo-item');
    moduloCounter = modulosExistentes.length;
    
    console.log('Inicializando módulos. Encontrados:', moduloCounter);
    
    // Se não há módulos, esconder a seção
    if (moduloCounter === 0) {
        const secaoModulos = document.getElementById('secao-modulos');
        const noModulosAlert = document.getElementById('noModulosAlert');
        
        if (secaoModulos) secaoModulos.style.display = 'none';
        if (noModulosAlert) noModulosAlert.style.display = 'block';
    } else {
        const secaoModulos = document.getElementById('secao-modulos');
        const noModulosAlert = document.getElementById('noModulosAlert');
        
        if (secaoModulos) secaoModulos.style.display = 'block';
        if (noModulosAlert) noModulosAlert.style.display = 'none';
        
        // Inicializar estado dos botões
        const toggleText = document.getElementById('toggleModulosText');
        const toggleIcon = document.querySelector('#toggleModulosBtn i');
        
        if (toggleText) toggleText.textContent = 'Recolher Todos';
        if (toggleIcon) toggleIcon.className = 'bi bi-arrows-expand';
        
        todosExpandidos = true;
    }
}

// Função para toggle de um módulo específico
function toggleModulo(id, tipo) {
    const content = document.getElementById(`content-${tipo}-${id}`);
    const icon = document.getElementById(`toggle-${tipo}-${id}`);
    
    console.log('Toggle módulo:', id, tipo);
    console.log('Content:', content);
    console.log('Icon:', icon);
    
    if (content && icon) {
        if (content.style.display === 'none') {
            content.style.display = 'block';
            icon.classList.remove('bi-chevron-right');
            icon.classList.add('bi-chevron-down');
            icon.style.transform = 'rotate(0deg)';
        } else {
            content.style.display = 'none';
            icon.classList.remove('bi-chevron-down');
            icon.classList.add('bi-chevron-right');
            icon.style.transform = 'rotate(-90deg)';
        }
    } else {
        console.error('Elementos não encontrados para módulo:', id, tipo);
    }
}

// Função para expandir/recolher todos os módulos
function toggleTodosModulos() {
    const contents = document.querySelectorAll('.modulo-content');
    const icons = document.querySelectorAll('#secao-modulos .toggle-icon');
    const toggleBtn = document.getElementById('toggleModulosBtn');
    const toggleText = document.getElementById('toggleModulosText');
    const toggleIcon = toggleBtn.querySelector('i');
    
    console.log('Toggle clicado. Estado atual:', todosExpandidos);
    console.log('Encontrados:', contents.length, 'conteúdos e', icons.length, 'ícones');
    
    contents.forEach(content => {
        if (todosExpandidos) {
            content.style.display = 'none';
        } else {
            content.style.display = 'block';
        }
    });
    
    icons.forEach(icon => {
        if (todosExpandidos) {
            icon.classList.remove('bi-chevron-down');
            icon.classList.add('bi-chevron-right');
        } else {
            icon.classList.remove('bi-chevron-right');
            icon.classList.add('bi-chevron-down');
        }
    });
    
    if (todosExpandidos) {
        toggleIcon.className = 'bi bi-arrows-collapse';
        toggleText.textContent = 'Expandir Todos';
        todosExpandidos = false;
    } else {
        toggleIcon.className = 'bi bi-arrows-expand';
        toggleText.textContent = 'Recolher Todos';
        todosExpandidos = true;
    }
    
    console.log('Novo estado:', todosExpandidos);
}

// Função para adicionar um novo módulo
function adicionarModulo() {
    moduloCounter++;
    
    const container = document.getElementById('modulosContainer');
    const moduloHtml = `
        <div class="modulo-item border rounded mb-3" id="modulo-${moduloCounter}">
            <div class="modulo-header d-flex justify-content-between align-items-center p-3 bg-primary bg-opacity-10 rounded-top border-bottom" 
                 style="cursor: pointer; transition: background-color 0.2s; user-select: none;" 
                 onclick="toggleModulo(${moduloCounter}, 'novo')"
                 onmouseover="this.style.backgroundColor='rgba(13, 110, 253, 0.15)'"
                 onmouseout="this.style.backgroundColor='rgba(13, 110, 253, 0.1)'">
                <h6 class="mb-0 d-flex align-items-center">
                    <i class="bi bi-cube text-primary me-2"></i> 
                    <span class="fw-semibold">Módulo ${moduloCounter}</span>
                    <i class="bi bi-chevron-down ms-2 toggle-icon text-primary" id="toggle-novo-${moduloCounter}" 
                       style="transition: transform 0.2s;"></i>
                </h6>
                <button type="button" class="btn btn-sm btn-outline-danger" 
                        onclick="event.stopPropagation(); removerModulo(${moduloCounter})"
                        title="Remover módulo">
                    <i class="bi bi-trash"></i> Remover
                </button>
            </div>
            
            <div class="modulo-content p-3" id="content-novo-${moduloCounter}">
                <div class="row">
                    <div class="col-md-6">
                        <div class="form-floating mb-3">
                            <input type="text" class="form-control" name="modulo_nome" 
                                   id="modulo_nome_${moduloCounter}" placeholder="Nome do módulo" required>
                            <label for="modulo_nome_${moduloCounter}">Nome do Módulo</label>
                        </div>
                    </div>
                    <div class="col-md-6">
                        <div class="form-floating mb-3">
                            <input type="number" step="0.01" class="form-control" name="modulo_profundidade_${moduloCounter}" 
                                   id="modulo_profundidade_${moduloCounter}" placeholder="Profundidade">
                            <label for="modulo_profundidade_${moduloCounter}">Profundidade (cm)</label>
                        </div>
                    </div>
                </div>
                
                <div class="row">
                    <div class="col-md-4">
                        <div class="form-floating mb-3">
                            <input type="number" step="0.01" class="form-control" name="modulo_altura_${moduloCounter}" 
                                   id="modulo_altura_${moduloCounter}" placeholder="Altura">
                            <label for="modulo_altura_${moduloCounter}">Altura (cm)</label>
                        </div>
                    </div>
                    <div class="col-md-4">
                        <div class="form-floating mb-3">
                            <input type="number" step="0.01" class="form-control" name="modulo_braco_${moduloCounter}" 
                                   id="modulo_braco_${moduloCounter}" placeholder="Braço">
                            <label for="modulo_braco_${moduloCounter}">Braço (cm)</label>
                        </div>
                    </div>
                    <div class="col-md-4">
                        <div class="mb-3">
                            <label for="modulo_imagem_${moduloCounter}" class="form-label">Imagem do Módulo</label>
                            <input type="file" class="form-control" name="modulo_imagem_principal_${moduloCounter}" 
                                   id="modulo_imagem_${moduloCounter}" accept="image/*">
                        </div>
                    </div>
                </div>
                
                <div class="mb-3">
                    <label for="modulo_descricao_${moduloCounter}" class="form-label">Descrição</label>
                    <textarea class="form-control" name="modulo_descricao_${moduloCounter}" 
                              id="modulo_descricao_${moduloCounter}" rows="2" placeholder="Descrição do módulo"></textarea>
                </div>
            </div>
        </div>
    `;
    
    container.insertAdjacentHTML('beforeend', moduloHtml);
    
    // Mostrar a seção de módulos
    document.getElementById('secao-modulos').style.display = 'block';
    document.getElementById('noModulosAlert').style.display = 'none';
    
    // Focar no campo nome do módulo recém-criado
    document.getElementById(`modulo_nome_${moduloCounter}`).focus();
}

// Função para remover um módulo
function removerModulo(id) {
    const modulo = document.getElementById(`modulo-${id}`);
    if (modulo) {
        modulo.remove();
        
        // Verificar se ainda há módulos
        const modulosRestantes = document.querySelectorAll('.modulo-item');
        if (modulosRestantes.length === 0) {
            document.getElementById('secao-modulos').style.display = 'none';
            document.getElementById('noModulosAlert').style.display = 'block';
        }
    }
}

// Função para remover um módulo existente
function removerModuloExistente(id) {
    const modulo = document.getElementById(`modulo-existente-${id}`);
    if (modulo) {
        modulo.remove();
        
        // Verificar se ainda há módulos
        const modulosRestantes = document.querySelectorAll('.modulo-item');
        if (modulosRestantes.length === 0) {
            document.getElementById('secao-modulos').style.display = 'none';
            document.getElementById('noModulosAlert').style.display = 'block';
        }
    }
}

// Inicializar quando a página carrega
document.addEventListener('DOMContentLoaded', function() {
    inicializarModulos();
});
