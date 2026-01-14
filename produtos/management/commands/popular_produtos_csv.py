"""
Script para popular dados de produtos a partir da pasta dados_produtos.
Suporta: sofás, cadeiras, banquetas, poltronas, pufes e almofadas.

Uso:
    python manage.py popular_produtos_csv --pasta /caminho/para/dados_produtos

Estrutura esperada da pasta:
    dados_produtos/
        fotos/
            sofas/
            cadeiras/
            banquetas/
            poltronas/
            PUFES/
            almofadas/
        infos/
            sofas/           (arquivos JSON)
            cadeiras/        (arquivos JSON)
            banquetas/       (arquivos JSON)
            poltronas/       (arquivos JSON)
            PUFES/           (arquivos JSON)
            almofadas/       (arquivos JSON)
"""

import os
import json
import logging
from pathlib import Path
from decimal import Decimal
from django.core.management.base import BaseCommand, CommandError
from django.core.files.base import ContentFile
from django.utils.text import slugify
from produtos.models import (
    Produto, TipoItem, Modulo, TamanhosModulosDetalhado,
    Cadeira, Banqueta, Poltrona, Pufe, Almofada
)

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Popular dados de produtos a partir da pasta dados_produtos'

    def add_arguments(self, parser):
        parser.add_argument(
            '--pasta',
            type=str,
            required=True,
            help='Caminho para a pasta dados_produtos'
        )
        parser.add_argument(
            '--limpar',
            action='store_true',
            help='Limpar dados antigos antes de popular'
        )
        parser.add_argument(
            '--tipo',
            type=str,
            choices=['sofas', 'cadeiras', 'banquetas', 'poltronas', 'pufes', 'almofadas', 'todos'],
            default='todos',
            help='Tipo de produto a popular'
        )

    def handle(self, *args, **options):
        pasta_base = Path(options['pasta'])
        
        if not pasta_base.exists():
            raise CommandError(f'Pasta não encontrada: {pasta_base}')
        
        if not (pasta_base / 'infos').exists() or not (pasta_base / 'fotos').exists():
            raise CommandError(
                f'Pasta deve conter subpastas "infos" e "fotos"\n'
                f'Estrutura encontrada: {list(pasta_base.iterdir())}'
            )
        
        self.stdout.write(self.style.SUCCESS(f'🚀 Iniciando população de dados...'))
        self.stdout.write(f'Pasta base: {pasta_base}')
        
        tipo = options['tipo']
        
        try:
            # Sofás
            if tipo in ['sofas', 'todos']:
                self._popular_sofas(pasta_base / 'infos' / 'sofas', pasta_base / 'fotos' / 'sofa')
            
            # Cadeiras
            if tipo in ['cadeiras', 'todos']:
                self._popular_cadeiras(pasta_base / 'infos' / 'cadeiras', pasta_base / 'fotos' / 'cadeiras')
            
            # Banquetas
            if tipo in ['banquetas', 'todos']:
                self._popular_banquetas(pasta_base / 'infos' / 'banquetas', pasta_base / 'fotos' / 'banquetas')
            
            # Poltronas
            if tipo in ['poltronas', 'todos']:
                self._popular_poltronas(pasta_base / 'infos' / 'poltronas', pasta_base / 'fotos' / 'poltronas')
            
            # Pufes
            if tipo in ['pufes', 'todos']:
                self._popular_pufes(pasta_base / 'infos' / 'PUFES', pasta_base / 'fotos' / 'PUFES')
            
            # Almofadas
            if tipo in ['almofadas', 'todos']:
                self._popular_almofadas(pasta_base / 'infos' / 'almofadas', pasta_base / 'fotos' / 'almofadas')
            
            self.stdout.write(self.style.SUCCESS('✅ População concluída com sucesso!'))
        
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'❌ Erro durante a população: {str(e)}'))
            logger.exception('Erro ao popular dados')
            raise

    def _popular_sofas(self, pasta_infos, pasta_fotos):
        """Popular sofás a partir dos arquivos JSON"""
        self.stdout.write('\n📦 Populando sofás...')
        
        if not pasta_infos.exists():
            self.stdout.write(self.style.WARNING(f'  ⚠️  Pasta de sofás não encontrada: {pasta_infos}'))
            return
        
        tipo_sofa, _ = TipoItem.objects.get_or_create(nome='Sofás')
        count = 0
        
        for arquivo_json in pasta_infos.glob('*.json'):
            try:
                with open(arquivo_json, 'r', encoding='utf-8') as f:
                    dados = json.load(f)
                
                ref_produto = dados.get('ref_produto') or dados.get('referencia') or arquivo_json.stem
                
                # Buscar ou criar produto
                produto, created = Produto.objects.get_or_create(
                    ref_produto=ref_produto,
                    defaults={
                        'nome_produto': dados.get('nome') or dados.get('nome_produto') or ref_produto,
                        'id_tipo_produto': tipo_sofa,
                        'ativo': dados.get('ativo', True),
                        'tem_cor_tecido': dados.get('tem_cor_tecido', False),
                        'tem_difer_desenho_lado_dir_esq': dados.get('tem_difer_desenho_lado_dir_esq', False),
                        'tem_difer_desenho_tamanho': dados.get('tem_difer_desenho_tamanho', False),
                    }
                )
                
                # Processar imagens
                self._processar_imagens_produto(produto, pasta_fotos, ref_produto)
                
                # Processar módulos
                modulos = dados.get('modulos', [])
                for mod_data in modulos:
                    self._criar_modulo_sofas(produto, mod_data, pasta_fotos, ref_produto)
                
                action = '✨ CRIADO' if created else '🔄 ATUALIZADO'
                self.stdout.write(f'  {action}: {ref_produto}')
                count += 1
            
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f'  ❌ Erro ao processar {arquivo_json.name}: {str(e)}')
                )
                logger.exception(f'Erro ao processar sofá {arquivo_json}')
        
        self.stdout.write(self.style.SUCCESS(f'  ✅ {count} sofá(s) processado(s)'))

    def _popular_cadeiras(self, pasta_infos, pasta_fotos):
        """Popular cadeiras"""
        self.stdout.write('\n🪑 Populando cadeiras...')
        
        if not pasta_infos.exists():
            self.stdout.write(self.style.WARNING(f'  ⚠️  Pasta de cadeiras não encontrada: {pasta_infos}'))
            return
        
        count = 0
        
        for arquivo_json in pasta_infos.glob('*.json'):
            try:
                with open(arquivo_json, 'r', encoding='utf-8') as f:
                    dados = json.load(f)
                
                ref_cadeira = dados.get('ref_cadeira') or dados.get('referencia') or arquivo_json.stem
                
                cadeira, created = Cadeira.objects.get_or_create(
                    ref_cadeira=ref_cadeira,
                    defaults={
                        'nome': dados.get('nome') or ref_cadeira,
                        'largura': Decimal(str(dados.get('largura', 0))),
                        'profundidade': Decimal(str(dados.get('profundidade', 0))),
                        'altura': Decimal(str(dados.get('altura', 0))),
                        'tecido_metros': Decimal(str(dados.get('tecido_metros', 0))),
                        'volume_m3': Decimal(str(dados.get('volume_m3', 0))),
                        'peso_kg': Decimal(str(dados.get('peso_kg', 0))),
                        'preco': Decimal(str(dados.get('preco', 0))),
                        'ativo': dados.get('ativo', True),
                        'tem_cor_tecido': dados.get('tem_cor_tecido', False),
                        'descricao': dados.get('descricao', ''),
                    }
                )
                
                self._processar_imagens_cadeira(cadeira, pasta_fotos, ref_cadeira)
                
                action = '✨ CRIADA' if created else '🔄 ATUALIZADA'
                self.stdout.write(f'  {action}: {ref_cadeira}')
                count += 1
            
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f'  ❌ Erro ao processar {arquivo_json.name}: {str(e)}')
                )
                logger.exception(f'Erro ao processar cadeira {arquivo_json}')
        
        self.stdout.write(self.style.SUCCESS(f'  ✅ {count} cadeira(s) processada(s)'))

    def _popular_banquetas(self, pasta_infos, pasta_fotos):
        """Popular banquetas"""
        self.stdout.write('\n🪑 Populando banquetas...')
        
        if not pasta_infos.exists():
            self.stdout.write(self.style.WARNING(f'  ⚠️  Pasta de banquetas não encontrada: {pasta_infos}'))
            return
        
        count = 0
        
        for arquivo_json in pasta_infos.glob('*.json'):
            try:
                with open(arquivo_json, 'r', encoding='utf-8') as f:
                    dados = json.load(f)
                
                ref_banqueta = dados.get('ref_banqueta') or dados.get('referencia') or arquivo_json.stem
                
                banqueta, created = Banqueta.objects.get_or_create(
                    ref_banqueta=ref_banqueta,
                    defaults={
                        'nome': dados.get('nome') or ref_banqueta,
                        'largura': Decimal(str(dados.get('largura', 0))),
                        'profundidade': Decimal(str(dados.get('profundidade', 0))),
                        'altura': Decimal(str(dados.get('altura', 0))),
                        'tecido_metros': Decimal(str(dados.get('tecido_metros', 0))),
                        'volume_m3': Decimal(str(dados.get('volume_m3', 0))),
                        'peso_kg': Decimal(str(dados.get('peso_kg', 0))),
                        'preco': Decimal(str(dados.get('preco', 0))),
                        'ativo': dados.get('ativo', True),
                        'descricao': dados.get('descricao', ''),
                    }
                )
                
                self._processar_imagens_banqueta(banqueta, pasta_fotos, ref_banqueta)
                
                action = '✨ CRIADA' if created else '🔄 ATUALIZADA'
                self.stdout.write(f'  {action}: {ref_banqueta}')
                count += 1
            
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f'  ❌ Erro ao processar {arquivo_json.name}: {str(e)}')
                )
                logger.exception(f'Erro ao processar banqueta {arquivo_json}')
        
        self.stdout.write(self.style.SUCCESS(f'  ✅ {count} banqueta(s) processada(s)'))

    def _popular_poltronas(self, pasta_infos, pasta_fotos):
        """Popular poltronas"""
        self.stdout.write('\n🪑 Populando poltronas...')
        
        if not pasta_infos.exists():
            self.stdout.write(self.style.WARNING(f'  ⚠️  Pasta de poltronas não encontrada: {pasta_infos}'))
            return
        
        count = 0
        
        for arquivo_json in pasta_infos.glob('*.json'):
            try:
                with open(arquivo_json, 'r', encoding='utf-8') as f:
                    dados = json.load(f)
                
                ref_poltrona = dados.get('ref_poltrona') or dados.get('referencia') or arquivo_json.stem
                
                poltrona, created = Poltrona.objects.get_or_create(
                    ref_poltrona=ref_poltrona,
                    defaults={
                        'nome': dados.get('nome') or ref_poltrona,
                        'largura': Decimal(str(dados.get('largura', 0))),
                        'profundidade': Decimal(str(dados.get('profundidade', 0))),
                        'altura': Decimal(str(dados.get('altura', 0))),
                        'tecido_metros': Decimal(str(dados.get('tecido_metros', 0))),
                        'volume_m3': Decimal(str(dados.get('volume_m3', 0))),
                        'peso_kg': Decimal(str(dados.get('peso_kg', 0))),
                        'preco': Decimal(str(dados.get('preco', 0))),
                        'ativo': dados.get('ativo', True),
                        'tem_cor_tecido': dados.get('tem_cor_tecido', False),
                        'descricao': dados.get('descricao', ''),
                    }
                )
                
                self._processar_imagens_poltrona(poltrona, pasta_fotos, ref_poltrona)
                
                action = '✨ CRIADA' if created else '🔄 ATUALIZADA'
                self.stdout.write(f'  {action}: {ref_poltrona}')
                count += 1
            
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f'  ❌ Erro ao processar {arquivo_json.name}: {str(e)}')
                )
                logger.exception(f'Erro ao processar poltrona {arquivo_json}')
        
        self.stdout.write(self.style.SUCCESS(f'  ✅ {count} poltrona(s) processada(s)'))

    def _popular_pufes(self, pasta_infos, pasta_fotos):
        """Popular pufes"""
        self.stdout.write('\n🪑 Populando pufes...')
        
        if not pasta_infos.exists():
            self.stdout.write(self.style.WARNING(f'  ⚠️  Pasta de pufes não encontrada: {pasta_infos}'))
            return
        
        count = 0
        
        for arquivo_json in pasta_infos.glob('*.json'):
            try:
                with open(arquivo_json, 'r', encoding='utf-8') as f:
                    dados = json.load(f)
                
                ref_pufe = dados.get('ref_pufe') or dados.get('referencia') or arquivo_json.stem
                
                pufe, created = Pufe.objects.get_or_create(
                    ref_pufe=ref_pufe,
                    defaults={
                        'nome': dados.get('nome') or ref_pufe,
                        'largura': Decimal(str(dados.get('largura', 0))),
                        'profundidade': Decimal(str(dados.get('profundidade', 0))),
                        'altura': Decimal(str(dados.get('altura', 0))),
                        'tecido_metros': Decimal(str(dados.get('tecido_metros', 0))),
                        'volume_m3': Decimal(str(dados.get('volume_m3', 0))),
                        'peso_kg': Decimal(str(dados.get('peso_kg', 0))),
                        'preco': Decimal(str(dados.get('preco', 0))),
                        'ativo': dados.get('ativo', True),
                        'descricao': dados.get('descricao', ''),
                    }
                )
                
                self._processar_imagens_pufe(pufe, pasta_fotos, ref_pufe)
                
                action = '✨ CRIADO' if created else '🔄 ATUALIZADO'
                self.stdout.write(f'  {action}: {ref_pufe}')
                count += 1
            
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f'  ❌ Erro ao processar {arquivo_json.name}: {str(e)}')
                )
                logger.exception(f'Erro ao processar pufe {arquivo_json}')
        
        self.stdout.write(self.style.SUCCESS(f'  ✅ {count} pufe(s) processado(s)'))

    def _popular_almofadas(self, pasta_infos, pasta_fotos):
        """Popular almofadas"""
        self.stdout.write('\n🪑 Populando almofadas...')
        
        if not pasta_infos.exists():
            self.stdout.write(self.style.WARNING(f'  ⚠️  Pasta de almofadas não encontrada: {pasta_infos}'))
            return
        
        count = 0
        
        for arquivo_json in pasta_infos.glob('*.json'):
            try:
                with open(arquivo_json, 'r', encoding='utf-8') as f:
                    dados = json.load(f)
                
                ref_almofada = dados.get('ref_almofada') or dados.get('referencia') or arquivo_json.stem
                
                almofada, created = Almofada.objects.get_or_create(
                    ref_almofada=ref_almofada,
                    defaults={
                        'nome': dados.get('nome') or ref_almofada,
                        'largura': Decimal(str(dados.get('largura', 0))),
                        'altura': Decimal(str(dados.get('altura', 0))),
                        'tecido_metros': Decimal(str(dados.get('tecido_metros', 0))),
                        'volume_m3': Decimal(str(dados.get('volume_m3', 0))),
                        'peso_kg': Decimal(str(dados.get('peso_kg', 0))),
                        'preco': Decimal(str(dados.get('preco', 0))),
                        'ativo': dados.get('ativo', True),
                        'descricao': dados.get('descricao', ''),
                    }
                )
                
                self._processar_imagens_almofada(almofada, pasta_fotos, ref_almofada)
                
                action = '✨ CRIADA' if created else '🔄 ATUALIZADA'
                self.stdout.write(f'  {action}: {ref_almofada}')
                count += 1
            
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f'  ❌ Erro ao processar {arquivo_json.name}: {str(e)}')
                )
                logger.exception(f'Erro ao processar almofada {arquivo_json}')
        
        self.stdout.write(self.style.SUCCESS(f'  ✅ {count} almofada(s) processada(s)'))

    def _criar_modulo_sofas(self, produto, mod_data, pasta_fotos, ref_produto):
        """Criar módulos para sofás"""
        nome_modulo = mod_data.get('nome') or mod_data.get('nome_modulo')
        if not nome_modulo:
            return
        
        modulo, _ = Modulo.objects.get_or_create(
            produto=produto,
            nome=nome_modulo,
            defaults={
                'profundidade': Decimal(str(mod_data.get('profundidade', 0))),
                'altura': Decimal(str(mod_data.get('altura', 0))),
                'braco': Decimal(str(mod_data.get('braco', 0))),
                'descricao': mod_data.get('descricao', ''),
            }
        )
        
        # Processar tamanhos do módulo
        tamanhos = mod_data.get('tamanhos', [])
        for tamanho_data in tamanhos:
            TamanhosModulosDetalhado.objects.get_or_create(
                id_modulo=modulo,
                largura_total=Decimal(str(tamanho_data.get('largura_total', 0))),
                defaults={
                    'largura_assento': Decimal(str(tamanho_data.get('largura_assento', 0))),
                    'tecido_metros': Decimal(str(tamanho_data.get('tecido_metros', 0))),
                    'volume_m3': Decimal(str(tamanho_data.get('volume_m3', 0))),
                    'peso_kg': Decimal(str(tamanho_data.get('peso_kg', 0))),
                    'preco': Decimal(str(tamanho_data.get('preco', 0))),
                    'descricao': tamanho_data.get('descricao', ''),
                }
            )

    def _processar_imagens_produto(self, produto, pasta_fotos, ref_produto):
        """Buscar e adicionar imagens ao produto (sofás)"""
        if not pasta_fotos.exists():
            return
        
        # Procurar por pasta com o nome do produto
        pasta_produto = None
        for pasta in pasta_fotos.iterdir():
            if pasta.is_dir() and ref_produto.lower() in pasta.name.lower():
                pasta_produto = pasta
                break
        
        if not pasta_produto:
            return
        
        imagens = sorted([f for f in pasta_produto.glob('*') if f.suffix.lower() in ['.jpg', '.jpeg', '.png']])
        
        if imagens:
            # Primeira imagem como principal
            if not produto.imagem_principal:
                with open(imagens[0], 'rb') as f:
                    nome_arquivo = f'produtos/{ref_produto}_principal{imagens[0].suffix}'
                    produto.imagem_principal.save(nome_arquivo, ContentFile(f.read()), save=False)
            
            # Segunda imagem como secundária
            if len(imagens) > 1 and not produto.imagem_secundaria:
                with open(imagens[1], 'rb') as f:
                    nome_arquivo = f'produtos/{ref_produto}_secundaria{imagens[1].suffix}'
                    produto.imagem_secundaria.save(nome_arquivo, ContentFile(f.read()), save=False)
            
            produto.save()

    def _processar_imagens_cadeira(self, cadeira, pasta_fotos, ref_cadeira):
        """Buscar e adicionar imagens ao cadeira"""
        if not pasta_fotos.exists():
            return
        
        pasta_produto = None
        for pasta in pasta_fotos.iterdir():
            if pasta.is_dir() and ref_cadeira.lower() in pasta.name.lower():
                pasta_produto = pasta
                break
        
        if not pasta_produto:
            return
        
        imagens = sorted([f for f in pasta_produto.glob('*') if f.suffix.lower() in ['.jpg', '.jpeg', '.png']])
        
        if imagens and not cadeira.imagem_principal:
            with open(imagens[0], 'rb') as f:
                nome_arquivo = f'produtos/cadeiras/{ref_cadeira}_principal{imagens[0].suffix}'
                cadeira.imagem_principal.save(nome_arquivo, ContentFile(f.read()), save=False)
        
        if len(imagens) > 1 and not cadeira.imagem_secundaria:
            with open(imagens[1], 'rb') as f:
                nome_arquivo = f'produtos/cadeiras/{ref_cadeira}_secundaria{imagens[1].suffix}'
                cadeira.imagem_secundaria.save(nome_arquivo, ContentFile(f.read()), save=False)
        
        cadeira.save()

    def _processar_imagens_banqueta(self, banqueta, pasta_fotos, ref_banqueta):
        """Buscar e adicionar imagens à banqueta"""
        if not pasta_fotos.exists():
            return
        
        pasta_produto = None
        for pasta in pasta_fotos.iterdir():
            if pasta.is_dir() and ref_banqueta.lower() in pasta.name.lower():
                pasta_produto = pasta
                break
        
        if not pasta_produto:
            return
        
        imagens = sorted([f for f in pasta_produto.glob('*') if f.suffix.lower() in ['.jpg', '.jpeg', '.png']])
        
        if imagens and not banqueta.imagem_principal:
            with open(imagens[0], 'rb') as f:
                nome_arquivo = f'produtos/banquetas/{ref_banqueta}_principal{imagens[0].suffix}'
                banqueta.imagem_principal.save(nome_arquivo, ContentFile(f.read()), save=False)
        
        if len(imagens) > 1 and not banqueta.imagem_secundaria:
            with open(imagens[1], 'rb') as f:
                nome_arquivo = f'produtos/banquetas/{ref_banqueta}_secundaria{imagens[1].suffix}'
                banqueta.imagem_secundaria.save(nome_arquivo, ContentFile(f.read()), save=False)
        
        banqueta.save()

    def _processar_imagens_poltrona(self, poltrona, pasta_fotos, ref_poltrona):
        """Buscar e adicionar imagens à poltrona"""
        if not pasta_fotos.exists():
            return
        
        pasta_produto = None
        for pasta in pasta_fotos.iterdir():
            if pasta.is_dir() and ref_poltrona.lower() in pasta.name.lower():
                pasta_produto = pasta
                break
        
        if not pasta_produto:
            return
        
        imagens = sorted([f for f in pasta_produto.glob('*') if f.suffix.lower() in ['.jpg', '.jpeg', '.png']])
        
        if imagens and not poltrona.imagem_principal:
            with open(imagens[0], 'rb') as f:
                nome_arquivo = f'produtos/poltronas/{ref_poltrona}_principal{imagens[0].suffix}'
                poltrona.imagem_principal.save(nome_arquivo, ContentFile(f.read()), save=False)
        
        if len(imagens) > 1 and not poltrona.imagem_secundaria:
            with open(imagens[1], 'rb') as f:
                nome_arquivo = f'produtos/poltronas/{ref_poltrona}_secundaria{imagens[1].suffix}'
                poltrona.imagem_secundaria.save(nome_arquivo, ContentFile(f.read()), save=False)
        
        poltrona.save()

    def _processar_imagens_pufe(self, pufe, pasta_fotos, ref_pufe):
        """Buscar e adicionar imagens ao pufe"""
        if not pasta_fotos.exists():
            return
        
        pasta_produto = None
        for pasta in pasta_fotos.iterdir():
            if pasta.is_dir() and ref_pufe.lower() in pasta.name.lower():
                pasta_produto = pasta
                break
        
        if not pasta_produto:
            return
        
        imagens = sorted([f for f in pasta_produto.glob('*') if f.suffix.lower() in ['.jpg', '.jpeg', '.png']])
        
        if imagens and not pufe.imagem_principal:
            with open(imagens[0], 'rb') as f:
                nome_arquivo = f'produtos/pufes/{ref_pufe}_principal{imagens[0].suffix}'
                pufe.imagem_principal.save(nome_arquivo, ContentFile(f.read()), save=False)
        
        if len(imagens) > 1 and not pufe.imagem_secundaria:
            with open(imagens[1], 'rb') as f:
                nome_arquivo = f'produtos/pufes/{ref_pufe}_secundaria{imagens[1].suffix}'
                pufe.imagem_secundaria.save(nome_arquivo, ContentFile(f.read()), save=False)
        
        pufe.save()

    def _processar_imagens_almofada(self, almofada, pasta_fotos, ref_almofada):
        """Buscar e adicionar imagens à almofada"""
        if not pasta_fotos.exists():
            return
        
        pasta_produto = None
        for pasta in pasta_fotos.iterdir():
            if pasta.is_dir() and ref_almofada.lower() in pasta.name.lower():
                pasta_produto = pasta
                break
        
        if not pasta_produto:
            return
        
        imagens = sorted([f for f in pasta_produto.glob('*') if f.suffix.lower() in ['.jpg', '.jpeg', '.png']])
        
        if imagens and not almofada.imagem_principal:
            with open(imagens[0], 'rb') as f:
                nome_arquivo = f'produtos/almofadas/{ref_almofada}_principal{imagens[0].suffix}'
                almofada.imagem_principal.save(nome_arquivo, ContentFile(f.read()), save=False)
        
        if len(imagens) > 1 and not almofada.imagem_secundaria:
            with open(imagens[1], 'rb') as f:
                nome_arquivo = f'produtos/almofadas/{ref_almofada}_secundaria{imagens[1].suffix}'
                almofada.imagem_secundaria.save(nome_arquivo, ContentFile(f.read()), save=False)
        
        almofada.save()
