#!/usr/bin/env python3
"""
Script para testar se o JavaScript está executando corretamente
"""

import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema_produtos.settings')
django.setup()

from django.test import Client
from authentication.models import CustomUser
import time

def teste_javascript_execucao():
    """Teste de execução do JavaScript usando selenium-like approach"""
    
    print("🧪 === TESTE DE EXECUÇÃO DO JAVASCRIPT ===")
    
    # Fazer login
    user = CustomUser.objects.get(email='teste@teste.com')
    client = Client()
    client.force_login(user)
    
    # Acessar página de edição
    response = client.get('/orcamentos/5/editar/')
    content = response.content.decode('utf-8')
    
    print("✅ Página acessada")
    
    # Vou criar um HTML com JavaScript de teste para simular o comportamento
    html_teste = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Teste Hidratação</title>
    </head>
    <body>
        <div id="resultado"></div>
        
        <!-- Simular dados do orçamento -->
        <script>
        {content[content.find('window.orcamentoData'):content.find('};', content.find('window.orcamentoData')) + 2]}
        </script>
        
        <!-- Simular elementos HTML -->
        <input type="text" id="cliente-busca" placeholder="Cliente">
        <input type="hidden" id="id_cliente">
        <input type="number" id="desconto_valor_unificado" value="0">
        <button type="button" id="desconto_tipo_btn" data-tipo="valor">
            <span class="tipo-texto">R$</span>
        </button>
        <input type="number" id="acrescimo_valor_unificado" value="0">
        <button type="button" id="acrescimo_tipo_btn" data-tipo="valor">
            <span class="tipo-texto">R$</span>
        </button>
        
        <!-- Campos originais ocultos -->
        <input type="hidden" id="id_desconto_valor">
        <input type="hidden" id="id_desconto_percentual">
        <input type="hidden" id="id_acrescimo_valor">
        <input type="hidden" id="id_acrescimo_percentual">
        
        <script>
        // Função específica para hidratar desconto e acréscimo
        function hidratarDescontoAcrescimo(data) {{
            console.log('Dados de desconto/acréscimo recebidos:', {{
                desconto_valor: data.desconto_valor,
                desconto_percentual: data.desconto_percentual,
                acrescimo_valor: data.acrescimo_valor,
                acrescimo_percentual: data.acrescimo_percentual
            }});
            
            // Elementos dos campos unificados
            const descontoInput = document.getElementById('desconto_valor_unificado');
            const descontoBtn = document.getElementById('desconto_tipo_btn');
            const acrescimoInput = document.getElementById('acrescimo_valor_unificado');
            const acrescimoBtn = document.getElementById('acrescimo_tipo_btn');
            
            // Elementos dos campos originais
            const descontoValorOrig = document.getElementById('id_desconto_valor');
            const descontoPercOrig = document.getElementById('id_desconto_percentual');
            const acrescimoValorOrig = document.getElementById('id_acrescimo_valor');
            const acrescimoPercOrig = document.getElementById('id_acrescimo_percentual');
            
            let resultado = document.getElementById('resultado');
            resultado.innerHTML = '<h3>Teste de Hidratação</h3>';
            
            // Hidratar desconto
            if (data.desconto_valor && data.desconto_valor > 0) {{
                console.log('Hidratando desconto em VALOR:', data.desconto_valor);
                if (descontoInput) descontoInput.value = data.desconto_valor;
                if (descontoBtn) {{
                    descontoBtn.setAttribute('data-tipo', 'valor');
                    const textoSpan = descontoBtn.querySelector('.tipo-texto');
                    if (textoSpan) textoSpan.textContent = 'R$';
                }}
                if (descontoValorOrig) descontoValorOrig.value = data.desconto_valor;
                if (descontoPercOrig) descontoPercOrig.value = '';
                resultado.innerHTML += '<p>✅ Desconto em valor hidratado: R$ ' + data.desconto_valor + '</p>';
            }} else if (data.desconto_percentual && data.desconto_percentual > 0) {{
                console.log('Hidratando desconto em PERCENTUAL:', data.desconto_percentual);
                if (descontoInput) descontoInput.value = data.desconto_percentual;
                if (descontoBtn) {{
                    descontoBtn.setAttribute('data-tipo', 'percentual');
                    const textoSpan = descontoBtn.querySelector('.tipo-texto');
                    if (textoSpan) textoSpan.textContent = '%';
                }}
                if (descontoPercOrig) descontoPercOrig.value = data.desconto_percentual;
                if (descontoValorOrig) descontoValorOrig.value = '';
                resultado.innerHTML += '<p>✅ Desconto em percentual hidratado: ' + data.desconto_percentual + '%</p>';
            }} else {{
                resultado.innerHTML += '<p>ℹ️ Nenhum desconto para hidratar</p>';
            }}
            
            // Hidratar acréscimo
            if (data.acrescimo_valor && data.acrescimo_valor > 0) {{
                console.log('Hidratando acréscimo em VALOR:', data.acrescimo_valor);
                if (acrescimoInput) acrescimoInput.value = data.acrescimo_valor;
                if (acrescimoBtn) {{
                    acrescimoBtn.setAttribute('data-tipo', 'valor');
                    const textoSpan = acrescimoBtn.querySelector('.tipo-texto');
                    if (textoSpan) textoSpan.textContent = 'R$';
                }}
                if (acrescimoValorOrig) acrescimoValorOrig.value = data.acrescimo_valor;
                if (acrescimoPercOrig) acrescimoPercOrig.value = '';
                resultado.innerHTML += '<p>✅ Acréscimo em valor hidratado: R$ ' + data.acrescimo_valor + '</p>';
            }} else if (data.acrescimo_percentual && data.acrescimo_percentual > 0) {{
                console.log('Hidratando acréscimo em PERCENTUAL:', data.acrescimo_percentual);
                if (acrescimoInput) acrescimoInput.value = data.acrescimo_percentual;
                if (acrescimoBtn) {{
                    acrescimoBtn.setAttribute('data-tipo', 'percentual');
                    const textoSpan = acrescimoBtn.querySelector('.tipo-texto');
                    if (textoSpan) textoSpan.textContent = '%';
                }}
                if (acrescimoPercOrig) acrescimoPercOrig.value = data.acrescimo_percentual;
                if (acrescimoValorOrig) acrescimoValorOrig.value = '';
                resultado.innerHTML += '<p>✅ Acréscimo em percentual hidratado: ' + data.acrescimo_percentual + '%</p>';
            }} else {{
                resultado.innerHTML += '<p>ℹ️ Nenhum acréscimo para hidratar</p>';
            }}
            
            // Mostrar estado final dos elementos
            resultado.innerHTML += '<h4>Estado Final dos Elementos:</h4>';
            resultado.innerHTML += '<p>Desconto Input: ' + (descontoInput ? descontoInput.value : 'NULO') + '</p>';
            resultado.innerHTML += '<p>Desconto Botão: ' + (descontoBtn ? descontoBtn.getAttribute('data-tipo') + ' - ' + descontoBtn.querySelector('.tipo-texto').textContent : 'NULO') + '</p>';
            resultado.innerHTML += '<p>Acréscimo Input: ' + (acrescimoInput ? acrescimoInput.value : 'NULO') + '</p>';
            resultado.innerHTML += '<p>Acréscimo Botão: ' + (acrescimoBtn ? acrescimoBtn.getAttribute('data-tipo') + ' - ' + acrescimoBtn.querySelector('.tipo-texto').textContent : 'NULO') + '</p>';
        }}
        
        // Função para hidratar campo cliente
        function hidratarCliente(data) {{
            const clienteBusca = document.getElementById('cliente-busca');
            const clienteSelect = document.getElementById('id_cliente');
            
            if (data.cliente_id && data.cliente_nome) {{
                if (clienteBusca) {{
                    clienteBusca.value = data.cliente_nome;
                    console.log('✓ Cliente hidratado no campo busca:', data.cliente_nome);
                }}
                if (clienteSelect) {{
                    clienteSelect.value = data.cliente_id;
                    console.log('✓ Cliente ID definido no select:', data.cliente_id);
                }}
                
                document.getElementById('resultado').innerHTML += '<p>✅ Cliente hidratado: ' + data.cliente_nome + ' (ID: ' + data.cliente_id + ')</p>';
            }}
        }}
        
        // Executar teste
        document.addEventListener('DOMContentLoaded', function() {{
            console.log('DOMContentLoaded disparado');
            console.log('window.orcamentoData:', window.orcamentoData);
            
            if (window.orcamentoData) {{
                console.log('Dados encontrados, iniciando hidratação...');
                hidratarCliente(window.orcamentoData);
                hidratarDescontoAcrescimo(window.orcamentoData);
            }} else {{
                document.getElementById('resultado').innerHTML = '<p>❌ window.orcamentoData não encontrado</p>';
            }}
        }});
        </script>
    </body>
    </html>
    """
    
    # Salvar HTML de teste
    with open('/tmp/teste_hidratacao.html', 'w', encoding='utf-8') as f:
        f.write(html_teste)
    
    print("💾 HTML de teste salvo em: /tmp/teste_hidratacao.html")
    print("🌐 Abra file:///tmp/teste_hidratacao.html no navegador para verificar se a hidratação funciona")
    
    return True

if __name__ == '__main__':
    teste_javascript_execucao()
    print("\n📝 INSTRUÇÕES:")
    print("1. Abra file:///tmp/teste_hidratacao.html no navegador")
    print("2. Abra DevTools (F12) → Console")
    print("3. Verifique se há logs de hidratação")
    print("4. Verifique se os campos são preenchidos")
    print("5. Compare com a página real de edição")
