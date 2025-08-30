"""
Management command para importação em massa de produtos no banco PostgreSQL.

Este comando implementa a inclusão dos produtos conforme especificado:
- Almofadas (produtos_almofada)
- Pufes (produtos_pufe) 
- Poltronas (produtos_poltrona)
- Cadeiras (produtos_cadeira)
- Banquetas (produtos_banqueta)
- Sofás (produtos_produto + produtos_modulo + produtos_tamanhosmodulosdetalhado)
- Acessórios (produtos_acessorio)

Realiza upsert por referência e gera relatório em Markdown.
"""

import os
from datetime import datetime
from decimal import Decimal
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from django.conf import settings

from produtos.models import (
    Almofada, Pufe, Poltrona, Cadeira, Banqueta, 
    Produto, Modulo, TamanhosModulosDetalhado, Acessorio, TipoItem
)


class Command(BaseCommand):
    help = 'Importa produtos em massa para o banco PostgreSQL'

    def __init__(self):
        super().__init__()
        self.relatorio = {
            'inseridos': [],
            'atualizados': [],
            'ignorados': [],
            'erros': []
        }
        self.timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    
    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Executa sem salvar no banco (simulação)',
        )
        parser.add_argument(
            '--verbose',
            action='store_true',
            help='Saída detalhada do processo',
        )

    def handle(self, *args, **options):
        self.stdout.write(
            self.style.SUCCESS('Iniciando importação em massa de produtos...')
        )
        
        try:
            with transaction.atomic():
                # Importar cada tipo de produto
                self._importar_almofadas(options)
                self._importar_pufes(options)
                self._importar_poltronas(options)
                self._importar_cadeiras(options)
                self._importar_banquetas(options)
                self._importar_sofas(options)
                self._importar_acessorios(options)
                
                if options['dry_run']:
                    self.stdout.write(
                        self.style.WARNING('DRY RUN: Nenhuma alteração foi salva no banco.')
                    )
                    transaction.set_rollback(True)
                
            # Gerar relatório final
            self._gerar_relatorio()
            
            self.stdout.write(
                self.style.SUCCESS('Importação concluída com sucesso!')
            )
            
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Erro durante a importação: {str(e)}')
            )
            raise CommandError(f'Falha na importação: {str(e)}')

    def _importar_almofadas(self, options):
        """Importa almofadas conforme especificação"""
        self.stdout.write('Importando almofadas...')
        
        almofadas_data = [
            {
                'ref_almofada': 'AL01',
                'nome': 'COM MOLDURA',
                'largura': Decimal('60'),
                'altura': Decimal('60'),
                'tecido_metros': Decimal('1.3'),
                'volume_m3': Decimal('0.5'),
                'peso_kg': Decimal('1'),
                'preco': Decimal('246')
            },
            {
                'ref_almofada': 'AL07',
                'nome': 'COM APOIO',
                'largura': Decimal('60'),
                'altura': Decimal('54'),
                'tecido_metros': Decimal('1.4'),
                'volume_m3': Decimal('0.10'),
                'peso_kg': Decimal('2'),
                'preco': Decimal('327')
            },
            {
                'ref_almofada': 'AL06',
                'nome': 'PASTEL',
                'largura': Decimal('55'),
                'altura': Decimal('55'),
                'tecido_metros': Decimal('1.0'),
                'volume_m3': Decimal('0.05'),
                'peso_kg': Decimal('2'),
                'preco': Decimal('169')
            },
            {
                'ref_almofada': 'AL08',
                'nome': 'LOMBAR',
                'largura': Decimal('53'),
                'altura': Decimal('29'),
                'tecido_metros': Decimal('1.0'),
                'volume_m3': Decimal('0.02'),
                'peso_kg': Decimal('2'),
                'preco': Decimal('145')
            },
            {
                'ref_almofada': 'AL05',
                'nome': 'COM ABAS',
                'largura': Decimal('62'),
                'altura': Decimal('62'),
                'tecido_metros': Decimal('1.0'),
                'volume_m3': Decimal('0.07'),
                'peso_kg': Decimal('2'),
                'preco': Decimal('242')
            }
        ]
        
        for data in almofadas_data:
            self._processar_item(Almofada, data, 'ref_almofada', options)

    def _importar_pufes(self, options):
        """Importa pufes conforme especificação"""
        self.stdout.write('Importando pufes...')
        
        pufes_data = [
            {
                'ref_pufe': 'PF934',
                'nome': 'PREMIER',
                'largura': Decimal('104'),
                'profundidade': Decimal('76'),
                'altura': Decimal('45'),
                'tecido_metros': Decimal('4.6'),
                'volume_m3': Decimal('0.31'),
                'peso_kg': Decimal('10'),
                'preco': Decimal('943')
            },
            {
                'ref_pufe': 'PF44',
                'nome': 'JANNET',
                'largura': Decimal('62'),
                'profundidade': Decimal('62'),
                'altura': Decimal('41'),
                'tecido_metros': Decimal('1.8'),
                'volume_m3': Decimal('0.17'),
                'peso_kg': Decimal('6'),
                'preco': Decimal('519')
            },
            {
                'ref_pufe': 'PF44/PL',
                'nome': 'JANNET/PELO',
                'largura': Decimal('62'),
                'profundidade': Decimal('62'),
                'altura': Decimal('41'),
                'tecido_metros': Decimal('1.8'),
                'volume_m3': Decimal('0.17'),
                'peso_kg': Decimal('6'),
                'preco': Decimal('1098')
            },
            {
                'ref_pufe': 'PF44/CR',
                'nome': 'JANNET/COURO',
                'largura': Decimal('62'),
                'profundidade': Decimal('62'),
                'altura': Decimal('41'),
                'tecido_metros': Decimal('1.8'),
                'volume_m3': Decimal('0.17'),
                'peso_kg': Decimal('6'),
                'preco': Decimal('589')
            },
            {
                'ref_pufe': 'PF44/TR',
                'nome': 'JANNET/TRAMA',
                'largura': Decimal('62'),
                'profundidade': Decimal('62'),
                'altura': Decimal('41'),
                'tecido_metros': Decimal('1.8'),
                'volume_m3': Decimal('0.17'),
                'peso_kg': Decimal('6'),
                'preco': Decimal('1098')
            }
        ]
        
        for data in pufes_data:
            self._processar_item(Pufe, data, 'ref_pufe', options)

    def _importar_poltronas(self, options):
        """Importa poltronas conforme especificação"""
        self.stdout.write('Importando poltronas...')
        
        poltronas_data = [
            {
                'ref_poltrona': 'PL243',
                'nome': 'ARIA',
                'largura': Decimal('82'),
                'profundidade': Decimal('81'),
                'altura': Decimal('84'),
                'tecido_metros': Decimal('4.6'),
                'volume_m3': Decimal('0.60'),
                'peso_kg': Decimal('25'),
                'preco': Decimal('1301')
            },
            {
                'ref_poltrona': 'PL246',
                'nome': 'ARISTOCRATA',
                'largura': Decimal('78'),
                'profundidade': Decimal('81'),
                'altura': Decimal('89'),
                'tecido_metros': Decimal('3.8'),
                'volume_m3': Decimal('0.60'),
                'peso_kg': Decimal('25'),
                'preco': Decimal('1168')
            },
            {
                'ref_poltrona': 'PL105',
                'nome': 'CERNE',
                'largura': Decimal('69'),
                'profundidade': Decimal('78'),
                'altura': Decimal('86'),
                'tecido_metros': Decimal('2.6'),
                'volume_m3': Decimal('0.50'),
                'peso_kg': Decimal('15'),
                'preco': Decimal('1673')
            },
            {
                'ref_poltrona': 'PL869',
                'nome': 'CHANEL',
                'largura': Decimal('104'),
                'profundidade': Decimal('80'),
                'altura': Decimal('73'),
                'tecido_metros': Decimal('6.4'),
                'volume_m3': Decimal('0.65'),
                'peso_kg': Decimal('20'),
                'preco': Decimal('1712')
            },
            {
                'ref_poltrona': 'PL97',
                'nome': 'CLARA',
                'largura': Decimal('67'),
                'profundidade': Decimal('74'),
                'altura': Decimal('86'),
                'tecido_metros': Decimal('3.5'),
                'volume_m3': Decimal('0.46'),
                'peso_kg': Decimal('15'),
                'preco': Decimal('1027')
            }
        ]
        
        for data in poltronas_data:
            self._processar_item(Poltrona, data, 'ref_poltrona', options)

    def _importar_cadeiras(self, options):
        """Importa cadeiras conforme especificação"""
        self.stdout.write('Importando cadeiras...')
        
        cadeiras_data = [
            {
                'ref_cadeira': 'CD01',
                'nome': 'EVA',
                'largura': Decimal('48'),
                'profundidade': Decimal('65'),
                'altura': Decimal('97'),
                'tecido_metros': Decimal('1.9'),
                'volume_m3': Decimal('0.40'),
                'peso_kg': Decimal('8'),
                'preco': Decimal('857')
            },
            {
                'ref_cadeira': 'CD24',
                'nome': 'EVA BR',
                'largura': Decimal('73'),
                'profundidade': Decimal('65'),
                'altura': Decimal('97'),
                'tecido_metros': Decimal('2.9'),
                'volume_m3': Decimal('0.48'),
                'peso_kg': Decimal('11'),
                'preco': Decimal('1033')
            },
            {
                'ref_cadeira': 'CD267',
                'nome': 'FIT',
                'largura': Decimal('47'),
                'profundidade': Decimal('58'),
                'altura': Decimal('89'),
                'tecido_metros': Decimal('1.3'),
                'volume_m3': Decimal('0.33'),
                'peso_kg': Decimal('7'),
                'preco': Decimal('520')
            },
            {
                'ref_cadeira': 'CD74/AC15',
                'nome': 'FIT GIRATÓRIA',
                'largura': Decimal('47'),
                'profundidade': Decimal('58'),
                'altura': Decimal('89'),
                'tecido_metros': Decimal('1.3'),
                'volume_m3': Decimal('0.33'),
                'peso_kg': Decimal('7'),
                'preco': Decimal('543')
            },
            {
                'ref_cadeira': 'CD210',
                'nome': 'KIA',
                'largura': Decimal('44'),
                'profundidade': Decimal('61'),
                'altura': Decimal('98'),
                'tecido_metros': Decimal('1.2'),
                'volume_m3': Decimal('0.32'),
                'peso_kg': Decimal('6'),
                'preco': Decimal('357')
            }
        ]
        
        for data in cadeiras_data:
            self._processar_item(Cadeira, data, 'ref_cadeira', options)

    def _importar_banquetas(self, options):
        """Importa banquetas conforme especificação"""
        self.stdout.write('Importando banquetas...')
        
        banquetas_data = [
            {
                'ref_banqueta': 'BQ13',
                'nome': 'CERES',
                'largura': Decimal('42'),
                'profundidade': Decimal('50'),
                'altura': Decimal('99'),
                'tecido_metros': Decimal('0.9'),
                'volume_m3': Decimal('0.24'),
                'peso_kg': Decimal('8'),
                'preco': Decimal('658')
            },
            {
                'ref_banqueta': 'BQ249',
                'nome': 'GIO',
                'largura': Decimal('44'),
                'profundidade': Decimal('50'),
                'altura': Decimal('99'),
                'tecido_metros': Decimal('1.7'),
                'volume_m3': Decimal('0.30'),
                'peso_kg': Decimal('8'),
                'preco': Decimal('908')
            },
            {
                'ref_banqueta': 'BQ278',
                'nome': 'GIO GIRATÓRIA',
                'largura': Decimal('55'),
                'profundidade': Decimal('50'),
                'altura': Decimal('100'),
                'tecido_metros': Decimal('1.7'),
                'volume_m3': Decimal('0.30'),
                'peso_kg': Decimal('8'),
                'preco': Decimal('908')
            },
            {
                'ref_banqueta': 'BQ250',
                'nome': 'IAN',
                'largura': Decimal('58'),
                'profundidade': Decimal('56'),
                'altura': Decimal('112'),
                'tecido_metros': Decimal('2.3'),
                'volume_m3': Decimal('0.38'),
                'peso_kg': Decimal('9'),
                'preco': Decimal('1065')
            },
            {
                'ref_banqueta': 'BQ251',
                'nome': 'MET',
                'largura': Decimal('49'),
                'profundidade': Decimal('50'),
                'altura': Decimal('99'),
                'tecido_metros': Decimal('1.3'),
                'volume_m3': Decimal('0.22'),
                'peso_kg': Decimal('8'),
                'preco': Decimal('988')
            }
        ]
        
        for data in banquetas_data:
            self._processar_item(Banqueta, data, 'ref_banqueta', options)

    def _importar_sofas(self, options):
        """Importa sofás e seus módulos/tamanhos conforme especificação"""
        self.stdout.write('Importando sofás...')
        
        # Obter ou criar tipo 'Sofás'
        tipo_sofa, _ = TipoItem.objects.get_or_create(nome='Sofás')
        
        # BIG BOSS - SF982
        self._processar_sofa_big_boss(tipo_sofa, options)
        
        # LE COULTRE - SF939
        self._processar_sofa_le_coultre(tipo_sofa, options)

    def _processar_sofa_big_boss(self, tipo_sofa, options):
        """Processa o sofá BIG BOSS e seus módulos"""
        # Produto base
        produto_data = {
            'ref_produto': 'SF982',
            'nome_produto': 'Big Boss',
            'id_tipo_produto': tipo_sofa,
            'tem_cor_tecido': True,
            'ativo': True
        }
        
        produto = self._processar_item(Produto, produto_data, 'ref_produto', options, retornar_objeto=True)
        if not produto:
            return
        
        # Módulos do BIG BOSS
        modulos_data = [
            {
                'produto': produto,
                'nome': '1 LUGAR S/BR',
                'numero': '02'
            },
            {
                'produto': produto,
                'nome': 'CHAISE',
                'numero': '03'
            },
            {
                'produto': produto,
                'nome': 'AUXILIAR',
                'numero': '05'
            }
        ]
        
        for modulo_data in modulos_data:
            self._processar_modulo_big_boss(modulo_data, options)

    def _processar_modulo_big_boss(self, modulo_data, options):
        """Processa módulos específicos do BIG BOSS"""
        # Criar ou atualizar módulo
        modulo, created = Modulo.objects.get_or_create(
            produto=modulo_data['produto'],
            nome=modulo_data['nome'],
            defaults={}
        )
        
        if created:
            self.relatorio['inseridos'].append(f"Módulo {modulo}")
        
        # Tamanhos por módulo
        if modulo_data['numero'] == '02':  # 1 LUGAR S/BR
            tamanhos = [
                {
                    'largura_total': Decimal('120'),
                    'tecido_metros': Decimal('7.2'),
                    'volume_m3': Decimal('1.4'),
                    'peso_kg': Decimal('45'),
                    'preco': Decimal('2659')
                },
                {
                    'largura_total': Decimal('110'),
                    'tecido_metros': Decimal('6.8'),
                    'volume_m3': Decimal('1.3'),
                    'peso_kg': Decimal('43'),
                    'preco': Decimal('2501')
                }
            ]
        elif modulo_data['numero'] == '03':  # CHAISE
            tamanhos = [
                {
                    'largura_total': Decimal('145'),
                    'tecido_metros': Decimal('9.0'),
                    'volume_m3': Decimal('2.3'),
                    'peso_kg': Decimal('70'),
                    'preco': Decimal('3575')
                },
                {
                    'largura_total': Decimal('135'),
                    'tecido_metros': Decimal('8.6'),
                    'volume_m3': Decimal('2.2'),
                    'peso_kg': Decimal('68'),
                    'preco': Decimal('3363')
                }
            ]
        elif modulo_data['numero'] == '05':  # AUXILIAR
            tamanhos = [
                {
                    'largura_total': Decimal('44'),
                    'largura_assento': Decimal('107'),
                    'tecido_metros': Decimal('2.3'),
                    'volume_m3': Decimal('0.6'),
                    'peso_kg': Decimal('30'),
                    'preco': Decimal('1169')
                }
            ]
        
        for tamanho_data in tamanhos:
            tamanho_data['id_modulo'] = modulo
            self._processar_item(TamanhosModulosDetalhado, tamanho_data, None, options)

    def _processar_sofa_le_coultre(self, tipo_sofa, options):
        """Processa o sofá LE COULTRE e seus módulos"""
        # Produto base
        produto_data = {
            'ref_produto': 'SF939',
            'nome_produto': 'LE COULTRE',
            'id_tipo_produto': tipo_sofa,
            'tem_cor_tecido': True,
            'ativo': True
        }
        
        produto = self._processar_item(Produto, produto_data, 'ref_produto', options, retornar_objeto=True)
        if not produto:
            return
        
        # Módulos do LE COULTRE
        modulos_data = [
            {
                'produto': produto,
                'nome': '2 ASSENTOS C/2BR',
                'numero': '01'
            },
            {
                'produto': produto,
                'nome': 'POLTRONA',
                'numero': '02'
            }
        ]
        
        for modulo_data in modulos_data:
            self._processar_modulo_le_coultre(modulo_data, options)

    def _processar_modulo_le_coultre(self, modulo_data, options):
        """Processa módulos específicos do LE COULTRE"""
        # Criar ou atualizar módulo
        modulo, created = Modulo.objects.get_or_create(
            produto=modulo_data['produto'],
            nome=modulo_data['nome'],
            defaults={}
        )
        
        if created:
            self.relatorio['inseridos'].append(f"Módulo {modulo}")
        
        # Tamanhos por módulo
        if modulo_data['numero'] == '01':  # 2 ASSENTOS C/2BR
            tamanhos = [
                {
                    'largura_total': Decimal('292'),
                    'tecido_metros': Decimal('14.3'),
                    'volume_m3': Decimal('2.8'),
                    'peso_kg': Decimal('80'),
                    'preco': Decimal('5952')
                },
                {
                    'largura_total': Decimal('272'),
                    'tecido_metros': Decimal('13.5'),
                    'volume_m3': Decimal('2.6'),
                    'peso_kg': Decimal('75'),
                    'preco': Decimal('5411')
                }
            ]
        elif modulo_data['numero'] == '02':  # POLTRONA
            tamanhos = [
                {
                    'largura_total': Decimal('115'),
                    'tecido_metros': Decimal('7.0'),
                    'volume_m3': Decimal('1.5'),
                    'peso_kg': Decimal('40'),
                    'preco': Decimal('2822')
                }
            ]
        
        for tamanho_data in tamanhos:
            tamanho_data['id_modulo'] = modulo
            self._processar_item(TamanhosModulosDetalhado, tamanho_data, None, options)

    def _importar_acessorios(self, options):
        """Importa acessórios conforme especificação"""
        self.stdout.write('Importando acessórios...')
        
        acessorios_data = [
            {
                'ref_acessorio': 'AC44',
                'nome': 'Carregador por Indução',
                'preco': Decimal('482'),
                'ativo': True
            },
            {
                'ref_acessorio': 'AC45',
                'nome': 'Luminária',
                'preco': Decimal('525'),
                'ativo': True
            },
            {
                'ref_acessorio': 'AC48',
                'nome': 'Torre USB',
                'preco': Decimal('641'),
                'ativo': True
            }
        ]
        
        for data in acessorios_data:
            self._processar_item(Acessorio, data, 'ref_acessorio', options)

    def _processar_item(self, model_class, data, ref_field, options, retornar_objeto=False):
        """Processa um item individual (upsert)"""
        try:
            if ref_field:
                # Upsert baseado na referência
                obj, created = model_class.objects.update_or_create(
                    **{ref_field: data[ref_field]},
                    defaults=data
                )
                
                if created:
                    self.relatorio['inseridos'].append(f"{model_class.__name__}: {data[ref_field]}")
                    if options['verbose']:
                        self.stdout.write(f"  + Inserido: {obj}")
                else:
                    self.relatorio['atualizados'].append(f"{model_class.__name__}: {data[ref_field]}")
                    if options['verbose']:
                        self.stdout.write(f"  ~ Atualizado: {obj}")
            else:
                # Para TamanhosModulosDetalhado (sem referência única)
                obj = model_class.objects.create(**data)
                self.relatorio['inseridos'].append(f"{model_class.__name__}: {obj}")
                if options['verbose']:
                    self.stdout.write(f"  + Inserido: {obj}")
            
            if retornar_objeto:
                return obj
                
        except Exception as e:
            erro_msg = f"{model_class.__name__}: {data.get(ref_field, 'N/A')} - {str(e)}"
            self.relatorio['erros'].append(erro_msg)
            self.stdout.write(self.style.ERROR(f"  ! Erro: {erro_msg}"))
            return None

    def _gerar_relatorio(self):
        """Gera relatório final em Markdown"""
        logs_dir = os.path.join(settings.BASE_DIR, 'logs')
        os.makedirs(logs_dir, exist_ok=True)
        
        relatorio_path = os.path.join(
            logs_dir, 
            f'inclusao_produtos_{datetime.now().strftime("%Y%m%d_%H%M%S")}.md'
        )
        
        with open(relatorio_path, 'w', encoding='utf-8') as f:
            f.write(f"# Relatório de Inclusão em Massa de Produtos\n\n")
            f.write(f"**Data/Hora:** {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n\n")
            
            # Resumo
            total_inseridos = len(self.relatorio['inseridos'])
            total_atualizados = len(self.relatorio['atualizados'])
            total_ignorados = len(self.relatorio['ignorados'])
            total_erros = len(self.relatorio['erros'])
            
            f.write(f"## Resumo Executivo\n\n")
            f.write(f"- **Itens Inseridos:** {total_inseridos}\n")
            f.write(f"- **Itens Atualizados:** {total_atualizados}\n")
            f.write(f"- **Itens Ignorados:** {total_ignorados}\n")
            f.write(f"- **Erros:** {total_erros}\n\n")
            
            # Detalhes dos inseridos
            if self.relatorio['inseridos']:
                f.write(f"## Itens Inseridos ({total_inseridos})\n\n")
                for item in self.relatorio['inseridos']:
                    f.write(f"- {item}\n")
                f.write(f"\n")
            
            # Detalhes dos atualizados
            if self.relatorio['atualizados']:
                f.write(f"## Itens Atualizados ({total_atualizados})\n\n")
                for item in self.relatorio['atualizados']:
                    f.write(f"- {item}\n")
                f.write(f"\n")
            
            # Detalhes dos ignorados
            if self.relatorio['ignorados']:
                f.write(f"## Itens Ignorados ({total_ignorados})\n\n")
                for item in self.relatorio['ignorados']:
                    f.write(f"- {item}\n")
                f.write(f"\n")
            
            # Detalhes dos erros
            if self.relatorio['erros']:
                f.write(f"## Erros Encontrados ({total_erros})\n\n")
                for erro in self.relatorio['erros']:
                    f.write(f"- {erro}\n")
                f.write(f"\n")
            
            f.write(f"---\n")
            f.write(f"*Relatório gerado automaticamente pelo sistema de importação em massa*\n")
        
        self.stdout.write(
            self.style.SUCCESS(f'Relatório salvo em: {relatorio_path}')
        )
