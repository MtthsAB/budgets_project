#!/usr/bin/env python3
"""
Script para testar problemas de hidratação na edição de sofás
"""

import os
import sys
import django

# Configurar o ambiente Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema_produtos.settings')
django.setup()

from produtos.models import Produto, Modulo, TamanhosModulosDetalhado

def testar_dados_sofa():
    """Testar se há sofás com dados problemáticos que podem causar erros de hidratação"""
    
    print("🔍 TESTE: Verificando dados de sofás que podem causar erros de hidratação")
    print("=" * 80)
    
    # Buscar sofás
    sofas = Produto.objects.filter(id_tipo_produto__nome__icontains='sofá')
    
    if not sofas.exists():
        print("❌ Nenhum sofá encontrado no banco de dados")
        return
    
    print(f"✅ Encontrados {sofas.count()} sofás")
    
    for sofa in sofas[:3]:  # Testar apenas os primeiros 3
        print(f"\n📋 Sofá: {sofa.ref_produto} - {sofa.nome_produto}")
        print(f"   ID: {sofa.id}")
        
        # Verificar campos numéricos do próprio sofá
        print(f"   Produto: {sofa.nome_produto}")
        
        # Verificar módulos
        modulos = sofa.modulos.all()
        print(f"   Módulos: {modulos.count()}")
        
        for modulo in modulos:
            print(f"     • Módulo: {modulo.nome}")
            print(f"       Profundidade: {modulo.profundidade}")
            print(f"       Altura: {modulo.altura}")
            print(f"       Braço: {modulo.braco}")
            
            # Verificar tamanhos
            tamanhos = modulo.tamanhos_detalhados.all()
            print(f"       Tamanhos: {tamanhos.count()}")
            
            for tamanho in tamanhos:
                print(f"         - Largura Total: {tamanho.largura_total}")
                print(f"         - Largura Assento: {tamanho.largura_assento}")
                print(f"         - Tecido (m): {tamanho.tecido_metros}")
                print(f"         - Volume (m³): {tamanho.volume_m3}")
                print(f"         - Peso (kg): {tamanho.peso_kg}")
                print(f"         - Preço: {tamanho.preco}")

def testar_formatacao_valores():
    """Testar como os valores são formatados pelo Django"""
    from django.template import Context, Template
    from django.template.loader import render_to_string
    
    print("\n🧪 TESTE: Verificando formatação de valores numéricos")
    print("=" * 80)
    
    # Buscar um sofá com dados numéricos
    sofa = Produto.objects.filter(id_tipo_produto__nome__icontains='sofá').first()
    
    if not sofa:
        print("❌ Nenhum sofá encontrado")
        return
    
    modulos = sofa.modulos.all()
    
    if not modulos.exists():
        print("❌ Nenhum módulo encontrado")
        return
    
    modulo = modulos.first()
    tamanhos = modulo.tamanhos_detalhados.all()
    
    if not tamanhos.exists():
        print("❌ Nenhum tamanho encontrado")
        return
    
    tamanho = tamanhos.first()
    
    # Testar formatação sem filtros
    template_sem_filtro = Template('{{ valor }}')
    
    # Testar formatação com unlocalize
    template_com_unlocalize = Template('{% load l10n %}{{ valor|unlocalize }}')
    
    valores_teste = [
        ('Profundidade Módulo', modulo.profundidade if modulo else None),
        ('Altura Módulo', modulo.altura if modulo else None),
        ('Largura Total Tamanho', tamanho.largura_total if tamanho else None),
        ('Preço Tamanho', tamanho.preco if tamanho else None),
    ]
    
    for nome, valor in valores_teste:
        if valor is not None:
            context = Context({'valor': valor})
            
            sem_filtro = template_sem_filtro.render(context)
            com_unlocalize = template_com_unlocalize.render(context)
            
            print(f"{nome}:")
            print(f"  Valor original: {valor}")
            print(f"  Sem filtro: '{sem_filtro}'")
            print(f"  Com unlocalize: '{com_unlocalize}'")
            
            # Verificar se há vírgulas problemáticas
            if ',' in sem_filtro and sem_filtro != com_unlocalize:
                print(f"  ⚠️  PROBLEMA: Formatação com vírgula detectada!")
            else:
                print(f"  ✅ OK: Sem problemas de formatação")
            print()

if __name__ == "__main__":
    try:
        testar_dados_sofa()
        testar_formatacao_valores()
        print("\n✅ Teste concluído!")
        
    except Exception as e:
        print(f"\n❌ Erro durante o teste: {str(e)}")
        import traceback
        traceback.print_exc()
