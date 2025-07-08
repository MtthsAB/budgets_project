from django.core.management.base import BaseCommand
from decimal import Decimal
from orcamentos.models import FaixaPreco, FormaPagamento


class Command(BaseCommand):
    help = 'Cria dados iniciais para o sistema de orçamentos'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Criando dados iniciais do sistema de orçamentos...'))
        
        # Criar faixas de preço
        faixas = [
            {'nome': 'Varejo', 'multiplicador': Decimal('1.00')},
            {'nome': 'Atacado', 'multiplicador': Decimal('0.85')},
            {'nome': 'Promocional', 'multiplicador': Decimal('0.75')},
        ]
        
        for faixa_data in faixas:
            faixa, created = FaixaPreco.objects.get_or_create(
                nome=faixa_data['nome'],
                defaults={
                    'multiplicador': faixa_data['multiplicador'],
                    'descricao': f'Faixa de preço {faixa_data["nome"].lower()}',
                    'ativo': True
                }
            )
            if created:
                self.stdout.write(f'✅ Faixa de preço criada: {faixa.nome}')
            else:
                self.stdout.write(f'⚠️ Faixa de preço já existe: {faixa.nome}')
        
        # Criar formas de pagamento
        formas = [
            {'nome': 'À Vista', 'prazo_dias': 0, 'desconto_maximo': Decimal('5.00')},
            {'nome': '30 DDL', 'prazo_dias': 30, 'desconto_maximo': Decimal('2.00')},
            {'nome': 'PIX', 'prazo_dias': 0, 'desconto_maximo': Decimal('7.00')},
        ]
        
        for forma_data in formas:
            forma, created = FormaPagamento.objects.get_or_create(
                nome=forma_data['nome'],
                defaults={
                    'prazo_dias': forma_data['prazo_dias'],
                    'desconto_maximo': forma_data['desconto_maximo'],
                    'descricao': f'Pagamento {forma_data["nome"].lower()}',
                    'ativo': True
                }
            )
            if created:
                self.stdout.write(f'✅ Forma de pagamento criada: {forma.nome}')
            else:
                self.stdout.write(f'⚠️ Forma de pagamento já existe: {forma.nome}')
        
        self.stdout.write(self.style.SUCCESS('Dados iniciais criados com sucesso!'))
        self.stdout.write(f'Faixas de preço: {FaixaPreco.objects.count()}')
        self.stdout.write(f'Formas de pagamento: {FormaPagamento.objects.count()}')
