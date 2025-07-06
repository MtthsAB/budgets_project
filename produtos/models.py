from django.db import models
from sistema_produtos.base_models import BaseModel

class TipoItem(BaseModel):
    """Tipos de produto: sofás, acessórios, cadeiras, banquetas, poltronas, pufes, almofadas"""
    nome = models.CharField(max_length=100, verbose_name="Nome do Tipo")
    
    class Meta:
        verbose_name = "Tipo de Item"
        verbose_name_plural = "Tipos de Item"
        ordering = ['nome']
    
    def __str__(self):
        return self.nome

class Linha(BaseModel):
    """Linha de produtos"""
    nome = models.CharField(max_length=100, verbose_name="Nome da Linha")
    descricao = models.TextField(blank=True, null=True, verbose_name="Descrição")
    
    class Meta:
        verbose_name = "Linha"
        verbose_name_plural = "Linhas"
        ordering = ['nome']
    
    def __str__(self):
        return self.nome

class Item(BaseModel):
    """Produto principal do sistema"""
    ref_produto = models.CharField(max_length=50, unique=True, verbose_name="Referência do Produto")
    nome_produto = models.CharField(max_length=200, verbose_name="Nome do Produto")
    id_tipo_produto = models.ForeignKey(
        TipoItem, 
        on_delete=models.PROTECT, 
        verbose_name="Tipo de Produto"
    )
    ativo = models.BooleanField(default=True, verbose_name="Ativo")
    tem_cor_tecido = models.BooleanField(default=False, verbose_name="Tem Cor Tecido")
    tem_difer_desenho_lado_dir_esq = models.BooleanField(
        default=False, 
        verbose_name="Diferencia Desenho Lado Direito/Esquerdo"
    )
    tem_difer_desenho_tamanho = models.BooleanField(
        default=False, 
        verbose_name="Diferencia Desenho por Tamanho"
    )
    imagem_principal = models.ImageField(
        upload_to='produtos/itens/',
        blank=True,
        null=True,
        verbose_name="Imagem Principal"
    )
    
    class Meta:
        verbose_name = "Item"
        verbose_name_plural = "Itens"
        ordering = ['ref_produto']
    
    def __str__(self):
        return f"{self.ref_produto} - {self.nome_produto}"

class Acessorio(BaseModel):
    """Acessórios disponíveis"""
    nome = models.CharField(max_length=100, verbose_name="Nome do Acessório")
    descricao = models.TextField(blank=True, null=True, verbose_name="Descrição")
    
    class Meta:
        verbose_name = "Acessório"
        verbose_name_plural = "Acessórios"
        ordering = ['nome']
    
    def __str__(self):
        return self.nome

class Modulo(BaseModel):
    """Módulos dos produtos"""
    item = models.ForeignKey(
        Item, 
        on_delete=models.CASCADE, 
        related_name='modulos',
        verbose_name="Item"
    )
    nome = models.CharField(max_length=100, verbose_name="Nome do Módulo")
    profundidade = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        verbose_name="Profundidade (cm)",
        blank=True,
        null=True
    )
    altura = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        verbose_name="Altura (cm)",
        blank=True,
        null=True
    )
    braco = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        verbose_name="Braço (cm)",
        blank=True,
        null=True
    )
    descricao = models.TextField(
        blank=True, 
        null=True, 
        verbose_name="Descrição"
    )
    imagem_principal = models.ImageField(
        upload_to='produtos/modulos/',
        blank=True,
        null=True,
        verbose_name="Imagem Principal"
    )
    
    class Meta:
        verbose_name = "Módulo"
        verbose_name_plural = "Módulos"
        ordering = ['item', 'nome']
    
    def __str__(self):
        return f"{self.item.ref_produto} - {self.nome}"

class TamanhosModulos(BaseModel):
    """Tamanhos dos módulos"""
    id_modulo = models.ForeignKey(
        Modulo, 
        on_delete=models.CASCADE, 
        verbose_name="Módulo"
    )
    tamanho = models.CharField(max_length=50, verbose_name="Tamanho")
    
    class Meta:
        verbose_name = "Tamanho do Módulo"
        verbose_name_plural = "Tamanhos dos Módulos"
        unique_together = ['id_modulo', 'tamanho']
    
    def __str__(self):
        return f"{self.id_modulo.nome} - {self.tamanho}"

class TamanhosModulosDetalhado(BaseModel):
    """Tamanhos dos módulos com todas as informações específicas"""
    id_modulo = models.ForeignKey(
        Modulo, 
        on_delete=models.CASCADE, 
        related_name='tamanhos_detalhados',
        verbose_name="Módulo"
    )
    largura_total = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        verbose_name="Largura Total (cm)",
        blank=True,
        null=True
    )
    largura_assento = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        verbose_name="Largura do Assento (cm)",
        blank=True,
        null=True
    )
    tecido_metros = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        verbose_name="Tecido (metros)",
        blank=True,
        null=True
    )
    volume_m3 = models.DecimalField(
        max_digits=10, 
        decimal_places=3, 
        verbose_name="Volume (m³)",
        blank=True,
        null=True
    )
    peso_kg = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        verbose_name="Peso (kg)",
        blank=True,
        null=True
    )
    preco = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        verbose_name="Preço (R$)",
        blank=True,
        null=True
    )
    descricao = models.TextField(
        blank=True, 
        null=True, 
        verbose_name="Descrição do Tamanho"
    )
    
    class Meta:
        verbose_name = "Tamanho Detalhado do Módulo"
        verbose_name_plural = "Tamanhos Detalhados dos Módulos"
    
    def __str__(self):
        dimensoes = []
        if self.largura_total:
            dimensoes.append(f"L:{self.largura_total}")
        
        dimensoes_str = f" ({' x '.join(dimensoes)}cm)" if dimensoes else ""
        preco_str = f" - R${self.preco}" if self.preco else ""
        return f"{self.id_modulo.nome} - Tamanho ID:{self.id}{dimensoes_str}{preco_str}"

class FaixaTecido(BaseModel):
    """Faixas de tecido para preços"""
    nome = models.CharField(max_length=100, verbose_name="Nome da Faixa")
    valor_minimo = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        verbose_name="Valor Mínimo"
    )
    valor_maximo = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        verbose_name="Valor Máximo"
    )
    
    class Meta:
        verbose_name = "Faixa de Tecido"
        verbose_name_plural = "Faixas de Tecido"
        ordering = ['valor_minimo']
    
    def __str__(self):
        return f"{self.nome} ({self.valor_minimo} - {self.valor_maximo})"

class PrecosBase(BaseModel):
    """Preços base dos itens por faixa de tecido"""
    id_item = models.ForeignKey(
        Item, 
        on_delete=models.CASCADE, 
        verbose_name="Item"
    )
    id_faixa_tecido = models.ForeignKey(
        FaixaTecido, 
        on_delete=models.CASCADE, 
        verbose_name="Faixa de Tecido"
    )
    data_inic_vigencia = models.DateField(verbose_name="Data Início Vigência")
    preco_base = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        verbose_name="Preço Base"
    )
    
    class Meta:
        verbose_name = "Preço Base"
        verbose_name_plural = "Preços Base"
        ordering = ['-data_inic_vigencia']
    
    def __str__(self):
        return f"{self.id_item.ref_produto} - {self.id_faixa_tecido.nome} - R$ {self.preco_base}"
