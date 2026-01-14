from django.db import models
from django.core.exceptions import ValidationError
from sistema_produtos.base_models import BaseModel

class TipoItem(BaseModel):
    """Tipos de produto: sofás, acessórios, cadeiras, banquetas, poltronas, pufes, almofadas"""
    nome = models.CharField(max_length=100, verbose_name="Nome do Tipo")
    
    class Meta:
        verbose_name = "Tipo de Produto"
        verbose_name_plural = "Tipos de Produtos"
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

class Produto(BaseModel):
    """Produto base do sistema - informações básicas e campos específicos para sofás"""
    ref_produto = models.CharField(max_length=50, unique=True, verbose_name="Referência do Produto")
    nome_produto = models.CharField(max_length=200, verbose_name="Nome do Produto")
    id_tipo_produto = models.ForeignKey(
        TipoItem, 
        on_delete=models.PROTECT, 
        verbose_name="Tipo de Produto"
    )
    ativo = models.BooleanField(default=True, verbose_name="Ativo")
    
    # Imagens básicas
    imagem_principal = models.ImageField(
        upload_to='produtos/',
        blank=True,
        null=True,
        verbose_name="Imagem Principal"
    )
    imagem_secundaria = models.ImageField(
        upload_to='produtos/',
        blank=True,
        null=True,
        verbose_name="Imagem Secundária"
    )
    
    # Campos específicos para sofás (opcionais para outros tipos)
    tem_cor_tecido = models.BooleanField(
        default=False, 
        verbose_name="Tem Cor Tecido",
        help_text="Apenas para sofás e produtos similares"
    )
    tem_difer_desenho_lado_dir_esq = models.BooleanField(
        default=False, 
        verbose_name="Diferencia Desenho Lado Direito/Esquerdo",
        help_text="Apenas para sofás e produtos similares"
    )
    tem_difer_desenho_tamanho = models.BooleanField(
        default=False, 
        verbose_name="Diferencia Desenho por Tamanho",
        help_text="Apenas para sofás e produtos similares"
    )
    
    class Meta:
        verbose_name = "Sofá"
        verbose_name_plural = "Sofás"
        ordering = ['ref_produto']
        db_table = 'produtos_produto'  # Define o nome da tabela
    
    def __str__(self):
        return f"[{self.id_tipo_produto.nome}] {self.ref_produto} - {self.nome_produto}"
    
    def eh_sofa(self):
        """Verifica se o produto é um sofá"""
        return self.id_tipo_produto.nome.lower() in ['sofá', 'sofas', 'sofa', 'sofás']
    
    def clean(self):
        """Validações customizadas do modelo"""
        super().clean()
        
        # Para produtos que não são sofás, forçar valores False nos campos específicos
        if not self.eh_sofa():
            self.tem_cor_tecido = False
            self.tem_difer_desenho_lado_dir_esq = False
            self.tem_difer_desenho_tamanho = False


# Classe Item mantida temporariamente para compatibilidade
# TODO: Remover após migração completa para Produto
class Item(BaseModel):
    """DEPRECATED: Use Produto em vez desta classe. Mantida apenas para compatibilidade."""
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
        verbose_name = "Item (Deprecated)"
        verbose_name_plural = "Itens (Deprecated)"
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
        'Produto',
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
    """Módulos dos produtos (apenas para sofás)"""
    produto = models.ForeignKey(
        Produto, 
        on_delete=models.CASCADE, 
        related_name='modulos',
        verbose_name="Produto"
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
    imagem_secundaria = models.ImageField(
        upload_to='produtos/modulos/',
        blank=True,
        null=True,
        verbose_name="Imagem Secundária"
    )
    
    class Meta:
        verbose_name = "Módulo"
        verbose_name_plural = "Módulos"
        ordering = ['produto', 'nome']
    
    def __str__(self):
        return f"{self.produto.ref_produto} - {self.nome}"

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

class Banqueta(BaseModel):
    """Modelo específico para Banquetas"""
    ref_banqueta = models.CharField(
        max_length=50, 
        unique=True, 
        verbose_name="Referência da Banqueta",
        help_text="Ex: BQ13, BQ249, etc."
    )
    nome = models.CharField(
        max_length=100, 
        verbose_name="Nome da Banqueta",
        help_text="Ex: CERES, GIO, etc."
    )
    
    # Dimensões separadas como solicitado
    largura = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        verbose_name="Largura (cm)",
        help_text="Largura em centímetros"
    )
    profundidade = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        verbose_name="Profundidade (cm)",
        help_text="Profundidade em centímetros"
    )
    altura = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        verbose_name="Altura (cm)",
        help_text="Altura em centímetros"
    )
    
    # Especificações técnicas
    tecido_metros = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        verbose_name="Tecido (m)",
        help_text="Quantidade de tecido necessária em metros"
    )
    volume_m3 = models.DecimalField(
        max_digits=10, 
        decimal_places=3, 
        verbose_name="Volume (m³)",
        help_text="Volume para cálculo de frete em metros cúbicos"
    )
    peso_kg = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        verbose_name="Peso (kg)",
        help_text="Peso para cálculo de frete em quilogramas"
    )
    preco = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        verbose_name="Preço (R$)",
        help_text="Preço em reais"
    )
    
    # Status e imagens
    ativo = models.BooleanField(default=True, verbose_name="Ativo")
    imagem_principal = models.ImageField(
        upload_to='produtos/banquetas/',
        blank=True,
        null=True,
        verbose_name="Imagem Principal"
    )
    imagem_secundaria = models.ImageField(
        upload_to='produtos/banquetas/',
        blank=True,
        null=True,
        verbose_name="Imagem Secundária"
    )
    descricao = models.TextField(
        blank=True, 
        null=True, 
        verbose_name="Descrição"
    )
    
    class Meta:
        verbose_name = "Banqueta"
        verbose_name_plural = "Banquetas"
        ordering = ['ref_banqueta']
    
    def __str__(self):
        return f"{self.ref_banqueta} - {self.nome}"
    
    def get_dimensoes_formatadas(self):
        """Retorna as dimensões formatadas como L x P x A"""
        return f"{self.largura} x {self.profundidade} x {self.altura}"
    
    def clean(self):
        """Validações customizadas do modelo"""
        super().clean()
        
        # Validar se as dimensões são positivas
        if self.largura and self.largura <= 0:
            raise ValidationError("A largura deve ser maior que zero.")
        if self.profundidade and self.profundidade <= 0:
            raise ValidationError("A profundidade deve ser maior que zero.")
        if self.altura and self.altura <= 0:
            raise ValidationError("A altura deve ser maior que zero.")
        
        # Validar valores monetários e quantidades
        if self.tecido_metros and self.tecido_metros <= 0:
            raise ValidationError("A quantidade de tecido deve ser maior que zero.")
        if self.volume_m3 and self.volume_m3 <= 0:
            raise ValidationError("O volume deve ser maior que zero.")
        if self.peso_kg and self.peso_kg <= 0:
            raise ValidationError("O peso deve ser maior que zero.")
        if self.preco and self.preco <= 0:
            raise ValidationError("O preço deve ser maior que zero.")

class Cadeira(BaseModel):
    """Modelo específico para Cadeiras"""
    ref_cadeira = models.CharField(
        max_length=50, 
        unique=True, 
        verbose_name="Referência da Cadeira",
        help_text="Ex: CD001, CD24, CD267, etc."
    )
    nome = models.CharField(
        max_length=100, 
        verbose_name="Nome da Cadeira",
        help_text="Ex: EVA, EVA BR, FIT, etc."
    )
    
    # Dimensões separadas como solicitado
    largura = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        verbose_name="Largura (cm)",
        help_text="Largura em centímetros"
    )
    profundidade = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        verbose_name="Profundidade (cm)",
        help_text="Profundidade em centímetros"
    )
    altura = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        verbose_name="Altura (cm)",
        help_text="Altura em centímetros"
    )
    
    # Especificações técnicas
    tecido_metros = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        verbose_name="Tecido (m)",
        help_text="Quantidade de tecido necessária em metros"
    )
    volume_m3 = models.DecimalField(
        max_digits=10, 
        decimal_places=3, 
        verbose_name="Volume (m³)",
        help_text="Volume para cálculo de frete em metros cúbicos"
    )
    peso_kg = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        verbose_name="Peso (kg)",
        help_text="Peso para cálculo de frete em quilogramas"
    )
    preco = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        verbose_name="Preço (R$)",
        help_text="Preço em reais"
    )
    
    # Status e imagens
    ativo = models.BooleanField(default=True, verbose_name="Ativo")
    tem_cor_tecido = models.BooleanField(
        default=False, 
        verbose_name="Tem Cor Tecido",
        help_text="Indica se a cadeira utiliza diferentes cores de tecido"
    )
    imagem_principal = models.ImageField(
        upload_to='produtos/cadeiras/',
        blank=True,
        null=True,
        verbose_name="Imagem Principal"
    )
    imagem_secundaria = models.ImageField(
        upload_to='produtos/cadeiras/',
        blank=True,
        null=True,
        verbose_name="Imagem Secundária"
    )
    descricao = models.TextField(
        blank=True, 
        null=True, 
        verbose_name="Descrição"
    )
    
    class Meta:
        verbose_name = "Cadeira"
        verbose_name_plural = "Cadeiras"
        ordering = ['ref_cadeira']

    def clean(self):
        if self.largura and self.largura <= 0:
            raise ValidationError({'largura': 'Largura deve ser maior que zero'})
        if self.profundidade and self.profundidade <= 0:
            raise ValidationError({'profundidade': 'Profundidade deve ser maior que zero'})
        if self.altura and self.altura <= 0:
            raise ValidationError({'altura': 'Altura deve ser maior que zero'})
        if self.tecido_metros and self.tecido_metros <= 0:
            raise ValidationError({'tecido_metros': 'Quantidade de tecido deve ser maior que zero'})
        if self.volume_m3 and self.volume_m3 <= 0:
            raise ValidationError({'volume_m3': 'Volume deve ser maior que zero'})
        if self.peso_kg and self.peso_kg <= 0:
            raise ValidationError({'peso_kg': 'Peso deve ser maior que zero'})
        if self.preco and self.preco <= 0:
            raise ValidationError({'preco': 'Preço deve ser maior que zero'})

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def get_dimensoes_formatadas(self):
        """Retorna as dimensões formatadas como string"""
        return f"{self.largura}×{self.profundidade}×{self.altura} cm"

    def __str__(self):
        return f"{self.ref_cadeira} - {self.nome}"


class Poltrona(BaseModel):
    """Modelo específico para Poltronas"""
    ref_poltrona = models.CharField(
        max_length=50, 
        unique=True, 
        verbose_name="Referência da Poltrona",
        help_text="Ex: PL243, PL246, PL105, etc."
    )
    nome = models.CharField(
        max_length=100, 
        verbose_name="Nome da Poltrona",
        help_text="Ex: ARIA, ARISTOCRATA, CERNE, etc."
    )
    
    # Dimensões separadas como solicitado
    largura = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        verbose_name="Largura (cm)",
        help_text="Largura em centímetros"
    )
    profundidade = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        verbose_name="Profundidade (cm)",
        help_text="Profundidade em centímetros"
    )
    altura = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        verbose_name="Altura (cm)",
        help_text="Altura em centímetros"
    )
    
    # Especificações técnicas
    tecido_metros = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        verbose_name="Tecido (m)",
        help_text="Quantidade de tecido necessária em metros"
    )
    volume_m3 = models.DecimalField(
        max_digits=10, 
        decimal_places=3, 
        verbose_name="Volume (m³)",
        help_text="Volume para cálculo de frete em metros cúbicos"
    )
    peso_kg = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        verbose_name="Peso (kg)",
        help_text="Peso para cálculo de frete em quilogramas"
    )
    preco = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        verbose_name="Preço (R$)",
        help_text="Preço em reais"
    )
    
    # Status e imagens
    ativo = models.BooleanField(default=True, verbose_name="Ativo")
    tem_cor_tecido = models.BooleanField(
        default=False, 
        verbose_name="Tem Cor Tecido",
        help_text="Indica se a poltrona utiliza diferentes cores de tecido"
    )
    imagem_principal = models.ImageField(
        upload_to='produtos/poltronas/',
        blank=True,
        null=True,
        verbose_name="Imagem Principal"
    )
    imagem_secundaria = models.ImageField(
        upload_to='produtos/poltronas/',
        blank=True,
        null=True,
        verbose_name="Imagem Secundária"
    )
    descricao = models.TextField(
        blank=True, 
        null=True, 
        verbose_name="Descrição"
    )
    
    class Meta:
        verbose_name = "Poltrona"
        verbose_name_plural = "Poltronas"
        ordering = ['ref_poltrona']

    def clean(self):
        if self.largura and self.largura <= 0:
            raise ValidationError({'largura': 'Largura deve ser maior que zero'})
        if self.profundidade and self.profundidade <= 0:
            raise ValidationError({'profundidade': 'Profundidade deve ser maior que zero'})
        if self.altura and self.altura <= 0:
            raise ValidationError({'altura': 'Altura deve ser maior que zero'})
        if self.tecido_metros and self.tecido_metros <= 0:
            raise ValidationError({'tecido_metros': 'Quantidade de tecido deve ser maior que zero'})
        if self.volume_m3 and self.volume_m3 <= 0:
            raise ValidationError({'volume_m3': 'Volume deve ser maior que zero'})
        if self.peso_kg and self.peso_kg <= 0:
            raise ValidationError({'peso_kg': 'Peso deve ser maior que zero'})
        if self.preco and self.preco <= 0:
            raise ValidationError({'preco': 'Preço deve ser maior que zero'})

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def get_dimensoes_formatadas(self):
        """Retorna as dimensões formatadas como string"""
        return f"{self.largura}×{self.profundidade}×{self.altura} cm"

    def __str__(self):
        return f"{self.ref_poltrona} - {self.nome}"

class Pufe(BaseModel):
    """Modelo específico para Pufes - mesmo padrão de Banquetas"""
    ref_pufe = models.CharField(
        max_length=50, 
        unique=True, 
        verbose_name="Referência do Pufe",
        help_text="Ex: PF13, PF249, etc."
    )
    nome = models.CharField(
        max_length=100, 
        verbose_name="Nome do Pufe",
        help_text="Ex: ROUND, SQUARE, CLASSIC, etc."
    )
    
    # Dimensões separadas como solicitado
    largura = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        verbose_name="Largura (cm)",
        help_text="Largura em centímetros"
    )
    profundidade = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        verbose_name="Profundidade (cm)",
        help_text="Profundidade em centímetros"
    )
    altura = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        verbose_name="Altura (cm)",
        help_text="Altura em centímetros"
    )
    
    # Especificações técnicas
    tecido_metros = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        verbose_name="Tecido (m)",
        help_text="Quantidade de tecido necessária em metros"
    )
    volume_m3 = models.DecimalField(
        max_digits=10, 
        decimal_places=3, 
        verbose_name="Volume (m³)",
        help_text="Volume para cálculo de frete em metros cúbicos"
    )
    peso_kg = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        verbose_name="Peso (kg)",
        help_text="Peso para cálculo de frete em quilogramas"
    )
    preco = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        verbose_name="Preço (R$)",
        help_text="Preço em reais"
    )
    
    # Status e imagens
    ativo = models.BooleanField(default=True, verbose_name="Ativo")
    imagem_principal = models.ImageField(
        upload_to='produtos/pufes/',
        blank=True,
        null=True,
        verbose_name="Imagem Principal"
    )
    imagem_secundaria = models.ImageField(
        upload_to='produtos/pufes/',
        blank=True,
        null=True,
        verbose_name="Imagem Secundária"
    )
    descricao = models.TextField(
        blank=True, 
        null=True, 
        verbose_name="Descrição"
    )
    
    class Meta:
        verbose_name = "Pufe"
        verbose_name_plural = "Pufes"
        ordering = ['ref_pufe']
    
    def __str__(self):
        return f"{self.ref_pufe} - {self.nome}"
    
    def get_dimensoes_formatadas(self):
        """Retorna as dimensões formatadas como L x P x A"""
        return f"{self.largura} x {self.profundidade} x {self.altura}"
    
    def clean(self):
        """Validações customizadas do modelo"""
        super().clean()
        
        # Validar se as dimensões são positivas
        if self.largura and self.largura <= 0:
            raise ValidationError("A largura deve ser maior que zero.")
        if self.profundidade and self.profundidade <= 0:
            raise ValidationError("A profundidade deve ser maior que zero.")
        if self.altura and self.altura <= 0:
            raise ValidationError("A altura deve ser maior que zero.")
        
        # Validar valores monetários e quantidades
        if self.tecido_metros and self.tecido_metros <= 0:
            raise ValidationError("A quantidade de tecido deve ser maior que zero.")
        if self.volume_m3 and self.volume_m3 <= 0:
            raise ValidationError("O volume deve ser maior que zero.")
        if self.peso_kg and self.peso_kg <= 0:
            raise ValidationError("O peso deve ser maior que zero.")
        if self.preco and self.preco <= 0:
            raise ValidationError("O preço deve ser maior que zero.")

class Almofada(BaseModel):
    """Modelo específico para Almofadas - só tem largura e altura (sem profundidade)"""
    ref_almofada = models.CharField(
        max_length=50, 
        unique=True, 
        verbose_name="Referência da Almofada",
        help_text="Ex: AL001, AL250, etc."
    )
    nome = models.CharField(
        max_length=100, 
        verbose_name="Nome da Almofada",
        help_text="Ex: DECORATIVA, LOMBAR, CERVICAL, etc."
    )
    
    # Dimensões - apenas largura e altura para almofadas
    largura = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        verbose_name="Largura (cm)",
        help_text="Largura em centímetros"
    )
    altura = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        verbose_name="Altura (cm)",
        help_text="Altura em centímetros"
    )
    
    # Especificações técnicas
    tecido_metros = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        verbose_name="Tecido (m)",
        help_text="Quantidade de tecido necessária em metros"
    )
    volume_m3 = models.DecimalField(
        max_digits=10, 
        decimal_places=3, 
        verbose_name="Volume (m³)",
        help_text="Volume para cálculo de frete em metros cúbicos"
    )
    peso_kg = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        verbose_name="Peso (kg)",
        help_text="Peso para cálculo de frete em quilogramas"
    )
    preco = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        verbose_name="Preço (R$)",
        help_text="Preço em reais"
    )
    
    # Status e imagens
    ativo = models.BooleanField(default=True, verbose_name="Ativo")
    imagem_principal = models.ImageField(
        upload_to='produtos/almofadas/',
        blank=True,
        null=True,
        verbose_name="Imagem Principal"
    )
    imagem_secundaria = models.ImageField(
        upload_to='produtos/almofadas/',
        blank=True,
        null=True,
        verbose_name="Imagem Secundária"
    )
    descricao = models.TextField(
        blank=True, 
        null=True, 
        verbose_name="Descrição"
    )
    
    class Meta:
        verbose_name = "Almofada"
        verbose_name_plural = "Almofadas"
        ordering = ['ref_almofada']
    
    def __str__(self):
        return f"{self.ref_almofada} - {self.nome}"
    
    def get_dimensoes_formatadas(self):
        """Retorna as dimensões formatadas como L x A (sem profundidade)"""
        return f"{self.largura} x {self.altura}"
    
    def clean(self):
        """Validações customizadas do modelo"""
        super().clean()
        
        # Validar se as dimensões são positivas
        if self.largura and self.largura <= 0:
            raise ValidationError("A largura deve ser maior que zero.")
        if self.altura and self.altura <= 0:
            raise ValidationError("A altura deve ser maior que zero.")
        
        # Validar valores monetários e quantidades
        if self.tecido_metros and self.tecido_metros <= 0:
            raise ValidationError("A quantidade de tecido deve ser maior que zero.")
        if self.volume_m3 and self.volume_m3 <= 0:
            raise ValidationError("O volume deve ser maior que zero.")
        if self.peso_kg and self.peso_kg <= 0:
            raise ValidationError("O peso deve ser maior que zero.")
        if self.preco and self.preco <= 0:
            raise ValidationError("O preço deve ser maior que zero.")


class SofaAcessorio(BaseModel):
    """Relação Many-to-Many entre Sofás e Acessórios com campos adicionais"""
    sofa = models.ForeignKey(
        Produto,
        on_delete=models.CASCADE,
        verbose_name="Sofá",
        help_text="Sofá ao qual o acessório está vinculado"
    )
    acessorio = models.ForeignKey(
        Acessorio,
        on_delete=models.CASCADE,
        verbose_name="Acessório",
        help_text="Acessório vinculado ao sofá"
    )
    quantidade = models.PositiveIntegerField(
        default=1,
        verbose_name="Quantidade",
        help_text="Quantidade do acessório para este sofá"
    )
    observacoes = models.TextField(
        blank=True,
        null=True,
        max_length=1000,
        verbose_name="Observações",
        help_text="Observações específicas sobre este acessório para este sofá"
    )

    class Meta:
        verbose_name = "Sofá - Acessório"
        verbose_name_plural = "Sofás - Acessórios"
        unique_together = ('sofa', 'acessorio')  # Evitar duplicação
        ordering = ['sofa__ref_produto', 'acessorio__ref_acessorio']

    def __str__(self):
        return f"{self.sofa.ref_produto} + {self.acessorio.ref_acessorio} (Qtd: {self.quantidade})"

    def clean(self):
        """Validações customizadas"""
        super().clean()
        
        # Validar se o produto é realmente um sofá
        if self.sofa and not self.sofa.eh_sofa():
            raise ValidationError("O produto selecionado não é um sofá.")
        
        # Validar se o acessório está ativo
        if self.acessorio and not self.acessorio.ativo:
            raise ValidationError("Não é possível vincular um acessório inativo.")
        
        # Validar quantidade
        if self.quantidade and self.quantidade <= 0:
            raise ValidationError("A quantidade deve ser maior que zero.")
        
        # Validar tamanho das observações
        if self.observacoes and len(self.observacoes) > 1000:
            raise ValidationError("As observações não podem exceder 1000 caracteres.")
