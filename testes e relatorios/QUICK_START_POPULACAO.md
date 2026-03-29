# 🚀 QUICK START - População de Produtos

## Opção 1: Gerar Dados de Teste (Recomendado para começar)

```bash
# Gerar estrutura completa de exemplo
python testes\ e\ relatorios/teste_populacao.py --gerar-exemplo /tmp/dados_exemplo

# Validar estrutura gerada
python testes\ e\ relatorios/teste_populacao.py --validar /tmp/dados_exemplo

# Popular no banco com os dados de exemplo
python manage.py popular_dados_produtos --pasta /tmp/dados_exemplo
```

## Opção 2: Usar Seus Próprios Dados

### Passo 1: Organizar Arquivos
```
seus_dados/
├── infos/
│   ├── cadeiras/      (coloque os JSONs aqui)
│   ├── banquetas/     (coloque os JSONs aqui)
│   ├── almofadas/     (coloque os JSONs aqui)
│   ├── sofas/         (coloque os JSONs aqui)
│   ├── poltronas/     (coloque os JSONs aqui)
│   └── PUFES/         (coloque os JSONs aqui)
└── fotos/
    ├── cadeiras/      (coloque as imagens aqui)
    ├── banquetas/     (coloque as imagens aqui)
    └── ... (mesma estrutura para os outros tipos)
```

### Passo 2: Converter de CSV (se necessário)
```bash
python testes\ e\ relatorios/converter_csv_json.py \
  --entrada seus_dados.csv \
  --saida seus_dados/infos/cadeiras \
  --tipo cadeiras
```

### Passo 3: Popular
```bash
python manage.py popular_dados_produtos --pasta /caminho/seus_dados
```

## Formato Mínimo de JSON

**Cadeira/Banqueta/Poltrona/Pufe:**
```json
{
  "ref_cadeira": "CD001",
  "nome": "Nome do Produto",
  "largura": 50,
  "profundidade": 45,
  "altura": 85,
  "preco": 450.00
}
```

**Almofada (sem profundidade):**
```json
{
  "ref_almofada": "AL001",
  "nome": "Almofada 40x40",
  "largura": 40,
  "altura": 40,
  "preco": 89.90
}
```

**Sofá:**
```json
{
  "ref_produto": "SF939",
  "nome": "Sofá SF939",
  "tem_cor_tecido": true,
  "modulos": [
    {
      "nome": "Assento",
      "profundidade": 90,
      "altura": 75,
      "braco": 25,
      "tamanhos": [
        {
          "largura_total": 180,
          "largura_assento": 150,
          "preco": 2500
        }
      ]
    }
  ]
}
```

## Comandos Úteis

### Popular apenas um tipo
```bash
python manage.py popular_dados_produtos --pasta /caminho --tipo cadeiras
python manage.py popular_dados_produtos --pasta /caminho --tipo sofas
python manage.py popular_dados_produtos --pasta /caminho --tipo almofadas
```

### Com Docker
```bash
docker compose exec app python manage.py popular_dados_produtos --pasta /caminho
```

### Validar antes de popular
```bash
python testes\ e\ relatorios/teste_populacao.py --validar /caminho
```

## Estrutura de Imagens

As imagens devem estar em subpastas com o nome do produto:
```
fotos/
└── cadeiras/
    ├── CD001/
    │   ├── 1.jpg    (principal)
    │   └── 2.jpg    (secundária)
    ├── CD24/
    │   └── 1.jpg
```

## ✅ Checklist

- [ ] Arquivos JSON têm formato válido
- [ ] Pastas `infos/` e `fotos/` existem
- [ ] Todos os campos obrigatórios estão preenchidos
- [ ] Valores numéricos usam ponto decimal (ex: 45.0)
- [ ] Imagens estão em subpastas com nome do produto
- [ ] Caminhos são absolutos

## 📁 Exemplo Completo

```bash
# 1. Gerar dados de teste
python testes\ e\ relatorios/teste_populacao.py --gerar-exemplo ~/dados_teste

# 2. Validar
python testes\ e\ relatorios/teste_populacao.py --validar ~/dados_teste

# 3. Popular
python manage.py popular_dados_produtos --pasta ~/dados_teste

# 4. Verificar no admin
# Acesse http://localhost:8000/admin e veja os produtos!
```

## 🆘 Troubleshooting

| Problema | Solução |
|----------|---------|
| "Pasta não encontrada" | Use caminho absoluto: `/home/usuario/dados` |
| "Arquivo JSON inválido" | Valide com `teste_populacao.py --validar` |
| Imagens não aparecem | Coloque em subpasta com nome do produto |
| Erro de encoding | Salve JSONs como UTF-8 |

---

**Documentação completa:** `GUIA_POPULACAO_DADOS.md`
