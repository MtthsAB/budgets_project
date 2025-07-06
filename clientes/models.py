from django.db import models
from django.core.validators import RegexValidator
from sistema_produtos.base_models import BaseModel


class Cliente(BaseModel):
    # Dados da empresa
    nome_empresa = models.CharField(
        max_length=200,
        verbose_name="Nome da Empresa",
        help_text="Razão social ou nome fantasia da empresa"
    )
    representante = models.CharField(
        max_length=150,
        verbose_name="Representante",
        help_text="Nome do representante da empresa"
    )
    
    # Dados legais
    cnpj = models.CharField(
        max_length=18,
        unique=True,
        verbose_name="CNPJ",
        validators=[
            RegexValidator(
                regex=r'^\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2}$',
                message='CNPJ deve estar no formato 00.000.000/0000-00'
            )
        ],
        help_text="CNPJ no formato 00.000.000/0000-00"
    )
    inscricao_estadual = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        verbose_name="Inscrição Estadual"
    )
    inscricao_municipal = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        verbose_name="Inscrição Municipal"
    )
    
    # Endereço
    logradouro = models.CharField(
        max_length=200,
        verbose_name="Logradouro",
        help_text="Rua, avenida, praça, etc."
    )
    numero = models.CharField(
        max_length=10,
        verbose_name="Número"
    )
    complemento = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name="Complemento",
        help_text="Apartamento, sala, andar, etc."
    )
    bairro = models.CharField(
        max_length=100,
        verbose_name="Bairro"
    )
    cidade = models.CharField(
        max_length=100,
        verbose_name="Cidade"
    )
    estado = models.CharField(
        max_length=2,
        verbose_name="Estado",
        help_text="UF do estado (ex: SP, RJ, MG)"
    )
    cep = models.CharField(
        max_length=9,
        verbose_name="CEP",
        validators=[
            RegexValidator(
                regex=r'^\d{5}-\d{3}$',
                message='CEP deve estar no formato 00000-000'
            )
        ],
        help_text="CEP no formato 00000-000"
    )
    
    # Contato
    telefone = models.CharField(
        max_length=20,
        verbose_name="Telefone",
        help_text="Telefone com DDD"
    )
    email = models.EmailField(
        verbose_name="E-mail",
        help_text="E-mail principal da empresa"
    )
    
    # Dados bancários (opcionais)
    banco = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name="Banco",
        help_text="Nome do banco"
    )
    agencia = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        verbose_name="Agência",
        help_text="Número da agência"
    )
    conta_corrente = models.CharField(
        max_length=30,
        blank=True,
        null=True,
        verbose_name="Conta Corrente",
        help_text="Número da conta corrente"
    )
    
    class Meta:
        verbose_name = "Cliente"
        verbose_name_plural = "Clientes"
        ordering = ['nome_empresa']
        
    def __str__(self):
        return f"{self.nome_empresa} - {self.cnpj}"
        
    def get_endereco_completo(self):
        """Retorna o endereço completo formatado"""
        endereco = f"{self.logradouro}, {self.numero}"
        if self.complemento:
            endereco += f", {self.complemento}"
        endereco += f" - {self.bairro}, {self.cidade}/{self.estado} - CEP: {self.cep}"
        return endereco
