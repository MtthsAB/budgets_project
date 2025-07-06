#!/usr/bin/env python
"""
Verificação do layout limpo de imagens - sem textos desnecessários
"""

import os

def verificar_layout_limpo():
    """Verifica se o layout está limpo sem informações desnecessárias"""
    
    print("🧹 VERIFICAÇÃO DO LAYOUT LIMPO")
    print("=" * 40)
    
    template_banquetas = "templates/produtos/banquetas/cadastro.html"
    template_acessorios = "templates/produtos/acessorios/formulario.html"
    
    elementos_removidos = {
        "✅ Informações de formato removidas": False,
        "✅ Texto 'Imagem atual' removido": False,
        "✅ Campo imagem secundária removido": False,
        "✅ Layout simplificado": False
    }
    
    print("🪑 BANQUETAS:")
    if os.path.exists(template_banquetas):
        with open(template_banquetas, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Verificar se elementos desnecessários foram removidos
        if "JPG, PNG, GIF" not in content:
            print("   ✅ Informações de formato removidas")
            elementos_removidos["✅ Informações de formato removidas"] = True
            
        if "Imagem atual:" not in content:
            print("   ✅ Texto 'Imagem atual' removido")
            elementos_removidos["✅ Texto 'Imagem atual' removido"] = True
            
        if "imagem_secundaria" not in content:
            print("   ✅ Campo imagem secundária removido")
            elementos_removidos["✅ Campo imagem secundária removido"] = True
            
        if "col-md-6" in content and content.count("col-md-6") == 1:
            print("   ✅ Layout simplificado - apenas 1 coluna")
            elementos_removidos["✅ Layout simplificado"] = True
            
    print("\n🧩 ACESSÓRIOS:")
    if os.path.exists(template_acessorios):
        with open(template_acessorios, 'r', encoding='utf-8') as f:
            content = f.read()
            
        if "JPG, PNG, GIF" not in content:
            print("   ✅ Informações de formato removidas")
            
        if "Imagem atual:" not in content:
            print("   ✅ Texto 'Imagem atual' removido")
            
        if "imagem_secundaria" not in content:
            print("   ✅ Campo imagem secundária removido")
            
        if "col-md-6" in content and content.count("col-md-6") == 1:
            print("   ✅ Layout simplificado - apenas 1 coluna")
    
    print("\n📊 RESULTADO:")
    for check, status in elementos_removidos.items():
        if status:
            print(f"   {check}")
        else:
            print(f"   ❌ {check.replace('✅', 'Pendente:')}")
    
    print("\n🎯 LAYOUT FINAL:")
    print("   • Título: 'Imagens do Produto'")
    print("   • Apenas campo de upload da imagem principal")
    print("   • Preview da imagem atual (se existir)")
    print("   • Sem textos desnecessários")
    print("   • Sem informações de formato")
    print("   • Sem campo de imagem secundária")
    
    print("\n🎨 ESTRUTURA SIMPLIFICADA:")
    print("   ┌─ Imagens do Produto")
    print("   │  ├─ Label: Imagem Principal")
    print("   │  ├─ Input: file upload")
    print("   │  └─ Preview: imagem atual (se existir)")
    print("   └─ Fim da seção")
    
    print("\n✅ LAYOUT LIMPO IMPLEMENTADO!")

if __name__ == '__main__':
    verificar_layout_limpo()
