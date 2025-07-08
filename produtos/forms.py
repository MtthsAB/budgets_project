from django import forms
from .models import (
    Item, Produto, TipoItem, Modulo, TamanhosModulosDetalhado, 
    Acessorio, FaixaTecido, PrecosBase, Banqueta, Cadeira, Poltrona, Pufe, Almofada
)

class TamanhosModulosDetalhadoForm(forms.ModelForm):
    """
    Formulário customizado para TamanhosModulosDetalhado que exclui 
    os campos altura_cm e profundidade_cm, já que são herdados do módulo.
    """
    
    class Meta:
        model = TamanhosModulosDetalhado
        fields = [
            'id_modulo',
            'largura_total',
            'largura_assento',
            'tecido_metros',
            'volume_m3',
            'peso_kg',
            'preco',
            'descricao'
        ]
        widgets = {
            'descricao': forms.Textarea(attrs={'rows': 3}),
            'largura_total': forms.NumberInput(attrs={'step': '0.01'}),
            'largura_assento': forms.NumberInput(attrs={'step': '0.01'}),
            'tecido_metros': forms.NumberInput(attrs={'step': '0.01'}),
            'volume_m3': forms.NumberInput(attrs={'step': '0.001'}),
            'peso_kg': forms.NumberInput(attrs={'step': '0.01'}),
            'preco': forms.NumberInput(attrs={'step': '0.01'}),
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Adicionar classes CSS para melhor apresentação
        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})
        
        # Adicionar help_text para campos importantes
        self.fields['largura_total'].help_text = "Largura total do produto em centímetros"
        self.fields['largura_assento'].help_text = "Largura útil do assento em centímetros"
        self.fields['tecido_metros'].help_text = "Quantidade de tecido necessária em metros"
        self.fields['volume_m3'].help_text = "Volume para cálculo de frete em metros cúbicos"
        self.fields['peso_kg'].help_text = "Peso para cálculo de frete em quilogramas"
        self.fields['preco'].help_text = "Preço base em reais (R$)"

class ModuloForm(forms.ModelForm):
    """
    Formulário customizado para Módulos com validações específicas.
    """
    
    class Meta:
        model = Modulo
        fields = [
            'produto',
            'nome',
            'profundidade',
            'altura',
            'braco',
            'descricao',
            'imagem_principal'
        ]
        widgets = {
            'descricao': forms.Textarea(attrs={'rows': 3}),
            'profundidade': forms.NumberInput(attrs={'step': '0.01'}),
            'altura': forms.NumberInput(attrs={'step': '0.01'}),
            'braco': forms.NumberInput(attrs={'step': '0.01'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Adicionar classes CSS
        for field_name, field in self.fields.items():
            if field_name != 'imagem_principal':
                field.widget.attrs.update({'class': 'form-control'})
        
        # Adicionar help_text
        self.fields['profundidade'].help_text = "Profundidade do módulo em centímetros (será herdada pelos tamanhos)"
        self.fields['altura'].help_text = "Altura do módulo em centímetros (será herdada pelos tamanhos)"
        self.fields['braco'].help_text = "Medida do braço em centímetros"
        
    def clean(self):
        cleaned_data = super().clean()
        profundidade = cleaned_data.get('profundidade')
        altura = cleaned_data.get('altura')
        
        if profundidade is not None and profundidade <= 0:
            raise forms.ValidationError("A profundidade deve ser maior que zero.")
            
        if altura is not None and altura <= 0:
            raise forms.ValidationError("A altura deve ser maior que zero.")
            
        return cleaned_data

class ItemForm(forms.ModelForm):
    """
    Formulário customizado para Itens.
    """
    
    class Meta:
        model = Item
        fields = [
            'ref_produto',
            'nome_produto',
            'id_tipo_produto',
            'ativo',
            'tem_cor_tecido',
            'tem_difer_desenho_lado_dir_esq',
            'tem_difer_desenho_tamanho',
            'imagem_principal'
        ]
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Adicionar classes CSS
        for field_name, field in self.fields.items():
            if isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs.update({'class': 'form-check-input'})
            elif field_name != 'imagem_principal':
                field.widget.attrs.update({'class': 'form-control'})
        
        # Adicionar help_text
        self.fields['ref_produto'].help_text = "Código único do produto"
        self.fields['tem_cor_tecido'].help_text = "Marque se o produto possui variações de cor/tecido"
        self.fields['tem_difer_desenho_lado_dir_esq'].help_text = "Marque se há diferença entre lado direito e esquerdo"
        self.fields['tem_difer_desenho_tamanho'].help_text = "Marque se o desenho varia conforme o tamanho"
        
        # Se for acessório, ocultar campos específicos
        if self.instance and self.instance.pk:
            tipo_produto = self.instance.id_tipo_produto
            if tipo_produto and tipo_produto.nome.lower() == 'acessório':
                # Remover campos não aplicáveis para acessórios
                campos_ocultar = ['tem_cor_tecido', 'tem_difer_desenho_lado_dir_esq', 'tem_difer_desenho_tamanho']
                for campo in campos_ocultar:
                    if campo in self.fields:
                        del self.fields[campo]
    
    def clean(self):
        cleaned_data = super().clean()
        tipo_produto = cleaned_data.get('id_tipo_produto')
        
        # Se for acessório, forçar valores False para os campos específicos
        if tipo_produto and tipo_produto.nome.lower() == 'acessório':
            cleaned_data['tem_cor_tecido'] = False
            cleaned_data['tem_difer_desenho_lado_dir_esq'] = False
            cleaned_data['tem_difer_desenho_tamanho'] = False
        
        return cleaned_data


class AcessorioForm(forms.ModelForm):
    """
    Formulário específico para Acessórios - campos simplificados.
    """
    
    class Meta:
        model = Acessorio
        fields = [
            'ref_acessorio',
            'nome',
            'ativo',
            'preco',
            'imagem_principal',
            'imagem_secundaria',
            'produtos_vinculados',
            'descricao'
        ]
        widgets = {
            'descricao': forms.Textarea(attrs={'rows': 3}),
            'preco': forms.NumberInput(attrs={'step': '0.01'}),
            'produtos_vinculados': forms.CheckboxSelectMultiple(),
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Adicionar classes CSS
        for field_name, field in self.fields.items():
            if isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs.update({'class': 'form-check-input'})
            elif isinstance(field.widget, forms.CheckboxSelectMultiple):
                field.widget.attrs.update({'class': 'form-check-input'})
            elif field_name not in ['imagem_principal', 'imagem_secundaria']:
                field.widget.attrs.update({'class': 'form-control'})
        
        # Adicionar help_text
        self.fields['ref_acessorio'].help_text = "Código único do acessório"
        self.fields['preco'].help_text = "Preço do acessório em reais (R$)"
        self.fields['produtos_vinculados'].help_text = "Selecione os produtos aos quais este acessório pode ser vinculado"
        
        # Filtrar APENAS sofás ativos para vinculação
        try:
            tipo_sofa = TipoItem.objects.filter(nome__icontains='sofá').first()
            if tipo_sofa:
                # Mostrar apenas sofás
                sofas_ativos = Produto.objects.filter(
                    ativo=True, 
                    id_tipo_produto=tipo_sofa
                ).order_by('ref_produto')
                self.fields['produtos_vinculados'].queryset = sofas_ativos
                self.fields['produtos_vinculados'].label = "Sofás Compatíveis"
                self.fields['produtos_vinculados'].help_text = "Selecione os sofás aos quais este acessório pode ser vinculado"
            else:
                # Se não encontrar tipo sofá, usar queryset vazio
                self.fields['produtos_vinculados'].queryset = Produto.objects.none()
                self.fields['produtos_vinculados'].help_text = "Nenhum sofá encontrado para vinculação"
        except:
            # Fallback: queryset vazio se houver erro
            self.fields['produtos_vinculados'].queryset = Produto.objects.none()
    
    def clean_ref_acessorio(self):
        ref_acessorio = self.cleaned_data.get('ref_acessorio')
        if ref_acessorio:
            ref_acessorio = ref_acessorio.strip().upper()
            
            # Verificar se já existe (exceto para o próprio objeto na edição)
            qs = Acessorio.objects.filter(ref_acessorio=ref_acessorio)
            if self.instance.pk:
                qs = qs.exclude(pk=self.instance.pk)
            
            if qs.exists():
                raise forms.ValidationError("Já existe um acessório com esta referência.")
        
        return ref_acessorio
    
    def clean_preco(self):
        preco = self.cleaned_data.get('preco')
        if preco is not None and preco < 0:
            raise forms.ValidationError("O preço deve ser maior ou igual a zero.")
        return preco

class BanquetaForm(forms.ModelForm):
    """
    Formulário específico para Banquetas.
    """
    
    class Meta:
        model = Banqueta
        fields = [
            'ref_banqueta',
            'nome',
            'largura',
            'profundidade', 
            'altura',
            'tecido_metros',
            'volume_m3',
            'peso_kg',
            'preco',
            'ativo',
            'imagem_principal',
            'imagem_secundaria',
            'descricao'
        ]
        widgets = {
            'descricao': forms.Textarea(attrs={'rows': 3}),
            'largura': forms.NumberInput(attrs={'step': '0.01', 'min': '0.01'}),
            'profundidade': forms.NumberInput(attrs={'step': '0.01', 'min': '0.01'}),
            'altura': forms.NumberInput(attrs={'step': '0.01', 'min': '0.01'}),
            'tecido_metros': forms.NumberInput(attrs={'step': '0.01', 'min': '0.01'}),
            'volume_m3': forms.NumberInput(attrs={'step': '0.001', 'min': '0.001'}),
            'peso_kg': forms.NumberInput(attrs={'step': '0.01', 'min': '0.01'}),
            'preco': forms.NumberInput(attrs={'step': '0.01', 'min': '0.01'}),
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Adicionar classes CSS
        for field_name, field in self.fields.items():
            if isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs.update({'class': 'form-check-input'})
            elif field_name not in ['imagem_principal', 'imagem_secundaria']:
                field.widget.attrs.update({'class': 'form-control'})
        
        # Adicionar help_text e placeholder
        self.fields['ref_banqueta'].help_text = "Código único da banqueta (ex: BQ13, BQ249)"
        self.fields['nome'].help_text = "Nome da banqueta (ex: CERES, GIO)"
        self.fields['largura'].help_text = "Largura em centímetros"
        self.fields['profundidade'].help_text = "Profundidade em centímetros"
        self.fields['altura'].help_text = "Altura em centímetros"
        self.fields['tecido_metros'].help_text = "Quantidade de tecido em metros"
        self.fields['volume_m3'].help_text = "Volume em metros cúbicos (m³)"
        self.fields['peso_kg'].help_text = "Peso em quilogramas (kg)"
        self.fields['preco'].help_text = "Preço em reais (R$)"
        
        # Adicionar placeholders
        self.fields['ref_banqueta'].widget.attrs['placeholder'] = 'Ex: BQ249'
        self.fields['nome'].widget.attrs['placeholder'] = 'Ex: CERES'
        self.fields['largura'].widget.attrs['placeholder'] = '42,50'
        self.fields['profundidade'].widget.attrs['placeholder'] = '50,99'
        self.fields['altura'].widget.attrs['placeholder'] = '99,00'
        self.fields['tecido_metros'].widget.attrs['placeholder'] = '0,90'
        self.fields['volume_m3'].widget.attrs['placeholder'] = '0,24'
        self.fields['peso_kg'].widget.attrs['placeholder'] = '8'
        self.fields['preco'].widget.attrs['placeholder'] = '658,00'
    
    def clean_ref_banqueta(self):
        ref_banqueta = self.cleaned_data.get('ref_banqueta')
        if ref_banqueta:
            ref_banqueta = ref_banqueta.strip().upper()
            
            # Verificar se já existe (exceto para o próprio objeto na edição)
            qs = Banqueta.objects.filter(ref_banqueta=ref_banqueta)
            if self.instance.pk:
                qs = qs.exclude(pk=self.instance.pk)
            
            if qs.exists():
                raise forms.ValidationError("Já existe uma banqueta com esta referência.")
        
        return ref_banqueta
    
    def clean(self):
        cleaned_data = super().clean()
        
        # Validações específicas para campos numéricos
        campos_numericos = ['largura', 'profundidade', 'altura', 'tecido_metros', 'volume_m3', 'peso_kg', 'preco']
        
        for campo in campos_numericos:
            valor = cleaned_data.get(campo)
            if valor is not None and valor <= 0:
                self.add_error(campo, f"O valor deve ser maior que zero.")
        
        return cleaned_data

class CadeiraForm(forms.ModelForm):
    """
    Formulário específico para Cadeiras.
    """
    
    class Meta:
        model = Cadeira
        fields = [
            'ref_cadeira',
            'nome',
            'largura',
            'profundidade', 
            'altura',
            'tecido_metros',
            'volume_m3',
            'peso_kg',
            'preco',
            'ativo',
            'tem_cor_tecido',
            'imagem_principal',
            'imagem_secundaria',
            'descricao'
        ]
        widgets = {
            'descricao': forms.Textarea(attrs={'rows': 3}),
            'largura': forms.NumberInput(attrs={'step': '0.01', 'min': '0.01'}),
            'profundidade': forms.NumberInput(attrs={'step': '0.01', 'min': '0.01'}),
            'altura': forms.NumberInput(attrs={'step': '0.01', 'min': '0.01'}),
            'tecido_metros': forms.NumberInput(attrs={'step': '0.01', 'min': '0.01'}),
            'volume_m3': forms.NumberInput(attrs={'step': '0.001', 'min': '0.001'}),
            'peso_kg': forms.NumberInput(attrs={'step': '0.01', 'min': '0.01'}),
            'preco': forms.NumberInput(attrs={'step': '0.01', 'min': '0.01'}),
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Adicionar classes CSS
        for field_name, field in self.fields.items():
            if isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs.update({'class': 'form-check-input'})
            elif field_name not in ['imagem_principal', 'imagem_secundaria']:
                field.widget.attrs.update({'class': 'form-control'})
        
        # Adicionar help_text e placeholder
        self.fields['ref_cadeira'].help_text = "Código único da cadeira (ex: CD001, CD24, CD267)"
        self.fields['nome'].help_text = "Nome da cadeira (ex: EVA, FIT, KIA)"
        self.fields['largura'].help_text = "Largura em centímetros"
        self.fields['profundidade'].help_text = "Profundidade em centímetros"
        self.fields['altura'].help_text = "Altura em centímetros"
        self.fields['tecido_metros'].help_text = "Quantidade de tecido em metros"
        self.fields['volume_m3'].help_text = "Volume em metros cúbicos (m³)"
        self.fields['peso_kg'].help_text = "Peso em quilogramas (kg)"
        self.fields['preco'].help_text = "Preço em reais (R$)"
        
        # Adicionar placeholders
        self.fields['ref_cadeira'].widget.attrs['placeholder'] = 'Ex: CD001'
        self.fields['nome'].widget.attrs['placeholder'] = 'Ex: EVA'
        self.fields['largura'].widget.attrs['placeholder'] = '48,00'
        self.fields['profundidade'].widget.attrs['placeholder'] = '65,00'
        self.fields['altura'].widget.attrs['placeholder'] = '97,00'
        self.fields['tecido_metros'].widget.attrs['placeholder'] = '1,30'
        self.fields['volume_m3'].widget.attrs['placeholder'] = '0,40'
        self.fields['peso_kg'].widget.attrs['placeholder'] = '8'
        self.fields['preco'].widget.attrs['placeholder'] = '857,00'
    
    def clean_ref_cadeira(self):
        ref_cadeira = self.cleaned_data.get('ref_cadeira')
        if ref_cadeira:
            ref_cadeira = ref_cadeira.strip().upper()
            
            # Verificar se já existe (exceto para o próprio objeto na edição)
            qs = Cadeira.objects.filter(ref_cadeira=ref_cadeira)
            if self.instance.pk:
                qs = qs.exclude(pk=self.instance.pk)
            
            if qs.exists():
                raise forms.ValidationError("Já existe uma cadeira com esta referência.")
        
        return ref_cadeira
    
    def clean(self):
        cleaned_data = super().clean()
        
        # Validações específicas para campos numéricos
        campos_numericos = ['largura', 'profundidade', 'altura', 'tecido_metros', 'volume_m3', 'peso_kg', 'preco']
        
        for campo in campos_numericos:
            valor = cleaned_data.get(campo)
            if valor is not None and valor <= 0:
                self.add_error(campo, f'{campo.replace("_", " ").title()} deve ser maior que zero.')
        
        return cleaned_data


class PoltronaForm(forms.ModelForm):
    """
    Formulário específico para Poltronas.
    """
    
    class Meta:
        model = Poltrona
        fields = [
            'ref_poltrona',
            'nome',
            'largura',
            'profundidade', 
            'altura',
            'tecido_metros',
            'volume_m3',
            'peso_kg',
            'preco',
            'ativo',
            'tem_cor_tecido',
            'imagem_principal',
            'imagem_secundaria',
            'descricao'
        ]
        widgets = {
            'descricao': forms.Textarea(attrs={'rows': 3}),
            'largura': forms.NumberInput(attrs={'step': '0.01', 'min': '0.01'}),
            'profundidade': forms.NumberInput(attrs={'step': '0.01', 'min': '0.01'}),
            'altura': forms.NumberInput(attrs={'step': '0.01', 'min': '0.01'}),
            'tecido_metros': forms.NumberInput(attrs={'step': '0.01', 'min': '0.01'}),
            'volume_m3': forms.NumberInput(attrs={'step': '0.001', 'min': '0.001'}),
            'peso_kg': forms.NumberInput(attrs={'step': '0.01', 'min': '0.01'}),
            'preco': forms.NumberInput(attrs={'step': '0.01', 'min': '0.01'}),
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Adicionar classes CSS
        for field_name, field in self.fields.items():
            if isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs.update({'class': 'form-check-input'})
            elif field_name not in ['imagem_principal', 'imagem_secundaria']:
                field.widget.attrs.update({'class': 'form-control'})
        
        # Adicionar help_text e placeholder
        self.fields['ref_poltrona'].help_text = "Código único da poltrona (ex: PL243, PL246, PL105)"
        self.fields['nome'].help_text = "Nome da poltrona (ex: ARIA, ARISTOCRATA, CERNE)"
        self.fields['largura'].help_text = "Largura em centímetros"
        self.fields['profundidade'].help_text = "Profundidade em centímetros"
        self.fields['altura'].help_text = "Altura em centímetros"
        self.fields['tecido_metros'].help_text = "Quantidade de tecido em metros"
        self.fields['volume_m3'].help_text = "Volume em metros cúbicos (m³)"
        self.fields['peso_kg'].help_text = "Peso em quilogramas (kg)"
        self.fields['preco'].help_text = "Preço em reais (R$)"
        
        # Adicionar placeholders
        self.fields['ref_poltrona'].widget.attrs['placeholder'] = 'Ex: PL243'
        self.fields['nome'].widget.attrs['placeholder'] = 'Ex: ARIA'
        self.fields['largura'].widget.attrs['placeholder'] = '82,00'
        self.fields['profundidade'].widget.attrs['placeholder'] = '81,00'
        self.fields['altura'].widget.attrs['placeholder'] = '84,00'
        self.fields['tecido_metros'].widget.attrs['placeholder'] = '4,60'
        self.fields['volume_m3'].widget.attrs['placeholder'] = '0,60'
        self.fields['peso_kg'].widget.attrs['placeholder'] = '25'
        self.fields['preco'].widget.attrs['placeholder'] = '1301,00'
    
    def clean_ref_poltrona(self):
        ref_poltrona = self.cleaned_data.get('ref_poltrona')
        if ref_poltrona:
            ref_poltrona = ref_poltrona.strip().upper()
            
            # Verificar se já existe (exceto para o próprio objeto na edição)
            qs = Poltrona.objects.filter(ref_poltrona=ref_poltrona)
            if self.instance.pk:
                qs = qs.exclude(pk=self.instance.pk)
            
            if qs.exists():
                raise forms.ValidationError("Já existe uma poltrona com esta referência.")
        
        return ref_poltrona
    
    def clean(self):
        cleaned_data = super().clean()
        
        # Validações específicas para campos numéricos
        campos_numericos = ['largura', 'profundidade', 'altura', 'tecido_metros', 'volume_m3', 'peso_kg', 'preco']
        
        for campo in campos_numericos:
            valor = cleaned_data.get(campo)
            if valor is not None and valor <= 0:
                self.add_error(campo, f'O valor deve ser maior que zero.')
        
        return cleaned_data


class PufeForm(forms.ModelForm):
    """
    Formulário específico para Pufes.
    """
    
    class Meta:
        model = Pufe
        fields = [
            'ref_pufe',
            'nome',
            'largura',
            'profundidade', 
            'altura',
            'tecido_metros',
            'volume_m3',
            'peso_kg',
            'preco',
            'ativo',
            'imagem_principal',
            'imagem_secundaria',
            'descricao'
        ]
        widgets = {
            'descricao': forms.Textarea(attrs={'rows': 3}),
            'largura': forms.NumberInput(attrs={'step': '0.01', 'min': '0.01'}),
            'profundidade': forms.NumberInput(attrs={'step': '0.01', 'min': '0.01'}),
            'altura': forms.NumberInput(attrs={'step': '0.01', 'min': '0.01'}),
            'tecido_metros': forms.NumberInput(attrs={'step': '0.01', 'min': '0.01'}),
            'volume_m3': forms.NumberInput(attrs={'step': '0.001', 'min': '0.001'}),
            'peso_kg': forms.NumberInput(attrs={'step': '0.01', 'min': '0.01'}),
            'preco': forms.NumberInput(attrs={'step': '0.01', 'min': '0.01'}),
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Adicionar classes CSS
        for field_name, field in self.fields.items():
            if isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs.update({'class': 'form-check-input'})
            elif field_name not in ['imagem_principal', 'imagem_secundaria']:
                field.widget.attrs.update({'class': 'form-control'})
        
        # Adicionar help_text e placeholder
        self.fields['ref_pufe'].help_text = "Código único do pufe (ex: PF13, PF249)"
        self.fields['nome'].help_text = "Nome do pufe (ex: ROUND, SQUARE)"
        self.fields['largura'].help_text = "Largura em centímetros"
        self.fields['profundidade'].help_text = "Profundidade em centímetros"
        self.fields['altura'].help_text = "Altura em centímetros"
        self.fields['tecido_metros'].help_text = "Quantidade de tecido em metros"
        self.fields['volume_m3'].help_text = "Volume em metros cúbicos (m³)"
        self.fields['peso_kg'].help_text = "Peso em quilogramas (kg)"
        self.fields['preco'].help_text = "Preço em reais (R$)"
        
        # Adicionar placeholders
        self.fields['ref_pufe'].widget.attrs['placeholder'] = 'Ex: PF249'
        self.fields['nome'].widget.attrs['placeholder'] = 'Ex: ROUND'
        self.fields['largura'].widget.attrs['placeholder'] = '40,00'
        self.fields['profundidade'].widget.attrs['placeholder'] = '40,00'
        self.fields['altura'].widget.attrs['placeholder'] = '35,00'
        self.fields['tecido_metros'].widget.attrs['placeholder'] = '0,80'
        self.fields['volume_m3'].widget.attrs['placeholder'] = '0,20'
        self.fields['peso_kg'].widget.attrs['placeholder'] = '6'
        self.fields['preco'].widget.attrs['placeholder'] = '450,00'
    
    def clean_ref_pufe(self):
        ref_pufe = self.cleaned_data.get('ref_pufe')
        if ref_pufe:
            ref_pufe = ref_pufe.strip().upper()
            
            # Verificar se já existe (exceto para o próprio objeto na edição)
            qs = Pufe.objects.filter(ref_pufe=ref_pufe)
            if self.instance.pk:
                qs = qs.exclude(pk=self.instance.pk)
            
            if qs.exists():
                raise forms.ValidationError("Já existe um pufe com esta referência.")
        
        return ref_pufe
    
    def clean(self):
        cleaned_data = super().clean()
        
        # Validações específicas para campos numéricos
        campos_numericos = ['largura', 'profundidade', 'altura', 'tecido_metros', 'volume_m3', 'peso_kg', 'preco']
        
        for campo in campos_numericos:
            valor = cleaned_data.get(campo)
            if valor is not None and valor <= 0:
                self.add_error(campo, f"O valor deve ser maior que zero.")
        
        return cleaned_data


class AlmofadaForm(forms.ModelForm):
    """
    Formulário específico para Almofadas - só tem largura e altura.
    """
    
    class Meta:
        model = Almofada
        fields = [
            'ref_almofada',
            'nome',
            'largura',
            'altura',
            'tecido_metros',
            'volume_m3',
            'peso_kg',
            'preco',
            'ativo',
            'imagem_principal',
            'imagem_secundaria',
            'descricao'
        ]
        widgets = {
            'descricao': forms.Textarea(attrs={'rows': 3}),
            'largura': forms.NumberInput(attrs={'step': '0.01', 'min': '0.01'}),
            'altura': forms.NumberInput(attrs={'step': '0.01', 'min': '0.01'}),
            'tecido_metros': forms.NumberInput(attrs={'step': '0.01', 'min': '0.01'}),
            'volume_m3': forms.NumberInput(attrs={'step': '0.001', 'min': '0.001'}),
            'peso_kg': forms.NumberInput(attrs={'step': '0.01', 'min': '0.01'}),
            'preco': forms.NumberInput(attrs={'step': '0.01', 'min': '0.01'}),
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Adicionar classes CSS
        for field_name, field in self.fields.items():
            if isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs.update({'class': 'form-check-input'})
            elif field_name not in ['imagem_principal', 'imagem_secundaria']:
                field.widget.attrs.update({'class': 'form-control'})
        
        # Adicionar help_text e placeholder
        self.fields['ref_almofada'].help_text = "Código único da almofada (ex: AL001, AL250)"
        self.fields['nome'].help_text = "Nome da almofada (ex: DECORATIVA, LOMBAR)"
        self.fields['largura'].help_text = "Largura em centímetros"
        self.fields['altura'].help_text = "Altura em centímetros"
        self.fields['tecido_metros'].help_text = "Quantidade de tecido em metros"
        self.fields['volume_m3'].help_text = "Volume em metros cúbicos (m³)"
        self.fields['peso_kg'].help_text = "Peso em quilogramas (kg)"
        self.fields['preco'].help_text = "Preço em reais (R$)"
        
        # Adicionar placeholders
        self.fields['ref_almofada'].widget.attrs['placeholder'] = 'Ex: AL250'
        self.fields['nome'].widget.attrs['placeholder'] = 'Ex: DECORATIVA'
        self.fields['largura'].widget.attrs['placeholder'] = '50,00'
        self.fields['altura'].widget.attrs['placeholder'] = '30,00'
        self.fields['tecido_metros'].widget.attrs['placeholder'] = '0,25'
        self.fields['volume_m3'].widget.attrs['placeholder'] = '0,05'
        self.fields['peso_kg'].widget.attrs['placeholder'] = '1'
        self.fields['preco'].widget.attrs['placeholder'] = '120,00'
    
    def clean_ref_almofada(self):
        ref_almofada = self.cleaned_data.get('ref_almofada')
        if ref_almofada:
            ref_almofada = ref_almofada.strip().upper()
            
            # Verificar se já existe (exceto para o próprio objeto na edição)
            qs = Almofada.objects.filter(ref_almofada=ref_almofada)
            if self.instance.pk:
                qs = qs.exclude(pk=self.instance.pk)
            
            if qs.exists():
                raise forms.ValidationError("Já existe uma almofada com esta referência.")
        
        return ref_almofada
    
    def clean(self):
        cleaned_data = super().clean()
        
        # Validações específicas para campos numéricos (sem profundidade para almofadas)
        campos_numericos = ['largura', 'altura', 'tecido_metros', 'volume_m3', 'peso_kg', 'preco']
        
        for campo in campos_numericos:
            valor = cleaned_data.get(campo)
            if valor is not None and valor <= 0:
                self.add_error(campo, f"O valor deve ser maior que zero.")
        
        return cleaned_data
