from django.contrib import admin
from .models import (
    TipoItem, Linha, Item, Acessorio, AcessoriosItens,
    Modulo, TamanhosModulos, TamanhosModulosDetalhado, FaixaTecido, PrecosBase
)

@admin.register(TipoItem)
class TipoItemAdmin(admin.ModelAdmin):
    list_display = ('nome', 'created_at', 'updated_at')
    search_fields = ('nome',)
    readonly_fields = ('created_at', 'updated_at')

@admin.register(Linha)
class LinhaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'created_at', 'updated_at')
    search_fields = ('nome',)
    readonly_fields = ('created_at', 'updated_at')

class ModuloInline(admin.TabularInline):
    model = Modulo
    extra = 1
    fields = ('nome', 'imagem_principal')

@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('ref_produto', 'nome_produto', 'id_tipo_produto', 'id_linha', 'ativo', 'created_at')
    list_filter = ('ativo', 'id_tipo_produto', 'id_linha', 'tem_cor_tecido')
    search_fields = ('ref_produto', 'nome_produto')
    readonly_fields = ('created_at', 'updated_at')
    inlines = [ModuloInline]
    
    fieldsets = (
        ('Informações Básicas', {
            'fields': ('ref_produto', 'nome_produto', 'id_tipo_produto', 'id_linha', 'ativo')
        }),
        ('Imagens', {
            'fields': ('imagem_principal', 'imagem_secundaria')
        }),
        ('Características', {
            'fields': ('tem_cor_tecido', 'tem_difer_desenho_lado_dir_esq', 'tem_difer_desenho_tamanho')
        }),
        ('Auditoria', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

@admin.register(Acessorio)
class AcessorioAdmin(admin.ModelAdmin):
    list_display = ('nome', 'created_at', 'updated_at')
    search_fields = ('nome',)
    readonly_fields = ('created_at', 'updated_at')

@admin.register(AcessoriosItens)
class AcessoriosItensAdmin(admin.ModelAdmin):
    list_display = ('id_acessorio', 'id_linha', 'created_at')
    list_filter = ('id_linha',)
    readonly_fields = ('created_at', 'updated_at')

@admin.register(Modulo)
class ModuloAdmin(admin.ModelAdmin):
    list_display = ('nome', 'item', 'created_at')
    list_filter = ('item__id_tipo_produto', 'item__id_linha')
    search_fields = ('nome', 'item__ref_produto', 'item__nome_produto')
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('Informações Básicas', {
            'fields': ('item', 'nome')
        }),
        ('Imagens', {
            'fields': ('imagem_principal', 'imagem_secundaria')
        }),
        ('Auditoria', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

@admin.register(TamanhosModulos)
class TamanhosModulosAdmin(admin.ModelAdmin):
    list_display = ('id_modulo', 'tamanho', 'created_at')
    list_filter = ('id_modulo__item__id_tipo_produto',)
    readonly_fields = ('created_at', 'updated_at')

@admin.register(FaixaTecido)
class FaixaTecidoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'valor_minimo', 'valor_maximo', 'created_at')
    readonly_fields = ('created_at', 'updated_at')

@admin.register(PrecosBase)
class PrecosBaseAdmin(admin.ModelAdmin):
    list_display = ('id_item', 'id_faixa_tecido', 'data_inic_vigencia', 'preco_base', 'created_at')
    list_filter = ('id_faixa_tecido', 'data_inic_vigencia')
    search_fields = ('id_item__ref_produto', 'id_item__nome_produto')
    readonly_fields = ('created_at', 'updated_at')

@admin.register(TamanhosModulosDetalhado)
class TamanhosModulosDetalhadoAdmin(admin.ModelAdmin):
    list_display = ('id_modulo', 'nome_tamanho', 'largura_total', 'largura_assento', 'peso_kg', 'preco', 'created_at')
    list_filter = ('id_modulo__item__id_tipo_produto',)
    search_fields = ('nome_tamanho', 'id_modulo__nome')
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('Informações Básicas', {
            'fields': ('id_modulo', 'nome_tamanho', 'descricao')
        }),
        ('Dimensões', {
            'fields': ('largura_total', 'largura_assento', 'altura_cm', 'profundidade_cm')
        }),
        ('Especificações', {
            'fields': ('tecido_metros', 'volume_m3', 'peso_kg', 'preco')
        }),
        ('Auditoria', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
