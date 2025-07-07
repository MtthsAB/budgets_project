#!/usr/bin/env python3

import os
import sys
import django
from django.conf import settings
from django.template.loader import get_template
from django.template import Context

# Add the project directory to the Python path
sys.path.insert(0, '/home/matas/projetos/Project')

# Configure Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema_produtos.settings')
django.setup()

def test_template_syntax():
    """Test if the template can be parsed without syntax errors."""
    try:
        template = get_template('produtos/sofas/cadastro.html')
        print("✓ Template syntax is valid!")
        
        # Count blocks to ensure they're balanced
        with open('/home/matas/projetos/Project/templates/produtos/sofas/cadastro.html', 'r') as f:
            content = f.read()
            
        block_opens = content.count('{% block')
        block_closes = content.count('{% endblock %}')
        
        print(f"✓ Block opens: {block_opens}")
        print(f"✓ Block closes: {block_closes}")
        
        if block_opens == block_closes:
            print("✓ All blocks are properly closed!")
        else:
            print("✗ Block mismatch!")
            return False
            
        # Test that specific sections exist
        if 'secao-imagens' in content:
            print("✓ Image section is present")
        else:
            print("✗ Image section missing")
            
        if 'secao-modulos' in content:
            print("✓ Modules section is present")
        else:
            print("✗ Modules section missing")
            
        return True
        
    except Exception as e:
        print(f"✗ Template syntax error: {e}")
        return False

if __name__ == '__main__':
    print("Testing fixed template...")
    if test_template_syntax():
        print("\n🎉 Template is fixed and ready to use!")
    else:
        print("\n❌ Template still has issues.")
