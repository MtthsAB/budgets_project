# Migração SQLite para PostgreSQL - Sistema de Produtos

## ⚠️ IMPORTANTE: Migração para PostgreSQL

O sistema estava originalmente configurado para usar SQLite, mas conforme especificado, deve utilizar **PostgreSQL** para garantir melhor performance, escalabilidade e recursos avançados.

## 🚀 Processo de Migração

### Pré-requisitos

1. **PostgreSQL instalado e rodando**
   ```bash
   # Ubuntu/Debian
   sudo apt update
   sudo apt install postgresql postgresql-contrib
   
   # Iniciar serviço
   sudo systemctl start postgresql
   sudo systemctl enable postgresql
   ```

2. **Configuração do usuário PostgreSQL**
   ```bash
   # Acessar console do PostgreSQL
   sudo -u postgres psql
   
   # Criar banco de dados
   CREATE DATABASE sistema_produtos;
   
   # Sair
   \q
   ```

### Opção 1: Migração Automática (Recomendada)

Execute o script Python de migração:

```bash
cd /home/matas/projetos/Project
python migrate_to_postgresql.py
```

### Opção 2: Migração Manual

1. **Backup dos dados SQLite**
   ```bash
   python manage.py dumpdata --natural-foreign --natural-primary \
     --exclude=contenttypes --exclude=auth.Permission \
     --exclude=admin.logentry --exclude=sessions.session \
     > backup_sqlite_data.json
   ```

2. **Aplicar migrations no PostgreSQL**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

3. **Carregar dados do backup**
   ```bash
   python manage.py loaddata backup_sqlite_data.json
   ```

4. **Criar superuser**
   ```bash
   python manage.py createsuperuser
   ```

## 📊 Nova Estrutura - App Clientes

### Modelo Cliente

O novo app `clientes` foi criado com o seguinte modelo:

```python
class Cliente(models.Model):
    # Dados da empresa
    nome_empresa = models.CharField(max_length=200)
    representante = models.CharField(max_length=150)
    
    # Dados legais
    cnpj = models.CharField(max_length=18, unique=True)
    inscricao_estadual = models.CharField(max_length=20, blank=True, null=True)
    inscricao_municipal = models.CharField(max_length=20, blank=True, null=True)
    
    # Endereço completo
    logradouro = models.CharField(max_length=200)
    numero = models.CharField(max_length=10)
    complemento = models.CharField(max_length=100, blank=True, null=True)
    bairro = models.CharField(max_length=100)
    cidade = models.CharField(max_length=100)
    estado = models.CharField(max_length=2)
    cep = models.CharField(max_length=9)
    
    # Contato
    telefone = models.CharField(max_length=20)
    email = models.EmailField()
    
    # Dados bancários (opcionais)
    banco = models.CharField(max_length=100, blank=True, null=True)
    agencia = models.CharField(max_length=20, blank=True, null=True)
    conta_corrente = models.CharField(max_length=30, blank=True, null=True)
    
    # Timestamps automáticos
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
```

### Funcionalidades Implementadas

- ✅ **CRUD completo** de clientes
- ✅ **Validação de CNPJ** e CEP com máscaras
- ✅ **Busca avançada** por múltiplos campos
- ✅ **Paginação** para listas grandes
- ✅ **Interface responsiva** seguindo padrão do sistema
- ✅ **Timestamps automáticos** (created_at, updated_at)
- ✅ **Administração Django** configurada

### URLs Disponíveis

```
/clientes/                    # Lista de clientes
/clientes/cadastro/           # Cadastrar novo cliente
/clientes/<id>/               # Detalhes do cliente
/clientes/<id>/editar/        # Editar cliente
/clientes/<id>/deletar/       # Excluir cliente
```

## 🎨 Interface Visual

A interface mantém consistência com o resto do sistema, utilizando:

- **Bootstrap 5.3** para layout responsivo
- **Bootstrap Icons** para ícones
- **Cores e padrões** idênticos às outras seções
- **Formulários organizados** por seções temáticas
- **Validação client-side** com máscaras JavaScript

## 🔧 Configurações

### Settings.py - Configuração do PostgreSQL

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('DB_NAME', default='sistema_produtos'),
        'USER': config('DB_USER', default='postgres'),
        'PASSWORD': config('DB_PASSWORD', default='postgres'),
        'HOST': config('DB_HOST', default='localhost'),
        'PORT': config('DB_PORT', default='5432'),
    }
}
```

### Arquivo .env

```properties
DB_NAME=sistema_produtos
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=localhost
DB_PORT=5432
```

## 🧪 Testes

Após a migração, execute os testes:

```bash
# Verificar se o sistema está funcionando
python manage.py check

# Executar servidor de desenvolvimento
python manage.py runserver

# Acessar:
# - Sistema: http://localhost:8000
# - Admin: http://localhost:8000/admin
# - Clientes: http://localhost:8000/clientes/
```

## 📋 Checklist Pós-Migração

- [ ] PostgreSQL configurado e rodando
- [ ] Dados migrados com sucesso
- [ ] App clientes funcionando
- [ ] Interface de cadastro testada
- [ ] Validações de formulário funcionando
- [ ] Busca e paginação operacionais
- [ ] Admin Django configurado
- [ ] Backup dos dados SQLite realizado

## 🔒 Segurança

- Altere as senhas padrão antes do deploy
- Configure adequadamente as variáveis de ambiente
- Mantenha backups regulares
- Monitore logs de acesso

## 📞 Suporte

Em caso de problemas na migração:

1. Verifique se o PostgreSQL está rodando
2. Confirme as configurações do .env
3. Execute `python manage.py check --database default`
4. Verifique os logs de erro
5. Consulte a documentação do Django para PostgreSQL
