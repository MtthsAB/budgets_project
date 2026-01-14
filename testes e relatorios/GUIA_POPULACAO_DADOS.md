# Script de População de Dados de Produtos

## 📋 Descrição

Script Django que popula o banco de dados com produtos (sofás, cadeiras, banquetas, poltronas, pufes e almofadas) a partir de uma estrutura de pasta com arquivos JSON e imagens.

## 📁 Estrutura de Pastas Esperada

```
dados_produtos/
├── infos/
│   ├── sofas/           # Arquivos JSON dos sofás
│   ├── cadeiras/        # Arquivos JSON das cadeiras
│   ├── banquetas/       # Arquivos JSON das banquetas
│   ├── poltronas/       # Arquivos JSON das poltronas
│   ├── PUFES/           # Arquivos JSON dos pufes
│   └── almofadas/       # Arquivos JSON das almofadas
└── fotos/
    ├── sofa/            # Imagens dos sofás
    ├── cadeiras/        # Imagens das cadeiras
    ├── banquetas/       # Imagens das banquetas
    ├── poltronas/       # Imagens das poltronas
    ├── PUFES/           # Imagens dos pufes
    └── almofadas/       # Imagens das almofadas
```

## 📝 Formato dos Arquivos JSON

### Cadeiras, Banquetas, Poltronas, Pufes, Almofadas

```json
{
  "ref_cadeira": "CD001",
  "nome": "EVA",
  "largura": 52.5,
  "profundidade": 45.0,
  "altura": 85.0,
  "tecido_metros": 1.5,
  "volume_m3": 0.2,
  "peso_kg": 8.5,
  "preco": 450.00,
  "ativo": true,
  "descricao": "Descrição do produto"
}
```

**Campos obrigatórios:**
- `ref_cadeira` (ref_banqueta, ref_poltrona, ref_pufe, ref_almofada): Referência única do produto
- `nome`: Nome do produto
- `largura`: Largura em cm
- `altura`: Altura em cm
- `profundidade`: Profundidade em cm (não para almofadas)
- `preco`: Preço em R$

**Campos opcionais:**
- `ativo`: true/false (padrão: true)
- `descricao`: Descrição textual
- `tem_cor_tecido`: true/false para cadeiras e poltronas
- `tecido_metros`: Metros de tecido necessários
- `volume_m3`: Volume para cálculo de frete
- `peso_kg`: Peso para cálculo de frete

### Sofás (Estrutura Completa)

```json
{
  "ref_produto": "SF939",
  "nome": "SOFÁ SF939",
  "tem_cor_tecido": true,
  "tem_difer_desenho_lado_dir_esq": true,
  "tem_difer_desenho_tamanho": false,
  "ativo": true,
  "modulos": [
    {
      "nome": "Assento",
      "profundidade": 90.0,
      "altura": 75.0,
      "braco": 25.0,
      "descricao": "Assento principal",
      "tamanhos": [
        {
          "largura_total": 180.0,
          "largura_assento": 150.0,
          "tecido_metros": 8.5,
          "volume_m3": 0.85,
          "peso_kg": 45.0,
          "preco": 2500.00
        }
      ]
    }
  ]
}
```

**Campos dos Sofás:**
- `ref_produto`: Referência única
- `nome`: Nome do sofá
- `tem_cor_tecido`: Tem variação de cor
- `tem_difer_desenho_lado_dir_esq`: Diferencia desenho esquerda/direita
- `tem_difer_desenho_tamanho`: Diferencia desenho por tamanho
- `modulos`: Array com os módulos do sofá

**Campos dos Módulos:**
- `nome`: Nome do módulo
- `profundidade`: Profundidade
- `altura`: Altura
- `braco`: Tamanho do braço (opcional)
- `tamanhos`: Array com os diferentes tamanhos

## 🖼️ Estrutura de Imagens

As imagens devem estar organizadas em subpastas com o nome do produto. O script automaticamente busca:

```
fotos/
├── cadeiras/
│   ├── CD001/
│   │   ├── 1.jpg (imagem principal)
│   │   └── 2.jpg (imagem secundária)
│   └── CD24/
│       └── 1.jpg
```

**Formatos suportados:** JPG, JPEG, PNG

## 🚀 Como Usar

### Opção 1: Popular Todos os Dados

```bash
python manage.py popular_dados_produtos --pasta /caminho/para/dados_produtos
```

### Opção 2: Popular Apenas um Tipo

```bash
# Apenas cadeiras
python manage.py popular_dados_produtos --pasta /caminho/para/dados_produtos --tipo cadeiras

# Apenas sofás
python manage.py popular_dados_produtos --pasta /caminho/para/dados_produtos --tipo sofas

# Tipos válidos: sofas, cadeiras, banquetas, poltronas, pufes, almofadas, todos
```

### Opção 3: Com Docker Compose

```bash
cd /caminho/para/budgets_project
docker compose exec app python manage.py popular_dados_produtos --pasta /caminho/para/dados_produtos
```

## 📊 Exemplos de Dados

Arquivos de exemplo estão em `testes e relatorios/`:
- `exemplo_cadeira.json`
- `exemplo_banqueta.json`
- `exemplo_almofada.json`
- `exemplo_sofa.json`

## ✅ Validações

O script realiza validações automáticas:

1. **Dimensões positivas** - Largura, profundidade, altura > 0
2. **Preço positivo** - Preço > 0
3. **Referência única** - Cada produto tem uma referência única
4. **Imagens opcionais** - O script continua mesmo sem encontrar imagens

## 📋 Log e Saída

O script exibe:
- ✨ CRIADO - Novo produto inserido
- 🔄 ATUALIZADO - Produto existente atualizado
- ⚠️ Avisos - Pastas não encontradas
- ❌ Erros - Problemas na leitura de arquivos

## 🔍 Troubleshooting

### Erro: "Pasta não encontrada"
- Verifique o caminho fornecido
- Confirme que a pasta existe no servidor/máquina local

### Erro: "Pasta deve conter subpastas 'infos' e 'fotos'"
- A estrutura deve ter exatamente estas subpastas
- Verifique a case (maiúsculas/minúsculas) das pastas

### Imagens não aparecem
- Imagens devem estar em subpastas com nome do produto
- Formatos suportados: JPG, JPEG, PNG
- As imagens serão armazenadas em `media/produtos/`

### Erro ao salvar produto
- Verifique se todos os campos obrigatórios estão no JSON
- Confirme que valores numéricos usam decimal (ex: 45.0, não 45)

## 📝 Próximos Passos

1. Coloque os arquivos JSON em `dados_produtos/infos/{tipo}/`
2. Coloque as imagens em `dados_produtos/fotos/{tipo}/`
3. Execute o comando com o caminho correto
4. Verifique o log para confirmar importação

## 🤝 Suporte

Se encontrar problemas:
1. Verifique o formato dos JSONs com `json.tool`
2. Confirme caminhos absolutos
3. Veja os logs em `testes e relatorios/`

---

**Criado em:** Janeiro 2026
**Versão:** 1.0
