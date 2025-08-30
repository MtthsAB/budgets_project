#!/usr/bin/env python
"""
Script para sincronizar produtos específicos (cadeiras, banquetas, etc.) 
com a tabela principal produtos_produto para permitir uso em orçamentos.
"""
import os
import sys
import django
from decimal import Decimal

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema_produtos.settings')
django.setup()

from produtos.models import (
    Produto, TipoItem, Cadeira, Banqueta, Poltrona, 
    Pufe, Almofada, Acessorio
)
from authentication.models import CustomUser

def sincronizar_produtos():
    """Sincroniza produtos específicos com a tabela principal"""
    
    print("🔄 Iniciando sincronização de produtos...")
    print("=" * 60)
    
    # Buscar usuário master para criação
    try:
        usuario_master = CustomUser.objects.filter(tipo_permissao='master').first()
        if not usuario_master:
            print("❌ Erro: Nenhum usuário master encontrado!")
            return
        print(f"✓ Usuário master: {usuario_master.email}")
    except Exception as e:
        print(f"❌ Erro ao buscar usuário master: {e}")
        return
    
    total_criados = 0
    total_atualizados = 0
    
    # === SINCRONIZAR CADEIRAS ===
    print("\n📍 Sincronizando Cadeiras...")
    try:
        tipo_cadeira = TipoItem.objects.filter(nome__icontains='Cadeira').first()
        if not tipo_cadeira:
            print("❌ Tipo 'Cadeiras' não encontrado!")
        else:
            cadeiras = Cadeira.objects.filter(ativo=True)
            print(f"   Encontradas {cadeiras.count()} cadeiras ativas")
            
            for cadeira in cadeiras:
                produto, created = Produto.objects.get_or_create(
                    ref_produto=cadeira.ref_cadeira,
                    defaults={
                        'nome_produto': cadeira.nome,
                        'id_tipo_produto': tipo_cadeira,
                        'ativo': cadeira.ativo,
                        'created_by': usuario_master,
                        'imagem_principal': cadeira.imagem_principal or '',
                        'imagem_secundaria': cadeira.imagem_secundaria or '',
                    }
                )
                
                if created:
                    total_criados += 1
                    print(f"   ✓ Criado: {cadeira.ref_cadeira} - {cadeira.nome}")
                else:
                    # Atualizar dados se já existe
                    produto.nome_produto = cadeira.nome
                    produto.ativo = cadeira.ativo
                    produto.imagem_principal = cadeira.imagem_principal or ''
                    produto.imagem_secundaria = cadeira.imagem_secundaria or ''
                    produto.save()
                    total_atualizados += 1
                    print(f"   ↻ Atualizado: {cadeira.ref_cadeira} - {cadeira.nome}")
    except Exception as e:
        print(f"❌ Erro ao sincronizar cadeiras: {e}")
    
    # === SINCRONIZAR BANQUETAS ===
    print("\n📍 Sincronizando Banquetas...")
    try:
        tipo_banqueta = TipoItem.objects.filter(nome__icontains='Banqueta').first()
        if not tipo_banqueta:
            print("❌ Tipo 'Banquetas' não encontrado!")
        else:
            banquetas = Banqueta.objects.filter(ativo=True)
            print(f"   Encontradas {banquetas.count()} banquetas ativas")
            
            for banqueta in banquetas:
                produto, created = Produto.objects.get_or_create(
                    ref_produto=banqueta.ref_banqueta,
                    defaults={
                        'nome_produto': banqueta.nome,
                        'id_tipo_produto': tipo_banqueta,
                        'ativo': banqueta.ativo,
                        'created_by': usuario_master,
                        'imagem_principal': banqueta.imagem_principal or '',
                        'imagem_secundaria': banqueta.imagem_secundaria or '',
                    }
                )
                
                if created:
                    total_criados += 1
                    print(f"   ✓ Criado: {banqueta.ref_banqueta} - {banqueta.nome}")
                else:
                    produto.nome_produto = banqueta.nome
                    produto.ativo = banqueta.ativo
                    produto.imagem_principal = banqueta.imagem_principal or ''
                    produto.imagem_secundaria = banqueta.imagem_secundaria or ''
                    produto.save()
                    total_atualizados += 1
                    print(f"   ↻ Atualizado: {banqueta.ref_banqueta} - {banqueta.nome}")
    except Exception as e:
        print(f"❌ Erro ao sincronizar banquetas: {e}")
    
    # === SINCRONIZAR POLTRONAS ===
    print("\n📍 Sincronizando Poltronas...")
    try:
        tipo_poltrona = TipoItem.objects.filter(nome__icontains='Poltrona').first()
        if not tipo_poltrona:
            print("❌ Tipo 'Poltronas' não encontrado!")
        else:
            poltronas = Poltrona.objects.filter(ativo=True)
            print(f"   Encontradas {poltronas.count()} poltronas ativas")
            
            for poltrona in poltronas:
                produto, created = Produto.objects.get_or_create(
                    ref_produto=poltrona.ref_poltrona,
                    defaults={
                        'nome_produto': poltrona.nome,
                        'id_tipo_produto': tipo_poltrona,
                        'ativo': poltrona.ativo,
                        'created_by': usuario_master,
                        'imagem_principal': poltrona.imagem_principal or '',
                        'imagem_secundaria': poltrona.imagem_secundaria or '',
                    }
                )
                
                if created:
                    total_criados += 1
                    print(f"   ✓ Criado: {poltrona.ref_poltrona} - {poltrona.nome}")
                else:
                    produto.nome_produto = poltrona.nome
                    produto.ativo = poltrona.ativo
                    produto.imagem_principal = poltrona.imagem_principal or ''
                    produto.imagem_secundaria = poltrona.imagem_secundaria or ''
                    produto.save()
                    total_atualizados += 1
                    print(f"   ↻ Atualizado: {poltrona.ref_poltrona} - {poltrona.nome}")
    except Exception as e:
        print(f"❌ Erro ao sincronizar poltronas: {e}")
    
    # === SINCRONIZAR PUFES ===
    print("\n📍 Sincronizando Pufes...")
    try:
        tipo_pufe = TipoItem.objects.filter(nome__icontains='Pufe').first()
        if not tipo_pufe:
            print("❌ Tipo 'Pufes' não encontrado!")
        else:
            pufes = Pufe.objects.filter(ativo=True)
            print(f"   Encontrados {pufes.count()} pufes ativos")
            
            for pufe in pufes:
                produto, created = Produto.objects.get_or_create(
                    ref_produto=pufe.ref_pufe,
                    defaults={
                        'nome_produto': pufe.nome,
                        'id_tipo_produto': tipo_pufe,
                        'ativo': pufe.ativo,
                        'created_by': usuario_master,
                        'imagem_principal': pufe.imagem_principal or '',
                        'imagem_secundaria': pufe.imagem_secundaria or '',
                    }
                )
                
                if created:
                    total_criados += 1
                    print(f"   ✓ Criado: {pufe.ref_pufe} - {pufe.nome}")
                else:
                    produto.nome_produto = pufe.nome
                    produto.ativo = pufe.ativo
                    produto.imagem_principal = pufe.imagem_principal or ''
                    produto.imagem_secundaria = pufe.imagem_secundaria or ''
                    produto.save()
                    total_atualizados += 1
                    print(f"   ↻ Atualizado: {pufe.ref_pufe} - {pufe.nome}")
    except Exception as e:
        print(f"❌ Erro ao sincronizar pufes: {e}")
    
    # === SINCRONIZAR ALMOFADAS ===
    print("\n📍 Sincronizando Almofadas...")
    try:
        tipo_almofada = TipoItem.objects.filter(nome__icontains='Almofada').first()
        if not tipo_almofada:
            print("❌ Tipo 'Almofadas' não encontrado!")
        else:
            almofadas = Almofada.objects.filter(ativo=True)
            print(f"   Encontradas {almofadas.count()} almofadas ativas")
            
            for almofada in almofadas:
                produto, created = Produto.objects.get_or_create(
                    ref_produto=almofada.ref_almofada,
                    defaults={
                        'nome_produto': almofada.nome,
                        'id_tipo_produto': tipo_almofada,
                        'ativo': almofada.ativo,
                        'created_by': usuario_master,
                        'imagem_principal': almofada.imagem_principal or '',
                        'imagem_secundaria': almofada.imagem_secundaria or '',
                    }
                )
                
                if created:
                    total_criados += 1
                    print(f"   ✓ Criado: {almofada.ref_almofada} - {almofada.nome}")
                else:
                    produto.nome_produto = almofada.nome
                    produto.ativo = almofada.ativo
                    produto.imagem_principal = almofada.imagem_principal or ''
                    produto.imagem_secundaria = almofada.imagem_secundaria or ''
                    produto.save()
                    total_atualizados += 1
                    print(f"   ↻ Atualizado: {almofada.ref_almofada} - {almofada.nome}")
    except Exception as e:
        print(f"❌ Erro ao sincronizar almofadas: {e}")
    
    print("\n" + "=" * 60)
    print("✅ Sincronização concluída!")
    print(f"📊 Resumo:")
    print(f"   • Produtos criados: {total_criados}")
    print(f"   • Produtos atualizados: {total_atualizados}")
    print(f"   • Total processado: {total_criados + total_atualizados}")
    
    # Verificar estado final
    print(f"\n📈 Estado final da tabela principal:")
    tipos = TipoItem.objects.all()
    for tipo in tipos:
        count = Produto.objects.filter(id_tipo_produto=tipo).count()
        print(f"   • {tipo.nome}: {count} produtos")

if __name__ == '__main__':
    try:
        sincronizar_produtos()
    except Exception as e:
        print(f"\n❌ Erro geral: {e}")
        sys.exit(1)
