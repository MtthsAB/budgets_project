#!/usr/bin/env python3
"""
Script para depuração em tempo real da hidratação
"""

import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema_produtos.settings')
django.setup()

from django.test import Client
from authentication.models import CustomUser
import re

def criar_pagina_debug():
    """Criar página de debug com console de hidratação"""
    
    # Fazer login e obter conteúdo da página
    user = CustomUser.objects.get(email='teste@teste.com')
    client = Client()
    client.force_login(user)
    
    response = client.get('/orcamentos/5/editar/')
    content = response.content.decode('utf-8')
    
    # Injetar JavaScript de debug
    debug_js = """
    <script>
    // Override console.log para capturar na página
    var originalLog = console.log;
    var debugOutput = [];
    
    console.log = function() {
        originalLog.apply(console, arguments);
        var args = Array.prototype.slice.call(arguments);
        var message = args.map(arg => typeof arg === 'object' ? JSON.stringify(arg) : String(arg)).join(' ');
        debugOutput.push(new Date().toLocaleTimeString() + ': ' + message);
        updateDebugConsole();
    };
    
    function updateDebugConsole() {
        var debugDiv = document.getElementById('debug-console');
        if (debugDiv) {
            debugDiv.innerHTML = '<h4>Console Debug:</h4><pre>' + debugOutput.join('\\n') + '</pre>';
        }
    }
    
    // Verificação detalhada dos elementos
    function verificarElementos() {
        console.log('=== VERIFICAÇÃO DE ELEMENTOS ===');
        
        var elementos = {
            'cliente-busca': document.getElementById('cliente-busca'),
            'id_cliente': document.getElementById('id_cliente'),
            'desconto_valor_unificado': document.getElementById('desconto_valor_unificado'),
            'acrescimo_valor_unificado': document.getElementById('acrescimo_valor_unificado'),
            'desconto_tipo_btn': document.getElementById('desconto_tipo_btn'),
            'acrescimo_tipo_btn': document.getElementById('acrescimo_tipo_btn'),
            'id_desconto_valor': document.getElementById('id_desconto_valor'),
            'id_desconto_percentual': document.getElementById('id_desconto_percentual'),
            'id_acrescimo_valor': document.getElementById('id_acrescimo_valor'),
            'id_acrescimo_percentual': document.getElementById('id_acrescimo_percentual')
        };
        
        for (var id in elementos) {
            var elemento = elementos[id];
            if (elemento) {
                console.log('✅ ' + id + ': encontrado - valor atual: "' + (elemento.value || elemento.textContent || 'N/A') + '"');
            } else {
                console.log('❌ ' + id + ': NÃO ENCONTRADO');
            }
        }
    }
    
    // Testar hidratação manual
    function testarHidratacaoManual() {
        console.log('=== TESTE DE HIDRATAÇÃO MANUAL ===');
        
        if (typeof window.orcamentoData === 'undefined') {
            console.log('❌ window.orcamentoData não definido');
            return;
        }
        
        console.log('✅ window.orcamentoData encontrado:', window.orcamentoData);
        
        // Testar hidratação do cliente
        var clienteBusca = document.getElementById('cliente-busca');
        var clienteSelect = document.getElementById('id_cliente');
        
        if (window.orcamentoData.cliente_nome && clienteBusca) {
            clienteBusca.value = window.orcamentoData.cliente_nome;
            console.log('✅ Cliente hidratado: ' + window.orcamentoData.cliente_nome);
        }
        
        if (window.orcamentoData.cliente_id && clienteSelect) {
            clienteSelect.value = window.orcamentoData.cliente_id;
            console.log('✅ Cliente ID hidratado: ' + window.orcamentoData.cliente_id);
        }
        
        // Testar hidratação de desconto
        var descontoInput = document.getElementById('desconto_valor_unificado');
        var descontoBtn = document.getElementById('desconto_tipo_btn');
        
        if (window.orcamentoData.desconto_percentual && window.orcamentoData.desconto_percentual > 0) {
            if (descontoInput) {
                descontoInput.value = window.orcamentoData.desconto_percentual;
                console.log('✅ Desconto valor hidratado: ' + window.orcamentoData.desconto_percentual);
            }
            
            if (descontoBtn) {
                descontoBtn.setAttribute('data-tipo', 'percentual');
                var textoSpan = descontoBtn.querySelector('.tipo-texto');
                if (textoSpan) {
                    textoSpan.textContent = '%';
                    console.log('✅ Desconto botão hidratado: %');
                }
            }
        }
        
        // Testar hidratação de acréscimo
        var acrescimoInput = document.getElementById('acrescimo_valor_unificado');
        var acrescimoBtn = document.getElementById('acrescimo_tipo_btn');
        
        if (window.orcamentoData.acrescimo_percentual && window.orcamentoData.acrescimo_percentual > 0) {
            if (acrescimoInput) {
                acrescimoInput.value = window.orcamentoData.acrescimo_percentual;
                console.log('✅ Acréscimo valor hidratado: ' + window.orcamentoData.acrescimo_percentual);
            }
            
            if (acrescimoBtn) {
                acrescimoBtn.setAttribute('data-tipo', 'percentual');
                var textoSpan = acrescimoBtn.querySelector('.tipo-texto');
                if (textoSpan) {
                    textoSpan.textContent = '%';
                    console.log('✅ Acréscimo botão hidratado: %');
                }
            }
        }
        
        // Verificar estado final
        console.log('=== ESTADO FINAL ===');
        setTimeout(function() {
            verificarElementos();
        }, 100);
    }
    
    // Executar quando DOM estiver pronto
    document.addEventListener('DOMContentLoaded', function() {
        console.log('DOMContentLoaded disparado para debug');
        
        // Adicionar div de debug
        var debugDiv = document.createElement('div');
        debugDiv.id = 'debug-console';
        debugDiv.style.cssText = 'position: fixed; top: 10px; right: 10px; width: 400px; height: 300px; background: white; border: 2px solid #333; z-index: 9999; padding: 10px; overflow-y: scroll; font-family: monospace; font-size: 12px;';
        document.body.appendChild(debugDiv);
        
        // Adicionar botões de teste
        var btnContainer = document.createElement('div');
        btnContainer.style.cssText = 'position: fixed; top: 320px; right: 10px; z-index: 9999;';
        
        var btnVerificar = document.createElement('button');
        btnVerificar.textContent = 'Verificar Elementos';
        btnVerificar.onclick = verificarElementos;
        btnVerificar.style.cssText = 'margin: 5px; padding: 10px; background: #007bff; color: white; border: none; cursor: pointer;';
        
        var btnTestar = document.createElement('button');
        btnTestar.textContent = 'Testar Hidratação';
        btnTestar.onclick = testarHidratacaoManual;
        btnTestar.style.cssText = 'margin: 5px; padding: 10px; background: #28a745; color: white; border: none; cursor: pointer;';
        
        var btnLimpar = document.createElement('button');
        btnLimpar.textContent = 'Limpar Console';
        btnLimpar.onclick = function() { debugOutput = []; updateDebugConsole(); };
        btnLimpar.style.cssText = 'margin: 5px; padding: 10px; background: #dc3545; color: white; border: none; cursor: pointer;';
        
        btnContainer.appendChild(btnVerificar);
        btnContainer.appendChild(btnTestar);
        btnContainer.appendChild(btnLimpar);
        document.body.appendChild(btnContainer);
        
        // Executar verificação inicial
        setTimeout(function() {
            console.log('Executando verificação inicial...');
            verificarElementos();
        }, 500);
    });
    </script>
    """
    
    # Injetar o script antes do fechamento do body
    content_with_debug = content.replace('</body>', debug_js + '</body>')
    
    # Salvar página com debug
    with open('/tmp/orcamento_debug_interativo.html', 'w', encoding='utf-8') as f:
        f.write(content_with_debug)
    
    print("💾 Página de debug criada: /tmp/orcamento_debug_interativo.html")
    print("🌐 Abra file:///tmp/orcamento_debug_interativo.html")
    print("📱 Use os botões no canto superior direito para testar")
    
    return True

if __name__ == '__main__':
    criar_pagina_debug()
    print("\n🧪 INSTRUÇÕES DE TESTE:")
    print("1. Abra file:///tmp/orcamento_debug_interativo.html")
    print("2. Use os botões de teste no canto superior direito")
    print("3. Verifique o console de debug na tela")
    print("4. Compare com o comportamento esperado")
