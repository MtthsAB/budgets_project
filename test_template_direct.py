#!/usr/bin/env python3
"""
Teste direto do template através do Django
"""

import os
import django
import sys

# Configurar Django
sys.path.append('/home/matas/projetos/Project')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema_produtos.settings')
django.setup()

from django.template.loader import render_to_string
from produtos.models import TipoItem

def test_template_directly():
    """Testa o template diretamente"""
    try:
        # Contexto similar ao da view
        context = {
            'tipos': TipoItem.objects.all(),
            'produtos_disponiveis': [],
        }
        
        # Renderizar template
        rendered = render_to_string('produtos/sofas/cadastro.html', context)
        
        print(f"Template renderizado com {len(rendered)} caracteres")
        
        # Verificar elementos essenciais
        checks = {
            'Seção de imagens presente': 'id="secao-imagens"' in rendered,
            'Include funcionando': 'Imagens do Produto' in rendered,
            'Função toggleCamposPorTipo': 'function toggleCamposPorTipo()' in rendered,
            'Select de tipo': 'id="tipo_produto"' in rendered,
            'Campo imagem principal': 'name="imagem_principal"' in rendered,
            'JavaScript para exibir seção': 'secaoImagens.style.display = \'block\'' in rendered,
        }
        
        print("\n=== VERIFICAÇÃO DIRETA DO TEMPLATE ===")
        all_ok = True
        for check_name, result in checks.items():
            status = "✅" if result else "❌"
            print(f"{status} {check_name}: {'OK' if result else 'FALTANDO'}")
            if not result:
                all_ok = False
        
        # Salvar para análise
        with open('/home/matas/projetos/Project/template_rendered.html', 'w', encoding='utf-8') as f:
            f.write(rendered)
        print("\n📄 Template renderizado salvo em template_rendered.html")
        
        return all_ok
        
    except Exception as e:
        print(f"❌ Erro ao renderizar template: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    print("🔍 Testando template diretamente...")
    result = test_template_directly()
    
    if result:
        print("\n✅ TEMPLATE FUNCIONANDO: Todos os elementos estão presentes!")
    else:
        print("\n❌ TEMPLATE COM PROBLEMAS: Alguns elementos estão faltando!")
