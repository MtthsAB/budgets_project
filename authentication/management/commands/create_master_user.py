from django.core.management.base import BaseCommand
from django.db import transaction
from authentication.models import CustomUser, TipoPermissao

class Command(BaseCommand):
    help = 'Cria um usuário Master para inicializar o sistema'

    def add_arguments(self, parser):
        parser.add_argument('--email', type=str, help='Email do usuário Master')
        parser.add_argument('--password', type=str, help='Senha do usuário Master')
        parser.add_argument('--first_name', type=str, help='Nome do usuário Master')
        parser.add_argument('--last_name', type=str, help='Sobrenome do usuário Master')

    def handle(self, *args, **options):
        email = options.get('email')
        password = options.get('password')
        first_name = options.get('first_name')
        last_name = options.get('last_name')

        # Verificar se já existe um usuário Master
        if CustomUser.objects.filter(tipo_permissao=TipoPermissao.MASTER).exists():
            self.stdout.write(
                self.style.WARNING('Já existe um usuário Master no sistema!')
            )
            return

        # Solicitar dados se não fornecidos
        if not email:
            email = input('Email do usuário Master: ')
        
        if not password:
            import getpass
            password = getpass.getpass('Senha do usuário Master: ')
        
        if not first_name:
            first_name = input('Nome do usuário Master: ')
        
        if not last_name:
            last_name = input('Sobrenome do usuário Master: ')

        # Validar dados
        if not email or not password or not first_name or not last_name:
            self.stdout.write(
                self.style.ERROR('Todos os campos são obrigatórios!')
            )
            return

        # Verificar se o email já está em uso
        if CustomUser.objects.filter(email=email).exists():
            self.stdout.write(
                self.style.ERROR(f'O email {email} já está em uso!')
            )
            return

        try:
            with transaction.atomic():
                # Criar usuário Master
                user = CustomUser.objects.create_user(
                    email=email,
                    password=password,
                    first_name=first_name,
                    last_name=last_name,
                    tipo_permissao=TipoPermissao.MASTER,
                    is_active=True,
                    is_staff=True,
                    is_superuser=True
                )

                self.stdout.write(
                    self.style.SUCCESS(
                        f'Usuário Master criado com sucesso!\n'
                        f'Email: {user.email}\n'
                        f'Nome: {user.get_full_name()}\n'
                        f'Tipo: {user.get_tipo_permissao_display()}'
                    )
                )

        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Erro ao criar usuário Master: {str(e)}')
            )
