# Sistema de Gestão de Produtos

Sistema web completo desenvolvido em Django para gestão de produtos, módulos e preços, com backend e frontend integrados.

## 🚀 Características Principais

- **Autenticação Segura**: Sistema de login/registro com JWT
- **Gestão de Produtos**: CRUD completo para produtos com módulos
- **Interface Moderna**: Frontend responsivo com Bootstrap 5
- **Banco PostgreSQL**: Estrutura robusta com auditoria automática
- **Campos de Auditoria**: created_at e updated_at em todas as tabelas
- **Admin Interface**: Interface administrativa completa

## 📋 Pré-requisitos

- Python 3.8+
- PostgreSQL 12+
- Navegador web moderno

## 🛠️ Instalação

### 1. Clone o projeto
```bash
git clone <repository-url>
cd sistema-produtos
```

### 2. Configure o ambiente virtual
```bash
python -m venv venv
# Windows
.\venv\Scripts\Activate.ps1
# Linux/Mac
source venv/bin/activate
```

### 3. Instale as dependências
```bash
pip install -r requirements.txt
```

### 4. Configure o banco PostgreSQL
Crie um banco de dados PostgreSQL e configure as credenciais no arquivo `.env`:

```env
DB_NAME=sistema_produtos
DB_USER=postgres
DB_PASSWORD=sua_senha
DB_HOST=localhost
DB_PORT=5432
```

### 5. Execute as migrações
```bash
python manage.py migrate
```

### 6. Popule dados iniciais
```bash
python manage.py popular_dados
```

### 7. Crie um superusuário
```bash
python manage.py createsuperuser
```

### 8. Execute o servidor
```bash
python manage.py runserver
```

Acesse: http://127.0.0.1:8000/

## 📊 Estrutura do Banco de Dados

### Tabelas Principais

1. **itens**
   - ID (chave primária)
   - refProduto (string)
   - nomeProduto (string)
   - idTipoProduto (FK para tipo_item)
   - ativo (boolean)
   - temCorTecido (boolean)
   - temDiferDesenhoLadoDirEsq (boolean)
   - temDiferDesenhoTamanho (boolean)
   - idLinha (FK para linha)
   - created_at, updated_at

2. **tipo_item**
   - ID (chave primária)
   - nome (string)
   - created_at, updated_at

3. **acessorios_itens**
   - ID (chave primária)
   - idAcessorio (FK para acessorios)
   - idLinha (FK para linha)
   - created_at, updated_at

4. **tamanhos_modulos**
   - ID (chave primária)
   - idModulo (FK para modulos)
   - tamanho (string)
   - created_at, updated_at

5. **precosBase**
   - ID (chave primária)
   - idItem (FK para itens)
   - idFaixaTecido (FK para faixa_tecido)
   - dataInicVigencia (date)
   - precoBase (decimal)
   - created_at, updated_at

## 🎯 Funcionalidades

### Autenticação
- ✅ Login com email e senha
- ✅ Registro de novos usuários
- ✅ JWT para APIs
- ✅ Logout seguro

### Gestão de Produtos
- ✅ Listagem com filtros e busca
- ✅ Cadastro de novos produtos
- ✅ Edição de produtos existentes
- ✅ Exclusão com confirmação
- ✅ Visualização detalhada

### Módulos
- ✅ Adicionar múltiplos módulos por produto
- ✅ Configuração de tamanhos
- ✅ Controle de tecido e volume
- ✅ Definição de preços

### Tipos de Produto Suportados
- Sofás
- Acessórios
- Cadeiras
- Banquetas
- Poltronas
- Pufes
- Almofadas

## 🛡️ Segurança

- Autenticação JWT
- Validação CSRF
- Sanitização de entrada
- Controle de acesso por usuário
- Senhas criptografadas

## 🎨 Interface

- Design responsivo com Bootstrap 5
- Ícones Bootstrap Icons
- Interface intuitiva e moderna
- Mensagens de feedback
- Modais de confirmação

## 📱 API Endpoints

### Autenticação
- `POST /api/login/` - Login com JWT
- `POST /api/token/refresh/` - Refresh token

### Web Interface
- `/` - Dashboard principal
- `/auth/login/` - Página de login
- `/auth/register/` - Página de registro
- `/produtos/` - Lista de produtos
- `/produtos/cadastro/` - Cadastro de produto
- `/produtos/{id}/` - Detalhes do produto
- `/produtos/{id}/editar/` - Editar produto

## 🔧 Comandos Úteis

```bash
# Fazer backup do banco
python manage.py dumpdata > backup.json

# Carregar backup
python manage.py loaddata backup.json

# Executar testes
python manage.py test

# Coletar arquivos estáticos
python manage.py collectstatic

# Shell interativo
python manage.py shell
```

## 📦 Tecnologias Utilizadas

- **Backend**: Django 5.2.4
- **Database**: PostgreSQL com psycopg2
- **API**: Django REST Framework
- **Auth**: JWT (Simple JWT)
- **Frontend**: Bootstrap 5, Bootstrap Icons
- **Config**: python-decouple

## 🏗️ Estrutura do Projeto

```
sistema_produtos/
├── authentication/          # App de autenticação
├── produtos/               # App principal de produtos
├── sistema_produtos/       # Configurações do projeto
├── templates/             # Templates HTML
├── static/               # Arquivos estáticos
├── requirements.txt      # Dependências
├── .env                 # Variáveis de ambiente
└── manage.py           # CLI do Django
```

## 🔄 Deploy em Produção

Para deploy em produção, configure:

1. **DEBUG=False** no `.env`
2. **ALLOWED_HOSTS** com seus domínios
3. Servidor web (nginx + gunicorn)
4. Banco PostgreSQL dedicado
5. Coleta de arquivos estáticos
6. HTTPS com certificado SSL

## 📞 Suporte

Para dúvidas ou problemas:
1. Verifique a documentação
2. Consulte os logs do Django
3. Teste em ambiente de desenvolvimento

## 📄 Licença

Este projeto foi desenvolvido como sistema personalizado para gestão de produtos.

---

**Sistema de Produtos v1.0** - Desenvolvido com Django Framework
