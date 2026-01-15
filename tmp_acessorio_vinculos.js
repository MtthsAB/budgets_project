(() => {
    const csrftoken = getCookie('csrftoken');

    document.addEventListener('DOMContentLoaded', () => {
        const tipoSelect = document.getElementById('tipo_produto');
        const vincSection = document.getElementById('vinculacao-produtos');
        if (vincSection && !tipoSelect) {
            vincSection.style.display = 'block';
        }

        document.querySelectorAll('[data-acessorio-vinculos]').forEach((root) => {
            const manager = new AcessorioVinculosManager(root, csrftoken);
            manager.init();
        });
    });

    function getCookie(name) {
        if (!document.cookie) {
            return null;
        }
        const cookies = document.cookie.split(';').map((cookie) => cookie.trim());
        for (const cookie of cookies) {
            if (cookie.startsWith(`${name}=`)) {
                return decodeURIComponent(cookie.substring(name.length + 1));
            }
        }
        return null;
    }

    class AcessorioVinculosManager {
        constructor(root, csrftoken) {
            this.root = root;
            this.csrftoken = csrftoken;
            this.sofasEndpoint = root.dataset.sofasEndpoint || '';
            this.vinculosEndpoint = root.dataset.vinculosEndpoint || '';
            this.acessorioId = root.dataset.acessorioId || '';

            this.searchInput = root.querySelector('[data-role="sofa-search"]');
            this.listEl = root.querySelector('[data-role="sofa-list"]');
            this.selectedEl = root.querySelector('[data-role="sofa-selected"]');
            this.messageEl = root.querySelector('[data-role="sofa-message"]');
            this.hiddenEl = root.querySelector('[data-role="sofa-hidden"]');

            this.sofas = [];
            this.sofasMap = new Map();
            this.selected = new Map();
        }

        init() {
            this.bindEvents();
            this.loadSofas();
            if (this.acessorioId && this.vinculosEndpoint) {
                this.loadVinculos();
            }
        }

        bindEvents() {
            if (this.searchInput) {
                this.searchInput.addEventListener('input', () => this.renderAvailable());
            }

            this.root.addEventListener('click', (event) => {
                const target = event.target.closest('[data-action]');
                if (!target) return;

                const action = target.dataset.action;
                const sofaId = target.dataset.sofaId;
                if (!sofaId) return;

                if (action === 'add') {
                    this.addSofa(sofaId);
                }

                if (action === 'remove') {
                    this.removeSofa(sofaId);
                }
            });
        }

        async loadSofas() {
            if (!this.sofasEndpoint) {
                this.showMessage('danger', 'Endpoint de sofás não configurado.');
                return;
            }

            try {
                const response = await fetch(this.sofasEndpoint, { headers: { 'Accept': 'application/json' } });
                const data = await response.json();
                if (!response.ok) {
                    throw new Error(data.error || 'Erro ao carregar sofás.');
                }

                this.sofas = Array.isArray(data.sofas) ? data.sofas : [];
                this.sofasMap = new Map(this.sofas.map((sofa) => [String(sofa.id), sofa]));
                this.renderAvailable();
            } catch (error) {
                this.sofas = [];
                this.sofasMap = new Map();
                this.renderAvailable();
                this.showMessage('danger', error.message);
            }
        }

        async loadVinculos() {
            try {
                const response = await fetch(this.vinculosEndpoint, { headers: { 'Accept': 'application/json' } });
                const data = await response.json();
                if (!response.ok) {
                    throw new Error(data.error || 'Erro ao carregar vínculos.');
                }

                const vinculados = Array.isArray(data.sofas) ? data.sofas : [];
                vinculados.forEach((sofa) => {
                    this.selected.set(String(sofa.id), sofa);
                });

                this.updateHiddenInputs();
                this.renderAvailable();
                this.renderSelected();
            } catch (error) {
                this.showMessage('danger', error.message);
            }
        }

        renderAvailable() {
            if (!this.listEl) return;

            const termo = (this.searchInput?.value || '').trim().toLowerCase();
            const sofasFiltrados = this.sofas.filter((sofa) => {
                if (!termo) return true;
                const ref = (sofa.ref_produto || '').toLowerCase();
                const nome = (sofa.nome_produto || '').toLowerCase();
                return ref.includes(termo) || nome.includes(termo);
            });

            if (!sofasFiltrados.length) {
                this.listEl.innerHTML = '<div class="list-group-item text-muted">Nenhum sofá encontrado.</div>';
                return;
            }

            this.listEl.innerHTML = sofasFiltrados.map((sofa) => {
                const sofaId = String(sofa.id);
                const isSelected = this.selected.has(sofaId);
                const buttonLabel = isSelected ? 'Vinculado' : 'Vincular';
                const buttonClass = isSelected ? 'btn-outline-secondary' : 'btn-outline-primary';
                const disabledAttr = isSelected ? 'disabled' : '';

                return `
                    <div class="list-group-item d-flex align-items-center justify-content-between">
                        <div>
                            <div class="fw-semibold">${sofa.ref_produto} - ${sofa.nome_produto}</div>
                        </div>
                        <button type="button" class="btn btn-sm ${buttonClass}" data-action="add" data-sofa-id="${sofaId}" ${disabledAttr}>
                            ${buttonLabel}
                        </button>
                    </div>
                `;
            }).join('');
        }

        renderSelected() {
            if (!this.selectedEl) return;

            const selectedArray = Array.from(this.selected.values());
            if (!selectedArray.length) {
                this.selectedEl.innerHTML = '<div class="list-group-item text-muted">Nenhum sofá vinculado.</div>';
                return;
            }

            this.selectedEl.innerHTML = selectedArray.map((sofa) => {
                const sofaId = String(sofa.id);
                return `
                    <div class="list-group-item d-flex align-items-center justify-content-between">
                        <div>
                            <div class="fw-semibold">${sofa.ref_produto} - ${sofa.nome_produto}</div>
                        </div>
                        <button type="button" class="btn btn-sm btn-outline-danger" data-action="remove" data-sofa-id="${sofaId}">
                            Remover
                        </button>
                    </div>
                `;
            }).join('');
        }

        async addSofa(sofaId) {
            if (this.selected.has(String(sofaId))) {
                return;
            }

            const sofa = this.sofasMap.get(String(sofaId));
            if (!sofa) {
                this.showMessage('danger', 'Sofá não encontrado na lista disponível.');
                return;
            }

            if (this.acessorioId && this.vinculosEndpoint) {
                const ok = await this.persistAdd([sofaId]);
                if (!ok) return;
            }

            this.selected.set(String(sofaId), sofa);
            this.updateHiddenInputs();
            this.renderAvailable();
            this.renderSelected();
        }

        async removeSofa(sofaId) {
            if (!this.selected.has(String(sofaId))) {
                return;
            }

            if (this.acessorioId && this.vinculosEndpoint) {
                const ok = await this.persistRemove(sofaId);
                if (!ok) return;
            }

            this.selected.delete(String(sofaId));
            this.updateHiddenInputs();
            this.renderAvailable();
            this.renderSelected();
        }

        async persistAdd(sofaIds) {
            if (!this.csrftoken) {
                this.showMessage('danger', 'CSRF token não encontrado.');
                return false;
            }

            try {
                const response = await fetch(this.vinculosEndpoint, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': this.csrftoken,
                        'Accept': 'application/json'
                    },
                    body: JSON.stringify({ sofa_ids: sofaIds })
                });
                const data = await response.json();
                if (!response.ok) {
                    throw new Error(data.error || 'Erro ao adicionar vínculo.');
                }
                this.showMessage('success', 'Vínculo adicionado com sucesso.');
                return true;
            } catch (error) {
                this.showMessage('danger', error.message);
                return false;
            }
        }

        async persistRemove(sofaId) {
            if (!this.csrftoken) {
                this.showMessage('danger', 'CSRF token não encontrado.');
                return false;
            }

            const url = this.vinculosEndpoint.endsWith('/')
                ? `${this.vinculosEndpoint}${sofaId}/`
                : `${this.vinculosEndpoint}/${sofaId}/`;

            try {
                const response = await fetch(url, {
                    method: 'DELETE',
                    headers: {
                        'X-CSRFToken': this.csrftoken,
                        'Accept': 'application/json'
                    }
                });
                const data = await response.json();
                if (!response.ok) {
                    throw new Error(data.error || 'Erro ao remover vínculo.');
                }
                this.showMessage('success', 'Vínculo removido com sucesso.');
                return true;
            } catch (error) {
                this.showMessage('danger', error.message);
                return false;
            }
        }

        updateHiddenInputs() {
            if (!this.hiddenEl) return;
            this.hiddenEl.innerHTML = '';
            this.selected.forEach((sofa) => {
                const input = document.createElement('input');
                input.type = 'hidden';
                input.name = 'produtos_vinculados';
                input.value = sofa.id;
                this.hiddenEl.appendChild(input);
            });
        }

        showMessage(type, message) {
            if (!this.messageEl) return;
            const alertType = type === 'success' ? 'alert-success' : 'alert-danger';
            this.messageEl.innerHTML = `
                <div class="alert ${alertType} py-2 mb-0" role="alert">
                    ${message}
                </div>
            `;
        }
    }

    window.toggleCamposEspecificos = function toggleCamposEspecificos(tipoNome) {
        const camposAcessorio = document.getElementById('campos-acessorio');
        const vinculacaoProdutos = document.getElementById('vinculacao-produtos');

        if (camposAcessorio) camposAcessorio.style.display = 'none';
        if (vinculacaoProdutos) vinculacaoProdutos.style.display = 'none';

        if (tipoNome === 'Acessórios') {
            if (camposAcessorio) camposAcessorio.style.display = 'flex';
            if (vinculacaoProdutos) vinculacaoProdutos.style.display = 'block';
        }
    };

    window.validacaoEspecifica = function validacaoEspecifica(e) {
        const precoAcessorio = document.getElementById('preco_acessorio');
        if (precoAcessorio) {
            const valor = parseFloat(precoAcessorio.value || '0');
            if (Number.isNaN(valor) || valor < 0) {
                e.preventDefault();
                alert('Por favor, informe um preço válido para o acessório.');
                return false;
            }
        }
        return true;
    };
})();
