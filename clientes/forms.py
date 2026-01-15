from django import forms
from .models import Cliente
from sistema_produtos.mixins import BootstrapValidationMixin


class ClienteForm(BootstrapValidationMixin, forms.ModelForm):
    class Meta:
        model = Cliente
        fields = [
            'nome_empresa', 'representante', 'cnpj', 'inscricao_estadual', 
            'inscricao_municipal', 'logradouro', 'numero', 'complemento', 
            'bairro', 'cidade', 'estado', 'cep', 'telefone', 'email', 
            'banco', 'agencia', 'conta_corrente'
        ]
        
        widgets = {
            'nome_empresa': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nome da empresa'
            }),
            'representante': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nome do representante'
            }),
            'cnpj': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '00.000.000/0000-00',
                'maxlength': '18'
            }),
            'inscricao_estadual': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Inscrição Estadual'
            }),
            'inscricao_municipal': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Inscrição Municipal'
            }),
            'logradouro': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Rua, avenida, praça, etc.'
            }),
            'numero': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Número'
            }),
            'complemento': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Apartamento, sala, andar, etc.'
            }),
            'bairro': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Bairro'
            }),
            'cidade': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Cidade'
            }),
            'estado': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'UF',
                'maxlength': '2',
                'style': 'text-transform: uppercase;'
            }),
            'cep': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '00000-000',
                'maxlength': '9'
            }),
            'telefone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '(11) 99999-9999'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'email@empresa.com'
            }),
            'banco': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nome do banco'
            }),
            'agencia': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Número da agência'
            }),
            'conta_corrente': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Número da conta corrente'
            }),
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Marcar campos obrigatórios
        required_fields = [
            'nome_empresa', 'representante', 'cnpj', 'logradouro', 
            'numero', 'bairro', 'cidade', 'estado', 'cep', 'telefone', 'email'
        ]
        
        for field_name in required_fields:
            if field_name in self.fields:
                self.fields[field_name].widget.attrs['required'] = True
        
        # Adicionar classe is-invalid aos campos com erro
        self.add_invalid_classes()
                
    def clean_cnpj(self):
        cnpj = self.cleaned_data.get('cnpj')
        if cnpj:
            # Remove pontuação para validação
            cnpj_digits = ''.join(filter(str.isdigit, cnpj))
            
            # Verifica se tem 14 dígitos
            if len(cnpj_digits) != 14:
                raise forms.ValidationError('CNPJ deve conter 14 dígitos.')
                
            # Adiciona formatação se não estiver formatado
            if len(cnpj) == 14:  # Se veio só com números
                cnpj = f"{cnpj[:2]}.{cnpj[2:5]}.{cnpj[5:8]}/{cnpj[8:12]}-{cnpj[12:]}"
                
        return cnpj
        
    def clean_cep(self):
        cep = self.cleaned_data.get('cep')
        if cep:
            # Remove hífen para validação
            cep_digits = ''.join(filter(str.isdigit, cep))
            
            # Verifica se tem 8 dígitos
            if len(cep_digits) != 8:
                raise forms.ValidationError('CEP deve conter 8 dígitos.')
                
            # Adiciona formatação se não estiver formatado
            if len(cep) == 8:  # Se veio só com números
                cep = f"{cep[:5]}-{cep[5:]}"
                
        return cep
        
    def clean_estado(self):
        estado = self.cleaned_data.get('estado')
        if estado:
            estado = estado.upper()
            # Lista de UFs válidas
            ufs_validas = [
                'AC', 'AL', 'AP', 'AM', 'BA', 'CE', 'DF', 'ES', 'GO', 
                'MA', 'MT', 'MS', 'MG', 'PA', 'PB', 'PR', 'PE', 'PI', 
                'RJ', 'RN', 'RS', 'RO', 'RR', 'SC', 'SP', 'SE', 'TO'
            ]
            if estado not in ufs_validas:
                raise forms.ValidationError('Digite uma UF válida.')
        return estado
