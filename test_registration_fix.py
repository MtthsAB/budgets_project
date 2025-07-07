#!/usr/bin/env python3

import os
import django
import sys

# Configure Django
sys.path.append('/home/matas/projetos/Project')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema_produtos.settings')
django.setup()

from django.test import Client
from django.contrib.auth import get_user_model
from produtos.models import TipoItem

def test_registration_page():
    """Test if the product registration page loads correctly and has the expected fields."""
    
    # Create test client
    client = Client()
    
    # Check if we have product types
    tipos = TipoItem.objects.all()
    print(f"Product types found: {tipos.count()}")
    for tipo in tipos:
        print(f"  - {tipo.id}: {tipo.nome}")
    
    # Test GET request to registration page
    try:
        response = client.get('/produtos/cadastro/')
        print(f"\nRegistration page status: {response.status_code}")
        
        if response.status_code == 200:
            content = response.content.decode('utf-8')
            
            # Check for key elements
            checks = [
                ('tipo_produto select', 'id="tipo_produto"' in content),
                ('cadeira fields', 'id="campos-cadeira"' in content),
                ('banqueta fields', 'id="campos-banqueta"' in content),
                ('acessorio fields', 'id="campos-acessorio"' in content),
                ('toggleCamposPorTipo function', 'toggleCamposPorTipo()' in content),
                ('toggleCamposEspecificos function', 'toggleCamposEspecificos(' in content),
            ]
            
            print("\nTemplate checks:")
            for check_name, result in checks:
                status = "✓" if result else "✗"
                print(f"  {status} {check_name}: {result}")
                
            # Check if specific chair fields are present
            chair_fields = [
                'largura_cadeira',
                'profundidade_cadeira', 
                'altura_cadeira',
                'tecido_metros_cadeira',
                'volume_m3_cadeira',
                'peso_kg_cadeira',
                'preco_cadeira',
                'ativo_cadeira',
                'descricao_cadeira'
            ]
            
            print("\nChair field checks:")
            for field in chair_fields:
                present = f'name="{field}"' in content
                status = "✓" if present else "✗"
                print(f"  {status} {field}: {present}")
                
        else:
            print(f"Failed to load page: {response.status_code}")
            if hasattr(response, 'content'):
                print(response.content.decode('utf-8')[:500])
                
    except Exception as e:
        print(f"Error testing registration page: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    test_registration_page()
