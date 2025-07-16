# Manual de Localização de Dados dos Produtos para Geração de Orçamentos

## Visão Geral

Este manual documenta onde encontrar todos os dados dos produtos exibidos na página de listagem de produtos, servindo como base para a implementação futura de um sistema de geração de orçamentos.

## Estrutura do Sistema

O sistema utiliza uma arquitetura híbrida com:
- **Tabela Principal**: `produtos_produto` (modelo `Produto`) - para dados básicos
- **Tabelas Específicas**: Para cada tipo de produto com dados detalhados
- **Tabelas de Apoio**: Para módulos, tamanhos, acessórios, etc.

## 1. Página de Listagem Principal

### 1.1 Localização
- **URL**: `/produtos/`
- **View**: `produtos_list_view` em `produtos/views.py` (linha 38)
- **Template**: `templates/produtos/lista.html`

### 1.2 Dados Exibidos na Listagem

#### Colunas da Tabela Principal:
1. **Referência** (`ref_produto`)
2. **Nome** (`nome_produto`)
3. **Tipo** (`id_tipo_produto.nome`)
4. **Módulos** (contagem de módulos relacionados)
5. **Status** (`ativo`)
6. **Criado em** (`created_at`)
7. **Criado por** (`created_by`)
8. **Ações** (Ver, Editar, Excluir)

## 2. Estrutura de Dados por Tipo de Produto

### 2.1 Produtos Básicos (Sofás)
**Tabela**: `produtos_produto`
**Modelo**: `Produto`
**Campos disponíveis**:
```python
# Dados básicos
ref_produto           # Referência única
nome_produto          # Nome do produto
id_tipo_produto       # FK para TipoItem
ativo                 # Status (True/False)
imagem_principal      # Imagem principal
imagem_secundaria     # Imagem secundária
created_at            # Data criação
created_by            # Usuário que criou
updated_at            # Data última modificação
updated_by            # Usuário que modificou

# Campos específicos para sofás
tem_cor_tecido                    # Boolean
tem_difer_desenho_lado_dir_esq    # Boolean
tem_difer_desenho_tamanho         # Boolean
```

### 2.2 Banquetas
**Tabela**: `produtos_banqueta`
**Modelo**: `Banqueta`
**Campos disponíveis**:
```python
# Identificação
ref_banqueta          # Referência única (Ex: BQ13, BQ249)
nome                  # Nome da banqueta (Ex: CERES, GIO)

# Dimensões
largura               # Decimal(10,2) em cm
profundidade          # Decimal(10,2) em cm
altura                # Decimal(10,2) em cm

# Especificações técnicas
tecido_metros         # Decimal(10,2) em metros
volume_m3             # Decimal(10,3) em m³
peso_kg               # Decimal(10,2) em kg
preco                 # Decimal(10,2) em R$

# Status e imagens
ativo                 # Boolean
imagem_principal      # ImageField
imagem_secundaria     # ImageField
descricao             # TextField
created_at            # Data criação
created_by            # Usuário que criou
```

### 2.3 Cadeiras
**Tabela**: `produtos_cadeira`
**Modelo**: `Cadeira`
**Campos disponíveis**:
```python
# Identificação
ref_cadeira           # Referência única (Ex: CD001, CD24)
nome                  # Nome da cadeira (Ex: EVA, FIT)

# Dimensões
largura               # Decimal(10,2) em cm
profundidade          # Decimal(10,2) em cm
altura                # Decimal(10,2) em cm

# Especificações técnicas
tecido_metros         # Decimal(10,2) em metros
volume_m3             # Decimal(10,3) em m³
peso_kg               # Decimal(10,2) em kg
preco                 # Decimal(10,2) em R$

# Status e recursos
ativo                 # Boolean
tem_cor_tecido        # Boolean
imagem_principal      # ImageField
imagem_secundaria     # ImageField
descricao             # TextField
created_at            # Data criação
created_by            # Usuário que criou
```

### 2.4 Poltronas
**Tabela**: `produtos_poltrona`
**Modelo**: `Poltrona`
**Campos disponíveis**:
```python
# Identificação
ref_poltrona          # Referência única (Ex: PL243, PL246)
nome                  # Nome da poltrona (Ex: ARIA, ARISTOCRATA)

# Dimensões
largura               # Decimal(10,2) em cm
profundidade          # Decimal(10,2) em cm
altura                # Decimal(10,2) em cm

# Especificações técnicas
tecido_metros         # Decimal(10,2) em metros
volume_m3             # Decimal(10,3) em m³
peso_kg               # Decimal(10,2) em kg
preco                 # Decimal(10,2) em R$

# Status e recursos
ativo                 # Boolean
tem_cor_tecido        # Boolean
imagem_principal      # ImageField
imagem_secundaria     # ImageField
descricao             # TextField
created_at            # Data criação
created_by            # Usuário que criou
```

### 2.5 Pufes
**Tabela**: `produtos_pufe`
**Modelo**: `Pufe`
**Campos disponíveis**:
```python
# Identificação
ref_pufe              # Referência única (Ex: PF13, PF249)
nome                  # Nome do pufe (Ex: ROUND, SQUARE)

# Dimensões
largura               # Decimal(10,2) em cm
profundidade          # Decimal(10,2) em cm
altura                # Decimal(10,2) em cm

# Especificações técnicas
tecido_metros         # Decimal(10,2) em metros
volume_m3             # Decimal(10,3) em m³
peso_kg               # Decimal(10,2) em kg
preco                 # Decimal(10,2) em R$

# Status e imagens
ativo                 # Boolean
imagem_principal      # ImageField
imagem_secundaria     # ImageField
descricao             # TextField
created_at            # Data criação
created_by            # Usuário que criou
```

### 2.6 Almofadas
**Tabela**: `produtos_almofada`
**Modelo**: `Almofada`
**Campos disponíveis**:
```python
# Identificação
ref_almofada          # Referência única (Ex: AL001, AL250)
nome                  # Nome da almofada (Ex: DECORATIVA, LOMBAR)

# Dimensões (SEM profundidade)
largura               # Decimal(10,2) em cm
altura                # Decimal(10,2) em cm

# Especificações técnicas
tecido_metros         # Decimal(10,2) em metros
volume_m3             # Decimal(10,3) em m³
peso_kg               # Decimal(10,2) em kg
preco                 # Decimal(10,2) em R$

# Status e imagens
ativo                 # Boolean
imagem_principal      # ImageField
imagem_secundaria     # ImageField
descricao             # TextField
created_at            # Data criação
created_by            # Usuário que criou
```

### 2.7 Acessórios
**Tabela**: `produtos_acessorio`
**Modelo**: `Acessorio`
**Campos disponíveis**:
```python
# Identificação
ref_acessorio         # Referência única
nome                  # Nome do acessório

# Especificações
preco                 # Decimal(10,2) em R$
descricao             # TextField
produtos_vinculados   # ManyToMany com Produto

# Status e imagens
ativo                 # Boolean
imagem_principal      # ImageField
imagem_secundaria     # ImageField
created_at            # Data criação
created_by            # Usuário que criou
```

## 3. Dados Relacionados (Para Sofás)

### 3.1 Módulos
**Tabela**: `produtos_modulo`
**Modelo**: `Modulo`
**Relacionamento**: `produto.modulos.all()`
**Campos disponíveis**:
```python
produto               # FK para Produto
nome                  # Nome do módulo
profundidade          # Decimal(10,2) em cm
altura                # Decimal(10,2) em cm
braco                 # Decimal(10,2) em cm
descricao             # TextField
imagem_principal      # ImageField
imagem_secundaria     # ImageField
```

### 3.2 Tamanhos Detalhados dos Módulos
**Tabela**: `produtos_tamanhosmodulosdetalhado`
**Modelo**: `TamanhosModulosDetalhado`
**Relacionamento**: `modulo.tamanhos_detalhados.all()`
**Campos disponíveis**:
```python
id_modulo             # FK para Modulo
largura_total         # Decimal(10,2) em cm
largura_assento       # Decimal(10,2) em cm
tecido_metros         # Decimal(10,2) em metros
volume_m3             # Decimal(10,3) em m³
peso_kg               # Decimal(10,2) em kg
preco                 # Decimal(10,2) em R$
descricao             # TextField
```

## 4. Consultas SQL Para Orçamento

### 4.1 Buscar Todos os Produtos da Listagem
```sql
-- Produtos básicos (sofás principalmente)
SELECT 
    p.id,
    p.ref_produto,
    p.nome_produto,
    tp.nome as tipo_produto,
    p.ativo,
    p.created_at,
    p.created_by_id,
    p.imagem_principal,
    p.imagem_secundaria
FROM produtos_produto p
JOIN produtos_tipoitem tp ON p.id_tipo_produto_id = tp.id
WHERE p.ativo = TRUE
ORDER BY p.ref_produto;

-- Banquetas
SELECT 
    b.id,
    b.ref_banqueta as referencia,
    b.nome,
    'Banquetas' as tipo_produto,
    b.largura,
    b.profundidade,
    b.altura,
    b.tecido_metros,
    b.volume_m3,
    b.peso_kg,
    b.preco,
    b.ativo,
    b.created_at,
    b.created_by_id,
    b.imagem_principal,
    b.imagem_secundaria,
    b.descricao
FROM produtos_banqueta b
WHERE b.ativo = TRUE
ORDER BY b.ref_banqueta;

-- Cadeiras
SELECT 
    c.id,
    c.ref_cadeira as referencia,
    c.nome,
    'Cadeiras' as tipo_produto,
    c.largura,
    c.profundidade,
    c.altura,
    c.tecido_metros,
    c.volume_m3,
    c.peso_kg,
    c.preco,
    c.ativo,
    c.tem_cor_tecido,
    c.created_at,
    c.created_by_id,
    c.imagem_principal,
    c.imagem_secundaria,
    c.descricao
FROM produtos_cadeira c
WHERE c.ativo = TRUE
ORDER BY c.ref_cadeira;

-- Poltronas
SELECT 
    p.id,
    p.ref_poltrona as referencia,
    p.nome,
    'Poltronas' as tipo_produto,
    p.largura,
    p.profundidade,
    p.altura,
    p.tecido_metros,
    p.volume_m3,
    p.peso_kg,
    p.preco,
    p.ativo,
    p.tem_cor_tecido,
    p.created_at,
    p.created_by_id,
    p.imagem_principal,
    p.imagem_secundaria,
    p.descricao
FROM produtos_poltrona p
WHERE p.ativo = TRUE
ORDER BY p.ref_poltrona;

-- Pufes
SELECT 
    p.id,
    p.ref_pufe as referencia,
    p.nome,
    'Pufes' as tipo_produto,
    p.largura,
    p.profundidade,
    p.altura,
    p.tecido_metros,
    p.volume_m3,
    p.peso_kg,
    p.preco,
    p.ativo,
    p.created_at,
    p.created_by_id,
    p.imagem_principal,
    p.imagem_secundaria,
    p.descricao
FROM produtos_pufe p
WHERE p.ativo = TRUE
ORDER BY p.ref_pufe;

-- Almofadas
SELECT 
    a.id,
    a.ref_almofada as referencia,
    a.nome,
    'Almofadas' as tipo_produto,
    a.largura,
    a.altura,
    a.tecido_metros,
    a.volume_m3,
    a.peso_kg,
    a.preco,
    a.ativo,
    a.created_at,
    a.created_by_id,
    a.imagem_principal,
    a.imagem_secundaria,
    a.descricao
FROM produtos_almofada a
WHERE a.ativo = TRUE
ORDER BY a.ref_almofada;

-- Acessórios
SELECT 
    a.id,
    a.ref_acessorio as referencia,
    a.nome,
    'Acessórios' as tipo_produto,
    a.preco,
    a.ativo,
    a.created_at,
    a.created_by_id,
    a.imagem_principal,
    a.imagem_secundaria,
    a.descricao
FROM produtos_acessorio a
WHERE a.ativo = TRUE
ORDER BY a.ref_acessorio;
```

### 4.2 Buscar Módulos e Tamanhos (Para Sofás)
```sql
-- Módulos de um produto específico
SELECT 
    m.id,
    m.nome,
    m.profundidade,
    m.altura,
    m.braco,
    m.descricao,
    m.imagem_principal,
    m.imagem_secundaria
FROM produtos_modulo m
WHERE m.produto_id = :produto_id
ORDER BY m.nome;

-- Tamanhos detalhados de um módulo específico
SELECT 
    t.id,
    t.largura_total,
    t.largura_assento,
    t.tecido_metros,
    t.volume_m3,
    t.peso_kg,
    t.preco,
    t.descricao
FROM produtos_tamanhosmodulosdetalhado t
WHERE t.id_modulo_id = :modulo_id
ORDER BY t.id;
```

### 4.3 Buscar Acessórios Vinculados
```sql
-- Acessórios vinculados a um produto específico
SELECT 
    a.id,
    a.ref_acessorio,
    a.nome,
    a.preco,
    a.descricao,
    a.imagem_principal
FROM produtos_acessorio a
JOIN produtos_acessorio_produtos_vinculados apv ON a.id = apv.acessorio_id
WHERE apv.produto_id = :produto_id
AND a.ativo = TRUE
ORDER BY a.ref_acessorio;
```

## 5. Queries Django (ORM)

### 5.1 Buscar Todos os Produtos para Listagem
```python
# View: produtos_list_view (linha 38 em produtos/views.py)
from produtos.models import Produto, Banqueta, Cadeira, Poltrona, Pufe, Almofada, Acessorio

# Produtos básicos (sofás principalmente)
produtos = Produto.objects.select_related('id_tipo_produto').all()

# Produtos das tabelas específicas
banquetas = Banqueta.objects.filter(ativo=True).all()
cadeiras = Cadeira.objects.filter(ativo=True).all()
poltronas = Poltrona.objects.filter(ativo=True).all()
pufes = Pufe.objects.filter(ativo=True).all()
almofadas = Almofada.objects.filter(ativo=True).all()
acessorios = Acessorio.objects.filter(ativo=True).all()
```

### 5.2 Buscar Produto com Todos os Dados
```python
# Para sofás (produtos básicos)
produto = Produto.objects.select_related('id_tipo_produto').get(id=produto_id)
modulos = produto.modulos.prefetch_related('tamanhos_detalhados').all()
acessorios_vinculados = Acessorio.objects.filter(produtos_vinculados=produto)

# Para banquetas
banqueta = Banqueta.objects.get(id=banqueta_id)

# Para cadeiras
cadeira = Cadeira.objects.get(id=cadeira_id)

# Para poltronas
poltrona = Poltrona.objects.get(id=poltrona_id)

# Para pufes
pufe = Pufe.objects.get(id=pufe_id)

# Para almofadas
almofada = Almofada.objects.get(id=almofada_id)

# Para acessórios
acessorio = Acessorio.objects.prefetch_related('produtos_vinculados').get(id=acessorio_id)
```

## 6. Campos Essenciais para Orçamento

### 6.1 Dados Obrigatórios para Todos os Produtos
- **Identificação**: referência, nome, tipo
- **Preço**: valor unitário
- **Status**: ativo/inativo
- **Imagens**: para apresentação visual

### 6.2 Dados Técnicos (Quando Disponíveis)
- **Dimensões**: largura, profundidade, altura
- **Especificações**: tecido_metros, volume_m3, peso_kg
- **Recursos**: tem_cor_tecido (para alguns tipos)

### 6.3 Dados Relacionados (Para Sofás)
- **Módulos**: nome, dimensões, imagens
- **Tamanhos**: largura_total, largura_assento, preços específicos
- **Acessórios**: produtos vinculados com preços

## 7. URLs de Detalhes por Tipo

### 7.1 URLs para Visualização Detalhada
```python
# Sofás
{% url 'sofa_detalhes' produto.id %}

# Banquetas
{% url 'banqueta_detalhes' banqueta.id %}

# Cadeiras
{% url 'cadeira_detalhes' cadeira.id %}

# Poltronas
{% url 'poltrona_detalhes' poltrona.id %}

# Pufes
{% url 'pufe_detalhes' pufe.id %}

# Almofadas
{% url 'almofada_detalhes' almofada.id %}

# Acessórios
{% url 'acessorio_detalhes' acessorio.id %}
```

### 7.2 URLs para Edição
```python
# Sofás
{% url 'sofa_editar' produto.id %}

# Banquetas
{% url 'banqueta_editar' banqueta.id %}

# Cadeiras
{% url 'cadeira_editar' cadeira.id %}

# Poltronas
{% url 'poltrona_editar' poltrona.id %}

# Pufes
{% url 'pufe_editar' pufe.id %}

# Almofadas
{% url 'almofada_editar' almofada.id %}

# Acessórios
{% url 'acessorio_editar' acessorio.id %}
```

## 8. Considerações para Implementação de Orçamento

### 8.1 Estrutura de Dados Recomendada
```python
# Exemplo de estrutura para item de orçamento
class ItemOrcamento:
    def __init__(self, produto_data):
        self.tipo = produto_data['tipo']           # 'sofa', 'banqueta', etc.
        self.referencia = produto_data['ref']      # Referência única
        self.nome = produto_data['nome']           # Nome do produto
        self.preco_unitario = produto_data['preco'] # Preço base
        self.quantidade = 1                        # Quantidade no orçamento
        self.dimensoes = produto_data.get('dimensoes', {})
        self.especificacoes = produto_data.get('specs', {})
        self.modulos = produto_data.get('modulos', [])     # Para sofás
        self.acessorios = produto_data.get('acessorios', []) # Acessórios vinculados
        self.imagem = produto_data.get('imagem_principal')
```

### 8.2 Funções Auxiliares Recomendadas
```python
def buscar_dados_produto(produto_id, tipo_produto):
    """Busca todos os dados necessários de um produto para orçamento"""
    
def calcular_preco_total(item_orcamento):
    """Calcula preço total incluindo módulos e acessórios"""
    
def formatar_dimensoes(produto):
    """Formata dimensões para exibição (L x P x A)"""
    
def verificar_disponibilidade(produto_id, tipo_produto):
    """Verifica se produto está ativo e disponível"""
```

### 8.3 Validações Importantes
- Verificar se produto está ativo antes de incluir no orçamento
- Validar se módulos e tamanhos existem (para sofás)
- Confirmar preços atualizados
- Verificar vinculações de acessórios

## 9. Exemplo de Implementação

### 9.1 Função para Buscar Produto Completo
```python
def buscar_produto_para_orcamento(produto_id, tipo_produto):
    """
    Busca todos os dados necessários de um produto para orçamento
    """
    produto_data = {}
    
    if tipo_produto.lower() == 'sofás':
        produto = Produto.objects.select_related('id_tipo_produto').get(id=produto_id)
        produto_data = {
            'id': produto.id,
            'tipo': 'sofa',
            'referencia': produto.ref_produto,
            'nome': produto.nome_produto,
            'ativo': produto.ativo,
            'imagem_principal': produto.imagem_principal.url if produto.imagem_principal else None,
            'modulos': []
        }
        
        # Buscar módulos e tamanhos
        for modulo in produto.modulos.all():
            modulo_data = {
                'id': modulo.id,
                'nome': modulo.nome,
                'profundidade': modulo.profundidade,
                'altura': modulo.altura,
                'braco': modulo.braco,
                'tamanhos': []
            }
            
            for tamanho in modulo.tamanhos_detalhados.all():
                tamanho_data = {
                    'id': tamanho.id,
                    'largura_total': tamanho.largura_total,
                    'largura_assento': tamanho.largura_assento,
                    'tecido_metros': tamanho.tecido_metros,
                    'volume_m3': tamanho.volume_m3,
                    'peso_kg': tamanho.peso_kg,
                    'preco': tamanho.preco,
                    'descricao': tamanho.descricao
                }
                modulo_data['tamanhos'].append(tamanho_data)
            
            produto_data['modulos'].append(modulo_data)
    
    elif tipo_produto.lower() == 'banquetas':
        banqueta = Banqueta.objects.get(id=produto_id)
        produto_data = {
            'id': banqueta.id,
            'tipo': 'banqueta',
            'referencia': banqueta.ref_banqueta,
            'nome': banqueta.nome,
            'largura': banqueta.largura,
            'profundidade': banqueta.profundidade,
            'altura': banqueta.altura,
            'tecido_metros': banqueta.tecido_metros,
            'volume_m3': banqueta.volume_m3,
            'peso_kg': banqueta.peso_kg,
            'preco': banqueta.preco,
            'ativo': banqueta.ativo,
            'imagem_principal': banqueta.imagem_principal.url if banqueta.imagem_principal else None,
            'descricao': banqueta.descricao
        }
    
    # Adicionar lógica similar para outros tipos...
    
    return produto_data
```

Este manual fornece uma visão completa de onde encontrar todos os dados necessários para implementar um sistema de geração de orçamentos baseado na listagem de produtos existente.
