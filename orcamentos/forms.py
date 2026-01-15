from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import timedelta
from decimal import Decimal

from .models import Orcamento, OrcamentoItem, FaixaPreco, FormaPagamento
from clientes.models import Cliente
from produtos.models import Produto
from sistema_produtos.mixins import BootstrapValidationMixin


class OrcamentoForm(BootstrapValidationMixin, forms.ModelForm):
    """Formulário para criar/editar orçamento"""
    
    class Meta:
        model = Orcamento
        fields = [
            'cliente', 'faixa_preco', 'forma_pagamento',
            'desconto_valor', 'desconto_percentual',
            'acrescimo_valor', 'acrescimo_percentual',
            'data_entrega', 'data_validade', 'status', 'observacoes'
        ]
        widgets = {
            'cliente': forms.Select(attrs={
                'class': 'form-select cliente-select',
                'required': True,
                'id': 'id_cliente'
            }),
            'faixa_preco': forms.Select(attrs={
                'class': 'form-select',
                'required': True
            }),
            'forma_pagamento': forms.Select(attrs={
                'class': 'form-select',
                'required': True
            }),
            'desconto_valor': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0',
                'placeholder': '0,00',
                'required': False
            }),
            'desconto_percentual': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0',
                'max': '100',
                'placeholder': '0,00',
                'required': False
            }),
            'acrescimo_valor': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0',
                'placeholder': '0,00',
                'required': False
            }),
            'acrescimo_percentual': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0',
                'placeholder': '0,00',
                'required': False
            }),
            'data_entrega': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
                'required': True
            }, format='%Y-%m-%d'),
            'data_validade': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
                'required': True
            }, format='%Y-%m-%d'),
            'status': forms.Select(attrs={
                'class': 'form-select'
            }),
            'observacoes': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Observações gerais do orçamento...'
            })
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Filtrar apenas faixas de preço e formas de pagamento ativas
        self.fields['cliente'].queryset = Cliente.objects.all().order_by('nome_empresa')
        self.fields['faixa_preco'].queryset = FaixaPreco.objects.filter(ativo=True).order_by('nome')
        self.fields['forma_pagamento'].queryset = FormaPagamento.objects.filter(ativo=True).order_by('nome')
        
        # Personalizar labels
        self.fields['cliente'].label = 'Cliente'
        self.fields['faixa_preco'].label = 'Faixa de Preço'
        self.fields['forma_pagamento'].label = 'Forma de Pagamento'
        self.fields['desconto_valor'].label = 'Desconto (R$)'
        self.fields['desconto_percentual'].label = 'Desconto (%)'
        self.fields['acrescimo_valor'].label = 'Acréscimo (R$)'
        self.fields['acrescimo_percentual'].label = 'Acréscimo (%)'
        self.fields['data_entrega'].label = 'Data de Entrega'
        self.fields['data_validade'].label = 'Data de Validade'
        self.fields['observacoes'].label = 'Observações'
        
        # Tornar campos de desconto e acréscimo não obrigatórios
        self.fields['desconto_valor'].required = False
        self.fields['desconto_percentual'].required = False
        self.fields['acrescimo_valor'].required = False
        self.fields['acrescimo_percentual'].required = False
        
        # Definir valor padrão para data de validade se for novo orçamento
        if not self.instance.pk:
            from django.utils import timezone
            from datetime import timedelta
            # Só definir se não foi passado um initial value
            if not self.initial.get('data_validade'):
                self.fields['data_validade'].initial = timezone.now().date() + timedelta(days=15)
            if not self.initial.get('data_entrega'):
                self.fields['data_entrega'].initial = timezone.now().date() + timedelta(days=30)
        
        # Adicionar classe is-invalid aos campos com erro
        self.add_invalid_classes()
    
    def clean_desconto_valor(self):
        value = self.cleaned_data.get('desconto_valor')
        if value == '' or value is None:
            return None
        try:
            return float(value) if value else None
        except (ValueError, TypeError):
            return None
    
    def clean_desconto_percentual(self):
        value = self.cleaned_data.get('desconto_percentual')
        if value == '' or value is None:
            return None
        try:
            return float(value) if value else None
        except (ValueError, TypeError):
            return None
    
    def clean_acrescimo_valor(self):
        value = self.cleaned_data.get('acrescimo_valor')
        if value == '' or value is None:
            return None
        try:
            return float(value) if value else None
        except (ValueError, TypeError):
            return None
    
    def clean_acrescimo_percentual(self):
        value = self.cleaned_data.get('acrescimo_percentual')
        if value == '' or value is None:
            return None
        try:
            return float(value) if value else None
        except (ValueError, TypeError):
            return None

    def clean_data_entrega(self):
        data_entrega = self.cleaned_data.get('data_entrega')
        if data_entrega and data_entrega <= timezone.now().date():
            raise ValidationError('A data de entrega deve ser maior que a data atual.')
        return data_entrega
    
    def clean_data_validade(self):
        data_validade = self.cleaned_data.get('data_validade')
        if data_validade and data_validade <= timezone.now().date():
            raise ValidationError('A data de validade deve ser maior que a data atual.')
        return data_validade
    
    def clean(self):
        cleaned_data = super().clean()
        
        # Validar se apenas um tipo de desconto é usado
        desconto_valor = cleaned_data.get('desconto_valor')
        desconto_percentual = cleaned_data.get('desconto_percentual')
        
        # Converter para float e tratar valores None/vazios
        try:
            desconto_valor = float(desconto_valor) if desconto_valor not in [None, ''] else 0
        except (ValueError, TypeError):
            desconto_valor = 0
            
        try:
            desconto_percentual = float(desconto_percentual) if desconto_percentual not in [None, ''] else 0
        except (ValueError, TypeError):
            desconto_percentual = 0
        
        if desconto_valor > 0 and desconto_percentual > 0:
            raise ValidationError('Use apenas desconto em valor OU percentual, não ambos.')
        
        # Validar se apenas um tipo de acréscimo é usado
        acrescimo_valor = cleaned_data.get('acrescimo_valor')
        acrescimo_percentual = cleaned_data.get('acrescimo_percentual')
        
        # Converter para float e tratar valores None/vazios
        try:
            acrescimo_valor = float(acrescimo_valor) if acrescimo_valor not in [None, ''] else 0
        except (ValueError, TypeError):
            acrescimo_valor = 0
            
        try:
            acrescimo_percentual = float(acrescimo_percentual) if acrescimo_percentual not in [None, ''] else 0
        except (ValueError, TypeError):
            acrescimo_percentual = 0
        
        if acrescimo_valor > 0 and acrescimo_percentual > 0:
            raise ValidationError('Use apenas acréscimo em valor OU percentual, não ambos.')
        
        return cleaned_data


class OrcamentoItemForm(BootstrapValidationMixin, forms.ModelForm):
    """Formulário para adicionar/editar item do orçamento"""
    
    class Meta:
        model = OrcamentoItem
        fields = ['produto', 'quantidade', 'preco_unitario', 'observacoes']
        widgets = {
            'produto': forms.Select(attrs={
                'class': 'form-select',
                'required': True
            }),
            'quantidade': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '1',
                'value': '1'
            }),
            'preco_unitario': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0',
                'placeholder': '0,00'
            }),
            'observacoes': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'Observações específicas deste item...'
            })
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Filtrar apenas produtos ativos
        self.fields['produto'].queryset = Produto.objects.filter(ativo=True).order_by('nome_produto')
        
        # Personalizar labels
        self.fields['produto'].label = 'Produto'
        self.fields['quantidade'].label = 'Quantidade'
        self.fields['preco_unitario'].label = 'Preço Unitário (R$)'
        self.fields['observacoes'].label = 'Observações'
        
        # Adicionar classe is-invalid aos campos com erro
        self.add_invalid_classes()
    
    def clean_quantidade(self):
        quantidade = self.cleaned_data.get('quantidade')
        if quantidade and quantidade < 1:
            raise ValidationError('A quantidade deve ser maior que zero.')
        return quantidade
    
    def clean_preco_unitario(self):
        preco_unitario = self.cleaned_data.get('preco_unitario')
        if preco_unitario and preco_unitario < 0:
            raise ValidationError('O preço unitário não pode ser negativo.')
        return preco_unitario


class BuscaClienteForm(forms.Form):
    """Formulário para busca de clientes"""
    
    termo = forms.CharField(
        max_length=200,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Buscar por nome da empresa, representante ou CNPJ...',
            'autocomplete': 'off'
        }),
        label='Buscar Cliente'
    )


class BuscaProdutoForm(forms.Form):
    """Formulário para busca de produtos"""
    
    termo = forms.CharField(
        max_length=200,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Buscar por nome do produto ou referência...',
            'autocomplete': 'off'
        }),
        label='Buscar Produto'
    )


class FiltroOrcamentosForm(forms.Form):
    """Formulário para filtros na listagem de orçamentos"""
    
    STATUS_CHOICES = [('', 'Todos')] + Orcamento.STATUS_CHOICES
    
    busca = forms.CharField(
        max_length=200,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Buscar por número, cliente ou vendedor...'
        }),
        label='Buscar'
    )
    
    status = forms.ChoiceField(
        choices=STATUS_CHOICES,
        required=False,
        widget=forms.Select(attrs={
            'class': 'form-select'
        }),
        label='Status'
    )
    
    data_inicio = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date'
        }),
        label='Data Início'
    )
    
    data_fim = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date'
        }),
        label='Data Fim'
    )


class FaixaPrecoForm(forms.ModelForm):
    """Formulário para faixas de preço"""
    
    class Meta:
        model = FaixaPreco
        fields = ['nome', 'descricao', 'multiplicador', 'ativo']
        widgets = {
            'nome': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ex: Varejo, Atacado, Promocional...'
            }),
            'descricao': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Descrição da faixa de preço...'
            }),
            'multiplicador': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0.01',
                'placeholder': '1,00'
            }),
            'ativo': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            })
        }
    
    def clean_multiplicador(self):
        multiplicador = self.cleaned_data.get('multiplicador')
        if multiplicador and multiplicador <= 0:
            raise ValidationError('O multiplicador deve ser maior que zero.')
        return multiplicador


class FormaPagamentoForm(forms.ModelForm):
    """Formulário para formas de pagamento"""
    
    class Meta:
        model = FormaPagamento
        fields = ['nome', 'descricao', 'prazo_dias', 'desconto_maximo', 'ativo']
        widgets = {
            'nome': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ex: À vista, 30 dias, 60 dias...'
            }),
            'descricao': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Descrição da forma de pagamento...'
            }),
            'prazo_dias': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0',
                'placeholder': '0'
            }),
            'desconto_maximo': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0',
                'max': '100',
                'placeholder': '0,00'
            }),
            'ativo': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            })
        }
    
    def clean_prazo_dias(self):
        prazo_dias = self.cleaned_data.get('prazo_dias')
        if prazo_dias and prazo_dias < 0:
            raise ValidationError('O prazo não pode ser negativo.')
        return prazo_dias
    
    def clean_desconto_maximo(self):
        desconto_maximo = self.cleaned_data.get('desconto_maximo')
        if desconto_maximo and desconto_maximo < 0:
            raise ValidationError('O desconto máximo não pode ser negativo.')
        if desconto_maximo and desconto_maximo > 100:
            raise ValidationError('O desconto máximo não pode ser maior que 100%.')
        return desconto_maximo
