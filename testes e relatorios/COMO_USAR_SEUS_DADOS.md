# 📂 Como Usar Seus Dados (Da Pasta Anexada)

## 🎯 Objetivo
Usar os dados da pasta que você anexou (`dados_produtos/`) para popular o banco de dados.

---

## 📋 Sua Estrutura de Pasta

Você anexou uma pasta com:

```
dados_produtos/
├── fotos/
│   ├── almofadas/
│   ├── banquetas/
│   ├── cadeiras/
│   ├── poltronas/
│   ├── PUFES/
│   └── sofa/
│       ├── bigboss/
│       └── sf939/
└── infos/
    ├── acessórios/
    ├── almofadas/
    ├── banquetas/
    ├── cadeiras/
    ├── poltronas/
    ├── PUFES/
    └── sofas/
```

---

## 🚀 Passo a Passo

### 1️⃣ **Localizar Seus Dados**

Você precisa colocar essa pasta em um local acessível ao seu sistema Linux:

**Opção A:** Copiar para uma pasta local
```bash
# Copie a pasta dados_produtos para seu computador Linux
# Exemplo: /home/matas/meus_dados_produtos
```

**Opção B:** Se está em Windows/OneDrive
```bash
# Sincronize ou copie para Linux via:
# - Pendrive
# - Compartilhamento de rede
# - Download local
```

### 2️⃣ **Organizar os Arquivos (IMPORTANTE)**

Os arquivos de informações devem estar como **arquivos JSON individuais**, não em pastas.

**Seu objetivo:**
```
/seu/caminho/dados_produtos/
├── infos/
│   ├── sofas/
│   │   ├── SF939.json      ← Um arquivo JSON por sofá
│   │   ├── BIGBOSS.json    ← Um arquivo JSON por sofá
│   │   └── ...
│   ├── cadeiras/
│   │   ├── CD001.json      ← Um arquivo JSON por cadeira
│   │   ├── CD024.json
│   │   └── ...
│   ├── banquetas/
│   ├── poltronas/
│   ├── PUFES/
│   └── almofadas/
└── fotos/
    ├── sofa/
    │   ├── SF939/
    │   │   ├── 1.jpg
    │   │   └── 2.jpg
    │   ├── BIGBOSS/
    │   │   └── 1.jpg
    │   └── ...
    ├── cadeiras/
    ├── banquetas/
    ├── poltronas/
    ├── PUFES/
    └── almofadas/
```

### 3️⃣ **Preparar os JSONs**

Se você tem arquivos de informação (Excel, CSV, TXT), converta para JSON usando:

```bash
python3 "testes e relatorios/converter_csv_json.py" \
  --entrada sua_lista_produtos.csv \
  --saida /seu/caminho/dados_produtos/infos/sofas \
  --tipo sofas
```

**Ou crie manualmente** seguindo o formato:

```json
{
  "ref_produto": "SF939",
  "nome": "SOFÁ SF939",
  "tem_cor_tecido": true,
  "modulos": [
    {
      "nome": "Assento",
      "profundidade": 90.0,
      "altura": 75.0,
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

### 4️⃣ **Organizar as Imagens**

As imagens já estão em `fotos/`, mas precisam estar em subpastas com o nome do produto:

```
fotos/sofa/
├── SF939/
│   ├── 1.jpg    ← Primeira imagem
│   └── 2.jpg    ← Segunda imagem (opcional)
├── BIGBOSS/
│   └── 1.jpg
└── LE_COULTRE/
    ├── 1.jpg
    └── 2.jpg
```

**Se as imagens estão em pastas diferentes:**
```bash
# Reorganize manualmente para a estrutura acima
# Ou use scripts para organizar automaticamente
```

### 5️⃣ **Validar Estrutura**

Antes de popular, valide:

```bash
python3 "testes e relatorios/teste_populacao.py" \
  --validar /seu/caminho/dados_produtos
```

### 6️⃣ **Popular o Banco**

```bash
docker compose exec app python manage.py popular_produtos_csv \
  --pasta /seu/caminho/dados_produtos
```

---

## 📝 Template de JSON para Seus Dados

### Para Sofás
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
      "tamanhos": [
        {
          "largura_total": 180.0,
          "largura_assento": 150.0,
          "tecido_metros": 8.5,
          "volume_m3": 0.85,
          "peso_kg": 45.0,
          "preco": 2500.00
        },
        {
          "largura_total": 200.0,
          "largura_assento": 170.0,
          "tecido_metros": 9.5,
          "volume_m3": 0.95,
          "peso_kg": 50.0,
          "preco": 2800.00
        }
      ]
    }
  ]
}
```

### Para Cadeiras
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
  "tem_cor_tecido": false
}
```

### Para Almofadas
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

---

## 🔄 Fluxo Completo

```
Seu computador Windows
    ↓
Copiar dados_produtos para Linux
    ↓
Organizar pastas (infos/{tipo}/, fotos/{tipo}/)
    ↓
Converter para JSON (se necessário)
    ↓
Validar com teste_populacao.py
    ↓
Popular com python manage.py
    ↓
Verificar no Admin (localhost:8000/admin)
```

---

## ⚙️ Dicas Importantes

### 💾 Para Arquivos Que Você Já Tem:

**Se tem Excel/CSV:**
```bash
python3 "testes e relatorios/converter_csv_json.py" \
  --entrada produtos.csv \
  --saida ./jsons \
  --tipo cadeiras
```

**Se tem TXT/Tabular:**
- Abra no Excel
- Exporte como CSV
- Use o conversor acima

**Se tem apenas imagens:**
- Crie JSONs manualmente com informações
- Use o template acima como base

### 📁 Problema Comum: Imagens em Pastas Diferentes

**Antes:**
```
fotos/sofa/
├── bigboss/
└── sf939/
```

**Depois (esperado):**
```
fotos/sofa/
├── BIGBOSS/
│   └── *.jpg
└── SF939/
    └── *.jpg
```

Mude os nomes das pastas para ser igual às referências dos produtos.

---

## ✅ Checklist Antes de Popular

- [ ] Arquivos JSON estão em `infos/{tipo}/`
- [ ] Cada tipo tem pasta: sofas/, cadeiras/, etc
- [ ] Imagens estão em `fotos/{tipo}/{nome_produto}/`
- [ ] Nomes de pastas de imagens correspondem aos ref_produto/ref_cadeira
- [ ] JSONs têm formato válido (use teste_populacao.py --validar)
- [ ] Caminho é absoluto (`/home/...`, não `~/`)

---

## 🆘 Precisa de Ajuda?

### Erro: "Pasta não encontrada"
```
Solução: Use caminho absoluto
❌ ~/dados_produtos
✅ /home/matas/dados_produtos
```

### Erro: "Arquivo JSON inválido"
```
Solução: Valide com
python3 "testes e relatorios/teste_populacao.py" --validar /caminho
```

### Imagens não aparecem
```
Solução: Coloque em pasta correta
fotos/{tipo}/{ref_produto}/1.jpg
```

### Não tem JSONs
```
Solução: Use o conversor
python3 "testes e relatorios/converter_csv_json.py"
```

---

## 🎯 Exemplo Real

Digamos que você tem:
- Sofás com fotos em `/home/matas/meus_sofas/`
- Lista de sofás em Excel

```bash
# 1. Criar pasta destino
mkdir -p /home/matas/sofas_para_importar/{infos/sofas,fotos/sofa}

# 2. Copiar imagens
cp -r /home/matas/meus_sofas/* /home/matas/sofas_para_importar/fotos/sofa/

# 3. Converter Excel para JSON
python3 "testes e relatorios/converter_csv_json.py" \
  --entrada /home/matas/sofas.csv \
  --saida /home/matas/sofas_para_importar/infos/sofas \
  --tipo sofas

# 4. Validar
python3 "testes e relatorios/teste_populacao.py" \
  --validar /home/matas/sofas_para_importar

# 5. Popular
docker compose exec app python manage.py popular_produtos_csv \
  --pasta /home/matas/sofas_para_importar

# 6. Verificar
# Acesse http://localhost:8000/admin/produtos/
```

---

## 📚 Próximas Ações

1. **Copie seus dados** para uma pasta local no Linux
2. **Organize em subpastas** (infos/{tipo}/, fotos/{tipo}/)
3. **Converta para JSON** se necessário
4. **Valide** com teste_populacao.py
5. **Popular** com popular_produtos_csv.py
6. **Verifique** no Admin

---

**Precisa de mais ajuda?**

Consulte:
- [QUICK_START_POPULACAO.md](QUICK_START_POPULACAO.md) - Exemplo rápido
- [GUIA_POPULACAO_DADOS.md](testes%20e%20relatorios/GUIA_POPULACAO_DADOS.md) - Referência completa
- Arquivos de exemplo em `testes e relatorios/`

Você está pronto! 🚀
