#!/bin/bash

# Script de inicialização para o ambiente Docker
# Este script automatiza o processo de configuração e execução do ambiente

set -e

echo "🚀 Iniciando configuração do ambiente Docker para Sistema de Produtos"

# Verificar se o Docker e Docker Compose (plugin) estão instalados
if ! command -v docker &> /dev/null; then
    echo "❌ Docker não está instalado. Por favor, instale o Docker primeiro."
    exit 1
fi

# docker compose é subcomando; checar executando
if ! docker compose version &> /dev/null; then
    echo "❌ Docker Compose (plugin) não está instalado. Por favor, instale o Docker Compose primeiro."
    exit 1
fi

# Criar arquivo .env se não existir
if [ ! -f .env ]; then
    echo "📝 Criando arquivo .env..."
    cp .env.example .env
    echo "⚠️  IMPORTANTE: Edite o arquivo .env com suas configurações específicas!"
fi

# Criar diretórios necessários
echo "📁 Criando diretórios necessários..."
mkdir -p media/produtos
mkdir -p staticfiles
mkdir -p docker/nginx/ssl

# Parar containers existentes (se houver)
echo "🛑 Parando containers existentes..."
docker compose down --remove-orphans

# Construir as imagens
echo "🏗️  Construindo imagens Docker..."
docker compose build --no-cache

# Iniciar os serviços
echo "🚀 Iniciando serviços..."
docker compose up -d

# Aguardar o banco de dados estar pronto
echo "⏳ Aguardando banco de dados..."
sleep 15

# Executar migrações
echo "🗄️  Executando migrações do banco de dados..."
docker compose exec app python manage.py migrate

# Coletar arquivos estáticos
echo "📦 Coletando arquivos estáticos..."
docker compose exec app python manage.py collectstatic --noinput


echo "✅ Configuração concluída!"
echo ""
echo "🌐 A aplicação está rodando em:"
echo "   - Local: http://localhost"
echo "   - Produção: http://meitans.shop (configure o DNS no Cloudflare)"
echo ""
echo "📊 Comandos úteis:"
echo "   - Ver logs: docker compose logs -f"
echo "   - Parar: docker compose down"
echo "   - Reiniciar: docker compose restart"
echo "   - Shell Django: docker compose exec app python manage.py shell"
echo "   - Backup DB: docker compose exec db pg_dump -U postgres sistema_produtos > backup.sql"
