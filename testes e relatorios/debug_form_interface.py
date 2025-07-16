#!/usr/bin/env python3
"""
Teste para verificar possíveis problemas com JavaScript ou interferências na submissão do formulário
"""
import os
import sys
import django

# Configurar o Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema_produtos.settings')
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
django.setup()

from django.template import Context, Template
from django.contrib.auth import get_user_model
from clientes.forms import ClienteForm

User = get_user_model()

def test_template_rendering():
    """Testa se o template está sendo renderizado corretamente"""
    print("🔍 Testando renderização do template...")
    
    try:
        # Criar um formulário vazio
        form = ClienteForm()
        
        # Template simples para testar
        template_content = """
        <form method="post" id="clienteForm">
            {{ form.nome_empresa }}
            <button type="submit" id="submitBtn">Salvar Cliente</button>
        </form>
        """
        
        template = Template(template_content)
        context = Context({'form': form})
        rendered = template.render(context)
        
        print("✅ Template renderizado com sucesso")
        print("Conteúdo renderizado:")
        print(rendered)
        
        # Verificar se os elementos estão presentes
        if 'type="submit"' in rendered:
            print("✅ Botão submit encontrado")
        else:
            print("❌ Botão submit não encontrado")
            
        if 'method="post"' in rendered:
            print("✅ Método POST encontrado")
        else:
            print("❌ Método POST não encontrado")
            
        return True
        
    except Exception as e:
        print(f"❌ Erro ao renderizar template: {str(e)}")
        return False

def verificar_ids_formulario():
    """Verifica se os IDs dos campos estão sendo gerados corretamente"""
    print("\n🔍 Verificando IDs dos campos do formulário...")
    
    try:
        form = ClienteForm()
        
        print("IDs dos campos:")
        for field_name, field in form.fields.items():
            field_id = form[field_name].id_for_label
            print(f"  - {field_name}: {field_id}")
            
        # Verificar se não há conflitos de ID
        ids = [form[field_name].id_for_label for field_name in form.fields.keys()]
        if len(ids) == len(set(ids)):
            print("✅ Todos os IDs são únicos")
        else:
            print("❌ Encontrados IDs duplicados")
            
        return True
        
    except Exception as e:
        print(f"❌ Erro ao verificar IDs: {str(e)}")
        return False

def test_form_validation_details():
    """Testa validação detalhada do formulário"""
    print("\n🔍 Testando validação detalhada do formulário...")
    
    # Dados válidos
    dados_validos = {
        'nome_empresa': 'Teste Validação Ltda',
        'representante': 'João da Silva',
        'cnpj': '12.345.678/0001-90',
        'logradouro': 'Rua das Flores',
        'numero': '123',
        'bairro': 'Centro',
        'cidade': 'São Paulo',
        'estado': 'SP',
        'cep': '01234-567',
        'telefone': '(11) 99999-9999',
        'email': 'validacao@teste.com'
    }
    
    # Testar cada campo individualmente
    for field_name in dados_validos.keys():
        dados_teste = dados_validos.copy()
        dados_teste[field_name] = ''  # Deixar campo vazio
        
        form = ClienteForm(data=dados_teste)
        
        if field_name in ['nome_empresa', 'representante', 'cnpj', 'logradouro', 
                         'numero', 'bairro', 'cidade', 'estado', 'cep', 'telefone', 'email']:
            # Campos obrigatórios
            if not form.is_valid() and field_name in form.errors:
                print(f"✅ Campo {field_name} validado como obrigatório")
            else:
                print(f"❌ Campo {field_name} não está sendo validado como obrigatório")
        else:
            # Campos opcionais
            if field_name not in form.errors:
                print(f"✅ Campo {field_name} aceito como opcional")
            else:
                print(f"⚠️  Campo {field_name} gerando erro quando deveria ser opcional")

def main():
    print("🚀 Diagnóstico avançado do sistema de cadastro de clientes\n")
    
    # Testar renderização do template
    template_ok = test_template_rendering()
    
    # Verificar IDs
    ids_ok = verificar_ids_formulario()
    
    # Testar validação
    test_form_validation_details()
    
    print("\n💡 POSSÍVEIS CAUSAS DO PROBLEMA:")
    print("1. JavaScript interferindo na submissão do formulário")
    print("2. CSS ou framework (Bootstrap) bloqueando o evento click")
    print("3. Middleware ou decorator redirecionando antes da submissão")
    print("4. Problema com CSRF token")
    print("5. Cache do navegador carregando versão antiga da página")
    
    print("\n🔧 SUGESTÕES DE VERIFICAÇÃO:")
    print("1. Abrir DevTools do navegador e verificar console de erros")
    print("2. Verificar aba Network para ver se a requisição POST está sendo enviada")
    print("3. Desabilitar JavaScript temporariamente para testar")
    print("4. Limpar cache do navegador")
    print("5. Testar em modo privado/incógnito")

if __name__ == '__main__':
    main()
