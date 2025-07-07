from django.contrib import admin
from .models import (
    TipoItem, Item, Acessorio, Banqueta, Cadeira,
    Modulo, TamanhosModulos, TamanhosModulosDetalhado, FaixaTecido, PrecosBase
)
from .forms import TamanhosModulosDetalhadoForm, ModuloForm, ItemForm

@admin.register(TipoItem)
class TipoItemAdmin(admin.ModelAdmin):
    list_display = ('nome', 'created_at', 'updated_at', 'created_by', 'updated_by')
    search_fields = ('nome',)
    readonly_fields = ('created_at', 'updated_at', 'created_by', 'updated_by')

class ModuloInline(admin.TabularInline):
    model = Modulo
    extra = 1
    fields = ('nome', 'profundidade', 'altura', 'braco', 'imagem_principal')

@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    form = ItemForm
    list_display = ('ref_produto', 'nome_produto', 'id_tipo_produto', 'ativo', 'created_at', 'created_by')
    list_filter = ('ativo', 'id_tipo_produto', 'tem_cor_tecido', 'created_by')
    search_fields = ('ref_produto', 'nome_produto')
    readonly_fields = ('created_at', 'updated_at', 'created_by', 'updated_by')
    inlines = [ModuloInline]
    
    fieldsets = (
        ('Informações Básicas', {
            'fields': ('ref_produto', 'nome_produto', 'id_tipo_produto', 'ativo')
        }),
        ('Imagens', {
            'fields': ('imagem_principal', 'imagem_secundaria')
        }),
        ('Características', {
            'fields': ('tem_cor_tecido', 'tem_difer_desenho_lado_dir_esq', 'tem_difer_desenho_tamanho')
        }),
        ('Auditoria', {
            'fields': ('created_at', 'updated_at', 'created_by', 'updated_by'),
            'classes': ('collapse',)
        }),
    )

@admin.register(Acessorio)
class AcessorioAdmin(admin.ModelAdmin):
    list_display = ('nome', 'ref_acessorio', 'ativo', 'created_at', 'created_by')
    list_filter = ('ativo', 'created_by')
    search_fields = ('nome', 'ref_acessorio')
    readonly_fields = ('created_at', 'updated_at', 'created_by', 'updated_by')

@admin.register(Modulo)
class ModuloAdmin(admin.ModelAdmin):
    form = ModuloForm
    list_display = ('nome', 'item', 'profundidade', 'altura', 'braco', 'created_at', 'created_by')
    list_filter = ('item__id_tipo_produto', 'created_by')
    search_fields = ('nome', 'item__ref_produto', 'item__nome_produto')
    readonly_fields = ('created_at', 'updated_at', 'created_by', 'updated_by')
    
    fieldsets = (
        ('Informações Básicas', {
            'fields': ('item', 'nome', 'descricao')
        }),
        ('Dimensões', {
            'fields': ('profundidade', 'altura', 'braco')
        }),
        ('Imagens', {
            'fields': ('imagem_principal', 'imagem_secundaria')
        }),
        ('Auditoria', {
            'fields': ('created_at', 'updated_at', 'created_by', 'updated_by'),
            'classes': ('collapse',)
        }),
    )

@admin.register(TamanhosModulos)
class TamanhosModulosAdmin(admin.ModelAdmin):
    list_display = ('id_modulo', 'tamanho', 'created_at', 'created_by')
    list_filter = ('id_modulo__item__id_tipo_produto', 'created_by')
    readonly_fields = ('created_at', 'updated_at', 'created_by', 'updated_by')

@admin.register(FaixaTecido)
class FaixaTecidoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'valor_minimo', 'valor_maximo', 'created_at', 'created_by')
    list_filter = ('created_by',)
    readonly_fields = ('created_at', 'updated_at', 'created_by', 'updated_by')

@admin.register(PrecosBase)
class PrecosBaseAdmin(admin.ModelAdmin):
    list_display = ('id_item', 'id_faixa_tecido', 'data_inic_vigencia', 'preco_base', 'created_at', 'created_by')
    list_filter = ('id_faixa_tecido', 'data_inic_vigencia', 'created_by')
    search_fields = ('id_item__ref_produto', 'id_item__nome_produto')
    readonly_fields = ('created_at', 'updated_at', 'created_by', 'updated_by')

@admin.register(TamanhosModulosDetalhado)
class TamanhosModulosDetalhadoAdmin(admin.ModelAdmin):
    form = TamanhosModulosDetalhadoForm
    list_display = ('id_modulo', 'id', 'largura_total', 'largura_assento', 'peso_kg', 'preco', 'created_at', 'created_by')
    list_filter = ('id_modulo__item__id_tipo_produto', 'created_by')
    search_fields = ('id_modulo__nome', 'descricao')
    readonly_fields = ('created_at', 'updated_at', 'created_by', 'updated_by')
    
    fieldsets = (
        ('Informações Básicas', {
            'fields': ('id_modulo', 'descricao')
        }),
        ('Dimensões', {
            'fields': ('largura_total', 'largura_assento')
        }),
        ('Especificações', {
            'fields': ('tecido_metros', 'volume_m3', 'peso_kg', 'preco')
        }),
        ('Auditoria', {
            'fields': ('created_at', 'updated_at', 'created_by', 'updated_by'),
            'classes': ('collapse',)
        }),
    )

@admin.register(Banqueta)
class BanquetaAdmin(admin.ModelAdmin):
    list_display = ('ref_banqueta', 'nome', 'ativo', 'preco', 'created_at', 'created_by')
    list_filter = ('ativo', 'created_by', 'created_at')
    search_fields = ('ref_banqueta', 'nome')
    readonly_fields = ('created_at', 'updated_at', 'created_by', 'updated_by')
    
    fieldsets = (
        ('Informações Básicas', {
            'fields': ('ref_banqueta', 'nome', 'ativo', 'descricao')
        }),
        ('Dimensões', {
            'fields': ('largura', 'profundidade', 'altura')
        }),
        ('Especificações Técnicas', {
            'fields': ('tecido_metros', 'volume_m3', 'peso_kg', 'preco')
        }),
        ('Imagens', {
            'fields': ('imagem_principal', 'imagem_secundaria')
        }),
        ('Auditoria', {
            'fields': ('created_at', 'updated_at', 'created_by', 'updated_by'),
            'classes': ('collapse',)
        }),
    )

@admin.register(Cadeira)
class CadeiraAdmin(admin.ModelAdmin):
    list_display = ('ref_cadeira', 'nome', 'ativo', 'preco', 'created_at', 'created_by')
    list_filter = ('ativo', 'created_by', 'created_at')
    search_fields = ('ref_cadeira', 'nome')
    readonly_fields = ('created_at', 'updated_at', 'created_by', 'updated_by')
    
    fieldsets = (
        ('Informações Básicas', {
            'fields': ('ref_cadeira', 'nome', 'ativo', 'descricao')
        }),
        ('Dimensões', {
            'fields': ('largura', 'profundidade', 'altura')
        }),
        ('Especificações Técnicas', {
            'fields': ('tecido_metros', 'volume_m3', 'peso_kg', 'preco')
        }),
        ('Imagens', {
            'fields': ('imagem_principal', 'imagem_secundaria')
        }),
        ('Auditoria', {
            'fields': ('created_at', 'updated_at', 'created_by', 'updated_by'),
            'classes': ('collapse',)
        }),
    )
