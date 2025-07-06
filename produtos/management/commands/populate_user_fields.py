from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from produtos.models import Item, Modulo, TamanhosModulosDetalhado, Acessorio, FaixaTecido, PrecosBase, TipoItem
from clientes.models import Cliente

User = get_user_model()

class Command(BaseCommand):
    help = 'Preenche campos created_by e updated_by para registros existentes'

    def add_arguments(self, parser):
        parser.add_argument(
            '--user-email',
            type=str,
            help='Email do usuário para ser usado como "Sistema" (padrão: primeiro superuser)',
        )

    def handle(self, *args, **options):
        user_email = options.get('user_email')
        
        if user_email:
            try:
                sistema_user = User.objects.get(email=user_email)
            except User.DoesNotExist:
                self.stdout.write(
                    self.style.ERROR(f'Usuário com email {user_email} não encontrado')
                )
                return
        else:
            # Usar o primeiro superuser encontrado
            sistema_user = User.objects.filter(is_superuser=True).first()
            if not sistema_user:
                self.stdout.write(
                    self.style.ERROR('Nenhum superuser encontrado. Crie um usuário primeiro.')
                )
                return

        self.stdout.write(f'Usando usuário: {sistema_user.email} ({sistema_user.get_full_name()})')

        # Modelos a atualizar
        models_to_update = [
            (TipoItem, 'TipoItem'),
            (Item, 'Item'),
            (Modulo, 'Modulo'),
            (TamanhosModulosDetalhado, 'TamanhosModulosDetalhado'),
            (Acessorio, 'Acessorio'),
            (FaixaTecido, 'FaixaTecido'),
            (PrecosBase, 'PrecosBase'),
            (Cliente, 'Cliente'),
        ]

        total_updated = 0

        for model_class, model_name in models_to_update:
            # Atualizar registros que não têm created_by
            created_count = model_class.objects.filter(created_by__isnull=True).update(
                created_by=sistema_user
            )
            
            # Atualizar registros que não têm updated_by
            updated_count = model_class.objects.filter(updated_by__isnull=True).update(
                updated_by=sistema_user
            )
            
            total_updated += max(created_count, updated_count)
            
            self.stdout.write(
                self.style.SUCCESS(
                    f'{model_name}: {created_count} registros com created_by atualizado, '
                    f'{updated_count} registros com updated_by atualizado'
                )
            )

        self.stdout.write(
            self.style.SUCCESS(
                f'Processamento concluído. Total de registros afetados: {total_updated}'
            )
        )
