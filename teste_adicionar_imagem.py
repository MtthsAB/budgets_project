#!/usr/bin/env python
"""
Script simples para testar adição de imagem às banquetas
"""
import os
import sys
import django

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema_produtos.settings')
django.setup()

from produtos.models import Banqueta
from django.core.files.base import ContentFile

def teste_simples_imagem():
    """Testa adição de imagem simples"""
    
    print("=== TESTE SIMPLES DE IMAGEM ===")
    
    # Pegar primeira banqueta
    try:
        banqueta = Banqueta.objects.first()
        if not banqueta:
            print("❌ Nenhuma banqueta encontrada")
            return
            
        print(f"📝 Testando com: {banqueta.ref_banqueta} - {banqueta.nome}")
        
        # Verificar estado atual
        print(f"Estado atual:")
        print(f"  Principal: {banqueta.imagem_principal}")
        print(f"  Secundária: {banqueta.imagem_secundaria}")
        
        # Criar conteúdo de imagem simples (pixel transparente PNG)
        # Este é um PNG válido de 1x1 pixel transparente
        png_data = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x06\x00\x00\x00\x1f\x15\xc4\x89\x00\x00\x00\rIDATx\x9cc\xf8\x0f\x00\x00\x01\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00IEND\xaeB`\x82'
        
        # Tentar adicionar imagem
        try:
            img_content = ContentFile(png_data)
            banqueta.imagem_principal.save(
                f'{banqueta.ref_banqueta.lower()}_teste.png',
                img_content,
                save=True
            )
            print(f"✅ Imagem adicionada com sucesso!")
            print(f"   Arquivo: {banqueta.imagem_principal.name}")
            print(f"   URL: {banqueta.imagem_principal.url}")
            
        except Exception as e:
            print(f"❌ Erro ao adicionar imagem: {e}")
            
        # Verificar novamente
        banqueta.refresh_from_db()
        print(f"\nApós tentativa:")
        print(f"  Principal: {banqueta.imagem_principal}")
        print(f"  Secundária: {banqueta.imagem_secundaria}")
        
    except Exception as e:
        print(f"❌ Erro geral: {e}")

if __name__ == '__main__':
    teste_simples_imagem()
