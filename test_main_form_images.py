#!/usr/bin/env python
"""
Script para verificar se a seção de imagens aparece corretamente na tela principal
"""

def test_main_form_image_section():
    """Testa se a seção de imagens está configurada corretamente no formulário principal"""
    
    template_path = '/home/matas/projetos/Project/templates/produtos/sofas/cadastro.html'
    
    with open(template_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    print("Verificando configuração da seção de imagens no formulário principal...")
    print("=" * 70)
    
    # Verificações
    checks = [
        ('✅ Seção de imagens com ID', 'id="secao-imagens"'),
        ('✅ Seção inicialmente oculta', 'secao-imagens" style="display: none;"'),
        ('✅ Include da seção reutilizável', 'includes/secao_imagens.html'),
        ('✅ Função toggleCamposPorTipo', 'function toggleCamposPorTipo()'),
        ('✅ Controle da seção no JavaScript', 'secaoImagens = document.getElementById(\'secao-imagens\')'),
        ('✅ Mostrar seção para todos os tipos', 'secaoImagens.style.display = \'block\''),
        ('✅ Dropdown de tipo de produto', 'onchange="toggleCamposPorTipo()"'),
        ('✅ Formulário com upload', 'enctype="multipart/form-data"'),
    ]
    
    all_good = True
    
    for check_name, pattern in checks:
        if pattern in content:
            print(f"{check_name}: ENCONTRADO")
        else:
            print(f"❌ {check_name}: NÃO ENCONTRADO")
            all_good = False
    
    print("\n" + "=" * 70)
    
    if all_good:
        print("🎉 SUCESSO: Seção de imagens está configurada corretamente!")
        print("\n📋 Como usar:")
        print("1. Acesse: http://localhost:8000/produtos/sofas/cadastro/")
        print("2. Selecione um tipo de produto no dropdown")
        print("3. A seção 'Imagens do Produto' deve aparecer")
        print("4. Preencha os campos e faça upload das imagens")
    else:
        print("❌ PROBLEMA: Algumas configurações estão faltando")
    
    # Verificar se há elementos duplicados
    print(f"\n🔍 Verificação de duplicação:")
    print(f"- Cards de imagem: {content.count('card border-primary')}")
    print(f"- Includes de seção: {content.count('includes/secao_imagens.html')}")
    print(f"- IDs secao-imagens: {content.count('id=\"secao-imagens\"')}")
    
    # Verificar tipos de produto suportados
    print(f"\n📝 Tipos de produto suportados:")
    tipos = ['Sofás', 'Cadeiras', 'Banquetas', 'Acessórios']
    for tipo in tipos:
        if f"tipoNome === '{tipo}'" in content:
            print(f"  ✅ {tipo}")
        else:
            print(f"  ❌ {tipo} - não encontrado na lógica")

if __name__ == '__main__':
    test_main_form_image_section()
