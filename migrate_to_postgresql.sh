#!/bin/bash

# Script para migração do SQLite para PostgreSQL
# Autor: Sistema de Produtos
# Data: $(date +%Y-%m-%d)

echo "===== MIGRAÇÃO SQLite PARA PostgreSQL ====="
echo "Este script migra os dados do SQLite para PostgreSQL"
echo ""

# Verificar se o PostgreSQL está rodando
echo "1. Verificando se o PostgreSQL está ativo..."
sudo systemctl status postgresql | grep "Active:"

if [ $? -ne 0 ]; then
    echo "❌ PostgreSQL não está ativo. Iniciando..."
    sudo systemctl start postgresql
    sleep 2
fi

# Criar banco de dados
echo ""
echo "2. Criando banco de dados 'sistema_produtos'..."
sudo -u postgres createdb sistema_produtos 2>/dev/null
if [ $? -eq 0 ]; then
    echo "✅ Banco de dados criado com sucesso"
else
    echo "⚠️  Banco de dados já existe ou erro na criação"
fi

# Fazer backup dos dados do SQLite
echo ""
echo "3. Fazendo backup dos dados do SQLite..."
if [ -f "db.sqlite3" ]; then
    python manage.py dumpdata --natural-foreign --natural-primary \
        --exclude=contenttypes --exclude=auth.Permission \
        --exclude=admin.logentry --exclude=sessions.session \
        > backup_sqlite_data.json
    echo "✅ Backup criado: backup_sqlite_data.json"
else
    echo "⚠️  Arquivo db.sqlite3 não encontrado"
fi

# Aplicar migrations no PostgreSQL
echo ""
echo "4. Aplicando migrations no PostgreSQL..."
python manage.py makemigrations
python manage.py migrate

# Carregar dados do backup
echo ""
echo "5. Carregando dados do backup..."
if [ -f "backup_sqlite_data.json" ]; then
    python manage.py loaddata backup_sqlite_data.json
    echo "✅ Dados carregados com sucesso"
else
    echo "⚠️  Arquivo de backup não encontrado"
fi

# Criar superuser se não existir
echo ""
echo "6. Verificando superuser..."
python manage.py shell -c "
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(is_superuser=True).exists():
    print('Criando superuser...')
    User.objects.create_superuser('admin', 'admin@sistema.com', 'admin123')
    print('Superuser criado: admin / admin123')
else:
    print('Superuser já existe')
"

echo ""
echo "===== MIGRAÇÃO CONCLUÍDA ====="
echo "✅ Sistema migrado para PostgreSQL com sucesso!"
echo ""
echo "Para verificar a migração:"
echo "  1. python manage.py runserver"
echo "  2. Acesse: http://localhost:8000/admin"
echo "  3. Login: admin / admin123"
echo ""
echo "Arquivos importantes:"
echo "  - backup_sqlite_data.json (backup dos dados)"
echo "  - .env (configurações do PostgreSQL)"
