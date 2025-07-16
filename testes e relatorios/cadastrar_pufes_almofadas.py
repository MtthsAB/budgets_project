#!/usr/bin/env python3
"""
Script para cadastrar Pufes e Almofadas baseado nos prints fornecidos.

Dados dos prints:
- 6 Pufes com especificações completas
- 3 Almofadas com especificações completas

As imagens já estão disponíveis em:
- /media/produtos/PUFES/
- /media/produtos/almofadas/

Segue rigorosamente as diretrizes do sistema existente.
"""

import os
import sys
import django
from decimal import Decimal
from django.contrib.auth import get_user_model
from django.core.files import File

# Configurar Django
sys.path.append('/home/matas/projetos/Project')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema_produtos.settings')
django.setup()

from produtos.models import TipoItem, Pufe, Almofada

def cadastrar_pufes():
    """Cadastra todos os pufes baseado nos prints fornecidos"""
    
    # Buscar o tipo de produto para Pufes
    try:
        tipo_pufe = TipoItem.objects.get(nome='Pufes')
    except TipoItem.DoesNotExist:
        print("⚠️  Tipo 'Pufes' não encontrado no banco de dados")
        return
    
    # Dados dos pufes conforme os prints
    pufes_dados = [
        {
            'ref_pufe': 'PF934',
            'nome': 'PREMIER',
            'largura': Decimal('104.00'),
            'profundidade': Decimal('75.00'),
            'altura': Decimal('45.00'),
            'tecido_metros': Decimal('4.60'),
            'volume_m3': Decimal('0.310'),
            'peso_kg': Decimal('10.00'),
            'preco': Decimal('943.00'),
            'imagem_nome': 'pf934.png',
            'descricao': 'Pufe Premier - Design elegante e confortável'
        },
        {
            'ref_pufe': 'PF44',
            'nome': 'JANNET',
            'largura': Decimal('62.00'),
            'profundidade': Decimal('62.00'),
            'altura': Decimal('41.00'),
            'tecido_metros': Decimal('1.80'),
            'volume_m3': Decimal('0.170'),
            'peso_kg': Decimal('6.00'),
            'preco': Decimal('519.00'),
            'imagem_nome': 'pf44.png',
            'descricao': 'Pufe Jannet - Estilo clássico e versátil'
        },
        {
            'ref_pufe': 'PF441PL',
            'nome': 'JANNETIPELO',
            'largura': Decimal('62.00'),
            'profundidade': Decimal('62.00'),
            'altura': Decimal('41.00'),
            'tecido_metros': Decimal('1.80'),
            'volume_m3': Decimal('0.170'),
            'peso_kg': Decimal('6.00'),
            'preco': Decimal('1098.00'),
            'imagem_nome': 'pf44 pl.png',
            'descricao': 'Pufe Jannet com acabamento em couro com pêlo'
        },
        {
            'ref_pufe': 'PF441CR',
            'nome': 'JANNETICOURO',
            'largura': Decimal('62.00'),
            'profundidade': Decimal('62.00'),
            'altura': Decimal('41.00'),
            'tecido_metros': Decimal('1.80'),
            'volume_m3': Decimal('0.170'),
            'peso_kg': Decimal('6.00'),
            'preco': Decimal('589.00'),
            'imagem_nome': 'pf44 cr.png',
            'descricao': 'Pufe Jannet com acabamento em couro recortado'
        },
        {
            'ref_pufe': 'PF441TR',
            'nome': 'JANNETITRAMA',
            'largura': Decimal('62.00'),
            'profundidade': Decimal('62.00'),
            'altura': Decimal('41.00'),
            'tecido_metros': Decimal('1.80'),
            'volume_m3': Decimal('0.170'),
            'peso_kg': Decimal('6.00'),
            'preco': Decimal('1098.00'),
            'imagem_nome': 'pf44 tr.png',
            'descricao': 'Pufe Jannet com acabamento em couro trama'
        },
        {
            'ref_pufe': 'PF57',
            'nome': 'LUIZ FELIPE',
            'largura': Decimal('80.00'),
            'profundidade': Decimal('57.00'),
            'altura': Decimal('37.00'),
            'tecido_metros': Decimal('1.20'),
            'volume_m3': Decimal('0.190'),
            'peso_kg': Decimal('6.00'),
            'preco': Decimal('1198.00'),
            'imagem_nome': 'pf57.png',
            'descricao': 'Pufe Luiz Felipe - Design sofisticado e moderno'
        }
    ]
    
    # Obter usuário master
    User = get_user_model()
    try:
        user_master = User.objects.get(email='admin@essere.com')
    except User.DoesNotExist:
        print("⚠️  Usuário 'admin@essere.com' não encontrado")
        return
    
    print("🔄 Iniciando cadastro dos Pufes...")
    
    for dados in pufes_dados:
        try:
            # Verificar se já existe
            if Pufe.objects.filter(ref_pufe=dados['ref_pufe']).exists():
                print(f"⚠️  Pufe {dados['ref_pufe']} já existe - pulando...")
                continue
            
            # Criar o pufe
            pufe = Pufe(
                ref_pufe=dados['ref_pufe'],
                nome=dados['nome'],
                largura=dados['largura'],
                profundidade=dados['profundidade'],
                altura=dados['altura'],
                tecido_metros=dados['tecido_metros'],
                volume_m3=dados['volume_m3'],
                peso_kg=dados['peso_kg'],
                preco=dados['preco'],
                ativo=True,
                descricao=dados['descricao'],
                created_by=user_master,
                updated_by=user_master
            )
            
            # Associar imagem se existir
            imagem_path = f"/home/matas/projetos/Project/media/produtos/PUFES/{dados['imagem_nome']}"
            if os.path.exists(imagem_path):
                with open(imagem_path, 'rb') as img_file:
                    pufe.imagem_principal.save(
                        dados['imagem_nome'],
                        File(img_file),
                        save=False
                    )
                print(f"📸 Imagem {dados['imagem_nome']} associada")
            else:
                print(f"⚠️  Imagem {dados['imagem_nome']} não encontrada")
            
            pufe.save()
            print(f"✅ Pufe {dados['ref_pufe']} - {dados['nome']} cadastrado com sucesso")
            
        except Exception as e:
            print(f"❌ Erro ao cadastrar pufe {dados['ref_pufe']}: {str(e)}")
    
    print("✅ Cadastro de Pufes concluído!\n")


def cadastrar_almofadas():
    """Cadastra todas as almofadas baseado nos prints fornecidos"""
    
    # Buscar o tipo de produto para Almofadas
    try:
        tipo_almofada = TipoItem.objects.get(nome='Almofadas')
    except TipoItem.DoesNotExist:
        print("⚠️  Tipo 'Almofadas' não encontrado no banco de dados")
        return
    
    # Dados das almofadas conforme os prints
    almofadas_dados = [
        {
            'ref_almofada': 'AL01',
            'nome': 'COM MOLDURA',
            'largura': Decimal('60.00'),
            'altura': Decimal('60.00'),
            'tecido_metros': Decimal('1.30'),
            'volume_m3': Decimal('0.500'),
            'peso_kg': Decimal('1.00'),
            'preco': Decimal('246.00'),
            'imagem_nome': 'al01.png',
            'descricao': 'Almofada decorativa com moldura'
        },
        {
            'ref_almofada': 'AL07',
            'nome': 'COM APOIO',
            'largura': Decimal('60.00'),
            'altura': Decimal('54.00'),
            'tecido_metros': Decimal('1.40'),
            'volume_m3': Decimal('0.100'),
            'peso_kg': Decimal('2.00'),
            'preco': Decimal('327.00'),
            'imagem_nome': 'al07.png',
            'descricao': 'Almofada com apoio ergonômico'
        },
        {
            'ref_almofada': 'AL06',
            'nome': 'PASTEL',
            'largura': Decimal('55.00'),
            'altura': Decimal('55.00'),
            'tecido_metros': Decimal('1.00'),
            'volume_m3': Decimal('0.050'),
            'peso_kg': Decimal('2.00'),
            'preco': Decimal('169.00'),
            'imagem_nome': 'al06.png',
            'descricao': 'Almofada em tons pastéis'
        }
    ]
    
    # Obter usuário master
    User = get_user_model()
    try:
        user_master = User.objects.get(email='admin@essere.com')
    except User.DoesNotExist:
        print("⚠️  Usuário 'admin@essere.com' não encontrado")
        return
    
    print("🔄 Iniciando cadastro das Almofadas...")
    
    for dados in almofadas_dados:
        try:
            # Verificar se já existe
            if Almofada.objects.filter(ref_almofada=dados['ref_almofada']).exists():
                print(f"⚠️  Almofada {dados['ref_almofada']} já existe - pulando...")
                continue
            
            # Criar a almofada
            almofada = Almofada(
                ref_almofada=dados['ref_almofada'],
                nome=dados['nome'],
                largura=dados['largura'],
                altura=dados['altura'],
                tecido_metros=dados['tecido_metros'],
                volume_m3=dados['volume_m3'],
                peso_kg=dados['peso_kg'],
                preco=dados['preco'],
                ativo=True,
                descricao=dados['descricao'],
                created_by=user_master,
                updated_by=user_master
            )
            
            # Associar imagem se existir
            imagem_path = f"/home/matas/projetos/Project/media/produtos/almofadas/{dados['imagem_nome']}"
            if os.path.exists(imagem_path):
                with open(imagem_path, 'rb') as img_file:
                    almofada.imagem_principal.save(
                        dados['imagem_nome'],
                        File(img_file),
                        save=False
                    )
                print(f"📸 Imagem {dados['imagem_nome']} associada")
            else:
                print(f"⚠️  Imagem {dados['imagem_nome']} não encontrada")
            
            almofada.save()
            print(f"✅ Almofada {dados['ref_almofada']} - {dados['nome']} cadastrada com sucesso")
            
        except Exception as e:
            print(f"❌ Erro ao cadastrar almofada {dados['ref_almofada']}: {str(e)}")
    
    print("✅ Cadastro de Almofadas concluído!\n")


def verificar_estrutura():
    """Verifica se a estrutura necessária está presente"""
    print("🔍 Verificando estrutura do sistema...\n")
    
    # Verificar tipos de produto
    tipos_necessarios = ['Pufes', 'Almofadas']
    for tipo in tipos_necessarios:
        try:
            obj = TipoItem.objects.get(nome=tipo)
            print(f"✅ Tipo '{tipo}' encontrado (ID: {obj.id})")
        except TipoItem.DoesNotExist:
            print(f"❌ Tipo '{tipo}' NÃO encontrado")
    
    # Verificar pastas de imagens
    pastas_imagens = [
        '/home/matas/projetos/Project/media/produtos/PUFES/',
        '/home/matas/projetos/Project/media/produtos/almofadas/'
    ]
    
    for pasta in pastas_imagens:
        if os.path.exists(pasta):
            arquivos = os.listdir(pasta)
            print(f"✅ Pasta {pasta} existe ({len(arquivos)} imagens)")
        else:
            print(f"❌ Pasta {pasta} NÃO existe")
    
    # Verificar usuário master
    User = get_user_model()
    try:
        User.objects.get(email='admin@essere.com')
        print("✅ Usuário 'admin@essere.com' encontrado")
    except User.DoesNotExist:
        print("❌ Usuário 'admin@essere.com' NÃO encontrado")
    
    print("\n" + "="*50)


def main():
    """Função principal"""
    print("🎯 CADASTRO DE PUFES E ALMOFADAS")
    print("="*50)
    
    # Verificar estrutura
    verificar_estrutura()
    
    # Cadastrar produtos
    cadastrar_pufes()
    cadastrar_almofadas()
    
    # Resumo final
    print("📊 RESUMO FINAL:")
    print("="*30)
    
    try:
        total_pufes = Pufe.objects.filter(ativo=True).count()
        total_almofadas = Almofada.objects.filter(ativo=True).count()
        
        print(f"📦 Pufes ativos: {total_pufes}")
        print(f"🛏️  Almofadas ativas: {total_almofadas}")
        print(f"🎉 Total de produtos cadastrados: {total_pufes + total_almofadas}")
        
    except Exception as e:
        print(f"❌ Erro ao obter resumo: {str(e)}")
    
    print("\n✅ Script executado com sucesso!")


if __name__ == '__main__':
    main()
