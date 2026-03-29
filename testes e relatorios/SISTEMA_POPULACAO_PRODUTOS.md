# 📦 Sistema Completo de População de Produtos

## ✅ O que foi criado

Criei um **sistema completo e robusto** para popular seus dados de produtos no banco de dados. O sistema suporta:

### ✨ Tipos de Produtos Suportados
- 🛋️ **Sofás** (com módulos e tamanhos específicos)
- 🪑 **Cadeiras** (com variação de cores)
- 🪑 **Banquetas**
- 🪑 **Poltronas** (com variação de cores)
- 🎁 **Pufes**
- 🏠 **Almofadas** (2 dimensões apenas)

### 📁 Arquivos Criados

#### 1. **Management Commands**
- [`produtos/management/commands/popular_produtos_csv.py`](produtos/management/commands/popular_produtos_csv.py) - Comando Django para popular os dados
- [`testes e relatorios/teste_populacao.py`](testes%20e%20relatorios/teste_populacao.py) - Ferramenta para gerar dados de exemplo e validar estrutura
- [`testes e relatorios/converter_csv_json.py`](testes%20e%20relatorios/converter_csv_json.py) - Conversor de CSV para JSON

#### 2. **Documentação**
- [`QUICK_START_POPULACAO.md`](QUICK_START_POPULACAO.md) - Guia rápido (comece daqui!)
- [`testes e relatorios/GUIA_POPULACAO_DADOS.md`](testes%20e%20relatorios/GUIA_POPULACAO_DADOS.md) - Documentação completa
- [`testes e relatorios/exemplo_*.json`](testes%20e%20relatorios/) - Exemplos de JSONs para cada tipo

#### 3. **Arquivos de Exemplo**
```
testes e relatorios/
├── exemplo_cadeira.json      # Exemplo de estrutura de cadeira
├── exemplo_banqueta.json     # Exemplo de estrutura de banqueta
├── exemplo_almofada.json     # Exemplo de estrutura de almofada
└── exemplo_sofa.json         # Exemplo de estrutura de sofá com módulos
```

---

## 🚀 Como Usar

### **OPÇÃO 1: Testar com Dados de Exemplo (RECOMENDADO)**

```bash
# 1️⃣ Gerar dados de exemplo
python3 "testes e relatorios/teste_populacao.py" --gerar-exemplo /tmp/dados_teste

# 2️⃣ Validar estrutura gerada
python3 "testes e relatorios/teste_populacao.py" --validar /tmp/dados_teste

# 3️⃣ Popular no banco (com Docker)
docker compose exec app python manage.py popular_produtos_csv --pasta /tmp/dados_teste

# ✅ Pronto! Acesse http://localhost:8000/admin para ver seus produtos
```

### **OPÇÃO 2: Usar Seus Próprios Dados**

#### Passo 1: Organizar Arquivos
```
seus_dados/
├── infos/
│   ├── sofas/       ← Coloque aqui sofas.json, sf939.json, etc
│   ├── cadeiras/    ← Coloque aqui cadeiras.json, cd001.json, etc
│   ├── banquetas/   ← Coloque aqui banquetas.json, bq13.json, etc
│   ├── poltronas/   ← Coloque aqui poltronas.json, pl243.json, etc
│   ├── PUFES/       ← Coloque aqui pufes.json, pf13.json, etc
│   └── almofadas/   ← Coloque aqui almofadas.json, al001.json, etc
└── fotos/
    ├── sofas/       ← Subpastas com nome do produto (SF939/, LE_COULTRE/)
    ├── cadeiras/    ← Subpastas com nome do produto (CD001/, CD24/)
    └── ... (mesma estrutura para os outros)
```

#### Passo 2 (Opcional): Converter de CSV

Se você tem dados em CSV:

```bash
python3 "testes e relatorios/converter_csv_json.py" \
  --entrada seus_dados.csv \
  --saida seus_dados/infos/cadeiras \
  --tipo cadeiras
```

#### Passo 3: Validar e Popular

```bash
# Validar antes
python3 "testes e relatorios/teste_populacao.py" --validar seus_dados/

# Popular
docker compose exec app python manage.py popular_produtos_csv --pasta seus_dados/
```

---

## 📋 Formato dos Dados

### Cadeira / Banqueta / Poltrona / Pufe

```json
{
  "ref_cadeira": "CD001",           // Identificador único
  "nome": "EVA",                     // Nome do produto
  "largura": 52.5,                   // em cm
  "profundidade": 45.0,              // em cm
  "altura": 85.0,                    // em cm
  "tecido_metros": 1.5,              // Quantos metros de tecido
  "volume_m3": 0.2,                  // Para calcular frete
  "peso_kg": 8.5,                    // Para calcular frete
  "preco": 450.00,                   // Preço em R$
  "ativo": true,                     // true/false
  "tem_cor_tecido": false,           // (opcional, para cadeiras/poltronas)
  "descricao": "Cadeira moderna"     // (opcional)
}
```

### Almofada (sem profundidade)

```json
{
  "ref_almofada": "AL001",
  "nome": "DECORATIVA 40x40",
  "largura": 40.0,
  "altura": 40.0,
  "tecido_metros": 0.3,
  "volume_m3": 0.02,
  "peso_kg": 0.8,
  "preco": 89.90,
  "ativo": true
}
```

### Sofá (com módulos)

```json
{
  "ref_produto": "SF939",
  "nome": "SOFÁ SF939",
  "tem_cor_tecido": true,
  "tem_difer_desenho_lado_dir_esq": true,  // Diferencia esquerda/direita
  "tem_difer_desenho_tamanho": false,      // Diferencia por tamanho
  "ativo": true,
  "modulos": [
    {
      "nome": "Assento",
      "profundidade": 90.0,
      "altura": 75.0,
      "braco": 25.0,
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

---

## 🖼️ Estrutura de Imagens

As imagens devem estar em **subpastas com o nome do produto**:

```
fotos/
└── cadeiras/
    ├── CD001/
    │   ├── 1.jpg    ← Será a imagem principal
    │   ├── 2.jpg    ← Será a imagem secundária
    │   └── ...
    ├── CD24/
    │   └── 1.jpg
    └── ...
```

**Importante:**
- A 1ª imagem se torna a imagem principal
- A 2ª imagem se torna a imagem secundária
- Formatos suportados: JPG, JPEG, PNG
- As imagens serão salvas em `media/produtos/`

---

## ⚙️ Opções de Linha de Comando

### Popular Todos os Dados
```bash
docker compose exec app python manage.py popular_produtos_csv --pasta /caminho/dados
```

### Popular Apenas um Tipo
```bash
# Apenas cadeiras
docker compose exec app python manage.py popular_produtos_csv --pasta /caminho/dados --tipo cadeiras

# Apenas sofás
docker compose exec app python manage.py popular_produtos_csv --pasta /caminho/dados --tipo sofas

# Tipos válidos: sofas, cadeiras, banquetas, poltronas, pufes, almofadas, todos
```

---

## ✅ Checklist Antes de Popular

- [ ] Arquivos JSON têm formato válido (use teste_populacao.py --validar)
- [ ] Pastas `infos/` e `fotos/` existem
- [ ] Todos os campos obrigatórios estão preenchidos
- [ ] Valores numéricos usam ponto decimal (45.0, não 45)
- [ ] Imagens estão em subpastas com nome do produto
- [ ] Caminhos são absolutos (/home/matas/dados, não ~/dados)

---

## 🔍 Validação

O script valida automaticamente:

✅ **Dimensões** - Deve ser maior que zero  
✅ **Preços** - Deve ser maior que zero  
✅ **Referência** - Deve ser única por produto  
✅ **Formato JSON** - Deve ser válido UTF-8  
✅ **Valores decimais** - Pode usar vírgula ou ponto  

---

## 📊 Exemplo Completo do Fluxo

```bash
# 1. Criar estrutura de exemplo
python3 "testes e relatorios/teste_populacao.py" \
  --gerar-exemplo ~/produtos_para_importar

# 2. Validar estrutura
python3 "testes e relatorios/teste_populacao.py" \
  --validar ~/produtos_para_importar

# 3. Popular no Docker
docker compose exec app python manage.py popular_produtos_csv \
  --pasta ~/produtos_para_importar

# 4. Ver resultado
# Acesse http://localhost:8000/admin/produtos/

# 5. (Opcional) Popular apenas um tipo
docker compose exec app python manage.py popular_produtos_csv \
  --pasta ~/produtos_para_importar \
  --tipo sofas
```

---

## 🎯 Características do Sistema

### 🔒 Segurança
- Validação de todos os dados
- Previne duplicação com campos unique
- Transações atômicas (tudo ou nada)

### 📈 Performance
- Usa batch operations
- Processa múltiplos arquivos
- Cache eficiente

### 🛠️ Flexibilidade
- Suporta múltiplos formatos de referência
- Procura imagens com flexibilidade de nomes
- Campos opcionais quando apropriado

### 📊 Rastreabilidade
- Log detalhado de cada operação
- Indica o que foi criado vs atualizado
- Mostra erros com contexto

---

## 🆘 Troubleshooting

| Problema | Solução |
|----------|---------|
| "Pasta não encontrada" | Use caminho absoluto: `/home/usuario/dados`, não `~/dados` |
| "Arquivo JSON inválido" | Valide com `teste_populacao.py --validar /caminho` |
| Imagens não aparecem | Coloque em `fotos/{tipo}/{nome_produto}/` |
| Erro de codificação | Salve JSONs como UTF-8 |
| Comando não encontrado | Reinicie o Docker: `docker compose restart app` |

---

## 📚 Próximos Passos

1. **Gerar exemplo** (comece aqui!)
   ```bash
   python3 "testes e relatorios/teste_populacao.py" --gerar-exemplo /tmp/teste
   ```

2. **Popular no banco**
   ```bash
   docker compose exec app python manage.py popular_produtos_csv --pasta /tmp/teste
   ```

3. **Verificar no admin**
   ```
   http://localhost:8000/admin/produtos/
   ```

4. **Adaptar para seus dados**
   - Seguir o mesmo formato dos arquivos de exemplo
   - Usar o conversor CSV→JSON se necessário

---

## 📞 Suporte

Consulte:
- [`QUICK_START_POPULACAO.md`](QUICK_START_POPULACAO.md) - Para começar rápido
- [`GUIA_POPULACAO_DADOS.md`](testes%20e%20relatorios/GUIA_POPULACAO_DADOS.md) - Para documentação completa
- Arquivos de exemplo em [`testes e relatorios/`](testes%20e%20relatorios/) - Para ver formatos

---

**Sistema criado:** Janeiro 2026  
**Versão:** 1.0  
**Status:** ✅ Pronto para uso
