from django.contrib import admin
from .models import Cliente


@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = [
        'nome_empresa', 'representante', 'cnpj', 'cidade', 
        'estado', 'telefone', 'email', 'created_at', 'created_by'
    ]
    list_filter = ['estado', 'cidade', 'created_at', 'created_by']
    search_fields = [
        'nome_empresa', 'representante', 'cnpj', 'email', 
        'cidade', 'bairro'
    ]
    readonly_fields = ['created_at', 'updated_at', 'created_by', 'updated_by']
    
    fieldsets = (
        ('Dados da Empresa', {
            'fields': ('nome_empresa', 'representante')
        }),
        ('Dados Legais', {
            'fields': ('cnpj', 'inscricao_estadual', 'inscricao_municipal')
        }),
        ('Endereço', {
            'fields': (
                'logradouro', 'numero', 'complemento', 
                'bairro', 'cidade', 'estado', 'cep'
            )
        }),
        ('Contato', {
            'fields': ('telefone', 'email')
        }),
        ('Dados Bancários', {
            'fields': ('banco', 'agencia', 'conta_corrente'),
            'classes': ('collapse',)
        }),
        ('Auditoria', {
            'fields': ('created_at', 'updated_at', 'created_by', 'updated_by'),
            'classes': ('collapse',)
        }),
    )
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related()
