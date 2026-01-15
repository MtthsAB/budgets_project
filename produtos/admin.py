from django.contrib import admin
from .models import (
    TipoItem, Produto, Acessorio, Banqueta, Cadeira, Poltrona, Pufe, Almofada,
    Modulo, TamanhosModulos, TamanhosModulosDetalhado, FaixaTecido, PrecosBase
)
from .forms import TamanhosModulosDetalhadoForm, ModuloForm

@admin.register(TipoItem)
class TipoItemAdmin(admin.ModelAdmin):
    list_display = ('nome', 'created_at')
    search_fields = ('nome',)
    readonly_fields = ('created_at', 'updated_at', 'created_by', 'updated_by')
    
    def has_delete_permission(self, request):
        return False  # Não permitir deletar tipos

class ModuloInline(admin.TabularInline):
    model = Modulo
    extra = 1
    fields = ('nome', 'profundidade', 'altura', 'braco', 'imagem_principal')

@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):
    list_display = ('get_tipo_display', 'ref_produto', 'nome_produto', 'ativo', 'created_at')
    list_filter = ('ativo', 'id_tipo_produto', 'created_by')
    search_fields = ('ref_produto', 'nome_produto', 'id_tipo_produto__nome')
    readonly_fields = ('created_at', 'updated_at', 'created_by', 'updated_by')
    inlines = [ModuloInline]
    
    def get_tipo_display(self, obj):
        """Exibir tipo com formatação"""
        return obj.id_tipo_produto.nome
    get_tipo_display.short_description = 'Tipo'

    def get_queryset(self, request):
        """Restringe o admin de Produto apenas a sofás."""
        qs = super().get_queryset(request)
        return qs.filter(id_tipo_produto__nome__icontains='Sofá')

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        """Limita a escolha do tipo de produto a sofás no admin."""
        if db_field.name == 'id_tipo_produto':
            kwargs['queryset'] = TipoItem.objects.filter(nome__icontains='Sofá')
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
    
    fieldsets = (
        ('Informações Básicas', {
            'fields': ('ref_produto', 'nome_produto', 'id_tipo_produto', 'ativo')
        }),
        ('Imagens', {
            'fields': ('imagem_principal', 'imagem_secundaria')
        }),
        ('Auditoria', {
            'fields': ('created_at', 'updated_at', 'created_by', 'updated_by'),
            'classes': ('collapse',)
        }),
    )


# Removido admin de Item (Deprecated)

@admin.register(Acessorio)
class AcessorioAdmin(admin.ModelAdmin):
    list_display = ('ref_acessorio', 'nome', 'ativo', 'preco', 'created_at')
    list_filter = ('ativo', 'created_by')
    search_fields = ('nome', 'ref_acessorio')
    readonly_fields = ('created_at', 'updated_at', 'created_by', 'updated_by')
    
    fieldsets = (
        ('Informações Básicas', {
            'fields': ('ref_acessorio', 'nome', 'ativo', 'descricao')
        }),
        ('Preço e Imagens', {
            'fields': ('preco', 'imagem_principal', 'imagem_secundaria')
        }),
        ('Auditoria', {
            'fields': ('created_at', 'updated_at', 'created_by', 'updated_by'),
            'classes': ('collapse',)
        }),
    )

@admin.register(Modulo)
class ModuloAdmin(admin.ModelAdmin):
    form = ModuloForm
    list_display = ('get_produto_display', 'nome', 'altura', 'profundidade', 'braco', 'created_at')
    list_filter = ('produto__id_tipo_produto', 'created_by')
    search_fields = ('nome', 'produto__ref_produto', 'produto__nome_produto')
    readonly_fields = ('created_at', 'updated_at', 'created_by', 'updated_by')
    
    def get_produto_display(self, obj):
        return f"{obj.produto.ref_produto} - {obj.produto.nome_produto}"
    get_produto_display.short_description = 'Produto'
    
    fieldsets = (
        ('Informações Básicas', {
            'fields': ('produto', 'nome', 'descricao')
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
    list_display = ('get_modulo_display', 'tamanho', 'created_at')
    list_filter = ('id_modulo__produto__id_tipo_produto', 'created_by')
    search_fields = ('id_modulo__nome', 'tamanho')
    readonly_fields = ('created_at', 'updated_at', 'created_by', 'updated_by')
    
    def get_modulo_display(self, obj):
        return f"{obj.id_modulo.produto.ref_produto} - {obj.id_modulo.nome}"
    get_modulo_display.short_description = 'Módulo'

@admin.register(FaixaTecido)
class FaixaTecidoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'valor_minimo', 'valor_maximo', 'created_at')
    list_filter = ('created_by',)
    search_fields = ('nome',)
    readonly_fields = ('created_at', 'updated_at', 'created_by', 'updated_by')

@admin.register(PrecosBase)
class PrecosBaseAdmin(admin.ModelAdmin):
    list_display = ('get_item_display', 'id_faixa_tecido', 'data_inic_vigencia', 'preco_base', 'created_at')
    list_filter = ('id_faixa_tecido', 'data_inic_vigencia', 'created_by')
    search_fields = ('id_item__ref_produto', 'id_item__nome_produto')
    readonly_fields = ('created_at', 'updated_at', 'created_by', 'updated_by')
    
    def get_item_display(self, obj):
        return f"{obj.id_item.ref_produto} - {obj.id_item.nome_produto}"
    get_item_display.short_description = 'Item'

@admin.register(TamanhosModulosDetalhado)
class TamanhosModulosDetalhadoAdmin(admin.ModelAdmin):
    form = TamanhosModulosDetalhadoForm
    list_display = ('get_modulo_display', 'largura_total', 'peso_kg', 'preco', 'created_at')
    list_filter = ('id_modulo__produto__id_tipo_produto', 'created_by')
    search_fields = ('id_modulo__nome', 'descricao')
    readonly_fields = ('created_at', 'updated_at', 'created_by', 'updated_by')
    
    def get_modulo_display(self, obj):
        return f"{obj.id_modulo.produto.ref_produto} - {obj.id_modulo.nome}"
    get_modulo_display.short_description = 'Módulo'
    
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

@admin.register(Poltrona)
class PoltronaAdmin(admin.ModelAdmin):
    list_display = ('ref_poltrona', 'nome', 'ativo', 'preco', 'created_at', 'created_by')
    list_filter = ('ativo', 'created_by', 'created_at')
    search_fields = ('ref_poltrona', 'nome')
    readonly_fields = ('created_at', 'updated_at', 'created_by', 'updated_by')
    
    fieldsets = (
        ('Informações Básicas', {
            'fields': ('ref_poltrona', 'nome', 'ativo', 'descricao')
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

@admin.register(Pufe)
class PufeAdmin(admin.ModelAdmin):
    list_display = ('ref_pufe', 'nome', 'ativo', 'largura', 'profundidade', 'altura', 'preco', 'created_at', 'created_by')
    list_filter = ('ativo', 'created_by', 'created_at')
    search_fields = ('ref_pufe', 'nome')
    readonly_fields = ('created_at', 'updated_at', 'created_by', 'updated_by')
    
    fieldsets = (
        ('Informações Básicas', {
            'fields': ('ref_pufe', 'nome', 'ativo', 'descricao')
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


@admin.register(Almofada)
class AlmofadaAdmin(admin.ModelAdmin):
    list_display = ('ref_almofada', 'nome', 'ativo', 'largura', 'altura', 'preco', 'created_at', 'created_by')
    list_filter = ('ativo', 'created_by', 'created_at')
    search_fields = ('ref_almofada', 'nome')
    readonly_fields = ('created_at', 'updated_at', 'created_by', 'updated_by')
    
    fieldsets = (
        ('Informações Básicas', {
            'fields': ('ref_almofada', 'nome', 'ativo', 'descricao')
        }),
        ('Dimensões', {
            'fields': ('largura', 'altura')  # Almofadas não têm profundidade
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
