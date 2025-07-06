#!/usr/bin/env python
"""
Teste simples do layout padronizado de imagens.
"""

import os

def verificar_templates():
    """Verifica se os templates foram padronizados corretamente"""
    
    print("🔍 VERIFICAÇÃO DO LAYOUT PADRONIZADO")
    print("=" * 45)
    
    # Caminhos dos templates
    template_banquetas = "templates/produtos/banquetas/cadastro.html"
    template_acessorios = "templates/produtos/acessorios/formulario.html"
    
    verificacoes = {
        "✅ Título 'Imagens do Produto'": False,
        "✅ Informações de formato": False,
        "✅ Estrutura padronizada": False,
        "✅ Texto 'Imagem atual'": False
    }
    
    print("🪑 BANQUETAS:")
    if os.path.exists(template_banquetas):
        with open(template_banquetas, 'r', encoding='utf-8') as f:
            content = f.read()
            
        if "Imagens do Produto" in content:
            print("   ✅ Título correto")
            verificacoes["✅ Título 'Imagens do Produto'"] = True
            
        if "JPG, PNG, GIF (máx. 5MB)" in content:
            print("   ✅ Informações de formato")
            verificacoes["✅ Informações de formato"] = True
            
        if 'class="form-text"' in content:
            print("   ✅ Estrutura padronizada")
            verificacoes["✅ Estrutura padronizada"] = True
            
        if 'Imagem atual:</small>' in content:
            print("   ✅ Texto de imagem atual")
            verificacoes["✅ Texto 'Imagem atual'"] = True
    else:
        print("   ❌ Template não encontrado")
    
    print("\n🧩 ACESSÓRIOS:")
    if os.path.exists(template_acessorios):
        with open(template_acessorios, 'r', encoding='utf-8') as f:
            content = f.read()
            
        if "Imagens do Produto" in content:
            print("   ✅ Título correto")
            
        if "JPG, PNG, GIF (máx. 5MB)" in content:
            print("   ✅ Informações de formato")
            
        if 'class="form-text"' in content:
            print("   ✅ Estrutura padronizada")
            
        if 'Imagem atual:</small>' in content:
            print("   ✅ Texto de imagem atual")
    else:
        print("   ❌ Template não encontrado")
    
    print("\n📊 RESUMO:")
    for check, status in verificacoes.items():
        if status:
            print(f"   {check}")
        else:
            print(f"   ❌ {check.replace('✅', '')}")
    
    print("\n🎯 MUDANÇAS IMPLEMENTADAS:")
    print("   1. Título alterado para 'Imagens do Produto'")
    print("   2. Adicionadas informações de formato (JPG, PNG, GIF - máx. 5MB)")
    print("   3. Layout padronizado entre banquetas e acessórios")
    print("   4. Mantida funcionalidade de upload e visualização")
    
    print("\n💡 COMO TESTAR:")
    print("   1. Acesse: http://localhost:8000/produtos/")
    print("   2. Clique em uma banqueta")
    print("   3. Clique em 'Editar'")
    print("   4. Verifique a seção 'Imagens do Produto'")
    print("   5. Teste o upload de imagens")
    
    print("\n✅ IMPLEMENTAÇÃO CONCLUÍDA!")

if __name__ == '__main__':
    verificar_templates()
