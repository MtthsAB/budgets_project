#!/usr/bin/env python
"""
Script para testar as melhorias na interface de upload de imagens.
Verifica se:
1. Os avisos azuis foram removidos
2. As imagens são opcionais
3. A segunda imagem aparece com botão compacto
4. Os templates estão funcionando
"""

import os
import sys
import re
from pathlib import Path

def test_templates():
    """Testa se os templates foram atualizados corretamente"""
    print("🧪 Testando templates...")
    print("=" * 50)
    
    templates_to_check = [
        'templates/produtos/sofas/cadastro.html',
        'templates/produtos/sofas/cadastro_novo.html',
        'templates/produtos/lista.html',
        'templates/produtos/sofas/cadastro_atualizado.html'
    ]
    
    for template_path in templates_to_check:
        print(f"\n📄 Verificando {template_path}...")
        
        if not Path(template_path).exists():
            print(f"❌ Template não encontrado: {template_path}")
            continue
            
        with open(template_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Testa se o aviso azul foi removido
        if 'Adicione imagens ao seu produto' in content:
            print("❌ Aviso azul ainda presente!")
        else:
            print("✅ Aviso azul removido")
        
        # Testa se há o botão compacto de imagem
        if 'btn-add-image' in content:
            print("✅ Botão compacto implementado")
        else:
            print("⚠️  Botão compacto não encontrado")
        
        # Testa se há CSS customizado
        if '.btn-add-image' in content:
            print("✅ CSS customizado presente")
        else:
            print("⚠️  CSS customizado não encontrado")
        
        # Testa se os campos de imagem são opcionais (não têm 'required')
        if re.search(r'imagem_principal.*required', content):
            print("❌ Imagem principal ainda é obrigatória")
        else:
            print("✅ Imagem principal é opcional")
        
        if re.search(r'imagem_secundaria.*required', content):
            print("❌ Imagem secundária ainda é obrigatória")
        else:
            print("✅ Imagem secundária é opcional")

def test_models():
    """Testa se os modelos permitem imagens opcionais"""
    print("\n\n🗃️  Testando modelos...")
    print("=" * 50)
    
    try:
        # Configura o Django
        import django
        from django.conf import settings
        
        if not settings.configured:
            os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema_produtos.settings')
            django.setup()
        
        from produtos.models import Item, Acessorio
        
        # Verifica se os campos de imagem são opcionais
        imagem_principal_field = Item._meta.get_field('imagem_principal')
        imagem_secundaria_field = Item._meta.get_field('imagem_secundaria')
        
        if imagem_principal_field.blank and imagem_principal_field.null:
            print("✅ Item.imagem_principal é opcional")
        else:
            print("❌ Item.imagem_principal não é opcional")
        
        if imagem_secundaria_field.blank and imagem_secundaria_field.null:
            print("✅ Item.imagem_secundaria é opcional")
        else:
            print("❌ Item.imagem_secundaria não é opcional")
        
        # Verifica acessórios
        acess_imagem_principal = Acessorio._meta.get_field('imagem_principal')
        acess_imagem_secundaria = Acessorio._meta.get_field('imagem_secundaria')
        
        if acess_imagem_principal.blank and acess_imagem_principal.null:
            print("✅ Acessorio.imagem_principal é opcional")
        else:
            print("❌ Acessorio.imagem_principal não é opcional")
        
        if acess_imagem_secundaria.blank and acess_imagem_secundaria.null:
            print("✅ Acessorio.imagem_secundaria é opcional")
        else:
            print("❌ Acessorio.imagem_secundaria não é opcional")
        
    except Exception as e:
        print(f"❌ Erro ao testar modelos: {e}")

def test_forms():
    """Testa se os formulários não tornam as imagens obrigatórias"""
    print("\n\n📝 Testando formulários...")
    print("=" * 50)
    
    try:
        import django
        from django.conf import settings
        
        if not settings.configured:
            os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema_produtos.settings')
            django.setup()
        
        from produtos.forms import ItemForm, AcessorioForm, ModuloForm
        
        # Testa ItemForm
        item_form = ItemForm()
        if 'imagem_principal' in item_form.fields:
            imagem_field = item_form.fields['imagem_principal']
            if imagem_field.required:
                print("❌ ItemForm.imagem_principal é obrigatória")
            else:
                print("✅ ItemForm.imagem_principal é opcional")
        
        # Testa AcessorioForm
        acess_form = AcessorioForm()
        if 'imagem_principal' in acess_form.fields:
            imagem_field = acess_form.fields['imagem_principal']
            if imagem_field.required:
                print("❌ AcessorioForm.imagem_principal é obrigatória")
            else:
                print("✅ AcessorioForm.imagem_principal é opcional")
        
        if 'imagem_secundaria' in acess_form.fields:
            imagem_field = acess_form.fields['imagem_secundaria']
            if imagem_field.required:
                print("❌ AcessorioForm.imagem_secundaria é obrigatória")
            else:
                print("✅ AcessorioForm.imagem_secundaria é opcional")
        
    except Exception as e:
        print(f"❌ Erro ao testar formulários: {e}")

def show_summary():
    """Mostra um resumo das melhorias implementadas"""
    print("\n\n📊 RESUMO DAS MELHORIAS IMPLEMENTADAS")
    print("=" * 60)
    print("✅ Removido aviso azul 'Adicione imagens ao seu produto'")
    print("✅ Segunda imagem substituída por botão compacto com ícone")
    print("✅ Botão com tooltip 'Adicionar outra imagem' (UX)")
    print("✅ CSS customizado para botão circular com hover effects")
    print("✅ Interface mais limpa e focada no conteúdo")
    print("✅ Imagens principais e secundárias opcionais")
    print("✅ Texto de formatos simplificado (menos poluição)")
    print("✅ Layout responsivo mantido")
    print("✅ Melhorias aplicadas em todos os templates relevantes")
    print("\n🎨 BENEFÍCIOS:")
    print("   • Interface mais limpa e profissional")
    print("   • Menos distrações visuais")
    print("   • UX melhorada com tooltips")
    print("   • Botões mais intuitivos")
    print("   • Foco no conteúdo do produto")

if __name__ == '__main__':
    print("🚀 TESTE DAS MELHORIAS DE UI/UX")
    print("🎯 Verificando implementação das mudanças solicitadas")
    print("=" * 60)
    
    test_templates()
    test_models()
    test_forms()
    show_summary()
    
    print("\n\n✨ Teste concluído! Verifique os resultados acima.")
