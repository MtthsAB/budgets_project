# Seção de Imagens Reutilizável

## 📁 Localização
`templates/produtos/includes/secao_imagens.html`

## 🎯 Propósito
Template reutilizável para upload de imagens em todos os produtos (cadeiras, banquetas, sofás, etc.).

## 🔧 Como Usar

### Em qualquer template de produto:
```html
<!-- Incluir a seção de imagens -->
{% include 'produtos/includes/secao_imagens.html' with objeto=produto_objeto %}
```

### Exemplos por tipo de produto:
```html
<!-- Para Cadeiras -->
{% include 'produtos/includes/secao_imagens.html' with objeto=cadeira %}

<!-- Para Banquetas -->
{% include 'produtos/includes/secao_imagens.html' with objeto=banqueta %}

<!-- Para Sofás -->
{% include 'produtos/includes/secao_imagens.html' with objeto=None %}

<!-- Para novos produtos -->
{% include 'produtos/includes/secao_imagens.html' with objeto=produto %}
```

## ✨ Funcionalidades Incluídas

### 🖼️ Upload de Imagens
- **Imagem Principal**: Campo obrigatório com preview
- **Segunda Imagem**: Campo opcional com botão "+"

### 🎨 Interface
- Card azul com bordas arredondadas
- Botão circular para adicionar segunda imagem
- Preview das imagens atuais (em modo edição)
- Mensagens de validação de erro

### 📱 JavaScript
- `mostrarSegundaImagem()`: Mostra campo da segunda imagem
- `previewImage()`: Preview de imagens selecionadas
- `removeImage()`: Remove imagens selecionadas

### 🎨 CSS
- Estilos para botão de adicionar imagem
- Animações hover
- Responsividade mobile

## 📋 Requisitos

### No formulário (form):
```python
# Campos obrigatórios no modelo
imagem_principal = models.ImageField()
imagem_secundaria = models.ImageField(blank=True, null=True)
```

### No template pai:
```html
<form method="post" enctype="multipart/form-data">
    {% csrf_token %}
    <!-- outros campos -->
    
    {% include 'produtos/includes/secao_imagens.html' with objeto=objeto %}
</form>
```

## 🔄 Migração de Templates Existentes

### ❌ Antes (duplicado):
```html
<!-- Seção de imagens copiada em cada template -->
<div class="card border-primary">
    <div class="card-header bg-primary text-white">
        <h5>Imagens do Produto</h5>
    </div>
    <!-- ... resto da seção ... -->
</div>
```

### ✅ Depois (reutilizável):
```html
<!-- Uma linha simples -->
{% include 'produtos/includes/secao_imagens.html' with objeto=produto %}
```

## 🎯 Benefícios

1. **Consistência**: Mesma interface em todos os produtos
2. **Manutenibilidade**: Alterar uma vez, atualiza todos
3. **Reutilização**: Funciona para qualquer tipo de produto
4. **Menos código**: Reduz duplicação massivamente

## 📝 Templates Atualizados
- ✅ `templates/produtos/cadeiras/cadastro.html`
- ✅ `templates/produtos/banquetas/cadastro.html`
- ✅ `templates/produtos/sofas/cadastro.html`
- 🎯 Pronto para novos produtos!
