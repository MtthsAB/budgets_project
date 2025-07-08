from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from .models import CustomUser, TipoPermissao

class CustomUserCreationForm(UserCreationForm):
    """Form para criação de usuários"""
    
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Digite o email do usuário'
        })
    )
    
    first_name = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Digite o nome'
        })
    )
    
    last_name = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Digite o sobrenome'
        })
    )
    
    tipo_permissao = forms.ChoiceField(
        choices=TipoPermissao.choices,
        required=True,
        widget=forms.Select(attrs={
            'class': 'form-control'
        })
    )
    
    is_active = forms.BooleanField(
        required=False,
        initial=True,
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input'
        })
    )
    
    password1 = forms.CharField(
        label="Senha",
        strip=False,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Digite a senha'
        })
    )
    
    password2 = forms.CharField(
        label="Confirmar Senha",
        strip=False,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirme a senha'
        })
    )
    
    class Meta:
        model = CustomUser
        fields = ('email', 'first_name', 'last_name', 'tipo_permissao', 'is_active')
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email=email).exists():
            raise ValidationError("Este email já está em uso.")
        return email
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.tipo_permissao = self.cleaned_data['tipo_permissao']
        user.is_active = self.cleaned_data['is_active']
        
        if commit:
            user.save()
        return user

class UserUpdateForm(forms.ModelForm):
    """Form para atualização de usuários"""
    
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Digite o email do usuário'
        })
    )
    
    first_name = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Digite o nome'
        })
    )
    
    last_name = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Digite o sobrenome'
        })
    )
    
    tipo_permissao = forms.ChoiceField(
        choices=TipoPermissao.choices,
        required=True,
        widget=forms.Select(attrs={
            'class': 'form-control'
        })
    )
    
    is_active = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input'
        })
    )
    
    class Meta:
        model = CustomUser
        fields = ('email', 'first_name', 'last_name', 'tipo_permissao', 'is_active')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Não permitir que o próprio usuário mude seu tipo de permissão ou desative-se
        if self.instance and hasattr(self, 'current_user') and self.instance == self.current_user:
            self.fields['tipo_permissao'].disabled = True
            self.fields['is_active'].disabled = True
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
            raise ValidationError("Este email já está em uso.")
        return email

class PasswordChangeForm(forms.Form):
    """Form para alteração de senha"""
    
    new_password1 = forms.CharField(
        label="Nova Senha",
        strip=False,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Digite a nova senha'
        })
    )
    
    new_password2 = forms.CharField(
        label="Confirmar Nova Senha",
        strip=False,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirme a nova senha'
        })
    )
    
    def clean_new_password1(self):
        password1 = self.cleaned_data.get('new_password1')
        try:
            validate_password(password1)
        except ValidationError as error:
            raise forms.ValidationError(error)
        return password1
    
    def clean_new_password2(self):
        password1 = self.cleaned_data.get('new_password1')
        password2 = self.cleaned_data.get('new_password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("As senhas não conferem.")
        return password2
