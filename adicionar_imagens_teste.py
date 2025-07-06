#!/usr/bin/env python
"""
Script para adicionar imagens de teste às banquetas
"""
import os
import sys
import django
from pathlib import Path
from PIL import Image
import io

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema_produtos.settings')
django.setup()

from produtos.models import Banqueta
from django.core.files.base import ContentFile

def criar_imagem_teste(texto, cor=(100, 100, 100)):
    """Cria uma imagem de teste com texto"""
    from PIL import Image, ImageDraw, ImageFont
    
    # Criar imagem
    img = Image.new('RGB', (400, 300), color=cor)
    draw = ImageDraw.Draw(img)
    
    # Adicionar texto
    try:
        # Tentar fonte padrão
        font = ImageFont.load_default()
    except:
        font = None
    
    # Centralizar texto
    bbox = draw.textbbox((0, 0), texto, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    
    x = (400 - text_width) // 2
    y = (300 - text_height) // 2
    
    draw.text((x, y), texto, fill=(255, 255, 255), font=font)
    
    # Salvar em BytesIO
    img_buffer = io.BytesIO()
    img.save(img_buffer, format='PNG')
    img_buffer.seek(0)
    
    return img_buffer

def adicionar_imagens_teste():
    """Adiciona imagens de teste às banquetas"""
    
    print("=== ADICIONANDO IMAGENS DE TESTE ===\n")
    
    # Pegar algumas banquetas para teste
    banquetas_teste = [
        ('BQ249', 'GIO'),
        ('BQ13', 'CERES'),
        ('BQ250', 'IAN')
    ]
    
    for ref, nome in banquetas_teste:
        try:
            banqueta = Banqueta.objects.get(ref_banqueta=ref)
            print(f"📝 Processando {ref} - {nome}")
            
            # Criar imagem de teste
            img_buffer = criar_imagem_teste(f"{ref}\n{nome}", cor=(70, 130, 180))
            
            # Salvar como imagem principal
            img_content = ContentFile(img_buffer.getvalue())
            banqueta.imagem_principal.save(
                f'{ref.lower()}_teste.png',
                img_content,
                save=True
            )
            
            print(f"✅ Imagem adicionada para {ref}")
            print(f"   Arquivo: {banqueta.imagem_principal.name}")
            print(f"   URL: {banqueta.imagem_principal.url}")
            
        except Banqueta.DoesNotExist:
            print(f"❌ Banqueta {ref} não encontrada")
        except Exception as e:
            print(f"❌ Erro ao processar {ref}: {e}")
    
    print(f"\n=== VERIFICANDO RESULTADOS ===")
    
    for ref, nome in banquetas_teste:
        try:
            banqueta = Banqueta.objects.get(ref_banqueta=ref)
            if banqueta.imagem_principal:
                print(f"✅ {ref}: {banqueta.imagem_principal.url}")
            else:
                print(f"❌ {ref}: Sem imagem")
        except:
            print(f"❌ {ref}: Erro")

if __name__ == '__main__':
    try:
        adicionar_imagens_teste()
    except Exception as e:
        print(f"Erro: {e}")
        # Método alternativo sem PIL
        print("\n=== MÉTODO ALTERNATIVO SEM IMAGENS ===")
        print("Para adicionar imagens:")
        print("1. Acesse /admin/produtos/banqueta/")
        print("2. Edite uma banqueta")
        print("3. Faça upload de uma imagem")
        print("4. Verifique se aparece na visualização")
