from django.core.management.base import BaseCommand
from django.db import transaction
from produtos.models import TipoItem, Linha, FaixaTecido

class Command(BaseCommand):
    help = 'Popula dados iniciais para o sistema'

    def handle(self, *args, **options):
        with transaction.atomic():
            self.stdout.write('Populando dados iniciais...')
            
            # Criar tipos de item
            tipos_item = [
                'Sofás',
                'Acessórios',
                'Cadeiras',
                'Banquetas',
                'Poltronas',
                'Pufes',
                'Almofadas'
            ]
            
            for tipo_nome in tipos_item:
                tipo, created = TipoItem.objects.get_or_create(nome=tipo_nome)
                if created:
                    self.stdout.write(f'✓ Tipo criado: {tipo.nome}')
                else:
                    self.stdout.write(f'- Tipo já existe: {tipo.nome}')
            
            # Criar linhas
            linhas = [
                {'nome': 'Linha Premium', 'descricao': 'Linha premium com acabamento diferenciado'},
                {'nome': 'Linha Confort', 'descricao': 'Linha confort com foco no conforto'},
                {'nome': 'Linha Basic', 'descricao': 'Linha básica com bom custo-benefício'},
                {'nome': 'Linha Executiva', 'descricao': 'Linha executiva para ambientes corporativos'},
            ]
            
            for linha_data in linhas:
                linha, created = Linha.objects.get_or_create(
                    nome=linha_data['nome'],
                    defaults={'descricao': linha_data['descricao']}
                )
                if created:
                    self.stdout.write(f'✓ Linha criada: {linha.nome}')
                else:
                    self.stdout.write(f'- Linha já existe: {linha.nome}')
            
            # Criar faixas de tecido
            faixas_tecido = [
                {'nome': 'Faixa A', 'valor_minimo': 0.00, 'valor_maximo': 50.00},
                {'nome': 'Faixa B', 'valor_minimo': 50.01, 'valor_maximo': 100.00},
                {'nome': 'Faixa C', 'valor_minimo': 100.01, 'valor_maximo': 200.00},
                {'nome': 'Faixa D', 'valor_minimo': 200.01, 'valor_maximo': 500.00},
                {'nome': 'Faixa Premium', 'valor_minimo': 500.01, 'valor_maximo': 9999.99},
            ]
            
            for faixa_data in faixas_tecido:
                faixa, created = FaixaTecido.objects.get_or_create(
                    nome=faixa_data['nome'],
                    defaults={
                        'valor_minimo': faixa_data['valor_minimo'],
                        'valor_maximo': faixa_data['valor_maximo']
                    }
                )
                if created:
                    self.stdout.write(f'✓ Faixa de tecido criada: {faixa.nome}')
                else:
                    self.stdout.write(f'- Faixa de tecido já existe: {faixa.nome}')
            
            self.stdout.write(
                self.style.SUCCESS('Dados iniciais populados com sucesso!')
            )
