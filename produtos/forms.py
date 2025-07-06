from django import forms
from .models import (
    Item, TipoItem, Modulo, TamanhosModulosDetalhado, 
    Acessorio, FaixaTecido, PrecosBase
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
            'item',
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
        
        # Filtrar apenas produtos ativos para vinculação
        self.fields['produtos_vinculados'].queryset = Item.objects.filter(ativo=True).order_by('ref_produto')
    
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
