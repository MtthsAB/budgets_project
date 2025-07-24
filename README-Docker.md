# 🐳 Ambiente Docker - Sistema de Produtos

Este documento descreve como configurar e executar o Sistema de Produtos usando Docker e Docker Compose, otimizado para uso com Cloudflare.

## 📋 Pré-requisitos

- Docker Engine 20.10+
- Docker Compose 2.0+
- Pelo menos 4GB de RAM disponível
- 10GB de espaço em disco

## 🏗️ Arquitetura

O ambiente é composto por três serviços principais:

### 🐍 App (Django)
- **Imagem**: Python 3.10-slim personalizada
- **Servidor**: Gunicorn com 3 workers
- **Porta interna**: 8000
- **Health check**: Endpoint `/admin/`

### 🐘 Database (PostgreSQL)
- **Imagem**: postgres:15-alpine
- **Porta**: 5432
- **Volume persistente**: `postgres_data`
- **Encoding**: UTF-8
- **Timezone**: America/Sao_Paulo

### 🔄 Nginx (Reverse Proxy)
- **Imagem**: nginx:1.25-alpine
- **Portas**: 80, 443
- **Otimizado para**: Cloudflare
- **Features**: Gzip, Rate limiting, Security headers

## 🚀 Início Rápido

### 1. Configuração Inicial

```bash
# Clonar o repositório (se necessário)
git clone <seu-repositorio>
cd Project

# Executar script de configuração automática
./docker-setup.sh
```

### 2. Configuração Manual

Se preferir configurar manualmente:

```bash
# 1. Copiar arquivo de ambiente
cp .env.example .env

# 2. Editar configurações
nano .env

# 3. Construir e iniciar
docker-compose up -d --build

# 4. Executar migrações
docker-compose exec app python manage.py migrate

# 5. Coletar arquivos estáticos
docker-compose exec app python manage.py collectstatic --noinput

# 6. Criar superusuário
docker-compose exec app python manage.py createsuperuser
```

## ⚙️ Configurações Importantes

### Variáveis de Ambiente (.env)

```bash
# Banco de Dados
DB_NAME=sistema_produtos
DB_USER=postgres
DB_PASSWORD=postgres_secure_2024
DB_HOST=db
DB_PORT=5432

# Django
DEBUG=False
SECRET_KEY=sua-chave-secreta-super-segura
ALLOWED_HOSTS=meitans.shop,www.meitans.shop,localhost

# Segurança
SECURE_SSL_REDIRECT=True
SECURE_HSTS_SECONDS=31536000
```

### Configuração Cloudflare

Para usar com Cloudflare, configure:

1. **DNS**: Aponte `meitans.shop` para o IP do seu servidor
2. **SSL/TLS**: Mode "Flexible" ou "Full"
3. **Speed**: Ative "Auto Minify" para CSS, JS, HTML
4. **Security**: Configure regras de firewall conforme necessário

## 📊 Comandos Úteis

### Gerenciamento de Containers

```bash
# Ver status dos serviços
docker-compose ps

# Ver logs
docker-compose logs -f
docker-compose logs app
docker-compose logs nginx
docker-compose logs db

# Parar todos os serviços
docker-compose down

# Parar e remover volumes (CUIDADO: apaga dados!)
docker-compose down -v

# Reiniciar um serviço específico
docker-compose restart app
```

### Django Management

```bash
# Shell Django
docker-compose exec app python manage.py shell

# Executar comandos personalizados
docker-compose exec app python manage.py <comando>

# Backup do banco de dados
docker-compose exec db pg_dump -U postgres sistema_produtos > backup_$(date +%Y%m%d_%H%M%S).sql

# Restaurar backup
docker-compose exec -T db psql -U postgres sistema_produtos < backup.sql
```

### Debugging

```bash
# Entrar no container da aplicação
docker-compose exec app bash

# Entrar no container do nginx
docker-compose exec nginx sh

# Entrar no container do banco
docker-compose exec db psql -U postgres -d sistema_produtos

# Ver configuração do nginx
docker-compose exec nginx nginx -t
docker-compose exec nginx nginx -s reload
```

## 🔧 Monitoramento

### Health Checks

Todos os serviços têm health checks configurados:

- **App**: HTTP GET para `/admin/`
- **Database**: `pg_isready`
- **Nginx**: HTTP GET para `/health/`

### Logs

```bash
# Logs em tempo real
docker-compose logs -f

# Logs com timestamps
docker-compose logs -t

# Logs de um serviço específico
docker-compose logs -f app
```

## 🛡️ Segurança

### Headers de Segurança Configurados

- `X-Frame-Options: SAMEORIGIN`
- `X-Content-Type-Options: nosniff`
- `X-XSS-Protection: 1; mode=block`
- `Referrer-Policy: strict-origin-when-cross-origin`

### Rate Limiting

- API endpoints: 30 req/min
- Login endpoints: 5 req/min

### Cloudflare Integration

O Nginx está configurado para:
- Receber IPs reais via `CF-Connecting-IP`
- Processar headers específicos do Cloudflare
- Logs incluem `CF-Ray` e `CF-IPCountry`

## 📈 Performance

### Otimizações Implementadas

1. **Nginx**:
   - Gzip compression
   - Static file caching (30 dias)
   - Keep-alive connections
   - Worker auto-tuning

2. **Django**:
   - Gunicorn com 3 workers
   - WhiteNoise para arquivos estáticos
   - Timeout configurado (120s)

3. **PostgreSQL**:
   - Shared buffers otimizados
   - Effective cache size configurado
   - Maintenance work memory ajustado

## 🔄 Backup e Restore

### Backup Automático

```bash
# Script de backup diário (adicionar ao cron)
#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
docker-compose exec db pg_dump -U postgres sistema_produtos > "backup_${DATE}.sql"
find . -name "backup_*.sql" -mtime +7 -delete
```

### Restore

```bash
# Restaurar de backup
docker-compose exec -T db psql -U postgres sistema_produtos < backup.sql
```

## 🚨 Troubleshooting

### Problemas Comuns

1. **Porta 80 ocupada**:
   ```bash
   sudo lsof -i :80
   sudo systemctl stop apache2  # ou nginx local
   ```

2. **Banco não conecta**:
   ```bash
   docker-compose logs db
   docker-compose restart db
   ```

3. **Arquivos estáticos não carregam**:
   ```bash
   docker-compose exec app python manage.py collectstatic --noinput
   docker-compose restart nginx
   ```

4. **Permissões de arquivo**:
   ```bash
   sudo chown -R $USER:$USER media/ staticfiles/
   chmod -R 755 media/ staticfiles/
   ```

## 📞 Suporte

Para problemas ou dúvidas:
1. Verifique os logs: `docker-compose logs -f`
2. Consulte a documentação do Django
3. Verifique a configuração do Cloudflare

---

**Nota**: Sempre teste as configurações em ambiente de desenvolvimento antes de aplicar em produção.
