#!/usr/bin/env python3
"""
Script para corrigir o template removendo o modal duplicado
"""

def fix_template():
    template_path = '/home/matas/projetos/Project/templates/orcamentos/form.html'
    
    with open(template_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Contar quantos modais existem
    modal_count = content.count('id="modalAdicionarItem"')
    print(f"Encontrados {modal_count} modais com ID 'modalAdicionarItem'")
    
    if modal_count > 1:
        print("Removendo modal duplicado...")
        
        # Encontrar as posições dos modais
        first_modal_start = content.find('<!-- Modal para Adicionar Item -->')
        first_modal_end = content.find('</div>\n</div>\n</div>', first_modal_start) + len('</div>\n</div>\n</div>')
        
        # Encontrar o segundo modal
        second_modal_start = content.find('<!-- Modal para Adicionar Item -->', first_modal_end)
        
        if second_modal_start != -1:
            # Encontrar o fim do segundo modal
            second_modal_end = len(content)  # Vai até o final do arquivo
            
            # Remover o segundo modal
            content = content[:second_modal_start] + content[second_modal_end:]
            
            # Salvar o arquivo corrigido
            with open(template_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print("✅ Modal duplicado removido com sucesso!")
            
            # Verificar se ficou apenas um modal
            with open(template_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            modal_count = content.count('id="modalAdicionarItem"')
            print(f"Agora existem {modal_count} modais com ID 'modalAdicionarItem'")
            
        else:
            print("❌ Não foi possível encontrar o segundo modal")
    else:
        print("✅ Apenas um modal encontrado, nenhuma correção necessária")

if __name__ == '__main__':
    fix_template()
