from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from decimal import Decimal
from datetime import timedelta
from django.utils import timezone
from sistema_produtos.base_models import BaseModel
from authentication.models import CustomUser
from clientes.models import Cliente
from produtos.models import Produto


class FaixaPreco(BaseModel):
    """Faixas de preço para orçamentos"""
    nome = models.CharField(max_length=100, verbose_name="Nome da Faixa")
    descricao = models.TextField(blank=True, null=True, verbose_name="Descrição")
    multiplicador = models.DecimalField(
        max_digits=5, 
        decimal_places=2, 
        default=1.00,
        verbose_name="Multiplicador",
        help_text="Multiplicador aplicado ao preço base (1.00 = 100%)"
    )
    ativo = models.BooleanField(default=True, verbose_name="Ativo")
    
    class Meta:
        verbose_name = "Faixa de Preço"
        verbose_name_plural = "Faixas de Preço"
        ordering = ['nome']
    
    def __str__(self):
        return f"{self.nome} ({self.multiplicador}x)"


class FormaPagamento(BaseModel):
    """Formas de pagamento disponíveis"""
    nome = models.CharField(max_length=100, verbose_name="Nome")
    descricao = models.TextField(blank=True, null=True, verbose_name="Descrição")
    prazo_dias = models.IntegerField(
        default=0,
        verbose_name="Prazo em dias",
        help_text="Prazo padrão em dias para esta forma de pagamento"
    )
    desconto_maximo = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0.00,
        verbose_name="Desconto Máximo (%)",
        help_text="Desconto máximo permitido para esta forma de pagamento"
    )
    ativo = models.BooleanField(default=True, verbose_name="Ativo")
    
    class Meta:
        verbose_name = "Forma de Pagamento"
        verbose_name_plural = "Formas de Pagamento"
        ordering = ['nome']
    
    def __str__(self):
        return self.nome


class Orcamento(BaseModel):
    """Orçamento principal"""
    numero = models.CharField(
        max_length=20,
        unique=True,
        verbose_name="Número do Orçamento",
        help_text="Número único do orçamento"
    )
    cliente = models.ForeignKey(
        Cliente,
        on_delete=models.PROTECT,
        verbose_name="Cliente"
    )
    vendedor = models.ForeignKey(
        CustomUser,
        on_delete=models.PROTECT,
        verbose_name="Vendedor",
        limit_choices_to={'tipo_permissao__in': ['vendedor', 'admin', 'master']}
    )
    
    # Configurações do orçamento
    faixa_preco = models.ForeignKey(
        FaixaPreco,
        on_delete=models.PROTECT,
        verbose_name="Faixa de Preço",
        null=True,
        blank=True
    )
    forma_pagamento = models.ForeignKey(
        FormaPagamento,
        on_delete=models.PROTECT,
        verbose_name="Forma de Pagamento"
    )
    
    # Valores e descontos
    desconto_valor = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0.00,
        null=True,
        blank=True,
        verbose_name="Desconto (R$)",
        help_text="Valor do desconto em reais"
    )
    desconto_percentual = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0.00,
        null=True,
        blank=True,
        verbose_name="Desconto (%)",
        help_text="Percentual de desconto"
    )
    acrescimo_valor = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0.00,
        null=True,
        blank=True,
        verbose_name="Acréscimo (R$)",
        help_text="Valor do acréscimo em reais"
    )
    acrescimo_percentual = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0.00,
        null=True,
        blank=True,
        verbose_name="Acréscimo (%)",
        help_text="Percentual de acréscimo"
    )
    
    # Datas
    data_entrega = models.DateField(
        verbose_name="Data de Entrega",
        help_text="Data prevista para entrega"
    )
    data_validade = models.DateField(
        verbose_name="Data de Validade",
        help_text="Data de validade do orçamento"
    )
    
    # Status
    STATUS_CHOICES = [
        ('rascunho', 'Rascunho'),
        ('enviado', 'Enviado'),
        ('aprovado', 'Aprovado'),
        ('rejeitado', 'Rejeitado'),
        ('expirado', 'Expirado'),
    ]
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='rascunho',
        verbose_name="Status"
    )
    
    # Observações
    observacoes = models.TextField(
        blank=True,
        null=True,
        verbose_name="Observações",
        help_text="Observações gerais do orçamento"
    )
    
    class Meta:
        verbose_name = "Orçamento"
        verbose_name_plural = "Orçamentos"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Orçamento {self.numero} - {self.cliente.nome_empresa}"
    
    def save(self, *args, **kwargs):
        # Gerar número do orçamento se não existir
        if not self.numero:
            self.numero = self.gerar_numero_orcamento()
        
        # Definir data de validade padrão (15 dias)
        if not self.data_validade:
            self.data_validade = timezone.now().date() + timedelta(days=15)
        
        # Definir data de entrega padrão (30 dias)
        if not self.data_entrega:
            self.data_entrega = timezone.now().date() + timedelta(days=30)
        
        super().save(*args, **kwargs)
    
    def gerar_numero_orcamento(self):
        """Gera número único para o orçamento"""
        hoje = timezone.now().date()
        ano = hoje.year
        mes = hoje.month
        
        # Contar orçamentos do mês atual
        ultimo_orcamento = Orcamento.objects.filter(
            created_at__year=ano,
            created_at__month=mes
        ).order_by('-id').first()
        
        if ultimo_orcamento:
            # Extrair número sequencial do último orçamento
            ultimo_numero = ultimo_orcamento.numero.split('-')[-1]
            proximo_numero = int(ultimo_numero) + 1
        else:
            proximo_numero = 1
        
        return f"ORC-{ano}{mes:02d}-{proximo_numero:04d}"
    
    def get_subtotal(self):
        """Calcula subtotal dos itens"""
        return sum(item.get_total() for item in self.itens.all())
    
    def get_total_desconto(self):
        """Calcula total de desconto"""
        from decimal import Decimal
        subtotal = self.get_subtotal()
        desconto_valor = Decimal(str(self.desconto_valor or 0))
        desconto_percentual = (subtotal * Decimal(str(self.desconto_percentual or 0)) / Decimal('100'))
        return desconto_valor + desconto_percentual
    
    def get_total_acrescimo(self):
        """Calcula total de acréscimo"""
        from decimal import Decimal
        subtotal = self.get_subtotal()
        acrescimo_valor = Decimal(str(self.acrescimo_valor or 0))
        acrescimo_percentual = (subtotal * Decimal(str(self.acrescimo_percentual or 0)) / Decimal('100'))
        return acrescimo_valor + acrescimo_percentual
    
    def get_total_final(self):
        """Calcula total final do orçamento"""
        subtotal = self.get_subtotal()
        desconto = self.get_total_desconto()
        acrescimo = self.get_total_acrescimo()
        return subtotal - desconto + acrescimo
    
    def get_peso_total(self):
        """Calcula peso total do orçamento"""
        peso_total = 0
        for item in self.itens.all():
            peso_total += item.get_peso_total()
        return peso_total
    
    def get_cubagem_total(self):
        """Calcula cubagem total do orçamento"""
        cubagem_total = 0
        for item in self.itens.all():
            cubagem_total += item.get_cubagem_total()
        return cubagem_total


class OrcamentoItem(BaseModel):
    """Item do orçamento"""
    orcamento = models.ForeignKey(
        Orcamento,
        on_delete=models.CASCADE,
        related_name='itens',
        verbose_name="Orçamento"
    )
    produto = models.ForeignKey(
        Produto,
        on_delete=models.PROTECT,
        verbose_name="Produto"
    )
    quantidade = models.PositiveIntegerField(
        default=1,
        verbose_name="Quantidade"
    )
    preco_unitario = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Preço Unitário",
        help_text="Preço unitário já com faixa de preço aplicada"
    )
    faixa_preco = models.ForeignKey(
        FaixaPreco,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        verbose_name="Faixa de Preço"
    )
    observacoes = models.TextField(
        blank=True,
        null=True,
        verbose_name="Observações",
        help_text="Observações específicas deste item"
    )
    
    # Campos para armazenar dados específicos do produto no momento do orçamento
    # (evita problemas se o produto for alterado posteriormente)
    dados_produto = models.JSONField(
        default=dict,
        blank=True,
        verbose_name="Dados do Produto",
        help_text="Dados específicos do produto (cor, tamanho, etc.)"
    )
    
    class Meta:
        verbose_name = "Item do Orçamento"
        verbose_name_plural = "Itens do Orçamento"
        ordering = ['id']
    
    def __str__(self):
        return f"{self.produto.nome_produto} - Qtd: {self.quantidade}"
    
    def get_total(self):
        """Calcula total do item"""
        return self.preco_unitario * self.quantidade
    
    def get_peso_total(self):
        """Calcula peso total do item"""
        # Buscar peso nos dados específicos do produto
        peso_unitario = self.get_peso_unitario()
        return peso_unitario * self.quantidade if peso_unitario else 0
    
    def get_cubagem_total(self):
        """Calcula cubagem total do item"""
        # Buscar cubagem nos dados específicos do produto
        cubagem_unitaria = self.get_cubagem_unitaria()
        return cubagem_unitaria * self.quantidade if cubagem_unitaria else 0
    
    def get_peso_unitario(self):
        """Retorna peso unitário do produto"""
        # Implementar lógica para buscar peso baseado no tipo de produto
        # Por enquanto retorna 0, mas pode ser expandido
        return 0
    
    def get_cubagem_unitaria(self):
        """Retorna cubagem unitária do produto"""
        # Implementar lógica para buscar cubagem baseada no tipo de produto
        # Por enquanto retorna 0, mas pode ser expandido
        return 0


class OrcamentoModulo(BaseModel):
    """Módulos de sofá em um orçamento"""
    item_orcamento = models.ForeignKey(
        OrcamentoItem,
        on_delete=models.CASCADE,
        related_name='modulos',
        verbose_name="Item do Orçamento"
    )
    modulo_id = models.PositiveIntegerField(
        verbose_name="ID do Módulo",
        help_text="ID do módulo original do produto"
    )
    nome_modulo = models.CharField(
        max_length=200,
        verbose_name="Nome do Módulo"
    )
    tamanho_selecionado = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name="Tamanho Selecionado"
    )
    tamanho_id = models.PositiveIntegerField(
        blank=True,
        null=True,
        verbose_name="ID do Tamanho",
        help_text="ID do tamanho detalhado selecionado"
    )
    quantidade = models.PositiveIntegerField(
        default=1,
        verbose_name="Quantidade"
    )
    observacoes = models.TextField(
        blank=True,
        null=True,
        max_length=1000,
        verbose_name="Observações",
        help_text="Observações específicas deste módulo"
    )
    
    class Meta:
        verbose_name = "Módulo do Orçamento"
        verbose_name_plural = "Módulos do Orçamento"
        ordering = ['id']
    
    def __str__(self):
        return f"{self.nome_modulo} - {self.tamanho_selecionado} (Qtd: {self.quantidade})"
