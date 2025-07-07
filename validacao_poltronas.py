#!/usr/bin/env python3
"""
Script de validação das poltronas cadastradas.
Sistema de Produtos - Julho 2025
"""

import os
import sys
import django
from decimal import Decimal

# Configurar Django
sys.path.append('/home/matas/projetos/Project')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema_produtos.settings')
django.setup()

from produtos.models import Poltrona

def validar_poltronas():
    """Valida se todas as poltronas foram cadastradas corretamente"""
    print("=" * 60)
    print("🪑 VALIDAÇÃO DE POLTRONAS CADASTRADAS")
    print("📅 Sistema de Produtos - Julho 2025")
    print("=" * 60)
    
    # Dados esperados
    poltronas_esperadas = [
        ('PL243', 'ARIA'),
        ('PL246', 'ARISTOCRATA'), 
        ('PL105', 'CERNE'),
        ('PL869', 'CHANEL'),
        ('PL97', 'CLARA'),
        ('PL32', 'COMPATIO'),
        ('PL214', 'CORDONE'),
        ('PL53', 'DEMETER'),
        ('PL134', 'DIPLOMATA'),
        ('PL988', 'FLOW'),
        ('PL273', 'BOLL'),
        ('PL287', 'GUCCI'),
        ('PL232/2B', 'HALL 2B'),
        ('PL232/1B', 'HALL 1B'),
        ('PL232/SB', 'HALL SB'),
        ('PL232', 'HALL'),
        ('ME232', 'HALL MESA'),
        ('PL25', 'ISIS'),
        ('PL915', 'JARRAR'),
        ('LE COULTHE', 'LE COULTHE'),
        ('LUXOR', 'LUXOR'),
        ('MALIBU', 'MALIBU'),
        ('PL244', 'MIS'),
        ('PL239', 'ORBI'),
        ('PL22', 'PIRRA'),
        ('RIALTO', 'RIALTO'),
        ('TIFFANY', 'TIFFANY'),
        ('VERSACE', 'VERSACE'),
        ('PL225', 'XANGAI'),
        ('PL238', 'ZARA'),
        ('PL262', 'RETRO'),
        ('PL274', 'KOLEOS'),
    ]
    
    print(f"🔍 Verificando {len(poltronas_esperadas)} poltronas esperadas...")
    print("-" * 60)
    
    # Verificar poltronas cadastradas
    poltronas_cadastradas = Poltrona.objects.all().count()
    print(f"📊 Total de poltronas no banco: {poltronas_cadastradas}")
    
    erros = []
    poltronas_encontradas = 0
    
    for ref, nome in poltronas_esperadas:
        try:
            poltrona = Poltrona.objects.get(ref_poltrona=ref)
            
            # Verificações
            checks = []
            if poltrona.nome == nome:
                checks.append("✅ Nome")
            else:
                checks.append(f"❌ Nome (esperado: {nome}, encontrado: {poltrona.nome})")
                erros.append(f"Nome incorreto para {ref}")
            
            if poltrona.ativo:
                checks.append("✅ Ativo")
            else:
                checks.append("❌ Inativo")
                erros.append(f"Poltrona {ref} está inativa")
            
            if poltrona.preco and poltrona.preco > 0:
                checks.append("✅ Preço")
            else:
                checks.append("❌ Preço")
                erros.append(f"Preço inválido para {ref}")
            
            if poltrona.imagem_principal:
                checks.append("✅ Imagem")
            else:
                checks.append("❌ Sem imagem")
            
            status = " | ".join(checks)
            print(f"🪑 {ref} - {poltrona.nome}: {status}")
            poltronas_encontradas += 1
            
        except Poltrona.DoesNotExist:
            print(f"❌ {ref} - {nome}: NÃO ENCONTRADA")
            erros.append(f"Poltrona {ref} não encontrada no banco")
    
    print("-" * 60)
    print("📈 RESUMO DA VALIDAÇÃO:")
    print(f"✅ Poltronas encontradas: {poltronas_encontradas}/{len(poltronas_esperadas)}")
    print(f"❌ Erros encontrados: {len(erros)}")
    
    if erros:
        print("\n🚨 ERROS DETECTADOS:")
        for i, erro in enumerate(erros, 1):
            print(f"{i}. {erro}")
    else:
        print("\n🎉 VALIDAÇÃO CONCLUÍDA COM SUCESSO!")
        print("✅ Todas as poltronas foram cadastradas corretamente.")
    
    print("-" * 60)
    
    # Verificar algumas poltronas específicas
    print("\n🔍 VERIFICAÇÃO DETALHADA:")
    
    try:
        # Verificar PL32 especificamente
        pl32 = Poltrona.objects.get(ref_poltrona='PL32')
        print(f"🪑 PL32 - COMPATIO:")
        print(f"   📏 Dimensões: {pl32.largura}×{pl32.profundidade}×{pl32.altura} cm")
        print(f"   🧵 Tecido: {pl32.tecido_metros}m")
        print(f"   📦 Volume: {pl32.volume_m3}m³")
        print(f"   ⚖️  Peso: {pl32.peso_kg}kg")
        print(f"   💰 Preço: R$ {pl32.preco}")
        if pl32.imagem_principal:
            print(f"   🖼️  Imagem: {pl32.imagem_principal.name}")
        else:
            print(f"   🖼️  Imagem: ❌ Não associada")
    except Poltrona.DoesNotExist:
        print("❌ PL32 não encontrada!")
    
    print("=" * 60)

if __name__ == '__main__':
    validar_poltronas()
