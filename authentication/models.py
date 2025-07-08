from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from sistema_produtos.base_models import BaseModel

class TipoPermissao(models.TextChoices):
    """Tipos de permissão do sistema"""
    MASTER = 'master', 'Master'
    ADMIN = 'admin', 'Admin'
    VENDEDOR = 'vendedor', 'Vendedor'
    OPERADOR_PRODUTOS = 'operador_produtos', 'Operador de Produtos'

class CustomUserManager(BaseUserManager):
    """Manager personalizado para o modelo de usuário"""
    
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('O email é obrigatório')
        
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser deve ter is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser deve ter is_superuser=True.')
        
        return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin, BaseModel):
    """Modelo de usuário personalizado usando email como username"""
    
    email = models.EmailField(unique=True, verbose_name="Email")
    first_name = models.CharField(max_length=30, verbose_name="Nome")
    last_name = models.CharField(max_length=30, verbose_name="Sobrenome")
    is_active = models.BooleanField(default=True, verbose_name="Ativo")
    is_staff = models.BooleanField(default=False, verbose_name="Staff")
    tipo_permissao = models.CharField(
        max_length=20,
        choices=TipoPermissao.choices,
        default=TipoPermissao.OPERADOR_PRODUTOS,
        verbose_name="Tipo de Permissão"
    )
    
    objects = CustomUserManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']
    
    class Meta:
        verbose_name = "Usuário"
        verbose_name_plural = "Usuários"
    
    def __str__(self):
        return self.email
    
    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"
    
    def get_short_name(self):
        return self.first_name
    
    def has_permission(self, permission):
        """Verifica se o usuário tem uma permissão específica"""
        if self.tipo_permissao == TipoPermissao.MASTER:
            return True
        elif self.tipo_permissao == TipoPermissao.ADMIN:
            return permission in ['produtos', 'clientes', 'home']
        elif self.tipo_permissao == TipoPermissao.VENDEDOR:
            return permission in ['orcamentos']
        elif self.tipo_permissao == TipoPermissao.OPERADOR_PRODUTOS:
            return permission in ['produtos']
        return False
    
    def can_access_home(self):
        """Verifica se pode acessar a página inicial"""
        return self.tipo_permissao in [TipoPermissao.MASTER, TipoPermissao.ADMIN]
    
    def can_access_produtos(self):
        """Verifica se pode acessar produtos"""
        return self.tipo_permissao in [TipoPermissao.MASTER, TipoPermissao.ADMIN, TipoPermissao.OPERADOR_PRODUTOS]
    
    def can_access_clientes(self):
        """Verifica se pode acessar clientes"""
        return self.tipo_permissao in [TipoPermissao.MASTER, TipoPermissao.ADMIN]
    
    def can_access_orcamentos(self):
        """Verifica se pode acessar orçamentos"""
        return self.tipo_permissao in [TipoPermissao.MASTER, TipoPermissao.ADMIN, TipoPermissao.VENDEDOR]
    
    def can_manage_users(self):
        """Verifica se pode gerenciar usuários"""
        return self.tipo_permissao == TipoPermissao.MASTER
