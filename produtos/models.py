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
    """Produto principal do sistema - inclui sofás, acessórios e outros tipos"""
    ref_produto = models.CharField(max_length=50, unique=True, verbose_name="Referência do Produto")
    nome_produto = models.CharField(max_length=200, verbose_name="Nome do Produto")
    id_tipo_produto = models.ForeignKey(
        TipoItem, 
        on_delete=models.PROTECT, 
        verbose_name="Tipo de Produto"
    )
    ativo = models.BooleanField(default=True, verbose_name="Ativo")
    
    # Campos específicos para sofás e similares
    tem_cor_tecido = models.BooleanField(default=False, verbose_name="Tem Cor Tecido")
    tem_difer_desenho_lado_dir_esq = models.BooleanField(
        default=False, 
        verbose_name="Diferencia Desenho Lado Direito/Esquerdo"
    )
    tem_difer_desenho_tamanho = models.BooleanField(
        default=False, 
        verbose_name="Diferencia Desenho por Tamanho"
    )
    
    # Campos específicos para acessórios
    preco_acessorio = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        verbose_name="Preço do Acessório (R$)",
        blank=True,
        null=True,
        help_text="Apenas para produtos do tipo acessório"
    )
    descricao_acessorio = models.TextField(
        blank=True, 
        null=True, 
        verbose_name="Descrição do Acessório",
        help_text="Apenas para produtos do tipo acessório"
    )
    
    # Imagens
    imagem_principal = models.ImageField(
        upload_to='produtos/itens/',
        blank=True,
        null=True,
        verbose_name="Imagem Principal"
    )
    imagem_secundaria = models.ImageField(
        upload_to='produtos/itens/',
        blank=True,
        null=True,
        verbose_name="Imagem Secundária"
    )
    
    # Vinculação para acessórios (ManyToMany para si mesmo)
    produtos_vinculados = models.ManyToManyField(
        'self',
        blank=True,
        symmetrical=False,
        verbose_name="Produtos Vinculados",
        help_text="Para acessórios: produtos aos quais este acessório pode ser vinculado"
    )
    
    class Meta:
        verbose_name = "Item"
        verbose_name_plural = "Itens"
        ordering = ['ref_produto']
    
    def __str__(self):
        return f"{self.ref_produto} - {self.nome_produto}"
    
    def eh_acessorio(self):
        """Verifica se o item é um acessório"""
        return self.id_tipo_produto.nome.lower() == 'acessórios'
    
    def clean(self):
        """Validações customizadas do modelo"""
        super().clean()
        
        if self.eh_acessorio():
            # Para acessórios, forçar valores False nos campos específicos de sofás
            self.tem_cor_tecido = False
            self.tem_difer_desenho_lado_dir_esq = False
            self.tem_difer_desenho_tamanho = False
        else:
            # Para não-acessórios, limpar campos específicos de acessórios
            self.preco_acessorio = None
            self.descricao_acessorio = None
            # Limpar vinculações também
            if self.pk:
                self.produtos_vinculados.clear()

class Acessorio(BaseModel):
    """Acessórios disponíveis"""
    ref_acessorio = models.CharField(max_length=50, unique=True, verbose_name="Referência do Acessório")
    nome = models.CharField(max_length=100, verbose_name="Nome do Acessório")
    ativo = models.BooleanField(default=True, verbose_name="Ativo")
    preco = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        verbose_name="Preço (R$)",
        blank=True,
        null=True
    )
    imagem_principal = models.ImageField(
        upload_to='produtos/acessorios/',
        blank=True,
        null=True,
        verbose_name="Imagem Principal"
    )
    imagem_secundaria = models.ImageField(
        upload_to='produtos/acessorios/',
        blank=True,
        null=True,
        verbose_name="Imagem Adicional"
    )
    produtos_vinculados = models.ManyToManyField(
        'Item',
        blank=True,
        verbose_name="Produtos Vinculados",
        help_text="Produtos aos quais este acessório pode ser vinculado"
    )
    descricao = models.TextField(blank=True, null=True, verbose_name="Descrição")
    
    class Meta:
        verbose_name = "Acessório"
        verbose_name_plural = "Acessórios"
        ordering = ['ref_acessorio']
    
    def __str__(self):
        if self.ref_acessorio:
            return f"{self.ref_acessorio} - {self.nome}"
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
