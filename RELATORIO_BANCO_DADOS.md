# RELATÓRIO DETALHADO DA ESTRUTURA DO BANCO DE DADOS POSTGRESQL
## Sistema de Produtos - Análise Completa

**Data do Relatório:** 19/07/2025  
**Banco de Dados:** PostgreSQL  
**Sistema:** Django 5.2.4  

---

## 1. VISÃO GERAL DO SISTEMA

O sistema de produtos é composto por **4 aplicações principais**:

1. **authentication** - Gestão de usuários e permissões
2. **produtos** - Catálogo de produtos (sofás, acessórios, cadeiras, etc.)
3. **clientes** - Cadastro de clientes empresariais
4. **orcamentos** - Sistema de orçamentos e vendas

**Total de tabelas:** 19 tabelas principais + tabelas auxiliares do Django

---

## 2. MAPEAMENTO COMPLETO DAS TABELAS

### 2.1. MÓDULO DE AUTENTICAÇÃO

#### `authentication_customuser`
**Descrição:** Usuários do sistema com permissões hierárquicas
**Campos principais:**
- `id` (BigAutoField) - Chave primária
- `email` (EmailField, UNIQUE) - Login do usuário
- `first_name`, `last_name` (CharField) - Nome completo
- `tipo_permissao` (CharField) - Níveis: master, admin, vendedor, operador_produtos
- `is_active`, `is_staff` (BooleanField) - Status
- **Auditoria:** `created_at`, `updated_at`, `created_by`, `updated_by`

**Constraints:**
- UNIQUE: email
- CHOICES: tipo_permissao (master, admin, vendedor, operador_produtos)

---

### 2.2. MÓDULO DE PRODUTOS

#### `produtos_tipoitem`
**Descrição:** Categorias de produtos (Sofás, Acessórios, Cadeiras, etc.)
**Campos:**
- `id` (BigAutoField) - PK
- `nome` (CharField, max_length=100) - Nome da categoria
- **Auditoria:** `created_at`, `updated_at`, `created_by`, `updated_by`

#### `produtos_produto` ⭐ **TABELA PRINCIPAL DE PRODUTOS**
**Descrição:** Produto base - informações básicas (principalmente sofás)
**Campos:**
- `id` (BigAutoField) - PK
- `ref_produto` (CharField, UNIQUE, max_length=50) - Referência única
- `nome_produto` (CharField, max_length=200) - Nome do produto
- `id_tipo_produto` (ForeignKey → TipoItem) - Categoria
- `ativo` (BooleanField) - Status ativo/inativo
- `imagem_principal`, `imagem_secundaria` (ImageField) - Imagens
- **Campos específicos para sofás:**
  - `tem_cor_tecido` (BooleanField) - Se permite escolha de cor
  - `tem_difer_desenho_lado_dir_esq` (BooleanField) - Diferenciação direita/esquerda
  - `tem_difer_desenho_tamanho` (BooleanField) - Desenho varia por tamanho

#### `produtos_modulo`
**Descrição:** Módulos de sofás (ex: canto, chaise, poltrona)
**Campos:**
- `id` (BigAutoField) - PK
- `produto` (ForeignKey → Produto) - Produto pai
- `nome` (CharField, max_length=100) - Nome do módulo
- `profundidade`, `altura`, `braco` (DecimalField) - Dimensões básicas
- `imagem_principal`, `imagem_secundaria` (ImageField) - Imagens

**Relacionamento:** 1 Produto → N Módulos

#### `produtos_tamanhosmodulosdetalhado`
**Descrição:** Tamanhos específicos de cada módulo com preços e especificações
**Campos:**
- `id` (BigAutoField) - PK
- `id_modulo` (ForeignKey → Modulo) - Módulo pai
- `largura_total`, `largura_assento` (DecimalField) - Dimensões
- `tecido_metros` (DecimalField) - Quantidade de tecido
- `volume_m3`, `peso_kg` (DecimalField) - Para frete
- `preco` (DecimalField) - Preço específico

**Relacionamento:** 1 Módulo → N Tamanhos

#### `produtos_acessorio`
**Descrição:** Acessórios disponíveis para produtos
**Campos:**
- `id` (BigAutoField) - PK
- `ref_acessorio` (CharField, UNIQUE) - Referência
- `nome` (CharField, max_length=100)
- `preco` (DecimalField, NULLABLE) - Preço
- `produtos_vinculados` (ManyToManyField → Produto) - Produtos compatíveis

### 2.3. PRODUTOS ESPECÍFICOS (Modelos separados)

#### `produtos_cadeira`
**Descrição:** Cadeiras com especificações completas
**Campos dimensionais:**
- `largura`, `profundidade`, `altura` (DecimalField)
- `tecido_metros`, `volume_m3`, `peso_kg` (DecimalField)
- `preco` (DecimalField)
- `tem_cor_tecido` (BooleanField)

#### `produtos_poltrona`
**Estrutura idêntica às cadeiras**

#### `produtos_banqueta`
**Estrutura similar, sem `tem_cor_tecido`**

#### `produtos_pufe`
**Estrutura similar às banquetas**

#### `produtos_almofada`
**Diferencial:** Apenas `largura` e `altura` (sem profundidade)

#### `produtos_item` ⚠️ **DEPRECATED**
**Descrição:** Modelo antigo mantido para compatibilidade
**Status:** A ser removido após migração completa

---

### 2.4. MÓDULO DE CLIENTES

#### `clientes_cliente`
**Descrição:** Dados completos de clientes empresariais
**Campos empresariais:**
- `nome_empresa` (CharField, max_length=200) - Razão social
- `representante` (CharField, max_length=150) - Nome do contato
- `cnpj` (CharField, UNIQUE) - CNPJ formatado
- `inscricao_estadual`, `inscricao_municipal` (CharField, NULLABLE)

**Endereço completo:**
- `logradouro`, `numero`, `complemento`, `bairro`
- `cidade`, `estado` (UF), `cep`

**Contato:**
- `telefone`, `email`

**Dados bancários (opcionais):**
- `banco`, `agencia`, `conta_corrente`

**Validações:**
- CNPJ: formato 00.000.000/0000-00
- CEP: formato 00000-000

---

### 2.5. MÓDULO DE ORÇAMENTOS

#### `orcamentos_faixapreco`
**Descrição:** Faixas de preço com multiplicadores
**Campos:**
- `nome` (CharField) - Nome da faixa
- `multiplicador` (DecimalField) - Ex: 1.20 = 120%
- `ativo` (BooleanField)

#### `orcamentos_formapagamento`
**Descrição:** Formas de pagamento disponíveis
**Campos:**
- `nome` (CharField) - Ex: "À vista", "30 dias"
- `prazo_dias` (IntegerField) - Prazo padrão
- `desconto_maximo` (DecimalField) - % máximo de desconto

#### `orcamentos_orcamento` ⭐ **TABELA PRINCIPAL DE ORÇAMENTOS**
**Descrição:** Cabeçalho do orçamento
**Campos principais:**
- `numero` (CharField, UNIQUE) - Número automático
- `cliente` (ForeignKey → Cliente) - Cliente
- `vendedor` (ForeignKey → CustomUser) - Vendedor responsável
- `faixa_preco` (ForeignKey → FaixaPreco) - Faixa aplicada
- `forma_pagamento` (ForeignKey → FormaPagamento)

**Ajustes financeiros:**
- `desconto_valor`, `desconto_percentual` (DecimalField)
- `acrescimo_valor`, `acrescimo_percentual` (DecimalField)

**Datas:**
- `data_entrega`, `data_validade` (DateField)

**Status:**
- `status` (CharField) - rascunho, enviado, aprovado, rejeitado, expirado

#### `orcamentos_orcamentoitem`
**Descrição:** Itens do orçamento
**Campos:**
- `orcamento` (ForeignKey → Orcamento) - Orçamento pai
- `produto` (ForeignKey → Produto) - Produto selecionado
- `quantidade` (PositiveIntegerField) - Quantidade
- `preco_unitario` (DecimalField) - Preço já com faixa aplicada
- `dados_produto` (JSONField) - Dados específicos (cor, tamanho, etc.)

#### `orcamentos_orcamentomodulo`
**Descrição:** Módulos específicos de sofás no orçamento
**Campos:**
- `item_orcamento` (ForeignKey → OrcamentoItem) - Item pai
- `modulo_id` (PositiveIntegerField) - ID do módulo original
- `nome_modulo` (CharField) - Nome copiado
- `tamanho_selecionado` (CharField) - Tamanho escolhido

---

## 3. RELACIONAMENTOS DETALHADOS

### 3.1. Fluxo Principal de Produtos (Sofás)

```
TipoItem (1) ←── (N) Produto (1) ←── (N) Modulo (1) ←── (N) TamanhosModulosDetalhado
    ↓                    ↑
"Sofás"               Acessorio (N) ←──→ (N) produtos_vinculados
```

### 3.2. Fluxo de Orçamentos

```
Cliente (1) ←── (N) Orcamento ──→ (N) OrcamentoItem
                    ↑                      ↓
            FaixaPreco (1)           (1) Produto
            FormaPagamento (1)             ↓
            CustomUser (vendedor)    OrcamentoModulo (N)
```

### 3.3. Estrutura de Auditoria (BaseModel)

**Todos os modelos herdam:**
```
BaseModel:
  - created_at (DateTimeField)
  - updated_at (DateTimeField)  
  - created_by (ForeignKey → CustomUser)
  - updated_by (ForeignKey → CustomUser)
```

---

## 4. EXEMPLOS PRÁTICOS

### 4.1. Exemplo: Sofá Completo

**Produto:** SF939 - LE COULTRE
```sql
-- Produto base
produtos_produto:
  id: 1
  ref_produto: "SF939"
  nome_produto: "LE COULTRE"
  id_tipo_produto: 1 (Sofás)
  tem_cor_tecido: true
  tem_difer_desenho_tamanho: true

-- Módulos disponíveis  
produtos_modulo:
  id: 1, produto_id: 1, nome: "CANTO DIREITO"
  id: 2, produto_id: 1, nome: "CANTO ESQUERDO"
  id: 3, produto_id: 1, nome: "MEIO SEM BRAÇO"

-- Tamanhos de cada módulo
produtos_tamanhosmodulosdetalhado:
  id: 1, id_modulo: 1, largura_total: 167, preco: 2500.00
  id: 2, id_modulo: 1, largura_total: 187, preco: 2800.00
  id: 3, id_modulo: 2, largura_total: 167, preco: 2500.00
```

### 4.2. Exemplo: Orçamento Completo

**Orçamento:** ORC-202507-0001
```sql
-- Cabeçalho
orcamentos_orcamento:
  numero: "ORC-202507-0001"
  cliente_id: 1 (Empresa XYZ)
  vendedor_id: 2 (João Silva)
  faixa_preco_id: 1 (Varejo - 1.00x)
  
-- Item do orçamento
orcamentos_orcamentoitem:
  orcamento_id: 1
  produto_id: 1 (SF939)
  quantidade: 1
  preco_unitario: 5300.00
  dados_produto: {"cor": "bege", "tecido": "linho"}

-- Módulos selecionados
orcamentos_orcamentomodulo:
  item_orcamento_id: 1
  modulo_id: 1
  nome_modulo: "CANTO DIREITO"
  tamanho_selecionado: "167cm"
```

### 4.3. Exemplo: Cliente Empresarial

```sql
clientes_cliente:
  nome_empresa: "MÓVEIS CASA LTDA"
  cnpj: "12.345.678/0001-99"
  representante: "Maria Santos"
  logradouro: "Rua das Flores"
  numero: "123"
  cidade: "São Paulo"
  estado: "SP"
```

---

## 5. ANÁLISE DE PROBLEMAS E INCONSISTÊNCIAS

### 5.1. ⚠️ PROBLEMAS IDENTIFICADOS

#### **Duplicação de Modelos:**
- **produtos_produto** vs **produtos_item**: Dois modelos similares causam confusão
- **Recomendação:** Finalizar migração e remover `produtos_item`

#### **Inconsistência de Estrutura:**
- Sofás usam **Produto + Módulos** (complexo)
- Cadeiras/Poltronas usam **modelos específicos** (simples)
- **Problema:** Dificuldade de unificar relatórios e buscas

#### **Campos Opcionais Demais:**
- Muitos campos com `NULL=True, BLANK=True`
- **Risco:** Dados incompletos afetarem cálculos

#### **Falta de Constraints:**
- Preços sem validação mínima
- Dimensões sem validação positiva no DB

### 5.2. ✅ PONTOS POSITIVOS

#### **Auditoria Completa:**
- Todos os modelos têm rastreamento de criação/modificação

#### **Flexibilidade:**
- JSONField permite dados específicos por produto
- Relacionamentos ManyToMany para acessórios

#### **Escalabilidade:**
- Estrutura permite novos tipos de produtos

---

## 6. RECOMENDAÇÕES PARA MELHORIAS

### 6.1. **Curto Prazo:**
1. **Finalizar migração:** Remover modelo `Item` deprecated
2. **Adicionar constraints:** Validações de preço > 0, dimensões > 0
3. **Padronizar campos:** Tornar obrigatórios os campos essenciais

### 6.2. **Médio Prazo:**
1. **Unificar estrutura:** Considerar modelo único para todos os produtos
2. **Melhorar performance:** Índices em campos de busca frequente
3. **Validações avançadas:** Constraints de negócio no banco

### 6.3. **Longo Prazo:**
1. **Histórico de preços:** Versionamento de alterações
2. **Cache inteligente:** Para cálculos complexos de orçamentos
3. **Analytics:** Tabelas de relatórios pré-calculados

---

## 7. QUERIES ÚTEIS PARA MANUTENÇÃO

### 7.1. Verificar Produtos sem Preço:
```sql
SELECT ref_produto, nome_produto 
FROM produtos_produto p
LEFT JOIN produtos_tamanhosmodulosdetalhado t ON p.id = t.id_modulo
WHERE t.preco IS NULL;
```

### 7.2. Orçamentos por Status:
```sql
SELECT status, COUNT(*) as total, SUM(subtotal) as valor_total
FROM orcamentos_orcamento 
GROUP BY status;
```

### 7.3. Produtos mais Orçados:
```sql
SELECT p.ref_produto, p.nome_produto, COUNT(*) as vezes_orcado
FROM produtos_produto p
JOIN orcamentos_orcamentoitem oi ON p.id = oi.produto_id
GROUP BY p.id, p.ref_produto, p.nome_produto
ORDER BY vezes_orcado DESC;
```

---

**Conclusão:** O banco está bem estruturado para as necessidades atuais, mas precisa de consolidação dos modelos duplicados e melhorias nas validações para maior robustez futura.
