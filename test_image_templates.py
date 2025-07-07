#!/usr/bin/env python
"""
Script para testar se todos os templates de produto têm a seção de imagens funcionando
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema_produtos.settings')
django.setup()

def test_image_sections():
    """Testa se todas as seções de imagem estão presentes nos templates"""
    
    templates_to_check = [
        'templates/produtos/cadeiras/cadastro.html',
        'templates/produtos/banquetas/cadastro.html', 
        'templates/produtos/sofas/cadastro.html',
        'templates/produtos/includes/secao_imagens.html'
    ]
    
    print("Verificando seções de imagem em todos os templates...")
    print("=" * 60)
    
    for template_path in templates_to_check:
        full_path = f'/home/matas/projetos/Project/{template_path}'
        
        if not os.path.exists(full_path):
            print(f"❌ {template_path} - ARQUIVO NÃO ENCONTRADO")
            continue
            
        with open(full_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        print(f"\n📄 {template_path}")
        print("-" * 40)
        
        # Verificar elementos específicos
        checks = []
        
        if 'includes/secao_imagens.html' in template_path:
            # Para o template incluído
            checks = [
                ('Card de imagem', 'card border-primary'),
                ('Título "Imagens do Produto"', 'Imagens do Produto'),
                ('Botão adicionar segunda imagem', 'btn_adicionar_segunda_imagem'),
                ('Função mostrarSegundaImagem', 'mostrarSegundaImagem'),
                ('Campo imagem principal', 'imagem_principal'),
                ('Campo imagem secundaria', 'imagem_secundaria'),
                ('CSS do botão', 'btn-add-image'),
                ('JavaScript preview', 'previewImage'),
            ]
        else:
            # Para templates principais
            checks = [
                ('Include da seção', 'includes/secao_imagens.html'),
                ('Declaração do formulário', 'enctype="multipart/form-data"'),
                ('CSRF token', '{% csrf_token %}'),
                ('Form method POST', 'method="post"'),
            ]
            
            # Verificar se não há seção duplicada
            if content.count('card border-primary') > 0:
                if 'includes/secao_imagens.html' not in content:
                    checks.append(('❌ Seção duplicada encontrada', 'card border-primary'))
                else:
                    checks.append(('✅ Usando include (correto)', 'includes/secao_imagens.html'))
        
        # Executar verificações
        for check_name, pattern in checks:
            count = content.count(pattern)
            if count > 0:
                if check_name.startswith('❌'):
                    print(f"  ❌ {check_name}: {count} ocorrência(s)")
                else:
                    print(f"  ✅ {check_name}: {count} ocorrência(s)")
            else:
                print(f"  ❌ {check_name}: NÃO ENCONTRADO")
    
    print("\n" + "=" * 60)
    print("Verificação de estrutura de arquivos:")
    print("-" * 40)
    
    # Verificar se o diretório includes existe
    includes_dir = '/home/matas/projetos/Project/templates/produtos/includes/'
    if os.path.exists(includes_dir):
        print(f"✅ Diretório includes existe: {includes_dir}")
        
        include_files = os.listdir(includes_dir)
        for file in include_files:
            print(f"  📄 {file}")
    else:
        print(f"❌ Diretório includes NÃO existe: {includes_dir}")
    
    print("\n" + "=" * 60)
    print("✨ Verificação concluída!")

if __name__ == '__main__':
    test_image_sections()
