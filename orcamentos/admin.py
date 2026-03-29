from django.contrib import admin
from .models import FaixaPreco, FormaPagamento, Orcamento, OrcamentoItem, OrcamentoModulo


@admin.register(FaixaPreco)
class FaixaPrecoAdmin(admin.ModelAdmin):
    list_display = ['nome', 'multiplicador', 'ativo', 'created_at']
    list_filter = ['ativo', 'created_at']
    search_fields = ['nome', 'descricao']
    ordering = ['nome']


@admin.register(FormaPagamento)
class FormaPagamentoAdmin(admin.ModelAdmin):
    list_display = ['nome', 'prazo_dias', 'desconto_maximo', 'ativo', 'created_at']
    list_filter = ['ativo', 'created_at']
    search_fields = ['nome', 'descricao']
    ordering = ['nome']


class OrcamentoItemInline(admin.TabularInline):
    model = OrcamentoItem
    extra = 0
    readonly_fields = ['get_total']
    
    def get_total(self, obj):
        if obj.pk:
            return f"R$ {obj.get_total():.2f}"
        return "-"
    get_total.short_description = "Total"


@admin.register(Orcamento)
class OrcamentoAdmin(admin.ModelAdmin):
    list_display = [
        'numero', 'cliente', 'vendedor', 'status', 
        'get_total_final', 'data_entrega', 'created_at'
    ]
    list_filter = ['status', 'forma_pagamento', 'created_at']
    search_fields = ['numero', 'cliente__nome_empresa', 'vendedor__first_name', 'vendedor__last_name']
    readonly_fields = ['numero', 'get_subtotal', 'get_total_final', 'created_at', 'updated_at']
    inlines = [OrcamentoItemInline]
    
    fieldsets = (
        ('Informações Básicas', {
            'fields': ('numero', 'cliente', 'vendedor', 'status')
        }),
        ('Configurações', {
            'fields': ('forma_pagamento',)
        }),
        ('Valores', {
            'fields': (
                ('desconto_valor', 'desconto_percentual'),
                ('acrescimo_valor', 'acrescimo_percentual'),
                ('get_subtotal', 'get_total_final')
            )
        }),
        ('Datas', {
            'fields': ('data_entrega', 'data_validade', 'created_at', 'updated_at')
        }),
        ('Observações', {
            'fields': ('observacoes',)
        })
    )
    
    def get_total_final(self, obj):
        return f"R$ {obj.get_total_final():.2f}"
    get_total_final.short_description = "Total Final"
    
    def get_subtotal(self, obj):
        return f"R$ {obj.get_subtotal():.2f}"
    get_subtotal.short_description = "Subtotal"


@admin.register(OrcamentoItem)
class OrcamentoItemAdmin(admin.ModelAdmin):
    list_display = ['orcamento', 'produto', 'faixa_preco', 'quantidade', 'preco_unitario', 'get_total']
    list_filter = ['orcamento__status', 'produto__id_tipo_produto']
    search_fields = ['orcamento__numero', 'produto__nome_produto', 'produto__ref_produto']
    
    def get_total(self, obj):
        return f"R$ {obj.get_total():.2f}"
    get_total.short_description = "Total"


@admin.register(OrcamentoModulo)
class OrcamentoModuloAdmin(admin.ModelAdmin):
    list_display = ['item_orcamento', 'nome_modulo', 'tamanho_selecionado']
    list_filter = ['item_orcamento__orcamento__status']
    search_fields = ['nome_modulo', 'item_orcamento__orcamento__numero']
