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
