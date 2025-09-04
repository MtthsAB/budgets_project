#!/usr/bin/env python3
"""
Script para testar se a configuração USE_L10N foi aplicada
"""

import os
import sys
import django

# Configurar o ambiente Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema_produtos.settings')
django.setup()

from django.conf import settings
from django.template import Context, Template

def testar_configuracao():
    print("🔍 TESTE: Verificando configuração de localização")
    print("=" * 60)
    
    print(f"USE_I18N: {settings.USE_I18N}")
    print(f"USE_L10N: {getattr(settings, 'USE_L10N', 'NÃO DEFINIDO')}")
    print(f"LANGUAGE_CODE: {settings.LANGUAGE_CODE}")
    
    # Testar formatação de números
    from decimal import Decimal
    
    teste_valores = [
        Decimal('85.00'),
        Decimal('25.50'),
        Decimal('140.25'),
        Decimal('3.50'),
        Decimal('0.850'),
        Decimal('1296.00'),
    ]
    
    print("\n📋 Teste de formatação de valores:")
    
    # Template sem filtro
    template_normal = Template('{{ valor }}')
    
    # Template com unlocalize
    template_unlocalize = Template('{% load l10n %}{{ valor|unlocalize }}')
    
    for valor in teste_valores:
        context = Context({'valor': valor})
        
        normal = template_normal.render(context)
        unlocalized = template_unlocalize.render(context)
        
        print(f"  {valor} → Normal: '{normal}' | Unlocalize: '{unlocalized}'")
        
        if ',' in normal:
            print(f"    ⚠️  PROBLEMA: Vírgula detectada na formatação normal!")
        else:
            print(f"    ✅ OK: Sem vírgulas na formatação")

if __name__ == "__main__":
    try:
        testar_configuracao()
        
    except Exception as e:
        print(f"\n❌ Erro durante o teste: {str(e)}")
        import traceback
        traceback.print_exc()
