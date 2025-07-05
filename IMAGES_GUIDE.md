# Guia de Uso do Sistema de Imagens

## Visão Geral

O sistema de produtos agora suporta upload de imagens tanto para **produtos** quanto para **módulos**. Cada item pode ter uma imagem principal e uma imagem secundária.

## Características Implementadas

### 1. Campos de Imagem nos Modelos

#### Para Produtos (Item):
- `imagem_principal`: Imagem principal do produto
- `imagem_secundaria`: Imagem secundária do produto

#### Para Módulos:
- `imagem_principal`: Imagem principal do módulo
- `imagem_secundaria`: Imagem secundária do módulo

### 2. Estrutura de Diretórios

As imagens são salvas em:
```
media/
├── produtos/
│   ├── itens/          # Imagens dos produtos
│   └── modulos/        # Imagens dos módulos
```

### 3. Funcionalidades na Interface

#### Admin Django:
- Campos de upload de imagem nos formulários de produto e módulo
- Preview das imagens no admin
- Organização em fieldsets separados

#### Templates Web:
- **Cadastro**: Upload de imagens com preview em tempo real
- **Edição**: Visualização das imagens atuais e opção de substituição
- **Detalhes**: Exibição das imagens do produto e módulos em formato elegante
- **Lista**: Miniaturas das imagens na tabela de módulos

### 4. Validações e Segurança

- Aceita apenas arquivos de imagem (JPG, PNG, GIF)
- Limite recomendado de 5MB por arquivo
- Upload seguro através do Django

## Como Usar

### 1. Cadastrar Produto com Imagens

1. Acesse a página de cadastro de produtos
2. Preencha os dados básicos
3. Na seção "Imagens do Produto":
   - Selecione a **Imagem Principal**
   - Opcionalmente, selecione a **Imagem Secundária**
   - Visualize o preview das imagens antes de salvar
4. Para cada módulo:
   - Adicione o nome do módulo
   - Faça upload das imagens do módulo
   - Configure os tamanhos e especificações

### 2. Visualizar Imagens

- **Página de Detalhes**: Imagens são exibidas em seção dedicada
- **Lista de Módulos**: Miniaturas das imagens aparecem na primeira coluna
- **Admin Django**: Preview nas páginas de edição

### 3. Editar Imagens

1. Acesse a página de edição do produto
2. As imagens atuais são exibidas (se existirem)
3. Para substituir uma imagem:
   - Selecione um novo arquivo
   - A imagem anterior será substituída
4. Para remover uma imagem:
   - Deixe o campo vazio e salve

## Estrutura Técnica

### Migração Aplicada
```
0004_item_imagem_principal_item_imagem_secundaria_and_more.py
```

### Campos Adicionados
- `Item.imagem_principal` (ImageField)
- `Item.imagem_secundaria` (ImageField)
- `Modulo.imagem_principal` (ImageField)
- `Modulo.imagem_secundaria` (ImageField)

### Configurações do Django
- `MEDIA_URL = '/media/'`
- `MEDIA_ROOT = BASE_DIR / 'media'`
- URLs configuradas para servir arquivos de mídia em desenvolvimento

### Dependências
- **Pillow**: Biblioteca necessária para processamento de imagens (já incluída no requirements.txt)

## Exemplos de Uso da API

### Acessar URL da Imagem
```python
# Em um template
{% if produto.imagem_principal %}
    <img src="{{ produto.imagem_principal.url }}" alt="{{ produto.nome_produto }}">
{% endif %}

# Em uma view
if produto.imagem_principal:
    url_imagem = produto.imagem_principal.url
```

### Upload via Formulário
```html
<form method="post" enctype="multipart/form-data">
    {% csrf_token %}
    <input type="file" name="imagem_principal" accept="image/*">
    <input type="file" name="imagem_secundaria" accept="image/*">
    <button type="submit">Salvar</button>
</form>
```

## Recomendações

### Tamanhos de Imagem
- **Produtos**: 800x600px (proporção 4:3)
- **Módulos**: 400x300px (proporção 4:3)
- **Formato**: JPG para fotos, PNG para imagens com transparência

### Performance
- Otimize as imagens antes do upload
- Use ferramentas de compressão para reduzir o tamanho dos arquivos
- Considere implementar thumbnails automáticos para melhor performance

### Backup
- As imagens não são versionadas no Git (incluídas no .gitignore)
- Faça backup regular da pasta `media/`
- Considere usar um serviço de storage em nuvem para produção

## Solução de Problemas

### Erro "No module named 'PIL'"
```bash
pip install Pillow
```

### Imagens não aparecem
1. Verifique se `MEDIA_URL` e `MEDIA_ROOT` estão configurados
2. Confirme se as URLs de mídia estão incluídas no `urls.py`
3. Verifique as permissões da pasta `media/`

### Upload falha
1. Verifique o atributo `enctype="multipart/form-data"` no formulário
2. Confirme o limite de tamanho do arquivo
3. Verifique as permissões de escrita na pasta `media/`
